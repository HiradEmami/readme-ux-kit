from collections import defaultdict
from pathlib import Path
import colorsys
import re
import xml.etree.ElementTree as ET


COLOR_ATTRIBUTES = {
    "fill",
    "stroke",
    "stop-color",
    "flood-color",
    "lighting-color",
}
SKIP_COLOR_VALUES = {"", "none", "transparent", "currentcolor", "inherit", "initial", "unset"}
TEXT_TAGS = {"text", "tspan", "textPath"}
ANIMATION_TAGS = {"animate", "animateMotion", "animateTransform", "set"}
NON_VISUAL_TAGS = {
    "defs",
    "desc",
    "linearGradient",
    "marker",
    "mask",
    "metadata",
    "pattern",
    "radialGradient",
    "script",
    "style",
    "symbol",
    "title",
}
COMPLEX_VISUAL_TAGS = {"clipPath", "filter", "mask", "pattern"}
COMMON_NAMED_COLORS = {
    "black",
    "blue",
    "cyan",
    "gray",
    "green",
    "grey",
    "lime",
    "magenta",
    "orange",
    "purple",
    "red",
    "silver",
    "white",
    "yellow",
}
QUALITY_LEVELS = {"excellent", "good", "limited"}
TRUTHY_VALUES = {"1", "true", "yes", "on", "locked"}

HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
FUNCTION_COLOR_RE = re.compile(r"\b(?:rgb|rgba|hsl|hsla)\([^)]*\)", re.IGNORECASE)
CSS_DECLARATION_RE = re.compile(r"(?P<property>[-a-zA-Z]+)\s*:\s*(?P<value>[^;{}]+)")
DURATION_RE = re.compile(r"(?<![-\w])\d*\.?\d+(?:ms|s)\b", re.IGNORECASE)
NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")


def local_name(tag):
    if not isinstance(tag, str):
        return ""
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def normalized_space(value):
    return " ".join(str(value).split())


def parse_number(value):
    if value is None:
        return None
    match = NUMBER_RE.search(str(value))
    if not match:
        return None
    number = float(match.group(0))
    return int(number) if number.is_integer() else number


def parse_length(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text or "%" in text:
        return None
    return parse_number(text)


def parse_view_box(value):
    if not value:
        return None
    numbers = [float(part) for part in NUMBER_RE.findall(value)]
    if len(numbers) != 4:
        return None
    return [int(number) if number.is_integer() else number for number in numbers]


def svg_dimensions(root):
    view_box = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    view_box_numbers = parse_view_box(view_box)
    width = parse_length(root.attrib.get("width"))
    height = parse_length(root.attrib.get("height"))

    if view_box_numbers:
        width = width if width is not None else view_box_numbers[2]
        height = height if height is not None else view_box_numbers[3]

    aspect_ratio = None
    if width and height:
        aspect_ratio = round(float(width) / float(height), 4)

    return {
        "width": width,
        "height": height,
        "viewBox": view_box,
        "aspectRatio": aspect_ratio,
    }


def colors_from_value(value):
    if value is None:
        return []

    text = str(value).strip()
    text = text.replace("!important", "").strip().strip("\"'")
    lowered = text.lower()

    if lowered in SKIP_COLOR_VALUES or lowered.startswith("url("):
        return []

    colors = []
    colors.extend(match.group(0).lower() for match in HEX_COLOR_RE.finditer(text))
    colors.extend(normalized_space(match.group(0)).lower() for match in FUNCTION_COLOR_RE.finditer(text))

    if not colors and lowered in COMMON_NAMED_COLORS:
        colors.append(lowered)

    return colors


def expand_short_hex(value):
    if len(value) in {4, 5}:
        return "#" + "".join(character * 2 for character in value[1:])
    return value


def hex_to_rgb(value):
    if not value.startswith("#"):
        return None

    normalized = expand_short_hex(value.lower())
    if len(normalized) not in {7, 9}:
        return None

    try:
        return tuple(int(normalized[index : index + 2], 16) for index in (1, 3, 5))
    except ValueError:
        return None


def color_stats(value):
    rgb = hex_to_rgb(value)
    if not rgb:
        return None

    r, g, b = [channel / 255 for channel in rgb]
    hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return {
        "hue": round(hue * 360, 2),
        "saturation": round(saturation, 4),
        "lightness": round(lightness, 4),
        "luminance": round(luminance, 4),
    }


def add_color_occurrences(color_data, attribute, value):
    for color in colors_from_value(value):
        color_data[color]["count"] += 1
        color_data[color]["attributes"].add(attribute)


def iter_element_paths(root):
    stack = [(root, "0")]
    while stack:
        element, path = stack.pop()
        yield element, path
        children = [child for child in list(element) if isinstance(child.tag, str)]
        for index, child in reversed(list(enumerate(children))):
            stack.append((child, f"{path}.{index}"))


def style_texts(root):
    for element, _ in iter_element_paths(root):
        if local_name(element.tag) == "style":
            text = "".join(element.itertext()).strip()
            if text:
                yield text


def semantic_role(value, attributes, accent_index):
    stats = color_stats(value)
    attr_set = set(attributes)
    lowered = value.lower()

    if lowered == "red":
        return "danger"
    if lowered in {"green", "lime"}:
        return "success"
    if lowered in {"orange", "yellow"}:
        return "warning"
    if lowered == "black":
        return "background"
    if lowered == "white":
        return "text"
    if not stats:
        return "accent"

    hue = stats["hue"]
    saturation = stats["saturation"]
    luminance = stats["luminance"]

    if 345 <= hue or hue <= 18:
        return "danger"
    if 70 <= hue <= 165 and saturation >= 0.35 and luminance >= 0.25:
        return "success"
    if 25 <= hue <= 65 and saturation >= 0.35 and luminance >= 0.25:
        return "warning"
    if luminance >= 0.86 and saturation <= 0.35:
        return "text"
    if 0.46 <= luminance < 0.86 and saturation <= 0.28:
        return "mutedText"
    if luminance < 0.09 and "fill" in attr_set:
        return "background"
    if luminance < 0.22 and "fill" in attr_set:
        return "surface"
    if "filter" in attr_set or "flood-color" in attr_set or "lighting-color" in attr_set:
        return "glow"
    if "stop-color" in attr_set and accent_index > 1:
        return "secondaryAccent"
    if saturation >= 0.35:
        return "primaryAccent" if accent_index <= 1 else "secondaryAccent"
    if "stroke" in attr_set:
        return "stroke"
    return "surface"


def color_tokens(root):
    color_data = defaultdict(lambda: {"count": 0, "attributes": set()})

    for element, _ in iter_element_paths(root):
        for attribute, value in element.attrib.items():
            attr_name = local_name(attribute)
            if attr_name in COLOR_ATTRIBUTES:
                add_color_occurrences(color_data, attr_name, value)
            elif attr_name == "style":
                for declaration in CSS_DECLARATION_RE.finditer(value):
                    property_name = declaration.group("property").strip().lower()
                    if property_name in COLOR_ATTRIBUTES or "color" in property_name:
                        add_color_occurrences(color_data, property_name, declaration.group("value"))

    for text in style_texts(root):
        for declaration in CSS_DECLARATION_RE.finditer(text):
            property_name = declaration.group("property").strip().lower()
            if property_name in COLOR_ATTRIBUTES or "color" in property_name:
                add_color_occurrences(color_data, f"css:{property_name}", declaration.group("value"))

    sorted_items = sorted(color_data.items(), key=lambda item: (-item[1]["count"], item[0]))
    accent_index = 0
    tokens = []
    for color, details in sorted_items:
        attributes = sorted(details["attributes"])
        stats = color_stats(color)
        if stats and stats["saturation"] >= 0.35 and 0.12 <= stats["luminance"] <= 0.86:
            accent_index += 1
        tokens.append(
            {
                "value": color,
                "role": semantic_role(color, attributes, accent_index),
                "count": details["count"],
                "attributes": attributes,
                "operations": ["replaceColor"],
            }
        )
    return tokens


def palette_by_role(tokens):
    palette = defaultdict(list)
    for token in tokens:
        if token["value"] not in palette[token["role"]]:
            palette[token["role"]].append(token["value"])
    return {role: values for role, values in sorted(palette.items())}


def element_text(element):
    return normalized_space("".join(element.itertext()))


def data_edit_value(element, name):
    return (
        element.attrib.get(f"data-edit-{name}")
        or element.attrib.get(f"data-editor-{name}")
        or element.attrib.get(f"data-{name}")
    )


def is_locked(element):
    value = data_edit_value(element, "lock")
    if value is None:
        value = data_edit_value(element, "locked")
    return str(value).strip().lower() in TRUTHY_VALUES


def edit_selector(element):
    edit_id = data_edit_value(element, "id")
    if edit_id:
        return f'[data-edit-id="{edit_id}"]'
    if element.attrib.get("id"):
        return f"#{element.attrib['id']}"
    return None


def edit_identity(element, path, fallback_label):
    edit_id = data_edit_value(element, "id")
    stable = bool(edit_id or element.attrib.get("id"))
    return {
        "editId": edit_id or element.attrib.get("id") or path,
        "editLabel": data_edit_value(element, "label") or fallback_label,
        "locked": is_locked(element),
        "stable": stable,
        "selector": edit_selector(element),
    }


def element_label(element, path):
    label = data_edit_value(element, "label")
    if label:
        return label
    edit_id = data_edit_value(element, "id")
    if edit_id:
        return edit_id
    if element.attrib.get("id"):
        return f"#{element.attrib['id']}"
    if element.attrib.get("class"):
        return "." + ".".join(element.attrib["class"].split())

    text = element_text(element)
    if text:
        return text[:48]

    tag = local_name(element.tag)
    useful_attrs = []
    for attribute in ("x", "y", "cx", "cy", "width", "height", "r"):
        if attribute in element.attrib:
            useful_attrs.append(f"{attribute}={element.attrib[attribute]}")
    suffix = f" ({', '.join(useful_attrs[:3])})" if useful_attrs else ""
    return f"{tag} {path}{suffix}"


def text_nodes(root):
    nodes = []
    for element, path in iter_element_paths(root):
        if local_name(element.tag) not in TEXT_TAGS:
            continue
        value = element_text(element)
        if not value:
            continue
        identity = edit_identity(element, path, element_label(element, path))
        nodes.append(
            {
                "nodePath": path,
                "tag": local_name(element.tag),
                "value": value,
                "length": len(value),
                "id": element.attrib.get("id"),
                "class": element.attrib.get("class"),
                "operations": [] if identity["locked"] else ["replaceText"],
                **identity,
            }
        )
    return nodes


def element_has_animation(element):
    for child in element.iter():
        if local_name(child.tag) in ANIMATION_TAGS:
            return True
    return False


def direct_visual_children(root):
    children = [child for child in list(root) if isinstance(child.tag, str)]
    for index, child in enumerate(children):
        tag = local_name(child.tag)
        if tag in NON_VISUAL_TAGS:
            continue
        yield child, f"0.{index}", 1


def nested_visual_groups(root):
    for element, path in iter_element_paths(root):
        tag = local_name(element.tag)
        if tag != "g" or path.count(".") < 2:
            continue
        yield element, path, path.count(".")


def removable_elements(root, limit=60):
    seen = set()
    elements = []

    for element, path, depth in list(direct_visual_children(root)) + list(nested_visual_groups(root)):
        if path in seen:
            continue
        seen.add(path)
        children = [child for child in list(element) if isinstance(child.tag, str)]
        identity = edit_identity(element, path, element_label(element, path))
        elements.append(
            {
                "nodePath": path,
                "tag": local_name(element.tag),
                "label": identity["editLabel"],
                "id": element.attrib.get("id"),
                "class": element.attrib.get("class"),
                "depth": depth,
                "childCount": len(children),
                "hasText": bool(element_text(element)),
                "hasAnimation": element_has_animation(element),
                "operations": [] if identity["locked"] else ["hideElement"],
                **identity,
            }
        )
        if len(elements) >= limit:
            break

    return elements


def animation_duration_tokens(root):
    durations = defaultdict(lambda: {"count": 0, "sources": set()})

    for element, _ in iter_element_paths(root):
        tag = local_name(element.tag)
        if tag in ANIMATION_TAGS and element.attrib.get("dur"):
            value = element.attrib["dur"].strip().lower()
            durations[value]["count"] += 1
            durations[value]["sources"].add("attribute:dur")

        style = element.attrib.get("style")
        if style:
            for declaration in CSS_DECLARATION_RE.finditer(style):
                property_name = declaration.group("property").strip().lower()
                if property_name.startswith("animation"):
                    for value in DURATION_RE.findall(declaration.group("value")):
                        durations[value.lower()]["count"] += 1
                        durations[value.lower()]["sources"].add("attribute:style")

    for text in style_texts(root):
        for declaration in CSS_DECLARATION_RE.finditer(text):
            property_name = declaration.group("property").strip().lower()
            if property_name.startswith("animation"):
                for value in DURATION_RE.findall(declaration.group("value")):
                    durations[value.lower()]["count"] += 1
                    durations[value.lower()]["sources"].add("style")

    tokens = [
        {
            "value": value,
            "count": details["count"],
            "sources": sorted(details["sources"]),
            "operations": ["scaleAnimationSpeed"],
        }
        for value, details in durations.items()
    ]
    return sorted(tokens, key=lambda token: (-token["count"], token["value"]))


def has_css_animation(root):
    return any("@keyframes" in text or "animation:" in text or "animation-duration" in text for text in style_texts(root))


def named_group_count(root):
    count = 0
    for element, _ in iter_element_paths(root):
        if local_name(element.tag) != "g":
            continue
        if data_edit_value(element, "id") or element.attrib.get("id") or element.attrib.get("class"):
            count += 1
    return count


def tag_count(root, tag_names):
    return sum(1 for element, _ in iter_element_paths(root) if local_name(element.tag) in tag_names)


def warning(code, message, severity="info"):
    return {"code": code, "severity": severity, "message": message}


def compatibility_warnings(root, colors, texts):
    warnings = []
    if has_css_animation(root):
        warnings.append(
            warning(
                "css-heavy-animation",
                "Uses CSS animation rules; speed editing may need stylesheet-aware updates.",
                "warning",
            )
        )
    if tag_count(root, {"linearGradient", "radialGradient"}) >= 4 or tag_count(root, {"stop"}) >= 12:
        warnings.append(
            warning(
                "gradient-heavy",
                "Uses many gradient definitions or stops; palette edits may affect layered color blends.",
            )
        )
    if not texts:
        warnings.append(warning("no-text", "No editable text nodes were detected."))
    if named_group_count(root) == 0:
        warnings.append(
            warning(
                "no-named-groups",
                "No named groups were detected; element toggles fall back to generated node paths.",
            )
        )
    if any(token["count"] >= 18 for token in colors):
        warnings.append(
            warning(
                "many-duplicate-colors",
                "At least one color appears many times; replacing it may affect multiple visual layers.",
            )
        )
    if tag_count(root, COMPLEX_VISUAL_TAGS) > 0:
        warnings.append(
            warning(
                "complex-masks-clips",
                "Uses masks, clips, filters, or patterns; some removals may have cascading visual effects.",
                "warning",
            )
        )
    return warnings


def editor_operations(colors, texts, removable, durations):
    operations = []
    if colors:
        operations.append("replaceColor")
    if any(not node["locked"] for node in texts):
        operations.append("replaceText")
    if any(not element["locked"] for element in removable):
        operations.append("hideElement")
    if durations:
        operations.append("scaleAnimationSpeed")
    return operations


def quality_reasons(colors, texts, removable, durations, warnings, dimensions):
    reasons = []
    if dimensions["viewBox"] and dimensions["width"] and dimensions["height"]:
        reasons.append("has explicit dimensions")
    if colors:
        reasons.append("has editable color tokens")
    if texts:
        reasons.append("has editable text nodes")
    if removable:
        reasons.append("has visual elements that can be toggled")
    if durations:
        reasons.append("has animation durations that can be scaled")
    if any(item["stable"] for item in texts + removable):
        reasons.append("has stable edit identifiers")
    if warnings:
        reasons.append("has compatibility warnings")
    return reasons


def editor_quality(colors, texts, removable, durations, warnings, dimensions):
    score = 0
    if dimensions["viewBox"]:
        score += 2
    if dimensions["width"] and dimensions["height"]:
        score += 2
    if colors:
        score += 2
    if texts:
        score += 1
    if removable:
        score += 1
    if durations:
        score += 1
    if any(item["stable"] for item in texts + removable):
        score += 2
    score -= sum(2 for item in warnings if item["severity"] == "warning")
    score -= sum(1 for item in warnings if item["severity"] == "info")
    score = max(0, min(10, score))

    if score >= 8:
        level = "excellent"
    elif score >= 5:
        level = "good"
    else:
        level = "limited"

    return {
        "level": level,
        "score": score,
        "reasons": quality_reasons(colors, texts, removable, durations, warnings, dimensions),
    }


def build_editor_metadata(root, dimensions):
    colors = color_tokens(root)
    texts = text_nodes(root)
    removable = removable_elements(root)
    durations = animation_duration_tokens(root)
    has_animation = bool(durations) or has_css_animation(root) or any(
        local_name(element.tag) in ANIMATION_TAGS for element, _ in iter_element_paths(root)
    )
    warnings = compatibility_warnings(root, colors, texts)
    operations = editor_operations(colors, texts, removable, durations)
    quality = editor_quality(colors, texts, removable, durations, warnings, dimensions)

    capabilities = []
    if colors:
        capabilities.append("colors")
    if texts:
        capabilities.append("text")
    if removable:
        capabilities.append("visibility")
    if has_animation:
        capabilities.append("animationSpeed")

    return {
        "editable": bool(operations),
        "quality": quality,
        "capabilities": capabilities,
        "operations": operations,
        "nodePathMode": "element-child-index",
        "palette": palette_by_role(colors),
        "colorTokens": colors,
        "textNodes": texts,
        "removableElements": removable,
        "animation": {
            "hasAnimation": has_animation,
            "durations": durations,
            "operations": ["scaleAnimationSpeed"] if durations else [],
        },
        "warnings": warnings,
    }


def empty_metadata(parse_error=None):
    editor = {
        "editable": False,
        "quality": {
            "level": "limited",
            "score": 0,
            "reasons": ["invalid SVG XML"] if parse_error else [],
        },
        "capabilities": [],
        "operations": [],
        "nodePathMode": "element-child-index",
        "palette": {},
        "colorTokens": [],
        "textNodes": [],
        "removableElements": [],
        "animation": {
            "hasAnimation": False,
            "durations": [],
            "operations": [],
        },
        "warnings": [],
    }
    if parse_error:
        editor["parseError"] = str(parse_error)

    return {
        "dimensions": {
            "width": None,
            "height": None,
            "viewBox": None,
            "aspectRatio": None,
        },
        "editor": editor,
    }


def svg_editor_metadata_from_text(source):
    try:
        root = ET.fromstring(source)
    except ET.ParseError as error:
        return empty_metadata(parse_error=error)

    dimensions = svg_dimensions(root)
    return {
        "dimensions": dimensions,
        "editor": build_editor_metadata(root, dimensions),
    }


def svg_editor_metadata(path):
    return svg_editor_metadata_from_text(path.read_text(encoding="utf-8"))


def fixture_path(name):
    return Path(__file__).resolve().parent / "fixtures" / name


def run_self_tests():
    metadata = svg_editor_metadata(fixture_path("editor_metadata_sample.svg"))
    editor = metadata["editor"]

    assert metadata["dimensions"]["width"] == 240
    assert metadata["dimensions"]["height"] == 80
    assert metadata["dimensions"]["aspectRatio"] == 3
    assert "replaceColor" in editor["operations"]
    assert "replaceText" in editor["operations"]
    assert "hideElement" in editor["operations"]
    assert "scaleAnimationSpeed" in editor["operations"]
    assert editor["quality"]["level"] in QUALITY_LEVELS
    assert any(token["role"] == "background" for token in editor["colorTokens"])
    assert any(token["role"] == "primaryAccent" for token in editor["colorTokens"])
    assert any(token["role"] == "text" for token in editor["colorTokens"])
    assert editor["textNodes"][0]["editId"] == "title"
    assert editor["textNodes"][0]["editLabel"] == "Title text"
    assert editor["textNodes"][0]["stable"] is True
    assert any(item["editId"] == "spark" and item["locked"] is True for item in editor["removableElements"])
    assert any(token["value"] == "1.5s" for token in editor["animation"]["durations"])

    complex_metadata = svg_editor_metadata(fixture_path("editor_metadata_complex.svg"))
    warning_codes = {item["code"] for item in complex_metadata["editor"]["warnings"]}
    assert "css-heavy-animation" in warning_codes
    assert "gradient-heavy" in warning_codes
    assert "complex-masks-clips" in warning_codes

    percent_metadata = svg_editor_metadata_from_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" width="100%" height="120"></svg>'
    )
    assert percent_metadata["dimensions"]["width"] == 1200
    assert percent_metadata["dimensions"]["height"] == 120
