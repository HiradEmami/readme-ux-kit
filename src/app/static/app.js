const state = {
  selected: null,
  selectedSource: "",
  editedSvg: "",
  editorLastFocus: null,
  lastGifExport: null,
};

const nodes = {
  grid: document.querySelector("#asset-grid"),
  count: document.querySelector("#asset-count"),
  category: document.querySelector("#filter-category"),
  search: document.querySelector("#filter-search"),
  quality: document.querySelector("#filter-quality"),
  animated: document.querySelector("#filter-animated"),
  summary: document.querySelector("#summary-list"),
  output: document.querySelector("#command-output"),
  detailTitle: document.querySelector("#detail-title"),
  detailPath: document.querySelector("#detail-path"),
  detailPreview: document.querySelector("#detail-preview"),
  copyMarkdown: document.querySelector("#copy-markdown"),
  copyHtml: document.querySelector("#copy-html"),
  openEditor: document.querySelector("#open-editor"),
  editorOverlay: document.querySelector("#editor-overlay"),
  editorClose: document.querySelector("#editor-close"),
  editorTitle: document.querySelector("#editor-title"),
  editorSubtitle: document.querySelector("#editor-subtitle"),
  editorMeta: document.querySelector("#editor-meta"),
  editorOriginalPreview: document.querySelector("#editor-original-preview"),
  editorEditedPreview: document.querySelector("#editor-edited-preview"),
  editorResult: document.querySelector("#editor-result"),
  editorColorList: document.querySelector("#editor-color-list"),
  editorTextList: document.querySelector("#editor-text-list"),
  editorElementList: document.querySelector("#editor-element-list"),
  editorSpeedRange: document.querySelector("#editor-speed-range"),
  editorSpeedNumber: document.querySelector("#editor-speed-number"),
  editorMotionStatus: document.querySelector("#editor-motion-status"),
  editorAdvancedJson: document.querySelector("#editor-advanced-json"),
  editorReset: document.querySelector("#editor-reset"),
  editorApply: document.querySelector("#editor-apply"),
  editorCopySvg: document.querySelector("#editor-copy-svg"),
  gifOutputDir: document.querySelector("#gif-output-dir"),
  gifFileName: document.querySelector("#gif-file-name"),
  gifDuration: document.querySelector("#gif-duration"),
  gifFps: document.querySelector("#gif-fps"),
  gifMaxWidth: document.querySelector("#gif-max-width"),
  gifMaxHeight: document.querySelector("#gif-max-height"),
  gifBackground: document.querySelector("#gif-background"),
  gifUseEdited: document.querySelector("#gif-use-edited"),
  gifExport: document.querySelector("#gif-export"),
  gifCopyMarkdown: document.querySelector("#gif-copy-markdown"),
  gifCopyHtml: document.querySelector("#gif-copy-html"),
  gifPreview: document.querySelector("#gif-preview"),
  gifResult: document.querySelector("#gif-result"),
};

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "content-type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const contentType = response.headers.get("content-type") || "";
  const body = contentType.includes("application/json") ? await response.json() : await response.text();
  if (!response.ok) {
    const message = typeof body === "string" ? body : body.detail || JSON.stringify(body);
    throw new Error(message);
  }
  return body;
}

function assetPath(path) {
  return String(path).split("/").map(encodeURIComponent).join("/");
}

function assetSourceUrl(path) {
  return `/api/assets/source/${assetPath(path)}`;
}

function copy(text) {
  return navigator.clipboard.writeText(text);
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;",
  }[character]));
}

function markdownSnippet(asset) {
  const source = asset.rawUrl || asset.localPath;
  return `[![${asset.name}](${source})](https://github.com/HiradEmami/readme-ux-kit)`;
}

function htmlSnippet(asset) {
  const source = escapeHtml(asset.rawUrl || asset.localPath);
  return `<img alt="${escapeHtml(asset.name)}" src="${source}">`;
}

function gifFileUrl(path) {
  return `/api/gif/file/${assetPath(path)}?t=${Date.now()}`;
}

function defaultGifFileName(asset, edited = false) {
  if (!asset) return "";
  const stem = String(asset.localPath || asset.name || "readme-ux-export")
    .split("/")
    .pop()
    .replace(/\.svg$/i, "")
    .replace(/[^A-Za-z0-9._-]+/g, "-")
    .replace(/^[-._]+|[-._]+$/g, "")
    .toLowerCase() || "readme-ux-export";
  return `${stem}${edited ? "-edited" : ""}.gif`;
}

function setOutput(value) {
  nodes.output.textContent = value;
}

function setEditorResult(value) {
  nodes.editorResult.textContent = value;
}

function setGifResult(value) {
  nodes.gifResult.textContent = value;
}

function normalizeHex(value) {
  const match = String(value || "").trim().match(/^#?([0-9a-f]{3}|[0-9a-f]{6})$/i);
  if (!match) return "";
  const body = match[1].toLowerCase();
  if (body.length === 3) {
    return `#${body.split("").map((character) => character + character).join("")}`;
  }
  return `#${body}`;
}

function uniqueHexTokens(tokens = []) {
  const seen = new Set();
  const output = [];
  for (const token of tokens) {
    const value = normalizeHex(token.value);
    if (!value || seen.has(value)) continue;
    seen.add(value);
    output.push({ ...token, value });
  }
  return output;
}

function editableOperations(item, operation) {
  return (item.operations || []).includes(operation);
}

function createEmptyState(text) {
  const element = document.createElement("p");
  element.className = "empty-state";
  element.textContent = text;
  return element;
}

function renderSummary(summary) {
  nodes.summary.innerHTML = "";
  const rows = [
    ["Assets", summary.assetCount],
    ["Commands", summary.commands.length],
    ["Generated data", summary.dataFiles.filter((item) => item.exists).length],
    ["Local only", summary.localOnly ? "yes" : "no"],
  ];
  for (const [label, value] of rows) {
    const dt = document.createElement("dt");
    const dd = document.createElement("dd");
    dt.textContent = label;
    dd.textContent = value;
    nodes.summary.append(dt, dd);
  }

  nodes.category.innerHTML = '<option value="">All categories</option>';
  for (const category of Object.keys(summary.categoryCounts || {}).sort()) {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = `${category} (${summary.categoryCounts[category]})`;
    nodes.category.append(option);
  }
}

function renderAssets(payload) {
  nodes.count.textContent = `${payload.matchCount} shown from ${payload.assetCount} assets`;
  nodes.grid.innerHTML = "";
  if (!payload.assets.length) {
    nodes.grid.append(createEmptyState("No assets match the current filters."));
    return;
  }

  for (const asset of payload.assets) {
    const card = document.createElement("article");
    card.className = "asset-card";
    if (state.selected?.localPath === asset.localPath) card.classList.add("is-selected");
    card.tabIndex = 0;
    const tagHtml = (asset.tags || [])
      .slice(0, 4)
      .map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`)
      .join("");
    card.innerHTML = `
      <img alt="${escapeHtml(asset.name)}" src="${assetSourceUrl(asset.localPath)}" loading="lazy">
      <div class="asset-card-body">
        <h3 class="asset-title">${escapeHtml(asset.name)}</h3>
        <p class="asset-meta">${escapeHtml(asset.category)} / ${escapeHtml(asset.subcategory)}</p>
        <div class="tag-row">${tagHtml}</div>
      </div>
    `;
    card.addEventListener("click", () => selectAsset(asset.localPath));
    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter") selectAsset(asset.localPath);
    });
    nodes.grid.append(card);
  }
}

async function loadSummary() {
  const summary = await api("/api/summary");
  renderSummary(summary);
}

async function loadAssets() {
  const params = new URLSearchParams();
  if (nodes.search.value) params.set("q", nodes.search.value);
  if (nodes.category.value) params.set("category", nodes.category.value);
  if (nodes.quality.value) params.set("editorQuality", nodes.quality.value);
  if (nodes.animated.value) params.set("animated", nodes.animated.value);
  const payload = await api(`/api/assets?${params.toString()}`);
  renderAssets(payload);
}

async function selectAsset(path) {
  const detail = await api(`/api/assets/detail/${assetPath(path)}`);
  state.selected = detail.asset;
  state.selectedSource = detail.source;
  state.editedSvg = "";
  state.lastGifExport = null;
  nodes.detailTitle.textContent = detail.asset.name;
  nodes.detailPath.textContent = detail.asset.localPath;
  nodes.detailPreview.src = assetSourceUrl(detail.asset.localPath);
  nodes.detailPreview.hidden = false;
  nodes.copyMarkdown.disabled = false;
  nodes.copyHtml.disabled = false;
  nodes.openEditor.disabled = false;
  nodes.editorCopySvg.disabled = true;
  resetGifPanel();
  if (!nodes.editorOverlay.hidden) renderEditor();
  await loadAssets();
}

function resetGifPanel() {
  nodes.gifFileName.value = defaultGifFileName(state.selected);
  nodes.gifUseEdited.checked = false;
  nodes.gifUseEdited.disabled = true;
  nodes.gifExport.disabled = !state.selected;
  nodes.gifCopyMarkdown.disabled = true;
  nodes.gifCopyHtml.disabled = true;
  nodes.gifPreview.hidden = true;
  nodes.gifPreview.removeAttribute("src");
  setGifResult(state.selected ? "Ready." : "Select an asset.");
}

function syncGifEditedOption() {
  const canUseEdited = Boolean(state.selected && state.editedSvg);
  nodes.gifUseEdited.disabled = !canUseEdited;
  if (!canUseEdited) nodes.gifUseEdited.checked = false;
  if (state.selected) {
    nodes.gifFileName.value = defaultGifFileName(state.selected, nodes.gifUseEdited.checked);
  }
}

function renderEditorMeta(editor) {
  nodes.editorMeta.innerHTML = "";
  const values = [
    state.selected.type,
    `${editor.quality?.level || state.selected.editorQuality || "unknown"} editor quality`,
    ...(editor.capabilities || []),
  ].filter(Boolean);
  for (const value of values.slice(0, 6)) {
    const badge = document.createElement("span");
    badge.className = "meta-badge";
    badge.textContent = value;
    nodes.editorMeta.append(badge);
  }
}

function renderColorControls(editor) {
  nodes.editorColorList.innerHTML = "";
  const tokens = uniqueHexTokens(editor.colorTokens || []).slice(0, 18);
  if (!tokens.length) {
    nodes.editorColorList.append(createEmptyState("No editable hex colors detected."));
    return;
  }

  for (const token of tokens) {
    const row = document.createElement("div");
    row.className = "color-token";
    row.dataset.source = token.value;

    const sourceSwatch = document.createElement("span");
    sourceSwatch.className = "color-swatch";
    sourceSwatch.style.background = token.value;

    const label = document.createElement("div");
    label.className = "color-token-label";
    const name = document.createElement("strong");
    name.textContent = token.role || "color";
    const detail = document.createElement("span");
    detail.textContent = `${token.value} - ${token.count || 1} use${token.count === 1 ? "" : "s"}`;
    label.append(name, detail);

    const picker = document.createElement("input");
    picker.type = "color";
    picker.value = token.value;
    picker.className = "color-picker";

    const hex = document.createElement("input");
    hex.type = "text";
    hex.value = token.value;
    hex.className = "color-hex";
    hex.spellcheck = false;

    picker.addEventListener("input", () => {
      hex.value = picker.value;
    });
    hex.addEventListener("input", () => {
      const value = normalizeHex(hex.value);
      if (value) picker.value = value;
    });

    row.append(sourceSwatch, label, picker, hex);
    nodes.editorColorList.append(row);
  }
}

function renderTextControls(editor) {
  nodes.editorTextList.innerHTML = "";
  const textNodes = (editor.textNodes || []).filter((item) => editableOperations(item, "replaceText"));
  if (!textNodes.length) {
    nodes.editorTextList.append(createEmptyState("No editable text detected."));
    return;
  }

  for (const item of textNodes.slice(0, 18)) {
    const label = document.createElement("label");
    label.className = "text-control";
    const caption = document.createElement("span");
    caption.textContent = item.editLabel || item.id || item.nodePath || "Text";
    const input = document.createElement("input");
    input.type = "text";
    input.value = item.value || "";
    input.dataset.original = item.value || "";
    input.dataset.target = item.editId || item.id || item.nodePath || item.value || "";
    label.append(caption, input);
    nodes.editorTextList.append(label);
  }
}

function renderElementControls(editor) {
  nodes.editorElementList.innerHTML = "";
  const elements = (editor.removableElements || []).filter((item) => editableOperations(item, "hideElement"));
  if (!elements.length) {
    nodes.editorElementList.append(createEmptyState("No removable elements detected."));
    return;
  }

  for (const item of elements.slice(0, 24)) {
    const label = document.createElement("label");
    label.className = "element-control";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.dataset.target = item.editId || item.id || item.nodePath || "";
    const body = document.createElement("span");
    const title = document.createElement("strong");
    title.textContent = item.label || item.editLabel || item.tag || "Element";
    const detail = document.createElement("span");
    detail.textContent = `${item.tag || "node"} - ${item.hasAnimation ? "animated" : "static"}`;
    body.append(title, detail);
    label.append(checkbox, body);
    nodes.editorElementList.append(label);
  }
}

function renderMotionControls(editor) {
  const hasAnimation = Boolean(editor.animation?.hasAnimation);
  nodes.editorSpeedRange.value = "1";
  nodes.editorSpeedNumber.value = "1";
  nodes.editorSpeedRange.disabled = !hasAnimation;
  nodes.editorSpeedNumber.disabled = !hasAnimation;
  const durations = (editor.animation?.durations || []).map((item) => item.value).join(", ");
  nodes.editorMotionStatus.textContent = hasAnimation ? `Detected: ${durations || "animation timing"}` : "No animation timing detected.";
}

function renderEditor() {
  const asset = state.selected;
  if (!asset) return;
  const editor = asset.editor || {};
  nodes.editorTitle.textContent = asset.name;
  nodes.editorSubtitle.textContent = asset.localPath;
  nodes.editorOriginalPreview.src = assetSourceUrl(asset.localPath);
  nodes.editorEditedPreview.innerHTML = state.editedSvg || state.selectedSource;
  nodes.editorAdvancedJson.value = "{}";
  nodes.editorCopySvg.disabled = !state.editedSvg;
  setEditorResult(state.editedSvg ? "Edited SVG is ready." : "No edits applied.");
  renderEditorMeta(editor);
  renderColorControls(editor);
  renderTextControls(editor);
  renderElementControls(editor);
  renderMotionControls(editor);
}

function openEditor() {
  if (!state.selected) return;
  state.editorLastFocus = document.activeElement;
  renderEditor();
  nodes.editorOverlay.hidden = false;
  document.body.classList.add("modal-open");
  nodes.editorClose.focus();
}

function closeEditor() {
  nodes.editorOverlay.hidden = true;
  document.body.classList.remove("modal-open");
  if (state.editorLastFocus) state.editorLastFocus.focus();
}

function readColorOperations() {
  const replaceColors = {};
  for (const row of nodes.editorColorList.querySelectorAll(".color-token")) {
    const source = row.dataset.source;
    const target = normalizeHex(row.querySelector(".color-hex").value);
    if (!target) {
      throw new Error(`Invalid color value for ${source}.`);
    }
    if (target !== source) replaceColors[source] = target;
  }
  return replaceColors;
}

function readTextOperations() {
  const replacements = [];
  for (const input of nodes.editorTextList.querySelectorAll("input[data-target]")) {
    if (input.value !== input.dataset.original) {
      replacements.push({ target: input.dataset.target, to: input.value });
    }
  }
  return replacements;
}

function readElementOperations() {
  return [...nodes.editorElementList.querySelectorAll("input[type='checkbox']:checked")]
    .map((input) => input.dataset.target)
    .filter(Boolean);
}

function mergeAdvancedOperations(operations, advanced) {
  if (!advanced || typeof advanced !== "object" || Array.isArray(advanced)) {
    throw new Error("Advanced JSON must be an object.");
  }
  if (advanced.replaceColors) {
    operations.replaceColors = { ...(operations.replaceColors || {}), ...advanced.replaceColors };
  }
  if (advanced.replaceText) {
    operations.replaceText = [...(operations.replaceText || []), ...advanced.replaceText];
  }
  if (advanced.removeElements) {
    operations.removeElements = [...new Set([...(operations.removeElements || []), ...advanced.removeElements])];
  }
  if (advanced.scaleAnimationSpeed) {
    operations.scaleAnimationSpeed = advanced.scaleAnimationSpeed;
  }
  for (const [key, value] of Object.entries(advanced)) {
    if (!(key in operations)) operations[key] = value;
  }
  return operations;
}

function editorOperations() {
  let operations = {};
  const replaceColors = readColorOperations();
  const replaceText = readTextOperations();
  const removeElements = readElementOperations();
  const speed = Number(nodes.editorSpeedNumber.value || nodes.editorSpeedRange.value);

  if (Object.keys(replaceColors).length) operations.replaceColors = replaceColors;
  if (replaceText.length) operations.replaceText = replaceText;
  if (removeElements.length) operations.removeElements = removeElements;
  if (speed && Math.abs(speed - 1) > 0.001) operations.scaleAnimationSpeed = speed;

  const advancedText = nodes.editorAdvancedJson.value.trim();
  if (advancedText && advancedText !== "{}") {
    operations = mergeAdvancedOperations(operations, JSON.parse(advancedText));
  }
  return operations;
}

async function applyEditorPreview() {
  if (!state.selected) return;
  const operations = editorOperations();
  if (!Object.keys(operations).length) {
    state.editedSvg = "";
    nodes.editorEditedPreview.innerHTML = state.selectedSource;
    nodes.editorCopySvg.disabled = true;
    syncGifEditedOption();
    setEditorResult("No edits selected.");
    return;
  }

  setEditorResult("Applying preview...");
  const result = await api("/api/svg/edit", {
    method: "POST",
    body: JSON.stringify({ path: state.selected.localPath, operations }),
  });
  state.editedSvg = result.svg;
  nodes.editorEditedPreview.innerHTML = result.svg;
  nodes.editorCopySvg.disabled = false;
  nodes.gifUseEdited.checked = true;
  syncGifEditedOption();
  setEditorResult(JSON.stringify(result.summary, null, 2));
}

async function runCommand(command) {
  setOutput(`Running ${command}...`);
  const result = await api(`/api/run/${command}`, { method: "POST", body: "{}" });
  setOutput([result.stdout, result.stderr].filter(Boolean).join("\n") || `Command ${command} completed.`);
  if (command.startsWith("generate")) {
    await loadSummary();
    await loadAssets();
  }
}

function numericValue(node, fallback) {
  const value = Number(node.value);
  return Number.isFinite(value) ? value : fallback;
}

async function exportSelectedGif() {
  if (!state.selected) return;
  const useEdited = Boolean(nodes.gifUseEdited.checked && state.editedSvg);
  const payload = {
    path: state.selected.localPath,
    outputDir: nodes.gifOutputDir.value,
    fileName: nodes.gifFileName.value,
    durationMs: numericValue(nodes.gifDuration, 1600),
    fps: numericValue(nodes.gifFps, 16),
    maxWidth: numericValue(nodes.gifMaxWidth, 960),
    maxHeight: numericValue(nodes.gifMaxHeight, 360),
    background: nodes.gifBackground.value,
  };
  if (useEdited) {
    payload.source = state.editedSvg;
    payload.sourcePath = state.selected.localPath;
    payload.name = `${state.selected.name} edited`;
  }

  nodes.gifExport.disabled = true;
  setGifResult(`Rendering ${payload.fileName || "GIF"}...`);
  try {
    const result = await api("/api/gif/export", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    state.lastGifExport = result;
    nodes.gifPreview.src = gifFileUrl(result.outputPath);
    nodes.gifPreview.hidden = false;
    nodes.gifCopyMarkdown.disabled = false;
    nodes.gifCopyHtml.disabled = false;
    setGifResult([
      `Wrote ${result.outputPath}`,
      `${result.dimensions.renderWidth}x${result.dimensions.renderHeight}, ${result.renderSettings.frameCount} frames`,
      `${result.byteLength} bytes`,
    ].join("\n"));
  } finally {
    nodes.gifExport.disabled = false;
  }
}

function bindEditorEvents() {
  nodes.openEditor.addEventListener("click", openEditor);
  nodes.editorClose.addEventListener("click", closeEditor);
  nodes.editorOverlay.addEventListener("click", (event) => {
    if (event.target === nodes.editorOverlay) closeEditor();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !nodes.editorOverlay.hidden) closeEditor();
  });
  nodes.editorSpeedRange.addEventListener("input", () => {
    nodes.editorSpeedNumber.value = nodes.editorSpeedRange.value;
  });
  nodes.editorSpeedNumber.addEventListener("input", () => {
    const value = Number(nodes.editorSpeedNumber.value);
    if (value >= 0.25 && value <= 3) nodes.editorSpeedRange.value = String(value);
  });
  nodes.editorReset.addEventListener("click", () => {
    state.editedSvg = "";
    renderEditor();
    syncGifEditedOption();
  });
  nodes.editorApply.addEventListener("click", () => applyEditorPreview().catch((error) => setEditorResult(error.message)));
  nodes.editorCopySvg.addEventListener("click", () => {
    if (state.editedSvg) copy(state.editedSvg).then(() => setEditorResult("Copied edited SVG."));
  });
}

function bindEvents() {
  let searchTimer = 0;
  nodes.search.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(loadAssets, 180);
  });
  nodes.category.addEventListener("change", loadAssets);
  nodes.quality.addEventListener("change", loadAssets);
  nodes.animated.addEventListener("change", loadAssets);
  document.querySelector("#refresh-assets").addEventListener("click", loadAssets);
  document.querySelector("#run-generate").addEventListener("click", () => runCommand("generate-all-data").catch((error) => setOutput(error.message)));
  document.querySelector("#run-modules").addEventListener("click", () => runCommand("modules-check").catch((error) => setOutput(error.message)));
  document.querySelector("#run-all").addEventListener("click", () => runCommand("check-all").catch((error) => setOutput(error.message)));
  nodes.copyMarkdown.addEventListener("click", () => {
    if (state.selected) copy(markdownSnippet(state.selected)).then(() => setOutput("Copied Markdown snippet."));
  });
  nodes.copyHtml.addEventListener("click", () => {
    if (state.selected) copy(htmlSnippet(state.selected)).then(() => setOutput("Copied HTML snippet."));
  });
  nodes.gifUseEdited.addEventListener("change", () => {
    if (state.selected) {
      nodes.gifFileName.value = defaultGifFileName(state.selected, nodes.gifUseEdited.checked);
    }
  });
  nodes.gifExport.addEventListener("click", () => exportSelectedGif().catch((error) => setGifResult(error.message)));
  nodes.gifCopyMarkdown.addEventListener("click", () => {
    if (state.lastGifExport) copy(state.lastGifExport.copy.markdown).then(() => setGifResult("Copied GIF Markdown snippet."));
  });
  nodes.gifCopyHtml.addEventListener("click", () => {
    if (state.lastGifExport) copy(state.lastGifExport.copy.html).then(() => setGifResult("Copied GIF HTML snippet."));
  });
  bindEditorEvents();
}

async function boot() {
  bindEvents();
  await loadSummary();
  await loadAssets();
  const params = new URLSearchParams(window.location.search);
  const selectedAsset = params.get("asset");
  if (selectedAsset) {
    await selectAsset(selectedAsset);
    if (params.get("editor") === "1") openEditor();
  }
}

boot().catch((error) => setOutput(error.message));
