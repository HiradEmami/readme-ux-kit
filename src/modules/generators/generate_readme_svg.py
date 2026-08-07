from pathlib import Path
import argparse
import html
import xml.etree.ElementTree as ET


SVG_NS = "http://www.w3.org/2000/svg"


def esc(value):
    return html.escape(str(value), quote=True)


def split_items(value, fallback):
    if not value:
        return fallback
    return [item.strip() for item in value.split("|") if item.strip()]


def svg(width, height, body, label):
    return f"""<svg xmlns="{SVG_NS}" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{esc(label)}">
{body}
</svg>
"""


def gradient_defs(name, colors):
    return f"""  <defs>
    <linearGradient id="{name}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{colors[0]}"/>
      <stop offset="100%" stop-color="{colors[1]}"/>
    </linearGradient>
  </defs>"""


def text(x, y, value, size=24, fill="#e5e7eb", weight=700, anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="Consolas, monospace" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{esc(value)}</text>'


def preset_terminal(args):
    lines = split_items(args.items, ["npm install", "npm run dev", "ready on localhost"])
    rows = []
    for index, line in enumerate(lines[:4]):
        y = 82 + index * 34
        rows.append(text(44, y, f"$ {line}", 18, "#bbf7d0", 600))
    body = f"""  <rect width="{args.width}" height="{args.height}" rx="14" fill="#020617"/>
  <circle cx="28" cy="28" r="6" fill="#fb7185"/>
  <circle cx="48" cy="28" r="6" fill="#facc15"/>
  <circle cx="68" cy="28" r="6" fill="#22c55e"/>
  {text(44, 58, args.title, 20, args.primary, 700)}
  {"".join(rows)}
  <rect x="42" y="{82 + len(lines[:4]) * 34}" width="10" height="22" rx="3" fill="#e5e7eb">
    <animate attributeName="opacity" values="1;0;1" dur=".8s" repeatCount="indefinite"/>
  </rect>"""
    return svg(args.width, args.height, body, args.title)


def preset_badge_strip(args):
    items = split_items(args.items, ["build:passing", "release:stable", "license:MIT"])
    x = 28
    badges = []
    for item in items[:6]:
        label, _, value = item.partition(":")
        value = value or "ok"
        width = max(92, 16 * (len(label) + len(value)))
        badges.append(f'<rect x="{x}" y="42" width="{width}" height="34" rx="17" fill="#111827" stroke="{args.primary}" stroke-width="2"/>')
        badges.append(text(x + 18, 64, f"{label} {value}", 14, "#f8fafc", 700))
        x += width + 14
    body = f"""  <rect width="{args.width}" height="{args.height}" rx="14" fill="#070b16"/>
  {text(28, 28, args.title, 18, args.secondary, 700)}
  {"".join(badges)}"""
    return svg(args.width, args.height, body, args.title)


def preset_metric_card(args):
    body = f"""{gradient_defs("metric-gradient", [args.primary, args.secondary])}
  <rect x="1" y="1" width="{args.width - 2}" height="{args.height - 2}" rx="18" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <circle cx="{args.width - 48}" cy="46" r="18" fill="url(#metric-gradient)" opacity=".9">
    <animate attributeName="r" values="14;20;14" dur="1.8s" repeatCount="indefinite"/>
  </circle>
  {text(32, 48, args.label, 18, "#94a3b8", 600)}
  {text(32, 104, args.value, 48, "#f8fafc", 800)}
  {text(32, 142, args.subtitle, 16, "#cbd5e1", 500)}"""
    return svg(args.width, args.height, body, args.label)


def preset_divider(args):
    body = f"""{gradient_defs("divider-gradient", [args.primary, args.secondary])}
  <rect width="{args.width}" height="{args.height}" fill="none"/>
  <path d="M24 {args.height // 2}H{args.width - 24}" stroke="#1f2937" stroke-width="8" stroke-linecap="round"/>
  <path d="M24 {args.height // 2}H{args.width - 24}" stroke="url(#divider-gradient)" stroke-width="8" stroke-linecap="round" stroke-dasharray="80 220">
    <animate attributeName="stroke-dashoffset" values="0;-300" dur="2s" repeatCount="indefinite"/>
  </path>
  <circle cx="{args.width // 2}" cy="{args.height // 2}" r="8" fill="{args.secondary}"/>"""
    return svg(args.width, args.height, body, args.title)


def preset_progress(args):
    progress = max(0, min(100, int(args.value)))
    bar_width = args.width - 220
    fill_width = int(bar_width * progress / 100)
    body = f"""{gradient_defs("progress-gradient", [args.primary, args.secondary])}
  <rect x="1" y="1" width="{args.width - 2}" height="{args.height - 2}" rx="14" fill="#0b1220" stroke="#24324f" stroke-width="2"/>
  {text(28, 38, args.label, 17, "#e2e8f0", 700)}
  <rect x="170" y="20" width="{bar_width}" height="24" rx="12" fill="#111827"/>
  <rect x="170" y="20" width="{fill_width}" height="24" rx="12" fill="url(#progress-gradient)"/>
  {text(args.width - 34, 38, f"{progress}%", 16, "#f8fafc", 700, "end")}"""
    return svg(args.width, args.height, body, args.label)


def preset_roadmap(args):
    items = split_items(args.items, ["Plan", "Build", "Review", "Ship"])
    gap = (args.width - 100) // max(1, len(items[:5]) - 1)
    nodes = []
    for index, item in enumerate(items[:5]):
        x = 50 + index * gap
        color = args.primary if index < len(items[:5]) - 1 else "#334155"
        nodes.append(f'<circle cx="{x}" cy="58" r="14" fill="{color}" stroke="#f8fafc" stroke-width="2"/>')
        nodes.append(text(x, 98, item, 13, "#e5e7eb", 700, "middle"))
    body = f"""  <rect width="{args.width}" height="{args.height}" rx="14" fill="#0f172a"/>
  {text(28, 30, args.title, 18, args.secondary, 700)}
  <path d="M50 58H{args.width - 50}" stroke="#334155" stroke-width="6" stroke-linecap="round"/>
  {"".join(nodes)}"""
    return svg(args.width, args.height, body, args.title)


def preset_status_panel(args):
    items = split_items(args.items, ["API:healthy", "Docs:ready", "CI:passing"])
    rows = []
    for index, item in enumerate(items[:5]):
        label, _, value = item.partition(":")
        y = 68 + index * 34
        rows.append(f'<circle cx="34" cy="{y - 6}" r="6" fill="{args.primary}"><animate attributeName="opacity" values=".4;1;.4" dur="1.4s" begin="{index * .15}s" repeatCount="indefinite"/></circle>')
        rows.append(text(54, y, label, 16, "#e5e7eb", 700))
        rows.append(text(args.width - 34, y, value or "ok", 16, args.secondary, 700, "end"))
    body = f"""  <rect x="1" y="1" width="{args.width - 2}" height="{args.height - 2}" rx="14" fill="#07111f" stroke="#1e293b" stroke-width="2"/>
  {text(28, 34, args.title, 20, "#f8fafc", 800)}
  {"".join(rows)}"""
    return svg(args.width, args.height, body, args.title)


def preset_quote(args):
    body = f"""  <rect x="1" y="1" width="{args.width - 2}" height="{args.height - 2}" rx="18" fill="#111827" stroke="#334155" stroke-width="2"/>
  <text x="34" y="70" font-family="Georgia, serif" font-size="70" fill="{args.primary}" opacity=".75">“</text>
  {text(82, 70, args.title, 28, "#f8fafc", 800)}
  {text(84, 112, args.subtitle, 18, "#cbd5e1", 500)}
  <path d="M84 134h{args.width - 140}" stroke="{args.secondary}" stroke-width="4" stroke-linecap="round" stroke-dasharray="20 14">
    <animate attributeName="stroke-dashoffset" values="0;-68" dur="1.8s" repeatCount="indefinite"/>
  </path>"""
    return svg(args.width, args.height, body, args.title)


def preset_feature_grid(args):
    items = split_items(args.items, ["Fast setup", "Typed API", "Clean docs", "Release ready"])
    cells = []
    for index, item in enumerate(items[:4]):
        col = index % 2
        row = index // 2
        x = 28 + col * ((args.width - 72) // 2 + 16)
        y = 52 + row * 76
        w = (args.width - 88) // 2
        cells.append(f'<rect x="{x}" y="{y}" width="{w}" height="56" rx="12" fill="#111827" stroke="#24324f" stroke-width="2"/>')
        cells.append(f'<circle cx="{x + 24}" cy="{y + 28}" r="8" fill="{args.primary}"/>')
        cells.append(text(x + 44, y + 34, item, 16, "#e5e7eb", 700))
    body = f"""  <rect width="{args.width}" height="{args.height}" rx="14" fill="#08111f"/>
  {text(28, 32, args.title, 20, args.secondary, 800)}
  {"".join(cells)}"""
    return svg(args.width, args.height, body, args.title)


def preset_architecture(args):
    body = f"""  <rect width="{args.width}" height="{args.height}" rx="14" fill="#07111f"/>
  {text(28, 34, args.title, 20, "#f8fafc", 800)}
  <g fill="#111827" stroke="{args.primary}" stroke-width="3">
    <rect x="44" y="70" width="130" height="54" rx="12"/>
    <rect x="{args.width // 2 - 65}" y="70" width="130" height="54" rx="12"/>
    <rect x="{args.width - 174}" y="70" width="130" height="54" rx="12"/>
  </g>
  <path d="M174 97H{args.width // 2 - 65}M{args.width // 2 + 65} 97H{args.width - 174}" stroke="{args.secondary}" stroke-width="4" stroke-linecap="round" stroke-dasharray="10 12">
    <animate attributeName="stroke-dashoffset" values="0;-44" dur="1.2s" repeatCount="indefinite"/>
  </path>
  {text(109, 103, "client", 15, "#e5e7eb", 700, "middle")}
  {text(args.width // 2, 103, "service", 15, "#e5e7eb", 700, "middle")}
  {text(args.width - 109, 103, "data", 15, "#e5e7eb", 700, "middle")}"""
    return svg(args.width, args.height, body, args.title)


def preset_wave_banner(args):
    body = f"""{gradient_defs("wave-gradient", [args.primary, args.secondary])}
  <rect width="{args.width}" height="{args.height}" rx="14" fill="#020617"/>
  <path d="M0 {args.height - 38}C120 {args.height - 80} 210 {args.height - 10} 330 {args.height - 48}S540 {args.height - 90} {args.width} {args.height - 44}V{args.height}H0Z" fill="url(#wave-gradient)" opacity=".45">
    <animate attributeName="d" values="M0 {args.height - 38}C120 {args.height - 80} 210 {args.height - 10} 330 {args.height - 48}S540 {args.height - 90} {args.width} {args.height - 44}V{args.height}H0Z;M0 {args.height - 48}C140 {args.height - 18} 220 {args.height - 90} 360 {args.height - 40}S560 {args.height - 12} {args.width} {args.height - 58}V{args.height}H0Z;M0 {args.height - 38}C120 {args.height - 80} 210 {args.height - 10} 330 {args.height - 48}S540 {args.height - 90} {args.width} {args.height - 44}V{args.height}H0Z" dur="4s" repeatCount="indefinite"/>
  </path>
  {text(38, 76, args.title, 34, "#f8fafc", 800)}
  {text(40, 112, args.subtitle, 17, "#cbd5e1", 500)}"""
    return svg(args.width, args.height, body, args.title)


def preset_profile_card(args):
    body = f"""{gradient_defs("profile-gradient", [args.primary, args.secondary])}
  <rect x="1" y="1" width="{args.width - 2}" height="{args.height - 2}" rx="18" fill="#0f172a" stroke="#334155" stroke-width="2"/>
  <circle cx="66" cy="70" r="32" fill="url(#profile-gradient)"/>
  <circle cx="66" cy="59" r="10" fill="#f8fafc"/>
  <path d="M44 91c6-15 38-15 44 0" fill="#f8fafc"/>
  {text(118, 58, args.title, 26, "#f8fafc", 800)}
  {text(120, 91, args.subtitle, 17, "#cbd5e1", 500)}
  <rect x="120" y="112" width="{args.width - 160}" height="8" rx="4" fill="#1e293b"/>
  <rect x="120" y="112" width="{max(80, args.width // 3)}" height="8" rx="4" fill="url(#profile-gradient)">
    <animate attributeName="width" values="{max(80, args.width // 4)};{max(100, args.width // 3)};{max(80, args.width // 4)}" dur="2.2s" repeatCount="indefinite"/>
  </rect>"""
    return svg(args.width, args.height, body, args.title)


PRESETS = {
    "terminal": preset_terminal,
    "badge-strip": preset_badge_strip,
    "metric-card": preset_metric_card,
    "divider": preset_divider,
    "progress": preset_progress,
    "roadmap": preset_roadmap,
    "status-panel": preset_status_panel,
    "quote": preset_quote,
    "feature-grid": preset_feature_grid,
    "architecture": preset_architecture,
    "wave-banner": preset_wave_banner,
    "profile-card": preset_profile_card,
}


def build_svg(args):
    return PRESETS[args.preset](args)


def run_self_test():
    for preset in PRESETS:
        args = argparse.Namespace(
            preset=preset,
            title="Project System",
            subtitle="Reusable README visual",
            label="coverage",
            value="82",
            items="build:passing|docs:ready|release:stable",
            primary="#38bdf8",
            secondary="#a78bfa",
            width=720,
            height=180,
        )
        ET.fromstring(build_svg(args))
    print(f"generate_readme_svg.py self-tests passed for {len(PRESETS)} presets.")


def main():
    parser = argparse.ArgumentParser(description="Generate reusable README SVG visuals.")
    parser.add_argument("--preset", choices=sorted(PRESETS), default="wave-banner")
    parser.add_argument("--title", default="Project System")
    parser.add_argument("--subtitle", default="Reusable README visual")
    parser.add_argument("--label", default="progress")
    parser.add_argument("--value", default="82")
    parser.add_argument("--items", default="", help="Pipe-separated items. Use label:value for status-like presets.")
    parser.add_argument("--primary", default="#38bdf8")
    parser.add_argument("--secondary", default="#a78bfa")
    parser.add_argument("--width", type=int, default=720)
    parser.add_argument("--height", type=int, default=180)
    parser.add_argument("--output", default="readme_visual.svg")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(args), encoding="utf-8")
    print(f"Generated {output} with preset {args.preset}")


if __name__ == "__main__":
    main()
