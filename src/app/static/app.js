/**
 * @module app/static/app
 * @description Local Studio client controller for readme-ux-kit asset browsing,
 * SVG token editing, GIF export, diagnostics, and local data governance.
 */

const APP_VERSION = "1.0.0";
const MAX_SVG_BYTES = 524288;
const MAX_JSON_BYTES = 65536;
const FORBIDDEN_KEYS = new Set(["__proto__", "constructor", "prototype"]);

const state = {
  selected: null,
  selectedSource: "",
  editedSvg: "",
  editedPreviewUrl: "",
  editorLastFocus: null,
  supportLastFocus: null,
  lastGifExport: null,
  loadSeq: 0,
  selectSeq: 0,
  reducedMotion: false,
  lastError: null,
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
  studioOpenHelp: document.querySelector("#studio-open-help"),
  studioOpenSupport: document.querySelector("#studio-open-support"),
  studioFooterHelp: document.querySelector("#studio-footer-help"),
  studioFooterBug: document.querySelector("#studio-footer-bug"),
  studioFooterExport: document.querySelector("#studio-footer-export"),
  studioFooterPurge: document.querySelector("#studio-footer-purge"),
  studioErrorBanner: document.querySelector("#studio-error-banner"),
  studioErrorMessage: document.querySelector("#studio-error-message"),
  studioErrorDetails: document.querySelector("#studio-error-details"),
  studioErrorRecover: document.querySelector("#studio-error-recover"),
  studioErrorReport: document.querySelector("#studio-error-report"),
  studioSupportModal: document.querySelector("#studio-support-modal"),
  studioSupportClose: document.querySelector("#studio-support-close"),
  studioBugArea: document.querySelector("#studio-bug-area"),
  studioBugDesc: document.querySelector("#studio-bug-desc"),
  studioBugSteps: document.querySelector("#studio-bug-steps"),
  studioBugPreview: document.querySelector("#studio-bug-preview"),
  studioCopyDiagnostic: document.querySelector("#studio-copy-diagnostic"),
  studioDownloadDiagnostic: document.querySelector("#studio-download-diagnostic"),
  studioFeedbackRating: document.querySelector("#studio-feedback-rating"),
  studioFeedbackCategory: document.querySelector("#studio-feedback-category"),
  studioFeedbackComment: document.querySelector("#studio-feedback-comment"),
  studioCopyFeedback: document.querySelector("#studio-copy-feedback"),
  studioDownloadFeedback: document.querySelector("#studio-download-feedback"),
  studioExportData: document.querySelector("#studio-export-data"),
  studioPurgeData: document.querySelector("#studio-purge-data"),
  studioLangSelect: document.querySelector("#studio-lang-select"),
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
  nodes.summary.replaceChildren();
  const rows = [
    ["Assets", summary.assetCount],
    ["Categories", Object.keys(summary.categoryCounts || {}).length],
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

  const allOption = document.createElement("option");
  allOption.value = "";
  allOption.textContent = "All categories";
  nodes.category.replaceChildren(allOption);
  for (const category of Object.keys(summary.categoryCounts || {}).sort()) {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = `${category} (${summary.categoryCounts[category]})`;
    nodes.category.append(option);
  }
}

function renderAssets(payload) {
  nodes.count.textContent = `${payload.matchCount} shown from ${payload.assetCount} assets`;
  nodes.grid.replaceChildren();
  if (!payload.assets.length) {
    nodes.grid.append(createEmptyState("No assets match the current filters."));
    return;
  }

  for (const asset of payload.assets) {
    const card = document.createElement("article");
    card.className = "asset-card";
    if (state.selected?.localPath === asset.localPath) card.classList.add("is-selected");
    card.tabIndex = 0;
    card.setAttribute("role", "button");
    card.setAttribute("aria-label", `${asset.name} (${asset.category} / ${asset.subcategory})`);

    const img = document.createElement("img");
    img.alt = asset.name;
    img.src = assetSourceUrl(asset.localPath);
    img.loading = "lazy";
    attachImageFallback(img, asset.name);

    const body = document.createElement("div");
    body.className = "asset-card-body";

    const title = document.createElement("h3");
    title.className = "asset-title";
    title.textContent = asset.name;

    const meta = document.createElement("p");
    meta.className = "asset-meta";
    meta.textContent = `${asset.category} / ${asset.subcategory}`;

    const tagRow = document.createElement("div");
    tagRow.className = "tag-row";
    for (const tag of (asset.tags || []).slice(0, 4)) {
      const span = document.createElement("span");
      span.className = "tag";
      span.textContent = tag;
      tagRow.append(span);
    }

    body.append(title, meta, tagRow);
    card.append(img, body);

    card.addEventListener("click", () => selectAsset(asset.localPath));
    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectAsset(asset.localPath);
      }
    });
    nodes.grid.append(card);
  }
}

async function loadSummary() {
  const summary = await api("/api/summary");
  renderSummary(summary);
}

async function loadAssets() {
  const seq = ++state.loadSeq;
  const params = new URLSearchParams();
  if (nodes.search.value) params.set("q", nodes.search.value);
  if (nodes.category.value) params.set("category", nodes.category.value);
  if (nodes.quality.value) params.set("editorQuality", nodes.quality.value);
  if (nodes.animated.value) params.set("animated", nodes.animated.value);
  const payload = await api(`/api/assets?${params.toString()}`);
  if (seq !== state.loadSeq) return;
  renderAssets(payload);
}

async function selectAsset(path) {
  if (!isSafeAssetUrl(path)) {
    throw new Error(`Unsafe asset path rejected: ${path}`);
  }
  const seq = ++state.selectSeq;
  const detail = await api(`/api/assets/detail/${assetPath(path)}`);
  if (seq !== state.selectSeq) return;
  state.selected = detail.asset;
  state.selectedSource = detail.source;
  state.editedSvg = "";
  state.lastGifExport = null;
  nodes.detailTitle.textContent = detail.asset.name;
  nodes.detailPath.textContent = detail.asset.localPath;
  delete nodes.detailPreview.dataset.fallbackApplied;
  nodes.detailPreview.src = assetSourceUrl(detail.asset.localPath);
  nodes.detailPreview.alt = detail.asset.name;
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
  nodes.editorMeta.replaceChildren();
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
  nodes.editorColorList.replaceChildren();
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
    picker.setAttribute("aria-label", `Target color for ${token.value}`);

    const hex = document.createElement("input");
    hex.type = "text";
    hex.maxLength = 7;
    hex.value = token.value;
    hex.className = "color-hex";
    hex.spellcheck = false;
    hex.setAttribute("aria-label", `Target hex value for ${token.value}`);

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
  nodes.editorTextList.replaceChildren();
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
    input.maxLength = 512;
    input.dataset.original = item.value || "";
    input.dataset.target = item.editId || item.id || item.nodePath || item.value || "";
    label.append(caption, input);
    nodes.editorTextList.append(label);
  }
}

function renderElementControls(editor) {
  nodes.editorElementList.replaceChildren();
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

function setEditedPreviewSvg(svgMarkup, label = "Edited SVG preview") {
  if (svgMarkup && new Blob([svgMarkup]).size > MAX_SVG_BYTES) {
    throw new Error(`SVG payload exceeds maximum size of ${MAX_SVG_BYTES} bytes.`);
  }
  if (state.editedPreviewUrl) {
    URL.revokeObjectURL(state.editedPreviewUrl);
    state.editedPreviewUrl = "";
  }
  const blob = new Blob([svgMarkup || "<svg xmlns='http://www.w3.org/2000/svg'/>"], { type: "image/svg+xml" });
  const url = URL.createObjectURL(blob);
  state.editedPreviewUrl = url;
  delete nodes.editorEditedPreview.dataset.fallbackApplied;
  nodes.editorEditedPreview.src = url;
  nodes.editorEditedPreview.alt = label;
}

function renderEditor() {
  const asset = state.selected;
  if (!asset) return;
  const editor = asset.editor || {};
  nodes.editorTitle.textContent = asset.name;
  nodes.editorSubtitle.textContent = asset.localPath;
  delete nodes.editorOriginalPreview.dataset.fallbackApplied;
  nodes.editorOriginalPreview.src = assetSourceUrl(asset.localPath);
  nodes.editorOriginalPreview.alt = `${asset.name} original preview`;
  setEditedPreviewSvg(state.editedSvg || state.selectedSource, `${asset.name} edited preview`);
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
  if (state.editorLastFocus instanceof HTMLElement) {
    state.editorLastFocus.focus();
    state.editorLastFocus = null;
  }
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
  sanitizeJsonObject(advanced);
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
    if (FORBIDDEN_KEYS.has(key)) {
      throw new Error(`Forbidden key in JSON payload: ${key}`);
    }
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
  if (advancedText.length > MAX_JSON_BYTES) {
    throw new Error(`Advanced JSON exceeds maximum size of ${MAX_JSON_BYTES} bytes.`);
  }
  if (advancedText && advancedText !== "{}") {
    const parsedAdvanced = sanitizeJsonObject(JSON.parse(advancedText));
    operations = mergeAdvancedOperations(operations, parsedAdvanced);
  }
  return sanitizeJsonObject(operations);
}

async function applyEditorPreview() {
  if (!state.selected) return;
  const operations = editorOperations();
  if (!Object.keys(operations).length) {
    state.editedSvg = "";
    setEditedPreviewSvg(state.selectedSource, `${state.selected.name} original preview`);
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
  setEditedPreviewSvg(result.svg, `${state.selected.name} edited preview`);
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
    if (new Blob([state.editedSvg]).size > MAX_SVG_BYTES) {
      throw new Error(`Edited SVG exceeds maximum size of ${MAX_SVG_BYTES} bytes.`);
    }
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
    const supportOpen = Boolean(nodes.studioSupportModal?.open || nodes.studioSupportModal?.hasAttribute("open"));
    if (supportOpen) return;
    if (event.key === "Escape" && !nodes.editorOverlay.hidden) {
      closeEditor();
    } else if (event.key === "Tab" && !nodes.editorOverlay.hidden) {
      trapFocusInOverlay(event, nodes.editorOverlay);
    } else if (event.key === "?" && !isTypingInEditableField(event.target)) {
      event.preventDefault();
      openStudioSupportModal("studio-help-heading");
    }
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
  if (nodes.studioOpenHelp) nodes.studioOpenHelp.addEventListener("click", () => openStudioSupportModal("studio-help-heading"));
  if (nodes.studioOpenSupport) nodes.studioOpenSupport.addEventListener("click", () => openStudioSupportModal("studio-bug-area"));
  if (nodes.studioFooterHelp) nodes.studioFooterHelp.addEventListener("click", () => openStudioSupportModal("studio-help-heading"));
  if (nodes.studioFooterBug) nodes.studioFooterBug.addEventListener("click", () => openStudioSupportModal("studio-bug-area"));
  if (nodes.studioFooterExport) nodes.studioFooterExport.addEventListener("click", exportStudioDataJson);
  if (nodes.studioFooterPurge) nodes.studioFooterPurge.addEventListener("click", purgeStudioLocalData);
  if (nodes.studioSupportClose) nodes.studioSupportClose.addEventListener("click", closeStudioSupportModal);
  if (nodes.studioSupportModal) {
    nodes.studioSupportModal.addEventListener("click", (event) => {
      if (event.target === nodes.studioSupportModal) closeStudioSupportModal();
    });
    nodes.studioSupportModal.addEventListener("close", restoreStudioSupportFocus);
  }
  if (nodes.studioBugArea) nodes.studioBugArea.addEventListener("change", updateStudioDiagnosticPreview);
  if (nodes.studioBugDesc) nodes.studioBugDesc.addEventListener("input", updateStudioDiagnosticPreview);
  if (nodes.studioBugSteps) nodes.studioBugSteps.addEventListener("input", updateStudioDiagnosticPreview);
  if (nodes.studioCopyDiagnostic) nodes.studioCopyDiagnostic.addEventListener("click", copyStudioDiagnosticBundle);
  if (nodes.studioDownloadDiagnostic) nodes.studioDownloadDiagnostic.addEventListener("click", downloadStudioDiagnosticBundle);
  if (nodes.studioCopyFeedback) nodes.studioCopyFeedback.addEventListener("click", copyStudioFeedback);
  if (nodes.studioDownloadFeedback) nodes.studioDownloadFeedback.addEventListener("click", downloadStudioFeedback);
  if (nodes.studioExportData) nodes.studioExportData.addEventListener("click", exportStudioDataJson);
  if (nodes.studioPurgeData) nodes.studioPurgeData.addEventListener("click", purgeStudioLocalData);
  if (nodes.studioLangSelect) {
    nodes.studioLangSelect.addEventListener("change", () => {
      const lang = nodes.studioLangSelect.value || "en";
      document.documentElement.lang = lang;
      updateStudioDiagnosticPreview();
      setOutput(`Interface language updated to ${lang}.`);
    });
  }
  if (nodes.studioErrorRecover) nodes.studioErrorRecover.addEventListener("click", recoverStudioFromError);
  if (nodes.studioErrorReport) {
    nodes.studioErrorReport.addEventListener("click", () => {
      if (state.lastError && nodes.studioBugDesc) {
        nodes.studioBugDesc.value = `Crash recovery report: ${state.lastError.message}`;
      }
      openStudioSupportModal("studio-bug-area");
    });
  }
  window.addEventListener("error", (event) => {
    showStudioRuntimeError(event.error || new Error(event.message || "Unhandled script error"), "window.onerror");
  });
  window.addEventListener("unhandledrejection", (event) => {
    showStudioRuntimeError(event.reason || new Error("Unhandled promise rejection"), "unhandledrejection");
  });
  bindEditorEvents();
}

function isSafeAssetUrl(url) {
  const raw = String(url || "").trim();
  if (!raw || raw.length > 2048) return false;
  const lower = raw.toLowerCase();
  if (lower.startsWith("javascript:") || lower.startsWith("vbscript:") || lower.startsWith("data:text/html") || lower.startsWith("file:")) {
    return false;
  }
  if (/^data:image\/(?:png|jpeg|jpg|webp|gif);base64,[a-z0-9+/=]+$/i.test(raw)) {
    return true;
  }
  if (lower.startsWith("data:")) {
    return false;
  }
  if (raw.includes("\\") || raw.includes("..") || raw.startsWith("//")) {
    return false;
  }
  if (raw.includes("://")) {
    try {
      const parsed = new URL(raw);
      return parsed.protocol === "https:" && !parsed.username && !parsed.password;
    } catch {
      return false;
    }
  }
  return raw.startsWith("assets/") || raw.startsWith("/local-assets/") || raw.startsWith("/api/assets/");
}

function sanitizeJsonObject(value, depth = 0) {
  if (depth > 16) {
    throw new Error("JSON operations exceed maximum allowed nesting depth.");
  }
  if (Array.isArray(value)) {
    for (const item of value) sanitizeJsonObject(item, depth + 1);
    return value;
  }
  if (value && typeof value === "object") {
    for (const key of Object.keys(value)) {
      if (!Object.prototype.hasOwnProperty.call(value, key)) continue;
      if (FORBIDDEN_KEYS.has(key)) {
        throw new Error(`Forbidden key in JSON payload: ${key}`);
      }
      sanitizeJsonObject(value[key], depth + 1);
    }
  }
  return value;
}

function sanitizeAttachmentFilename(filename, fallback = "readme-ux-export.json") {
  const raw = String(filename || fallback).replace(/\0/g, "").replace(/[<>"'&/\\]+/g, "-").replace(/\.\.+/g, "-").trim();
  const blocked = /\.(?:exe|bat|cmd|sh|ps1|msi|dll|scr|vbs|jar|com|pif)(?:\.|$)/i;
  if (!raw || blocked.test(raw)) return fallback;
  return raw.slice(0, 160);
}

function attachImageFallback(image, label) {
  if (!image) return;
  image.addEventListener("load", () => {
    if (!String(image.src || "").startsWith("data:image/svg+xml")) {
      delete image.dataset.fallbackApplied;
    }
  });
  image.addEventListener("error", () => {
    if (image.dataset.fallbackApplied === "true") return;
    image.dataset.fallbackApplied = "true";
    const safeTitle = escapeHtml(label || "SVG preview unavailable");
    const fallbackSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 200" role="img" aria-label="${safeTitle}"><rect width="480" height="200" rx="12" fill="#111827" stroke="#334155" stroke-width="2"/><text x="240" y="96" fill="#e2e8f0" font-family="system-ui,sans-serif" font-size="15" font-weight="700" text-anchor="middle">${safeTitle}</text><text x="240" y="124" fill="#94a3b8" font-family="system-ui,sans-serif" font-size="12" text-anchor="middle">Preview fallback active</text></svg>`;
    image.src = `data:image/svg+xml;utf8,${encodeURIComponent(fallbackSvg)}`;
  });
}

function trapFocusInOverlay(event, container) {
  const focusable = [...container.querySelectorAll("button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), summary, [tabindex]:not([tabindex='-1'])")]
    .filter((element) => element instanceof HTMLElement && !element.hidden && element.offsetParent !== null);
  if (!focusable.length) return;
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}

function isTypingInEditableField(target) {
  if (!(target instanceof HTMLElement)) return false;
  const tag = target.tagName;
  return tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || target.isContentEditable;
}

function setupStudioReducedMotion() {
  if (typeof window.matchMedia !== "function") return;
  const media = window.matchMedia("(prefers-reduced-motion: reduce)");
  const update = () => {
    state.reducedMotion = Boolean(media.matches);
    document.body.dataset.reducedMotion = String(state.reducedMotion);
  };
  update();
  if (typeof media.addEventListener === "function") {
    media.addEventListener("change", update);
  }
}

function openStudioSupportModal(focusTargetId) {
  updateStudioDiagnosticPreview();
  if (!nodes.studioSupportModal) return;
  const alreadyOpen = Boolean(nodes.studioSupportModal.open || nodes.studioSupportModal.hasAttribute("open"));
  if (!alreadyOpen) {
    state.supportLastFocus = document.activeElement;
    if (typeof nodes.studioSupportModal.showModal === "function") {
      nodes.studioSupportModal.showModal();
    } else {
      nodes.studioSupportModal.setAttribute("open", "");
    }
  }
  const target = focusTargetId ? document.getElementById(focusTargetId) : nodes.studioSupportClose;
  if (target instanceof HTMLElement) target.focus();
}

function closeStudioSupportModal() {
  if (!nodes.studioSupportModal) return;
  if (typeof nodes.studioSupportModal.close === "function") {
    nodes.studioSupportModal.close();
  } else {
    nodes.studioSupportModal.removeAttribute("open");
  }
  restoreStudioSupportFocus();
}

function restoreStudioSupportFocus() {
  if (state.supportLastFocus instanceof HTMLElement) {
    state.supportLastFocus.focus();
    state.supportLastFocus = null;
  }
}

function buildStudioDiagnosticBundle() {
  return {
    schemaVersion: 1,
    app: "readme-ux-kit-local-studio",
    appVersion: APP_VERSION,
    mode: "local-loopback-studio",
    piiFree: true,
    timestamp: new Date().toISOString(),
    locale: document.documentElement.lang || navigator.language || "en",
    viewport: {
      width: window.innerWidth,
      height: window.innerHeight,
      reducedMotion: state.reducedMotion,
    },
    viewState: {
      selectedAsset: state.selected?.localPath || null,
      categoryFilter: nodes.category?.value || "",
      qualityFilter: nodes.quality?.value || "",
      animatedFilter: nodes.animated?.value || "",
      editorOpen: !nodes.editorOverlay?.hidden,
    },
    issueReport: {
      affectedArea: nodes.studioBugArea?.value || "Asset Browser & Filters",
      summary: (nodes.studioBugDesc?.value || "").trim().slice(0, 4000),
      reproductionSteps: (nodes.studioBugSteps?.value || "").trim().slice(0, 4000),
      lastRuntimeError: state.lastError ? state.lastError.message : null,
    },
  };
}

function updateStudioDiagnosticPreview() {
  if (!nodes.studioBugPreview) return;
  nodes.studioBugPreview.textContent = JSON.stringify(buildStudioDiagnosticBundle(), null, 2);
}

function triggerStudioDownload(content, filename) {
  const url = URL.createObjectURL(new Blob([content], { type: "application/json" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = sanitizeAttachmentFilename(filename);
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

async function copyStudioDiagnosticBundle() {
  const bundle = JSON.stringify(buildStudioDiagnosticBundle(), null, 2);
  await copy(bundle);
  setOutput("Copied PII-free diagnostic bundle to clipboard.");
}

function downloadStudioDiagnosticBundle() {
  const bundle = JSON.stringify(buildStudioDiagnosticBundle(), null, 2);
  triggerStudioDownload(bundle, "readme-ux-kit-studio-diagnostic.json");
  setOutput("Downloaded PII-free diagnostic bundle JSON.");
}

function buildStudioFeedbackPayload() {
  return {
    schemaVersion: 1,
    app: "readme-ux-kit-local-studio",
    appVersion: APP_VERSION,
    timestamp: new Date().toISOString(),
    rating: Number(nodes.studioFeedbackRating?.value || 5),
    category: nodes.studioFeedbackCategory?.value || "Local Studio UX",
    comment: (nodes.studioFeedbackComment?.value || "").trim().slice(0, 4000),
  };
}

async function copyStudioFeedback() {
  const payload = JSON.stringify(buildStudioFeedbackPayload(), null, 2);
  await copy(payload);
  setOutput("Copied structured feedback JSON to clipboard.");
}

function downloadStudioFeedback() {
  const payload = JSON.stringify(buildStudioFeedbackPayload(), null, 2);
  triggerStudioDownload(payload, "readme-ux-kit-studio-feedback.json");
  setOutput("Downloaded structured feedback JSON.");
}

function exportStudioDataJson() {
  const localKeys = {};
  try {
    for (let i = 0; i < localStorage.length; i += 1) {
      const key = localStorage.key(i);
      if (key) localKeys[key] = localStorage.getItem(key);
    }
  } catch {
    // Storage access may be restricted.
  }
  const archive = {
    schemaVersion: 1,
    exportType: "GDPR-Article-15-20-SAR-Data-Export",
    app: "readme-ux-kit-local-studio",
    appVersion: APP_VERSION,
    exportedAt: new Date().toISOString(),
    storageInventory: {
      localStorage: localKeys,
      sessionStorage: {},
      cookies: [],
    },
    workspaceState: {
      selectedAsset: state.selected?.localPath || null,
      filters: {
        search: nodes.search?.value || "",
        category: nodes.category?.value || "",
        quality: nodes.quality?.value || "",
        animated: nodes.animated?.value || "",
      },
    },
  };
  triggerStudioDownload(JSON.stringify(archive, null, 2), "readme-ux-kit-user-data-export.json");
  setOutput("Exported Local Studio workspace data (JSON).");
}

async function purgeStudioLocalData() {
  try {
    localStorage.clear();
    sessionStorage.clear();
  } catch {
    // Storage access may be restricted.
  }
  if (state.editedPreviewUrl) {
    URL.revokeObjectURL(state.editedPreviewUrl);
    state.editedPreviewUrl = "";
  }
  state.selected = null;
  state.selectedSource = "";
  state.editedSvg = "";
  state.lastGifExport = null;
  if (nodes.search) nodes.search.value = "";
  if (nodes.category) nodes.category.value = "";
  if (nodes.quality) nodes.quality.value = "";
  if (nodes.animated) nodes.animated.value = "";
  if (nodes.studioLangSelect) nodes.studioLangSelect.value = "en";
  document.documentElement.lang = "en";
  nodes.detailTitle.textContent = "Select an asset";
  nodes.detailPath.textContent = "Choose from the asset grid to preview, copy, or edit.";
  nodes.detailPreview.hidden = true;
  resetGifPanel();
  await loadAssets();
  setOutput("Purged all local storage and reset Local Studio workspace state.");
}

function showStudioRuntimeError(error, sourceLabel = "runtime") {
  const message = error instanceof Error ? error.message : String(error || "Unknown runtime fault");
  const stack = error instanceof Error && error.stack ? error.stack : `${sourceLabel}: ${message}`;
  state.lastError = { message, stack, sourceLabel, timestamp: new Date().toISOString() };
  if (nodes.studioErrorMessage) {
    nodes.studioErrorMessage.textContent = `A recoverable fault occurred (${message}). Use Reset / Recover to restore the default studio state.`;
  }
  if (nodes.studioErrorDetails) {
    nodes.studioErrorDetails.textContent = stack;
  }
  if (nodes.studioErrorBanner) {
    nodes.studioErrorBanner.hidden = false;
  }
  setOutput(`Runtime error caught: ${message}`);
}

async function recoverStudioFromError() {
  state.lastError = null;
  if (nodes.studioErrorBanner) nodes.studioErrorBanner.hidden = true;
  if (!nodes.editorOverlay.hidden) closeEditor();
  if (nodes.studioSupportModal?.hasAttribute("open")) closeStudioSupportModal();
  await purgeStudioLocalData();
  setOutput("Recovered Local Studio workspace cleanly.");
}

async function boot() {
  setupStudioReducedMotion();
  attachImageFallback(nodes.detailPreview, "Selected asset preview");
  attachImageFallback(nodes.gifPreview, "Generated GIF preview");
  attachImageFallback(nodes.editorOriginalPreview, "Original SVG preview");
  attachImageFallback(nodes.editorEditedPreview, "Edited SVG preview");
  bindEvents();
  await loadSummary();
  await loadAssets();
  const params = new URLSearchParams(window.location.search);
  const selectedAsset = params.get("asset");
  if (selectedAsset && isSafeAssetUrl(selectedAsset)) {
    await selectAsset(selectedAsset);
    if (params.get("editor") === "1") openEditor();
  }
}

boot().catch((error) => showStudioRuntimeError(error, "boot"));
