/**
 * @module site/app
 * @description Self-contained static browser showcase, interactive SVG editor,
 * diagnostic reporter, and local data governance controller for readme-ux-kit.
 */

const APP_VERSION = "1.0.0";
const REPO_OWNER = "HiradEmami";
const REPO_NAME = "readme-ux-kit";
const REPO_URL = `https://github.com/${REPO_OWNER}/${REPO_NAME}`;
const RAW_BASE = `https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/master`;
const FAVORITES_KEY = "readmeUxKitFavorites";
const GRID_OPTIONS = ["1", "2", "3", "5", "7"];
const MAX_SVG_BYTES = 524288;
const MAX_JSON_BYTES = 65536;
const FORBIDDEN_KEYS = new Set(["__proto__", "constructor", "prototype"]);
const DEFAULT_GIF_SETTINGS = {
  outputDir: "output/gifs",
  durationMs: 1600,
  fps: 16,
  maxWidth: 960,
  maxHeight: 360,
  background: "#ffffff",
};

const STYLE_FILTERS = [
  "All Themes",
  "Architecture",
  "Interface",
  "Motion",
  "Terminal",
  "Security",
  "Progress",
  "Catalog",
  "Energy",
  "Core",
];

const state = {
  manifest: null,
  assets: [],
  query: "",
  category: "all",
  theme: "All Themes",
  cols: "3",
  favoritesOnly: false,
  favorites: loadFavorites(),
  flipped: new Set(),
  order: [],
  orderIndex: new Map(),
  editorPalettes: [],
  editorPresets: [],
  svgCache: new Map(),
  modalLastFocus: null,
  supportLastFocus: null,
  reducedMotion: false,
  lastError: null,
  editor: {
    item: null,
    source: "",
    editedSvg: "",
    editedUrl: "",
    lastOperations: {},
    lastFocus: null,
    gifFileNameTouched: false,
  },
};

const nodes = {
  body: document.body,
  searchInput: document.getElementById("searchInput"),
  controlPanel: document.querySelector(".control-panel"),
  categoryFilterToggle: document.getElementById("categoryFilterToggle"),
  categoryFilterLabel: document.getElementById("categoryFilterLabel"),
  categoryFilterCount: document.getElementById("categoryFilterCount"),
  categoryPopover: document.getElementById("categoryPopover"),
  categoryPopoverClose: document.getElementById("categoryPopoverClose"),
  categoryFilters: document.getElementById("categoryFilters"),
  themeFilterToggle: document.getElementById("themeFilterToggle"),
  themeFilterLabel: document.getElementById("themeFilterLabel"),
  themeFilterCount: document.getElementById("themeFilterCount"),
  themePopover: document.getElementById("themePopover"),
  themePopoverClose: document.getElementById("themePopoverClose"),
  themeFilters: document.getElementById("themeFilters"),
  gridCycle: document.getElementById("gridCycle"),
  gridCycleIcon: document.getElementById("gridCycleIcon"),
  gridCycleText: document.getElementById("gridCycleText"),
  assetGrid: document.getElementById("assetGrid"),
  resultCount: document.getElementById("resultCount"),
  totalAssets: document.getElementById("totalAssets"),
  categoryCount: document.getElementById("categoryCount"),
  favoriteCount: document.getElementById("favoriteCount"),
  gridSummary: document.getElementById("gridSummary"),
  status: document.getElementById("status"),
  emptyState: document.getElementById("emptyState"),
  favoritesOnly: document.getElementById("favoritesOnly"),
  shuffleCards: document.getElementById("shuffleCards"),
  openHelpModal: document.getElementById("openHelpModal"),
  openSupportModal: document.getElementById("openSupportModal"),
  footerHelpBtn: document.getElementById("footerHelpBtn"),
  footerBugReportBtn: document.getElementById("footerBugReportBtn"),
  footerExportDataBtn: document.getElementById("footerExportDataBtn"),
  footerPurgeDataBtn: document.getElementById("footerPurgeDataBtn"),
  errorBanner: document.getElementById("errorBanner"),
  errorBannerMessage: document.getElementById("errorBannerMessage"),
  errorTechnicalDetails: document.getElementById("errorTechnicalDetails"),
  errorRecoverBtn: document.getElementById("errorRecoverBtn"),
  errorReportBtn: document.getElementById("errorReportBtn"),
  copyBundle: document.getElementById("copyBundle"),
  actionsAll: document.getElementById("actionsAll"),
  previewAll: document.getElementById("previewAll"),
  assetModal: document.getElementById("assetModal"),
  modalTitle: document.getElementById("modalTitle"),
  modalMeta: document.getElementById("modalMeta"),
  modalImage: document.getElementById("modalImage"),
  modalPath: document.getElementById("modalPath"),
  modalClose: document.getElementById("modalClose"),
  modalDownload: document.getElementById("modalDownload"),
  modalCopyMd: document.getElementById("modalCopyMd"),
  modalCopySvg: document.getElementById("modalCopySvg"),
  modalCopyHtml: document.getElementById("modalCopyHtml"),
  modalSource: document.getElementById("modalSource"),
  editorModal: document.getElementById("editorModal"),
  editorTitle: document.getElementById("editorTitle"),
  editorMeta: document.getElementById("editorMeta"),
  editorSubtitle: document.getElementById("editorSubtitle"),
  editorBadges: document.getElementById("editorBadges"),
  editorClose: document.getElementById("editorClose"),
  editorOriginalImage: document.getElementById("editorOriginalImage"),
  editorEditedImage: document.getElementById("editorEditedImage"),
  editorStatus: document.getElementById("editorStatus"),
  editorPaletteList: document.getElementById("editorPaletteList"),
  editorColorList: document.getElementById("editorColorList"),
  editorTextList: document.getElementById("editorTextList"),
  editorElementList: document.getElementById("editorElementList"),
  editorSpeedRange: document.getElementById("editorSpeedRange"),
  editorSpeedNumber: document.getElementById("editorSpeedNumber"),
  editorMotionStatus: document.getElementById("editorMotionStatus"),
  editorGifOutputDir: document.getElementById("editorGifOutputDir"),
  editorGifFileName: document.getElementById("editorGifFileName"),
  editorGifDuration: document.getElementById("editorGifDuration"),
  editorGifFps: document.getElementById("editorGifFps"),
  editorGifMaxWidth: document.getElementById("editorGifMaxWidth"),
  editorGifMaxHeight: document.getElementById("editorGifMaxHeight"),
  editorGifBackground: document.getElementById("editorGifBackground"),
  editorCopyGifCommand: document.getElementById("editorCopyGifCommand"),
  editorCopyGifPayload: document.getElementById("editorCopyGifPayload"),
  editorAdvancedJson: document.getElementById("editorAdvancedJson"),
  editorPath: document.getElementById("editorPath"),
  editorReset: document.getElementById("editorReset"),
  editorApply: document.getElementById("editorApply"),
  editorCopySvg: document.getElementById("editorCopySvg"),
  editorDownloadSvg: document.getElementById("editorDownloadSvg"),
  editorCopyMd: document.getElementById("editorCopyMd"),
  editorCopyHtml: document.getElementById("editorCopyHtml"),
  supportModal: document.getElementById("supportModal"),
  supportModalClose: document.getElementById("supportModalClose"),
  bugAreaSelect: document.getElementById("bugAreaSelect"),
  bugDescription: document.getElementById("bugDescription"),
  bugSteps: document.getElementById("bugSteps"),
  bugDiagnosticPreview: document.getElementById("bugDiagnosticPreview"),
  copyDiagnosticBtn: document.getElementById("copyDiagnosticBtn"),
  downloadDiagnosticBtn: document.getElementById("downloadDiagnosticBtn"),
  feedbackRating: document.getElementById("feedbackRating"),
  feedbackCategory: document.getElementById("feedbackCategory"),
  feedbackComment: document.getElementById("feedbackComment"),
  copyFeedbackBtn: document.getElementById("copyFeedbackBtn"),
  downloadFeedbackBtn: document.getElementById("downloadFeedbackBtn"),
  exportUserDataBtn: document.getElementById("exportUserDataBtn"),
  purgeUserDataBtn: document.getElementById("purgeUserDataBtn"),
  interfaceLangSelect: document.getElementById("interfaceLangSelect"),
};

async function boot() {
  setupReducedMotionListener();
  attachImageFallback(nodes.modalImage, "Large asset preview");
  attachImageFallback(nodes.editorOriginalImage, "Original SVG preview");
  attachImageFallback(nodes.editorEditedImage, "Edited SVG preview");
  bindEvents();
  setDensity(state.cols);
  setControlsDisabled(true);

  try {
    const [manifest, paletteData, presetData] = await Promise.all([
      loadManifest(),
      loadJson("./data/theme-palettes.json", { palettes: [] }),
      loadJson("./data/editor-presets.json", { presets: [] }),
    ]);
    state.manifest = manifest;
    state.editorPalettes = Array.isArray(paletteData.palettes) ? paletteData.palettes : [];
    state.editorPresets = Array.isArray(presetData.presets) ? presetData.presets : [];
    state.assets = normalizeAssets(manifest.assets || []);
    state.order = state.assets.map((item) => item.key);
    updateOrderIndex();
    render();
    setControlsDisabled(false);
    setStatus(`Ready. ${state.assets.length} generated SVG assets loaded.`);
  } catch (error) {
    nodes.emptyState.textContent = "Could not load site/data/assets.json. Serve the repository locally or deploy the site with generated data.";
    nodes.emptyState.classList.add("is-visible");
    nodes.gridSummary.textContent = error.message;
    setStatus(error.message);
  }
}

async function loadManifest() {
  const response = await fetch("./data/assets.json", { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Asset data request failed: ${response.status}`);
  }
  const payload = await response.json();
  if (!Array.isArray(payload.assets)) {
    throw new Error("Asset data is missing an assets array.");
  }
  return payload;
}

async function loadJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) throw new Error(`${path} request failed: ${response.status}`);
    return await response.json();
  } catch {
    return fallback;
  }
}

function normalizeAssets(assets) {
  return assets.map((asset, index) => {
    const path = asset.localPath || asset.path || "";
    const name = asset.name || path.split("/").pop()?.replace(/\.svg$/i, "") || `asset_${index + 1}`;
    const category = asset.category || "uncategorized";
    const subcategory = asset.subcategory || "general";
    const tags = Array.isArray(asset.tags) ? asset.tags.filter(Boolean) : [];
    const styleThemes = inferStyleThemes({ ...asset, name, category, subcategory, tags });
    const dimensions = asset.dimensions || {};
    const aspectRatio = normalizedAspectRatio(dimensions);
    const previewShape = previewShapeFor({ category, subcategory, dimensions, aspectRatio });
    const label = humanize(name);
    const categoryLabel = humanize(category);
    const subcategoryLabel = humanize(subcategory);
    const operationList = normalizeOperationList(asset.editor?.operations || []);
    const description = assetDescription({
      ...asset,
      name,
      categoryLabel,
      subcategoryLabel,
      styleThemes,
      dimensions,
      operationList,
    });

    const searchable = [
      name,
      label,
      category,
      categoryLabel,
      subcategory,
      subcategoryLabel,
      asset.type,
      asset.editorQuality,
      tags.join(" "),
      styleThemes.join(" "),
      operationList.join(" "),
      description,
    ].join(" ").toLowerCase();

    return {
      ...asset,
      key: path || name,
      name,
      label,
      category,
      categoryLabel,
      subcategory,
      subcategoryLabel,
      path,
      localPath: path,
      rawUrl: asset.rawUrl || `${RAW_BASE}/${path}`,
      sourceUrl: sourceUrl(path),
      previewUrl: previewUrl(asset.previewPath),
      tags,
      styleThemes,
      theme: styleThemes[0] || "Core",
      dimensions,
      aspectRatio,
      previewShape,
      operationList,
      description,
      searchText: searchable,
    };
  });
}

function inferStyleThemes(asset) {
  const haystack = [
    asset.name,
    asset.category,
    asset.subcategory,
    asset.type,
    asset.editorQuality,
    ...(asset.tags || []),
  ].join(" ").toLowerCase();

  const matches = [];
  addStyle(matches, "Architecture", haystack, ["isometric", "3d", "architecture", "topology", "diagram", "cloud", "mesh", "pipeline", "storage", "cluster", "axonometric"]);
  addStyle(matches, "Terminal", haystack, ["terminal", "cli", "command", "console", "shell", "code"]);
  addStyle(matches, "Security", haystack, ["security", "privacy", "shield", "vault", "auth", "secret", "policy", "incident", "danger", "alert", "cyber"]);
  addStyle(matches, "Progress", haystack, ["progress", "roadmap", "status", "maturity", "coverage", "release", "dataset", "lifecycle", "readiness"]);
  addStyle(matches, "Catalog", haystack, ["gallery", "catalog", "docs", "documentation", "template", "faq", "examples", "readme", "file"]);
  addStyle(matches, "Energy", haystack, ["energy", "reactor", "neural", "quantum", "plasma", "vortex", "glow", "neon", "particle", "orbit", "solar", "portal", "wave"]);
  addStyle(matches, "Interface", haystack, ["button", "icon", "ui", "copy", "search", "filter", "panel", "menu", "navigation", "settings", "toggle"]);

  if (asset.animated || haystack.includes("animated") || haystack.includes("loading") || haystack.includes("spinner") || haystack.includes("pulse")) {
    if (!matches.includes("Motion")) matches.unshift("Motion");
  }

  if (!matches.length) matches.push("Core");
  return [...new Set(matches)];
}

function addStyle(matches, label, haystack, tokens) {
  if (tokens.some((token) => haystack.includes(token)) && !matches.includes(label)) {
    matches.push(label);
  }
}

function normalizedAspectRatio(dimensions = {}) {
  const width = Number(dimensions.width);
  const height = Number(dimensions.height);
  const ratio = Number(dimensions.aspectRatio) || (width > 0 && height > 0 ? width / height : 0);
  return Number.isFinite(ratio) && ratio > 0 ? ratio : 0;
}

function previewShapeFor(asset) {
  const ratio = asset.aspectRatio || normalizedAspectRatio(asset.dimensions);
  const width = Number(asset.dimensions?.width) || 0;
  const height = Number(asset.dimensions?.height) || 0;
  const area = width * height;

  if (ratio >= 16) return "strip";
  if (ratio >= 4) return "wide";
  if (ratio > 0 && ratio <= 0.85) return "tall";
  if (area >= 700000) return "large";
  return "standard";
}

function assetDescription(asset) {
  const motion = asset.animated ? "Animated" : "Static";
  const size = asset.dimensions?.width && asset.dimensions?.height
    ? `${asset.dimensions.width}x${asset.dimensions.height}`
    : "scalable";
  const quality = asset.editorQuality ? `${asset.editorQuality} editor metadata` : "editor metadata";
  const operations = asset.operationList?.length ? ` Supports ${asset.operationList.join(", ")}.` : "";
  return `${motion} ${asset.categoryLabel.toLowerCase()} asset for ${asset.theme?.toLowerCase() || "README"} sections. ${size}, ${quality}.${operations}`;
}

function render() {
  renderCategories();
  renderThemes();
  updateFilterTriggers();
  renderGrid();
  updateMetrics();
}

function renderCategories() {
  nodes.categoryFilters.replaceChildren();
  for (const option of categoryOptions()) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = option.id === state.category ? "chip is-active" : "chip";
    button.dataset.category = option.id;
    button.setAttribute("aria-pressed", String(option.id === state.category));
    appendChipLabel(button, option.label, option.count);
    button.addEventListener("click", () => {
      state.category = option.id;
      closeFilterPopovers();
      render();
      setStatus(`${option.label} category selected.`);
    });
    nodes.categoryFilters.append(button);
  }
}

function renderThemes() {
  nodes.themeFilters.replaceChildren();
  const counts = styleCounts();
  const allCount = matchingAssets({ includeTheme: false }).length;
  for (const label of STYLE_FILTERS) {
    const count = label === "All Themes" ? allCount : counts.get(label) || 0;
    const button = document.createElement("button");
    button.type = "button";
    button.className = label === state.theme ? "chip is-active" : "chip";
    button.dataset.theme = label;
    button.setAttribute("aria-pressed", String(label === state.theme));
    appendChipLabel(button, label, count);
    button.addEventListener("click", () => {
      state.theme = label;
      closeFilterPopovers();
      render();
      setStatus(`${label} theme filter selected.`);
    });
    nodes.themeFilters.append(button);
  }
}

function appendChipLabel(button, label, count) {
  const text = document.createElement("span");
  text.textContent = label;
  const countEl = document.createElement("span");
  countEl.className = "chip-count";
  countEl.textContent = String(count);
  button.append(text, countEl);
}

function categoryOptions() {
  const sourceAssets = matchingAssets({ includeCategory: false });
  const counts = new Map();
  for (const item of sourceAssets) {
    counts.set(item.category, (counts.get(item.category) || 0) + 1);
  }
  const options = [{ id: "all", label: "All", count: sourceAssets.length }];
  for (const category of allCategories()) {
    options.push({ id: category, label: humanize(category), count: counts.get(category) || 0 });
  }
  return options;
}

function styleCounts() {
  const sourceAssets = matchingAssets({ includeTheme: false });
  const counts = new Map();
  for (const item of sourceAssets) {
    for (const style of item.styleThemes) {
      counts.set(style, (counts.get(style) || 0) + 1);
    }
  }
  return counts;
}

function filteredAssets() {
  const visible = matchingAssets();
  return visible.sort((a, b) => (state.orderIndex.get(a.key) ?? 0) - (state.orderIndex.get(b.key) ?? 0));
}

function matchingAssets({ includeCategory = true, includeTheme = true } = {}) {
  const query = state.query.trim().toLowerCase();
  return state.assets.filter((item) => {
    const matchesQuery = !query || item.searchText.includes(query);
    const matchesCategory = !includeCategory || state.category === "all" || item.category === state.category;
    const matchesTheme = !includeTheme || state.theme === "All Themes" || item.styleThemes.includes(state.theme);
    const matchesFavorite = !state.favoritesOnly || state.favorites.has(item.key);
    return matchesQuery && matchesCategory && matchesTheme && matchesFavorite;
  });
}

function allCategories() {
  return [...new Set(state.assets.map((item) => item.category))]
    .sort((a, b) => a.localeCompare(b));
}

function renderGrid() {
  const visible = filteredAssets();
  nodes.assetGrid.replaceChildren();
  nodes.resultCount.textContent = String(visible.length);
  nodes.emptyState.classList.toggle("is-visible", visible.length === 0);
  updateGridSummary(visible.length);

  const fragment = document.createDocumentFragment();
  visible.forEach((item, index) => {
    const card = buildCard(item);
    card.style.setProperty("--delay", `${Math.min(index * 18, 180)}ms`);
    fragment.append(card);
  });
  nodes.assetGrid.append(fragment);
}

function buildCard(item) {
  const card = document.createElement("article");
  card.className = "asset-card";
  card.dataset.assetKey = item.key;
  card.dataset.previewShape = item.previewShape;
  card.tabIndex = 0;
  card.setAttribute("aria-label", `${item.label}. Press Enter to switch between preview and actions.`);
  card.classList.toggle("is-favorite", state.favorites.has(item.key));
  card.classList.toggle("is-flipped", state.flipped.has(item.key));

  const favorite = iconButton("favorite-toggle", state.favorites.has(item.key) ? starFilled() : starOutline(), `Favorite ${item.label}`);
  favorite.setAttribute("aria-pressed", String(state.favorites.has(item.key)));
  favorite.addEventListener("click", (event) => {
    event.stopPropagation();
    toggleFavorite(item, card, favorite);
  });

  const flipper = document.createElement("div");
  flipper.className = "card-flip";

  const isFlipped = state.flipped.has(item.key);
  const front = document.createElement("div");
  front.className = "card-face card-front";
  front.inert = isFlipped;

  const preview = document.createElement("div");
  preview.className = "preview";
  preview.dataset.previewShape = item.previewShape;
  const image = document.createElement("img");
  image.src = assetDisplayUrl(item);
  image.alt = item.label;
  image.loading = "lazy";
  image.decoding = "async";
  applyImageMetadata(image, item);
  attachImageFallback(image, item.label);
  preview.append(image);

  const bodyEl = document.createElement("div");
  bodyEl.className = "card-body";

  const titleRow = document.createElement("div");
  titleRow.className = "card-title-row";
  titleRow.append(titleBlock(item), tagEl(item.theme));

  const switchRow = document.createElement("div");
  switchRow.className = "switch-row";
  const hint = document.createElement("span");
  hint.textContent = cardFootnote(item);
  const flip = document.createElement("button");
  flip.type = "button";
  flip.className = "button secondary flip-button";
  flip.textContent = isFlipped ? "Preview" : "Actions";
  flip.addEventListener("click", (event) => {
    event.stopPropagation();
    const isKeyboard = event.detail === 0;
    toggleFlipped(item.key, isKeyboard ? "keyboard" : "pointer");
    if (isKeyboard) {
      backButton.focus();
    } else {
      releaseCardFocus(card);
    }
  });
  switchRow.append(hint, flip);

  bodyEl.append(titleRow, switchRow);
  front.append(favorite, preview, bodyEl);

  const back = document.createElement("div");
  back.className = "card-face card-back";
  back.inert = !isFlipped;

  const backHead = document.createElement("div");
  backHead.className = "back-head";
  const backButton = document.createElement("button");
  backButton.type = "button";
  backButton.className = "icon-button";
  backButton.setAttribute("aria-label", `Return to ${item.label} preview`);
  backButton.replaceChildren(createSvgIcon("close"));
  backButton.addEventListener("click", (event) => {
    event.stopPropagation();
    const isKeyboard = event.detail === 0;
    toggleFlipped(item.key, isKeyboard ? "keyboard" : "pointer");
    if (isKeyboard) {
      flip.focus();
    } else {
      releaseCardFocus(card);
    }
  });
  backHead.append(titleBlock(item), backButton);

  const summary = document.createElement("p");
  summary.className = "card-summary";
  summary.textContent = item.description;

  const pathText = document.createElement("code");
  pathText.className = "asset-path";
  pathText.textContent = item.path;

  const actions = document.createElement("div");
  actions.className = "card-actions";
  actions.append(
    actionButton("Edit", "secondary", (event) => {
      event.stopPropagation();
      openEditor(item);
    }),
    actionButton("Make Bigger", "secondary", (event) => {
      event.stopPropagation();
      openBigger(item);
    }),
    actionButton("Download", "", (event) => {
      event.stopPropagation();
      downloadAsset(item);
    }),
    actionButton("Copy MD", "primary", (event) => {
      event.stopPropagation();
      copyText(markdownSnippet(item), `Markdown copied for ${item.label}.`);
    }),
    actionButton("Copy SVG", "", (event) => {
      event.stopPropagation();
      copySvgMarkup(item);
    }),
    actionButton("Copy HTML", "", (event) => {
      event.stopPropagation();
      copyText(htmlSnippet(item), `HTML copied for ${item.label}.`);
    }),
    actionButton("Copy Raw", "", (event) => {
      event.stopPropagation();
      copyText(item.rawUrl, `Raw URL copied for ${item.label}.`);
    }),
    actionLink("Source", item.sourceUrl),
    actionLink("Preview", item.previewUrl)
  );

  back.append(backHead, summary, pathText, actions);
  flipper.append(front, back);
  card.append(flipper);

  card.addEventListener("click", () => {
    toggleFlipped(item.key, "pointer");
    releaseCardFocus(card);
  });
  card.addEventListener("pointerleave", () => closePointerFlippedCard(item.key));
  card.addEventListener("keydown", (event) => {
    if ((event.key === "Enter" || event.key === " ") && event.target === card) {
      event.preventDefault();
      toggleFlipped(item.key, "keyboard");
    }
  });

  return card;
}

function titleBlock(item) {
  const wrapper = document.createElement("div");
  const title = document.createElement("strong");
  title.textContent = item.label;
  const meta = document.createElement("span");
  meta.textContent = `${item.categoryLabel} / ${item.subcategoryLabel}`;
  wrapper.append(title, meta);
  return wrapper;
}

function tagEl(value) {
  const tag = document.createElement("span");
  tag.className = "tag";
  tag.textContent = value;
  tag.title = `Theme: ${value}`;
  tag.setAttribute("aria-label", `Theme: ${value}`);
  return tag;
}

function cardFootnote(item) {
  const motion = item.animated ? "Animated" : "Static";
  const size = item.dimensions?.width && item.dimensions?.height
    ? `${item.dimensions.width}x${item.dimensions.height}`
    : "Scalable";
  return `${motion} / ${size} SVG`;
}

function actionButton(label, kind, handler) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = `card-action ${kind}`.trim();
  button.dataset.action = slugify(label);
  button.textContent = label;
  button.addEventListener("click", handler);
  return button;
}

function actionLink(label, href) {
  const link = document.createElement("a");
  link.className = "card-action";
  link.dataset.action = slugify(label);
  link.href = isSafeAssetUrl(href) ? href : REPO_URL;
  link.target = "_blank";
  link.rel = "noreferrer";
  link.textContent = label;
  link.addEventListener("click", (event) => event.stopPropagation());
  return link;
}

function toggleFavorite(item, card, button) {
  const nextFavorite = !state.favorites.has(item.key);
  if (nextFavorite) {
    state.favorites.add(item.key);
    setStatus(`${item.label} added to favorites.`);
  } else {
    state.favorites.delete(item.key);
    setStatus(`${item.label} removed from favorites.`);
  }
  saveFavorites();
  button.replaceChildren(createSvgIcon(nextFavorite ? "star-filled" : "star-outline"));
  button.setAttribute("aria-pressed", String(nextFavorite));
  card.classList.toggle("is-favorite", nextFavorite);
  updateFilterTriggers();
  updateFavoriteCount();
  if (state.favoritesOnly && !nextFavorite) {
    card.remove();
    updateVisibleCountFromDom();
  }
}

function toggleFlipped(key, source = "programmatic") {
  const nextFlipped = !state.flipped.has(key);
  setCardFlipped(key, nextFlipped, source);
  const item = state.assets.find((assetItem) => assetItem.key === key);
  if (item) {
    setStatus(nextFlipped ? `${item.label} switched to actions.` : `${item.label} returned to preview.`);
  }
}

function setCardFlipped(key, flipped, source = "programmatic") {
  if (flipped) {
    state.flipped.add(key);
  } else {
    state.flipped.delete(key);
  }

  const card = cardForKey(key);
  if (!card) return;
  card.classList.toggle("is-flipped", flipped);
  const frontFace = card.querySelector(".card-front");
  const backFace = card.querySelector(".card-back");
  if (frontFace) frontFace.inert = flipped;
  if (backFace) backFace.inert = !flipped;
  if (flipped) {
    card.dataset.flipSource = source;
  } else {
    delete card.dataset.flipSource;
  }
  const flipButton = card.querySelector(".flip-button");
  if (flipButton) {
    flipButton.textContent = flipped ? "Preview" : "Actions";
  }
}

function closePointerFlippedCard(key) {
  const card = cardForKey(key);
  if (!card || card.dataset.flipSource !== "pointer" || !state.flipped.has(key)) return;
  setCardFlipped(key, false);
  releaseCardFocus(card);
  const item = state.assets.find((assetItem) => assetItem.key === key);
  if (item) setStatus(`${item.label} returned to preview.`);
}

function releaseCardFocus(card) {
  const active = document.activeElement;
  if (active instanceof HTMLElement && card.contains(active)) {
    active.blur();
  }
}

function cardForKey(key) {
  return Array.from(nodes.assetGrid.children).find((card) => card.dataset.assetKey === key);
}

function openBigger(item) {
  state.modalLastFocus = document.activeElement;
  nodes.assetModal.dataset.assetKey = item.key;
  nodes.assetModal.dataset.previewShape = item.previewShape;
  nodes.modalTitle.textContent = item.label;
  nodes.modalMeta.textContent = `${item.categoryLabel} / ${item.subcategoryLabel} / ${item.theme}`;
  delete nodes.modalImage.dataset.fallbackApplied;
  nodes.modalImage.src = assetDisplayUrl(item);
  nodes.modalImage.alt = item.label;
  applyImageMetadata(nodes.modalImage, item);
  nodes.modalPath.textContent = item.path;
  nodes.modalSource.href = isSafeAssetUrl(item.sourceUrl) ? item.sourceUrl : REPO_URL;

  if (typeof nodes.assetModal.showModal === "function") {
    nodes.assetModal.showModal();
  } else {
    nodes.assetModal.setAttribute("open", "");
  }
  setStatus(`${item.label} opened in large preview.`);
}

function applyImageMetadata(image, item) {
  const width = Number(item.dimensions?.width);
  const height = Number(item.dimensions?.height);
  if (width > 0 && height > 0) {
    image.width = width;
    image.height = height;
    image.style.setProperty("--asset-ratio", String(item.aspectRatio || width / height));
  } else {
    image.removeAttribute("width");
    image.removeAttribute("height");
    image.style.removeProperty("--asset-ratio");
  }
}

function selectedModalAsset() {
  return state.assets.find((item) => item.key === nodes.assetModal.dataset.assetKey);
}

async function openEditor(item) {
  closeFilterPopovers();
  state.editor.lastFocus = document.activeElement;
  resetEditorSession(item);
  renderEditorShell(item);
  renderEditorControls(item);
  setEditorActionState(false);
  showDialog(nodes.editorModal);
  setEditorStatus("Loading SVG source...");

  try {
    const source = await fetchSvgSource(item);
    if (state.editor.item?.key !== item.key) return;
    state.editor.source = source;
    setEditorPreviewSource(source);
    setEditorActionState(true);
    setEditorStatus(`${item.label} is ready for browser-side editing.`);
  } catch (error) {
    setEditorActionState(false);
    setEditorStatus(`Could not load SVG source.\n${error.message}`);
  }
}

function resetEditorSession(item) {
  revokeEditorPreviewUrl();
  state.editor.item = item;
  state.editor.source = "";
  state.editor.editedSvg = "";
  state.editor.lastOperations = {};
  state.editor.gifFileNameTouched = false;
}

function renderEditorShell(item) {
  nodes.editorModal.dataset.assetKey = item.key;
  nodes.editorModal.dataset.previewShape = item.previewShape;
  nodes.editorTitle.textContent = item.label;
  nodes.editorMeta.textContent = `${item.categoryLabel} / ${item.subcategoryLabel} / ${item.theme}`;
  nodes.editorSubtitle.textContent = item.path;
  nodes.editorPath.textContent = item.path;
  delete nodes.editorOriginalImage.dataset.fallbackApplied;
  delete nodes.editorEditedImage.dataset.fallbackApplied;
  nodes.editorOriginalImage.src = assetDisplayUrl(item);
  nodes.editorOriginalImage.alt = item.label;
  nodes.editorEditedImage.src = assetDisplayUrl(item);
  nodes.editorEditedImage.alt = `${item.label} edited preview`;
  applyImageMetadata(nodes.editorOriginalImage, item);
  applyImageMetadata(nodes.editorEditedImage, item);
  resetEditorGifSettings(item);
}

function renderEditorControls(item) {
  const editor = item.editor || {};
  renderEditorBadges(item, editor);
  renderEditorPaletteControls(editor);
  renderEditorColorControls(editor);
  renderEditorTextControls(editor);
  renderEditorElementControls(editor);
  renderEditorMotionControls(editor);
  nodes.editorAdvancedJson.value = "{}";
}

function renderEditorBadges(item, editor) {
  nodes.editorBadges.replaceChildren();
  const values = [
    item.type,
    `${editor.quality?.level || item.editorQuality || "unknown"} metadata`,
    ...(editor.capabilities || []),
    ...item.operationList.map(humanOperationName),
  ].filter(Boolean);

  for (const value of [...new Set(values)].slice(0, 8)) {
    const badge = document.createElement("span");
    badge.className = "editor-badge";
    badge.textContent = value;
    nodes.editorBadges.append(badge);
  }
}

function renderEditorPaletteControls(editor) {
  nodes.editorPaletteList.replaceChildren();
  const tokens = uniqueHexTokens(editor.colorTokens || []);
  const roles = new Set(tokens.map((token) => token.role).filter(Boolean));
  const palettes = sortedEditorPalettes();
  if (!palettes.length || !roles.size) {
    nodes.editorPaletteList.append(emptyControl("No palette targets available."));
    return;
  }

  for (const palette of palettes) {
    const matchingRoles = Object.keys(palette.roles || {}).filter((role) => roles.has(role));
    if (!matchingRoles.length) continue;

    const button = document.createElement("button");
    button.type = "button";
    button.className = "palette-button";
    button.dataset.palette = palette.id;
    button.append(document.createTextNode(palette.name || humanize(palette.id)));

    const swatches = document.createElement("span");
    swatches.className = "palette-swatches";
    for (const role of matchingRoles.slice(0, 5)) {
      const swatch = document.createElement("span");
      swatch.style.background = palette.roles[role];
      swatch.title = role;
      swatches.append(swatch);
    }
    button.append(swatches);
    button.addEventListener("click", () => applyPaletteToEditor(palette));
    nodes.editorPaletteList.append(button);
  }

  if (!nodes.editorPaletteList.children.length) {
    nodes.editorPaletteList.append(emptyControl("No palette roles match this SVG."));
  }
}

function sortedEditorPalettes() {
  const itemOperations = new Set(state.editor.item?.operationList || []);
  const recommended = new Set(
    state.editorPresets
      .filter((preset) => normalizeOperationList(preset.operations || []).some((operation) => itemOperations.has(operation)))
      .map((preset) => preset.defaultPalette)
      .filter(Boolean)
  );

  return [...state.editorPalettes].sort((a, b) => {
    const aRecommended = recommended.has(a.id) ? 0 : 1;
    const bRecommended = recommended.has(b.id) ? 0 : 1;
    if (aRecommended !== bRecommended) return aRecommended - bRecommended;
    return String(a.name || a.id).localeCompare(String(b.name || b.id));
  });
}

function applyPaletteToEditor(palette) {
  const roles = palette.roles || {};
  let changed = 0;
  for (const row of nodes.editorColorList.querySelectorAll(".color-token")) {
    const target = roles[row.dataset.role];
    if (!target) continue;
    const normalized = normalizeHex(target);
    if (!normalized) continue;
    const picker = row.querySelector(".color-picker");
    const hex = row.querySelector(".color-hex");
    picker.value = normalized;
    hex.value = normalized;
    changed += 1;
  }
  setEditorStatus(`${palette.name || "Palette"} applied to ${changed} color token${changed === 1 ? "" : "s"}.`);
}

function renderEditorColorControls(editor) {
  nodes.editorColorList.replaceChildren();
  const tokens = uniqueHexTokens(editor.colorTokens || [])
    .filter((token) => supportsOperation(token, "replaceColors"))
    .slice(0, 24);
  if (!tokens.length) {
    nodes.editorColorList.append(emptyControl("No editable hex colors detected."));
    return;
  }

  for (const token of tokens) {
    const row = document.createElement("div");
    row.className = "color-token";
    row.dataset.source = token.value;
    row.dataset.role = token.role || "";

    const sourceSwatch = document.createElement("span");
    sourceSwatch.className = "color-swatch";
    sourceSwatch.style.background = token.value;

    const label = document.createElement("div");
    label.className = "color-token-label";
    const name = document.createElement("strong");
    name.textContent = token.role || "color";
    const detail = document.createElement("span");
    detail.textContent = `${token.value} / ${token.count || 1} use${token.count === 1 ? "" : "s"}`;
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
    hex.setAttribute("aria-label", `Target hex for ${token.value}`);

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

function renderEditorTextControls(editor) {
  nodes.editorTextList.replaceChildren();
  const textNodes = (editor.textNodes || [])
    .filter((item) => supportsOperation(item, "replaceText"))
    .slice(0, 24);
  if (!textNodes.length) {
    nodes.editorTextList.append(emptyControl("No editable text detected."));
    return;
  }

  for (const item of textNodes) {
    const label = document.createElement("label");
    label.className = "text-control";
    const caption = document.createElement("span");
    caption.textContent = item.editLabel || item.id || item.nodePath || "Text";
    const input = document.createElement("input");
    input.type = "text";
    input.maxLength = 512;
    input.value = item.value || "";
    input.dataset.original = item.value || "";
    input.dataset.target = item.editId || item.id || item.nodePath || item.value || "";
    label.append(caption, input);
    nodes.editorTextList.append(label);
  }
}

function renderEditorElementControls(editor) {
  nodes.editorElementList.replaceChildren();
  const elements = (editor.removableElements || [])
    .filter((item) => supportsOperation(item, "removeElements"))
    .slice(0, 30);
  if (!elements.length) {
    nodes.editorElementList.append(emptyControl("No removable layers detected."));
    return;
  }

  for (const item of elements) {
    const label = document.createElement("label");
    label.className = "element-control";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.dataset.target = item.editId || item.id || item.nodePath || "";
    const body = document.createElement("span");
    const title = document.createElement("strong");
    title.textContent = item.label || item.editLabel || item.tag || "Layer";
    const detail = document.createElement("span");
    detail.textContent = `${item.tag || "node"} / ${item.hasAnimation ? "animated" : "static"}`;
    body.append(title, detail);
    label.append(checkbox, body);
    nodes.editorElementList.append(label);
  }
}

function renderEditorMotionControls(editor) {
  const hasAnimation = Boolean(editor.animation?.hasAnimation);
  nodes.editorSpeedRange.value = "1";
  nodes.editorSpeedNumber.value = "1";
  nodes.editorSpeedRange.disabled = !hasAnimation;
  nodes.editorSpeedNumber.disabled = !hasAnimation;
  const durations = (editor.animation?.durations || []).map((item) => item.value).join(", ");
  nodes.editorMotionStatus.textContent = hasAnimation ? `Detected: ${durations || "animation timing"}` : "No animation timing detected.";
}

function emptyControl(text) {
  const empty = document.createElement("p");
  empty.className = "control-note";
  empty.textContent = text;
  return empty;
}

function setEditorActionState(sourceReady) {
  [
    nodes.editorApply,
    nodes.editorReset,
    nodes.editorCopySvg,
    nodes.editorDownloadSvg,
    nodes.editorCopyMd,
    nodes.editorCopyHtml,
  ].forEach((node) => {
    if (node) node.disabled = !sourceReady;
  });

  const hasItem = Boolean(state.editor.item);
  [nodes.editorCopyGifCommand, nodes.editorCopyGifPayload].forEach((node) => {
    if (node) node.disabled = !hasItem;
  });
}

function resetEditorGifSettings(item) {
  nodes.editorGifOutputDir.value = DEFAULT_GIF_SETTINGS.outputDir;
  nodes.editorGifFileName.value = defaultEditorGifFileName(item);
  nodes.editorGifDuration.value = String(DEFAULT_GIF_SETTINGS.durationMs);
  nodes.editorGifFps.value = String(DEFAULT_GIF_SETTINGS.fps);
  nodes.editorGifMaxWidth.value = String(DEFAULT_GIF_SETTINGS.maxWidth);
  nodes.editorGifMaxHeight.value = String(DEFAULT_GIF_SETTINGS.maxHeight);
  nodes.editorGifBackground.value = DEFAULT_GIF_SETTINGS.background;
}

async function fetchSvgSource(item) {
  if (state.svgCache.has(item.key)) return state.svgCache.get(item.key);
  const response = await fetch(assetDisplayUrl(item), { cache: "no-store" });
  if (!response.ok) throw new Error(`SVG request failed: ${response.status}`);
  const source = await response.text();
  if (!/<svg[\s>]/i.test(source)) throw new Error("The loaded source is not SVG markup.");
  state.svgCache.set(item.key, source);
  return source;
}

function setEditorPreviewSource(svg) {
  revokeEditorPreviewUrl();
  const blob = new Blob([svg], { type: "image/svg+xml" });
  const url = URL.createObjectURL(blob);
  state.editor.editedUrl = url;
  nodes.editorEditedImage.src = url;
  if (state.editor.item) applyImageMetadata(nodes.editorEditedImage, state.editor.item);
}

function revokeEditorPreviewUrl() {
  if (state.editor.editedUrl) {
    URL.revokeObjectURL(state.editor.editedUrl);
    state.editor.editedUrl = "";
  }
}

function applyEditorPreview() {
  if (!state.editor.item || !state.editor.source) return;

  try {
    const operations = readEditorOperations();
    state.editor.lastOperations = operations;
    if (!Object.keys(operations).length) {
      state.editor.editedSvg = "";
      setEditorPreviewSource(state.editor.source);
      syncEditorGifFileName(false);
      setEditorStatus("No edits selected. Preview reset to the original SVG.");
      return;
    }

    const result = applyStaticSvgOperations(state.editor.source, operations);
    state.editor.editedSvg = result.svg;
    setEditorPreviewSource(result.svg);
    syncEditorGifFileName(true);
    setEditorStatus(formatEditorSummary(result.summary));
    setStatus(`${state.editor.item.label} edited preview applied.`);
  } catch (error) {
    setEditorStatus(`Edit failed.\n${error.message}`);
  }
}

function resetEditorControls() {
  for (const row of nodes.editorColorList.querySelectorAll(".color-token")) {
    const value = row.dataset.source;
    row.querySelector(".color-picker").value = value;
    row.querySelector(".color-hex").value = value;
  }
  for (const input of nodes.editorTextList.querySelectorAll("input[data-original]")) {
    input.value = input.dataset.original;
  }
  for (const checkbox of nodes.editorElementList.querySelectorAll("input[type='checkbox']")) {
    checkbox.checked = false;
  }
  nodes.editorSpeedRange.value = "1";
  nodes.editorSpeedNumber.value = "1";
  nodes.editorAdvancedJson.value = "{}";
  state.editor.editedSvg = "";
  state.editor.lastOperations = {};
  if (state.editor.source) setEditorPreviewSource(state.editor.source);
  syncEditorGifFileName(false);
  setEditorStatus("Editor controls reset.");
}

function readEditorOperations() {
  let operations = {};
  const replaceColors = readEditorColorOperations();
  const replaceText = readEditorTextOperations();
  const removeElements = readEditorElementOperations();
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
  return normalizeOperationsObject(operations);
}

function readEditorColorOperations() {
  const replaceColors = {};
  for (const row of nodes.editorColorList.querySelectorAll(".color-token")) {
    const source = row.dataset.source;
    const target = normalizeHex(row.querySelector(".color-hex").value);
    if (!target) throw new Error(`Invalid color value for ${source}.`);
    if (target !== source) replaceColors[source] = target;
  }
  return replaceColors;
}

function readEditorTextOperations() {
  const replacements = [];
  for (const input of nodes.editorTextList.querySelectorAll("input[data-target]")) {
    if (input.value !== input.dataset.original) {
      replacements.push({ target: input.dataset.target, to: input.value });
    }
  }
  return replacements;
}

function readEditorElementOperations() {
  return [...nodes.editorElementList.querySelectorAll("input[type='checkbox']:checked")]
    .map((input) => input.dataset.target)
    .filter(Boolean);
}

function mergeAdvancedOperations(operations, advanced) {
  const normalized = normalizeOperationsObject(advanced);
  return normalizeOperationsObject({
    replaceColors: { ...(operations.replaceColors || {}), ...(normalized.replaceColors || {}) },
    replaceText: [...(operations.replaceText || []), ...(normalized.replaceText || [])],
    removeElements: [...new Set([...(operations.removeElements || []), ...(normalized.removeElements || [])])],
    scaleAnimationSpeed: normalized.scaleAnimationSpeed || operations.scaleAnimationSpeed,
  });
}

function normalizeOperationsObject(value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error("Advanced JSON must be an object.");
  }
  sanitizeJsonObject(value);

  const replaceColors = { ...(value.replaceColors || {}), ...(value.replaceColor || {}) };
  const replaceText = Array.isArray(value.replaceText) ? value.replaceText : [];
  const removeElements = [
    ...(Array.isArray(value.removeElements) ? value.removeElements : []),
    ...(Array.isArray(value.hideElement) ? value.hideElement : []),
  ];
  const operations = {};
  if (Object.keys(replaceColors).length) operations.replaceColors = replaceColors;
  if (replaceText.length) operations.replaceText = replaceText;
  if (removeElements.length) operations.removeElements = [...new Set(removeElements.map(String))];
  if (value.scaleAnimationSpeed) operations.scaleAnimationSpeed = Number(value.scaleAnimationSpeed);
  return operations;
}

function applyStaticSvgOperations(source, rawOperations) {
  if (typeof source !== "string" || source.length > MAX_SVG_BYTES) {
    throw new Error(`SVG source exceeds maximum allowed size (${MAX_SVG_BYTES} bytes).`);
  }
  const operations = normalizeOperationsObject(rawOperations);
  const summary = { colorsChanged: false, textNodesChanged: 0, elementsRemoved: 0, animationScaled: false };
  let output = source;

  if (operations.replaceColors) {
    output = replaceSvgColors(output, operations.replaceColors);
    summary.colorsChanged = true;
  }
  if (operations.scaleAnimationSpeed) {
    output = scaleSvgAnimationSpeed(output, operations.scaleAnimationSpeed);
    summary.animationScaled = true;
  }

  const document = parseSvgDocument(output);
  const root = document.documentElement;
  if (operations.replaceText) {
    summary.textNodesChanged = replaceSvgText(root, operations.replaceText);
  }
  if (operations.removeElements) {
    summary.elementsRemoved = removeSvgElements(root, operations.removeElements);
  }

  output = new XMLSerializer().serializeToString(root);
  if (!output.endsWith("\n")) output += "\n";
  parseSvgDocument(output);
  return { svg: output, summary };
}

function replaceSvgColors(source, colorMap) {
  const normalized = new Map();
  for (const [sourceColor, targetColor] of Object.entries(colorMap)) {
    const from = normalizeHex(sourceColor);
    const to = normalizeHex(targetColor);
    if (!from || !to) throw new Error(`Invalid color replacement: ${sourceColor} -> ${targetColor}`);
    normalized.set(from, to);
  }

  return source.replace(/#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b/g, (match) => {
    const value = normalizeHex(match);
    return normalized.get(value) || match;
  });
}

function scaleSvgAnimationSpeed(source, factor) {
  const speed = Number(factor);
  if (!Number.isFinite(speed) || speed <= 0) {
    throw new Error("Animation speed factor must be greater than 0.");
  }
  const durationFactor = 1 / speed;
  return source.replace(/(\b(?:dur|animation-duration)\s*[:=]\s*["']?)(\d+(?:\.\d+)?)(ms|s)/gi, (_match, prefix, amount, unit) => {
    const scaled = Math.max(Number(amount) * durationFactor, 0.01);
    return `${prefix}${formatDuration(scaled)}${unit}`;
  });
}

function replaceSvgText(root, replacements) {
  let changed = 0;
  const textTags = new Set(["text", "tspan", "textPath"]);
  for (const entry of svgElementEntries(root)) {
    if (!textTags.has(localElementName(entry.element))) continue;
    const current = entry.element.textContent.trim();
    const identities = textIdentities(entry.element, entry.semanticPath, entry.numericPath, current);
    for (const replacement of replacements) {
      const target = replacement.target ?? replacement.from ?? replacement.editId ?? replacement.id ?? replacement.nodePath;
      if ((target && identities.has(String(target))) || (replacement.from && current === replacement.from)) {
        entry.element.textContent = String(replacement.to ?? "");
        changed += 1;
        break;
      }
    }
  }
  return changed;
}

function removeSvgElements(root, targets) {
  const targetSet = new Set(targets.map(String));
  const removeNodes = [];
  for (const entry of svgElementEntries(root)) {
    const identities = elementIdentities(entry.element, entry.semanticPath, entry.numericPath);
    if ([...identities].some((identity) => targetSet.has(identity))) {
      removeNodes.push(entry.element);
    }
  }

  let removed = 0;
  for (const element of removeNodes) {
    if (element !== root && element.parentNode) {
      element.parentNode.removeChild(element);
      removed += 1;
    }
  }
  return removed;
}

function parseSvgDocument(source) {
  const document = new DOMParser().parseFromString(source, "image/svg+xml");
  const parserError = document.querySelector("parsererror");
  if (parserError) throw new Error(parserError.textContent.trim() || "SVG parser rejected the edited markup.");
  if (localElementName(document.documentElement) !== "svg") throw new Error("Edited output is not an SVG document.");
  return document;
}

function svgElementEntries(root) {
  const entries = [];
  const walk = (element, semanticPath, numericPath) => {
    entries.push({ element, semanticPath, numericPath });
    const childCounts = new Map();
    const children = [...element.children].filter((child) => child.nodeType === 1);
    children.forEach((child, index) => {
      const tag = localElementName(child);
      const count = (childCounts.get(tag) || 0) + 1;
      childCounts.set(tag, count);
      walk(child, `${semanticPath}/${tag}[${count}]`, `${numericPath}.${index}`);
    });
  };
  walk(root, localElementName(root) || "svg", "0");
  return entries;
}

function elementIdentities(element, semanticPath, numericPath) {
  return new Set([
    element.getAttribute("data-edit-id"),
    element.getAttribute("data-editor-id"),
    element.getAttribute("data-id"),
    element.getAttribute("id"),
    semanticPath,
    numericPath,
  ].filter(Boolean).map(String));
}

function textIdentities(element, semanticPath, numericPath, current) {
  return new Set([...elementIdentities(element, semanticPath, numericPath), current].filter(Boolean).map(String));
}

function localElementName(element) {
  return element?.localName || String(element?.tagName || "").replace(/^.*:/, "");
}

function formatDuration(value) {
  return value.toFixed(3).replace(/0+$/, "").replace(/\.$/, "");
}

function formatEditorSummary(summary) {
  return [
    `Colors changed: ${summary.colorsChanged ? "yes" : "no"}`,
    `Text nodes changed: ${summary.textNodesChanged}`,
    `Layers removed: ${summary.elementsRemoved}`,
    `Animation scaled: ${summary.animationScaled ? "yes" : "no"}`,
  ].join("\n");
}

function currentEditorSvg() {
  return state.editor.editedSvg || state.editor.source;
}

function currentEditorFileName() {
  const item = state.editor.item;
  if (!item) return "readme-ux-kit-edited.svg";
  return state.editor.editedSvg ? `${safeFileBase(item.name)}-edited.svg` : `${safeFileBase(item.name)}.svg`;
}

async function copyEditorSvg() {
  const item = state.editor.item;
  const svg = currentEditorSvg();
  if (!item || !svg) return;
  await copyText(svg, `SVG copied for ${item.label}.`);
}

function downloadEditorSvg() {
  const item = state.editor.item;
  const svg = currentEditorSvg();
  if (!item || !svg) return;
  const objectUrl = URL.createObjectURL(new Blob([svg], { type: "image/svg+xml" }));
  triggerDownload(objectUrl, currentEditorFileName());
  URL.revokeObjectURL(objectUrl);
  setStatus(`Download started for ${item.label}.`);
}

function editorMarkdownSnippet() {
  const item = state.editor.item;
  if (!item) return "";
  if (!state.editor.editedSvg) return markdownSnippet(item);
  return `[![${item.name} edited](./${currentEditorFileName()})](${REPO_URL})`;
}

function editorHtmlSnippet() {
  const item = state.editor.item;
  if (!item) return "";
  if (!state.editor.editedSvg) return htmlSnippet(item);
  return `<a href="${REPO_URL}"><img src="./${currentEditorFileName()}" alt="${escapeAttribute(`${item.label} edited`)}" /></a>`;
}

function buildGifCommand() {
  const item = state.editor.item;
  if (!item) return "";
  const settings = editorGifSettings();
  return [
    "npm run export:gif --",
    "--asset",
    quoteCommandArg(item.path),
    "--output-dir",
    quoteCommandArg(settings.outputDir),
    "--duration-ms",
    String(settings.durationMs),
    "--fps",
    String(settings.fps),
    "--max-width",
    String(settings.maxWidth),
    "--max-height",
    String(settings.maxHeight),
    "--background",
    quoteCommandArg(settings.background),
  ].join(" ");
}

function buildGifPayload() {
  const item = state.editor.item;
  const settings = editorGifSettings();
  const payload = {
    path: item?.path,
    outputDir: settings.outputDir,
    fileName: settings.fileName,
    durationMs: settings.durationMs,
    fps: settings.fps,
    maxWidth: settings.maxWidth,
    maxHeight: settings.maxHeight,
    background: settings.background,
  };

  if (state.editor.editedSvg && item) {
    payload.source = state.editor.editedSvg;
    payload.sourcePath = item.path;
    payload.name = `${item.name} edited`;
  }
  return payload;
}

function editorGifSettings() {
  return {
    outputDir: nodes.editorGifOutputDir.value.trim() || DEFAULT_GIF_SETTINGS.outputDir,
    fileName: nodes.editorGifFileName.value.trim() || defaultEditorGifFileName(state.editor.item, Boolean(state.editor.editedSvg)),
    durationMs: boundedNumber(nodes.editorGifDuration.value, DEFAULT_GIF_SETTINGS.durationMs),
    fps: boundedNumber(nodes.editorGifFps.value, DEFAULT_GIF_SETTINGS.fps),
    maxWidth: boundedNumber(nodes.editorGifMaxWidth.value, DEFAULT_GIF_SETTINGS.maxWidth),
    maxHeight: boundedNumber(nodes.editorGifMaxHeight.value, DEFAULT_GIF_SETTINGS.maxHeight),
    background: nodes.editorGifBackground.value.trim() || DEFAULT_GIF_SETTINGS.background,
  };
}

function syncEditorGifFileName(edited) {
  if (!state.editor.item || state.editor.gifFileNameTouched) return;
  nodes.editorGifFileName.value = defaultEditorGifFileName(state.editor.item, edited);
}

function defaultEditorGifFileName(item, edited = false) {
  const base = safeFileBase(item?.name || "readme-ux-export");
  return `${base}${edited ? "-edited" : ""}.gif`;
}

function safeFileBase(value) {
  return slugify(value).replace(/-svg$/, "") || "readme-ux-export";
}

function boundedNumber(value, fallback) {
  const number = Number(value);
  return Number.isFinite(number) && number > 0 ? number : fallback;
}

function quoteCommandArg(value) {
  return `"${String(value ?? "").replace(/"/g, '\\"')}"`;
}

function setEditorStatus(text) {
  nodes.editorStatus.textContent = text;
}

function showDialog(dialog) {
  if (!dialog || dialog.open || dialog.hasAttribute("open")) return;
  if (typeof dialog.showModal === "function") {
    dialog.showModal();
  } else {
    dialog.setAttribute("open", "");
  }
}

function closeEditor() {
  if (typeof nodes.editorModal.close === "function") {
    nodes.editorModal.close();
  } else {
    nodes.editorModal.removeAttribute("open");
  }
  if (state.editor.lastFocus instanceof HTMLElement) {
    state.editor.lastFocus.focus();
  }
}

function supportsOperation(item, operation) {
  return normalizeOperationList(item?.operations || []).includes(operation);
}

function normalizeOperationList(operations) {
  return [...new Set((Array.isArray(operations) ? operations : [])
    .map(normalizeOperationName)
    .filter(Boolean))];
}

function normalizeOperationName(operation) {
  return {
    replaceColor: "replaceColors",
    hideElement: "removeElements",
  }[operation] || operation;
}

function humanOperationName(operation) {
  return {
    replaceColors: "colors",
    replaceText: "text",
    removeElements: "layers",
    scaleAnimationSpeed: "motion",
  }[normalizeOperationName(operation)] || humanize(operation);
}

function uniqueHexTokens(tokens) {
  const colorMap = new Map();
  for (const token of tokens) {
    const value = normalizeHex(token.value);
    if (!value) continue;
    const existing = colorMap.get(value) || {
      ...token,
      value,
      count: 0,
      attributes: [],
      operations: normalizeOperationList(token.operations || []),
    };
    existing.count += Number(token.count) || 1;
    existing.role ||= token.role;
    existing.attributes = [...new Set([...(existing.attributes || []), ...(token.attributes || [])])];
    existing.operations = [...new Set([...normalizeOperationList(existing.operations), ...normalizeOperationList(token.operations || [])])];
    colorMap.set(value, existing);
  }
  return [...colorMap.values()];
}

function normalizeHex(value) {
  let text = String(value || "").trim().toLowerCase();
  if (!text) return "";
  if (!text.startsWith("#")) text = `#${text}`;
  if (/^#[0-9a-f]{3}$/.test(text)) {
    text = `#${text.slice(1).split("").map((character) => character + character).join("")}`;
  }
  return /^#[0-9a-f]{6}$/.test(text) ? text : "";
}

function updateVisibleCountFromDom() {
  const visibleCount = nodes.assetGrid.querySelectorAll(".asset-card").length;
  nodes.resultCount.textContent = String(visibleCount);
  nodes.emptyState.classList.toggle("is-visible", visibleCount === 0);
  updateGridSummary(visibleCount);
}

function updateMetrics() {
  const manifestCount = state.manifest?.assetCount || state.assets.length;
  nodes.totalAssets.textContent = String(manifestCount);
  nodes.categoryCount.textContent = String(categoryOptions().length - 1);
  updateFavoriteCount();
}

function updateFavoriteCount() {
  nodes.favoriteCount.textContent = String(state.favorites.size);
}

function updateGridSummary(visibleCount) {
  const filters = [];
  if (state.category !== "all") filters.push(humanize(state.category));
  if (state.theme !== "All Themes") filters.push(state.theme);
  if (state.favoritesOnly) filters.push("Favorites");
  const suffix = filters.length ? ` filtered by ${filters.join(", ")}` : "";
  nodes.gridSummary.textContent = `Showing ${visibleCount} of ${state.assets.length} generated SVG assets${suffix}.`;
}

function setDensity(cols) {
  state.cols = cols;
  nodes.body.dataset.cols = cols;
  updateGridCycle();
}

function updateGridCycle() {
  const iconClass = gridIconClass(state.cols);
  const nextCols = nextGridCols();
  nodes.gridCycle.dataset.colsCurrent = state.cols;
  nodes.gridCycle.setAttribute("aria-label", `Grid layout: ${gridLabel(state.cols)}. Activate to switch to ${gridLabel(nextCols)}.`);
  nodes.gridCycle.title = `Switch to ${gridLabel(nextCols)}`;
  nodes.gridCycleIcon.className = `layout-icon ${iconClass}`;
  nodes.gridCycleIcon.replaceChildren(...Array.from({ length: Number(state.cols) }, () => document.createElement("span")));
  nodes.gridCycleText.textContent = gridLabel(state.cols);
}

function nextGridCols() {
  const index = GRID_OPTIONS.indexOf(state.cols);
  return GRID_OPTIONS[(index + 1) % GRID_OPTIONS.length];
}

function gridLabel(cols) {
  return `${cols} column${cols === "1" ? "" : "s"}`;
}

function gridIconClass(cols) {
  return {
    "1": "single",
    "2": "pair",
    "3": "triple",
    "5": "five",
    "7": "seven",
  }[cols] || "triple";
}

function updateFilterTriggers() {
  const selectedCategory = categoryOptions().find((option) => option.id === state.category) || categoryOptions()[0];
  const counts = styleCounts();
  const selectedThemeCount = state.theme === "All Themes" ? state.assets.length : counts.get(state.theme) || 0;

  nodes.categoryFilterLabel.textContent = selectedCategory.id === "all" ? "All Categories" : selectedCategory.label;
  nodes.categoryFilterCount.textContent = String(selectedCategory.count);
  nodes.themeFilterLabel.textContent = state.theme;
  nodes.themeFilterCount.textContent = String(selectedThemeCount);
}

function toggleFilterPopover(type) {
  const isCategory = type === "category";
  const trigger = isCategory ? nodes.categoryFilterToggle : nodes.themeFilterToggle;
  const popover = isCategory ? nodes.categoryPopover : nodes.themePopover;
  const wasOpen = !popover.hidden;
  closeFilterPopovers();

  if (!wasOpen) {
    openFilterPopover(trigger, popover);
  }
}

function openFilterPopover(trigger, popover) {
  positionFilterPopover(trigger, popover);
  popover.hidden = false;
  trigger.setAttribute("aria-expanded", "true");
}

function closeFilterPopovers({ restoreFocus = false } = {}) {
  let focusTarget = null;
  [
    [nodes.categoryPopover, nodes.categoryFilterToggle],
    [nodes.themePopover, nodes.themeFilterToggle],
  ].forEach(([popover, trigger]) => {
    if (!popover || !trigger) return;
    if (!popover.hidden && restoreFocus) {
      focusTarget = trigger;
    }
    popover.hidden = true;
    trigger.setAttribute("aria-expanded", "false");
  });
  if (focusTarget instanceof HTMLElement) {
    focusTarget.focus();
  }
}

function positionFilterPopover(trigger, popover) {
  const panelRect = nodes.controlPanel.getBoundingClientRect();
  const triggerRect = trigger.getBoundingClientRect();
  const width = Math.min(560, Math.max(240, panelRect.width - 28));
  const rightLimit = panelRect.width - width - 14;
  const left = Math.max(14, Math.min(triggerRect.left - panelRect.left, rightLimit));
  popover.style.setProperty("--popover-left", `${left}px`);
  popover.style.setProperty("--popover-width", `${width}px`);
}

function setControlsDisabled(disabled) {
  [
    nodes.searchInput,
    nodes.categoryFilterToggle,
    nodes.themeFilterToggle,
    nodes.gridCycle,
    nodes.favoritesOnly,
    nodes.shuffleCards,
    nodes.copyBundle,
    nodes.actionsAll,
    nodes.previewAll,
    nodes.modalDownload,
    nodes.modalCopyMd,
    nodes.modalCopySvg,
    nodes.modalCopyHtml,
  ].forEach((node) => {
    if (node) node.disabled = disabled;
  });
}

function bindEvents() {
  let searchTimer = 0;
  nodes.searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      state.query = nodes.searchInput.value;
      render();
    }, 120);
  });

  nodes.gridCycle.addEventListener("click", () => {
    setDensity(nextGridCols());
    setStatus(`Grid changed to ${gridLabel(state.cols)}.`);
  });

  nodes.categoryFilterToggle.addEventListener("click", (event) => {
    event.stopPropagation();
    toggleFilterPopover("category");
  });

  nodes.themeFilterToggle.addEventListener("click", (event) => {
    event.stopPropagation();
    toggleFilterPopover("theme");
  });

  nodes.categoryPopoverClose.addEventListener("click", () => closeFilterPopovers({ restoreFocus: true }));
  nodes.themePopoverClose.addEventListener("click", () => closeFilterPopovers({ restoreFocus: true }));

  [nodes.categoryPopover, nodes.themePopover].forEach((popover) => {
    popover.addEventListener("click", (event) => event.stopPropagation());
  });

  document.addEventListener("click", () => closeFilterPopovers());
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeFilterPopovers({ restoreFocus: true });
    } else if (event.key === "?" && !isTypingInEditableField(event.target)) {
      event.preventDefault();
      openSupportModal("helpSectionTitle");
    }
  });
  window.addEventListener("resize", () => closeFilterPopovers());
  window.addEventListener("error", (event) => {
    showRuntimeError(event.error || new Error(event.message || "Unhandled script error"), "window.onerror");
  });
  window.addEventListener("unhandledrejection", (event) => {
    showRuntimeError(event.reason || new Error("Unhandled promise rejection"), "unhandledrejection");
  });

  if (nodes.openHelpModal) {
    nodes.openHelpModal.addEventListener("click", () => openSupportModal("helpSectionTitle"));
  }
  if (nodes.openSupportModal) {
    nodes.openSupportModal.addEventListener("click", () => openSupportModal("bugAreaSelect"));
  }
  if (nodes.footerHelpBtn) {
    nodes.footerHelpBtn.addEventListener("click", () => openSupportModal("helpSectionTitle"));
  }
  if (nodes.footerBugReportBtn) {
    nodes.footerBugReportBtn.addEventListener("click", () => openSupportModal("bugAreaSelect"));
  }
  if (nodes.footerExportDataBtn) {
    nodes.footerExportDataBtn.addEventListener("click", exportUserDataJson);
  }
  if (nodes.footerPurgeDataBtn) {
    nodes.footerPurgeDataBtn.addEventListener("click", purgeAllLocalData);
  }
  if (nodes.supportModalClose) {
    nodes.supportModalClose.addEventListener("click", closeSupportModal);
  }
  if (nodes.supportModal) {
    nodes.supportModal.addEventListener("click", (event) => {
      if (event.target === nodes.supportModal) closeSupportModal();
    });
    nodes.supportModal.addEventListener("close", restoreSupportModalFocus);
  }
  if (nodes.bugAreaSelect) nodes.bugAreaSelect.addEventListener("change", updateDiagnosticPreview);
  if (nodes.bugDescription) nodes.bugDescription.addEventListener("input", updateDiagnosticPreview);
  if (nodes.bugSteps) nodes.bugSteps.addEventListener("input", updateDiagnosticPreview);
  if (nodes.copyDiagnosticBtn) nodes.copyDiagnosticBtn.addEventListener("click", copyDiagnosticBundle);
  if (nodes.downloadDiagnosticBtn) nodes.downloadDiagnosticBtn.addEventListener("click", downloadDiagnosticBundle);
  if (nodes.copyFeedbackBtn) nodes.copyFeedbackBtn.addEventListener("click", copyFeedbackPayload);
  if (nodes.downloadFeedbackBtn) nodes.downloadFeedbackBtn.addEventListener("click", downloadFeedbackPayload);
  if (nodes.exportUserDataBtn) nodes.exportUserDataBtn.addEventListener("click", exportUserDataJson);
  if (nodes.purgeUserDataBtn) nodes.purgeUserDataBtn.addEventListener("click", purgeAllLocalData);
  if (nodes.interfaceLangSelect) {
    nodes.interfaceLangSelect.addEventListener("change", () => {
      const lang = nodes.interfaceLangSelect.value || "en";
      document.documentElement.lang = lang;
      updateDiagnosticPreview();
      setStatus(`Interface language updated to ${lang}.`);
    });
  }
  if (nodes.errorRecoverBtn) nodes.errorRecoverBtn.addEventListener("click", recoverFromError);
  if (nodes.errorReportBtn) {
    nodes.errorReportBtn.addEventListener("click", () => {
      if (state.lastError && nodes.bugDescription) {
        nodes.bugDescription.value = `Crash recovery report: ${state.lastError.message}`;
      }
      openSupportModal("bugAreaSelect");
    });
  }

  nodes.favoritesOnly.addEventListener("click", () => {
    state.favoritesOnly = !state.favoritesOnly;
    nodes.favoritesOnly.setAttribute("aria-pressed", String(state.favoritesOnly));
    nodes.favoritesOnly.classList.toggle("primary", state.favoritesOnly);
    nodes.favoritesOnly.classList.toggle("secondary", !state.favoritesOnly);
    render();
    setStatus(state.favoritesOnly ? "Showing favorite assets only." : "Showing all matching assets.");
  });

  nodes.shuffleCards.addEventListener("click", () => {
    shuffleOrder();
    renderGrid();
    setStatus("Cards shuffled.");
  });

  nodes.copyBundle.addEventListener("click", () => {
    const bundle = filteredAssets().map(markdownSnippet).join("\n");
    copyText(bundle, "Visible asset Markdown bundle copied.");
  });

  nodes.actionsAll.addEventListener("click", () => {
    filteredAssets().forEach((item) => setCardFlipped(item.key, true));
    setStatus("Visible cards switched to actions.");
  });

  nodes.previewAll.addEventListener("click", () => {
    state.flipped.clear();
    nodes.assetGrid.querySelectorAll(".asset-card").forEach((card) => {
      card.classList.remove("is-flipped");
      const frontFace = card.querySelector(".card-front");
      const backFace = card.querySelector(".card-back");
      if (frontFace) frontFace.inert = false;
      if (backFace) backFace.inert = true;
      const flipButton = card.querySelector(".flip-button");
      if (flipButton) flipButton.textContent = "Actions";
    });
    setStatus("All cards returned to preview.");
  });

  nodes.modalClose.addEventListener("click", closeModal);
  nodes.assetModal.addEventListener("click", (event) => {
    if (event.target === nodes.assetModal) closeModal();
  });
  nodes.assetModal.addEventListener("close", restoreAssetModalFocus);

  nodes.modalDownload.addEventListener("click", () => {
    const item = selectedModalAsset();
    if (item) downloadAsset(item);
  });
  nodes.modalCopyMd.addEventListener("click", () => {
    const item = selectedModalAsset();
    if (item) copyText(markdownSnippet(item), `Markdown copied for ${item.label}.`);
  });
  nodes.modalCopySvg.addEventListener("click", () => {
    const item = selectedModalAsset();
    if (item) copySvgMarkup(item);
  });
  nodes.modalCopyHtml.addEventListener("click", () => {
    const item = selectedModalAsset();
    if (item) copyText(htmlSnippet(item), `HTML copied for ${item.label}.`);
  });

  nodes.editorClose.addEventListener("click", closeEditor);
  nodes.editorModal.addEventListener("click", (event) => {
    if (event.target === nodes.editorModal) closeEditor();
  });
  nodes.editorModal.addEventListener("close", () => {
    if (state.editor.lastFocus instanceof HTMLElement) {
      state.editor.lastFocus.focus();
    }
  });
  nodes.editorApply.addEventListener("click", applyEditorPreview);
  nodes.editorReset.addEventListener("click", resetEditorControls);
  nodes.editorCopySvg.addEventListener("click", copyEditorSvg);
  nodes.editorDownloadSvg.addEventListener("click", downloadEditorSvg);
  nodes.editorCopyMd.addEventListener("click", () => {
    const item = state.editor.item;
    if (item) copyText(editorMarkdownSnippet(), `Markdown copied for ${item.label}.`);
  });
  nodes.editorCopyHtml.addEventListener("click", () => {
    const item = state.editor.item;
    if (item) copyText(editorHtmlSnippet(), `HTML copied for ${item.label}.`);
  });
  nodes.editorCopyGifCommand.addEventListener("click", () => {
    const item = state.editor.item;
    if (item) copyText(buildGifCommand(), `Local GIF command copied for ${item.label}.`);
  });
  nodes.editorCopyGifPayload.addEventListener("click", () => {
    const item = state.editor.item;
    if (item) copyText(JSON.stringify(buildGifPayload(), null, 2), `Local GIF payload copied for ${item.label}.`);
  });
  nodes.editorSpeedRange.addEventListener("input", () => {
    nodes.editorSpeedNumber.value = nodes.editorSpeedRange.value;
  });
  nodes.editorSpeedNumber.addEventListener("input", () => {
    const value = Number(nodes.editorSpeedNumber.value);
    if (Number.isFinite(value)) nodes.editorSpeedRange.value = String(value);
  });
  nodes.editorGifFileName.addEventListener("input", () => {
    state.editor.gifFileNameTouched = true;
  });
}

function closeModal() {
  if (typeof nodes.assetModal.close === "function") {
    nodes.assetModal.close();
  } else {
    nodes.assetModal.removeAttribute("open");
  }
  restoreAssetModalFocus();
}

function restoreAssetModalFocus() {
  if (state.modalLastFocus instanceof HTMLElement) {
    state.modalLastFocus.focus();
    state.modalLastFocus = null;
  }
}

function shuffleOrder() {
  for (let index = state.order.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(Math.random() * (index + 1));
    [state.order[index], state.order[swapIndex]] = [state.order[swapIndex], state.order[index]];
  }
  updateOrderIndex();
}

function updateOrderIndex() {
  state.orderIndex = new Map(state.order.map((key, index) => [key, index]));
}

function markdownSnippet(item) {
  const safeUrl = isSafeAssetUrl(item.rawUrl) ? item.rawUrl : REPO_URL;
  return `[![${item.name}](${safeUrl})](${REPO_URL})`;
}

function htmlSnippet(item) {
  const safeUrl = isSafeAssetUrl(item.rawUrl) ? item.rawUrl : REPO_URL;
  return `<a href="${REPO_URL}"><img src="${escapeAttribute(safeUrl)}" alt="${escapeAttribute(item.label)}" /></a>`;
}

async function copySvgMarkup(item) {
  try {
    const response = await fetch(assetDisplayUrl(item));
    if (!response.ok) throw new Error(`SVG request failed: ${response.status}`);
    const svg = await response.text();
    await copyText(svg, `SVG markup copied for ${item.label}.`);
  } catch {
    await copyText(item.rawUrl, `SVG fetch was unavailable; raw URL copied for ${item.label}.`);
  }
}

async function copyText(text, message) {
  try {
    await navigator.clipboard.writeText(text);
    setStatus(message);
  } catch {
    const helper = document.createElement("textarea");
    helper.value = text;
    helper.setAttribute("readonly", "");
    helper.style.position = "fixed";
    helper.style.inset = "0 auto auto 0";
    helper.style.opacity = "0";
    document.body.append(helper);
    helper.select();
    document.execCommand("copy");
    helper.remove();
    setStatus(message);
  }
}

async function downloadAsset(item) {
  try {
    const response = await fetch(assetDisplayUrl(item));
    if (!response.ok) throw new Error(`Download request failed: ${response.status}`);
    const blob = await response.blob();
    const objectUrl = URL.createObjectURL(blob);
    triggerDownload(objectUrl, `${item.name}.svg`);
    URL.revokeObjectURL(objectUrl);
  } catch {
    setStatus(`Download failed for ${item.label}. Build the self-contained Pages artifact or serve the repository root.`);
    return;
  }
  setStatus(`Download started for ${item.label}.`);
}

function triggerDownload(href, filename) {
  const link = document.createElement("a");
  link.href = href;
  link.download = sanitizeAttachmentFilename(filename);
  document.body.append(link);
  link.click();
  link.remove();
}

function assetDisplayUrl(item) {
  if (!item.path) return isSafeAssetUrl(item.rawUrl) ? item.rawUrl : "";
  const candidate = String(item.path).replace(/^\/+/, "");
  if (!isSafeAssetUrl(candidate)) return "";
  const sourceTreeSite = location.protocol === "file:" || location.pathname.includes("/site/");
  return `${sourceTreeSite ? "../" : "./"}${candidate}`;
}

function sourceUrl(path) {
  return path ? `${REPO_URL}/blob/master/${path}` : REPO_URL;
}

function previewUrl(previewPath) {
  if (!previewPath) return REPO_URL;
  const [path, anchor] = previewPath.split("#");
  return `${REPO_URL}/blob/master/${path}${anchor ? `#${anchor}` : ""}`;
}

function slugify(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

function humanize(value) {
  return String(value || "")
    .replace(/[-_]+/g, " ")
    .replace(/\b(api|ci|ui|ux|ml|ai|svg|md)\b/gi, (match) => match.toUpperCase())
    .replace(/\b\w/g, (match) => match.toUpperCase());
}

function escapeAttribute(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;",
  }[character]));
}

function loadFavorites() {
  try {
    const parsed = JSON.parse(localStorage.getItem(FAVORITES_KEY) || "[]");
    return new Set(Array.isArray(parsed) ? parsed : []);
  } catch {
    return new Set();
  }
}

function saveFavorites() {
  localStorage.setItem(FAVORITES_KEY, JSON.stringify([...state.favorites]));
}

function setStatus(text) {
  nodes.status.textContent = text;
}

function iconButton(className, svg, label) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = `icon-button ${className}`;
  button.setAttribute("aria-label", label);
  button.replaceChildren(typeof svg === "string" ? createSvgIcon(svg) : svg);
  return button;
}

function createSvgIcon(kind) {
  const ns = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(ns, "svg");
  svg.setAttribute("class", "icon");
  svg.setAttribute("viewBox", "0 0 24 24");
  svg.setAttribute("aria-hidden", "true");
  const path = document.createElementNS(ns, "path");
  if (kind === "star-filled") {
    path.setAttribute("d", "M12 3l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2 7.5 14 3 9.6l6.2-.9L12 3z");
    path.setAttribute("fill", "currentColor");
  } else if (kind === "star-outline") {
    path.setAttribute("d", "M12 3l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2 7.5 14 3 9.6l6.2-.9L12 3z");
    path.setAttribute("fill", "none");
    path.setAttribute("stroke", "currentColor");
    path.setAttribute("stroke-width", "2");
    path.setAttribute("stroke-linejoin", "round");
  } else {
    path.setAttribute("d", "M6 6l12 12M18 6L6 18");
    path.setAttribute("fill", "none");
    path.setAttribute("stroke", "currentColor");
    path.setAttribute("stroke-width", "2.2");
    path.setAttribute("stroke-linecap", "round");
  }
  svg.append(path);
  return svg;
}

function starOutline() {
  return "star-outline";
}

function starFilled() {
  return "star-filled";
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
  return raw.startsWith("assets/") || raw.startsWith("./assets/");
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
    const safeTitle = escapeAttribute(label || "SVG asset preview unavailable");
    const fallbackSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 200" role="img" aria-label="${safeTitle}"><rect width="480" height="200" rx="14" fill="#111827" stroke="#334155" stroke-width="2"/><text x="240" y="96" fill="#e2e8f0" font-family="system-ui,sans-serif" font-size="15" font-weight="700" text-anchor="middle">${safeTitle}</text><text x="240" y="124" fill="#94a3b8" font-family="system-ui,sans-serif" font-size="12" text-anchor="middle">Preview fallback active</text></svg>`;
    image.src = `data:image/svg+xml;utf8,${encodeURIComponent(fallbackSvg)}`;
  });
}

function setupReducedMotionListener() {
  if (typeof window.matchMedia !== "function") return;
  const media = window.matchMedia("(prefers-reduced-motion: reduce)");
  const applyPreference = () => {
    state.reducedMotion = Boolean(media.matches);
    document.body.dataset.reducedMotion = String(state.reducedMotion);
  };
  applyPreference();
  if (typeof media.addEventListener === "function") {
    media.addEventListener("change", applyPreference);
  }
}

function isTypingInEditableField(target) {
  if (!(target instanceof HTMLElement)) return false;
  const tag = target.tagName;
  return tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || target.isContentEditable;
}

function openSupportModal(focusTargetId) {
  closeFilterPopovers();
  updateDiagnosticPreview();
  if (nodes.supportModal) {
    const alreadyOpen = Boolean(nodes.supportModal.open || nodes.supportModal.hasAttribute("open"));
    if (!alreadyOpen) {
      state.supportLastFocus = document.activeElement;
      showDialog(nodes.supportModal);
    }
    const target = focusTargetId ? document.getElementById(focusTargetId) : nodes.supportModalClose;
    if (target instanceof HTMLElement) target.focus();
  }
  setStatus("Opened Help Center, Bug Reporter, and Privacy Controls.");
}

function closeSupportModal() {
  if (!nodes.supportModal) return;
  if (typeof nodes.supportModal.close === "function") {
    nodes.supportModal.close();
  } else {
    nodes.supportModal.removeAttribute("open");
  }
  restoreSupportModalFocus();
}

function restoreSupportModalFocus() {
  if (state.supportLastFocus instanceof HTMLElement) {
    state.supportLastFocus.focus();
    state.supportLastFocus = null;
  }
}

function buildDiagnosticBundle() {
  return {
    schemaVersion: 1,
    app: "readme-ux-kit-showcase",
    appVersion: APP_VERSION,
    mode: "static-browser-showcase",
    piiFree: true,
    timestamp: new Date().toISOString(),
    locale: document.documentElement.lang || navigator.language || "en",
    viewport: {
      width: window.innerWidth,
      height: window.innerHeight,
      reducedMotion: state.reducedMotion,
    },
    viewState: {
      activeCategory: state.category,
      activeTheme: state.theme,
      gridColumns: state.cols,
      favoritesOnly: state.favoritesOnly,
      favoritesCount: state.favorites.size,
      totalAssetsLoaded: state.assets.length,
      visibleAssetsCount: nodes.assetGrid ? nodes.assetGrid.querySelectorAll(".asset-card").length : 0,
    },
    issueReport: {
      affectedArea: nodes.bugAreaSelect ? nodes.bugAreaSelect.value : "General",
      summary: nodes.bugDescription ? nodes.bugDescription.value.trim().slice(0, 4000) : "",
      reproductionSteps: nodes.bugSteps ? nodes.bugSteps.value.trim().slice(0, 4000) : "",
      lastRuntimeError: state.lastError ? state.lastError.message : null,
    },
  };
}

function updateDiagnosticPreview() {
  if (!nodes.bugDiagnosticPreview) return;
  nodes.bugDiagnosticPreview.textContent = JSON.stringify(buildDiagnosticBundle(), null, 2);
}

async function copyDiagnosticBundle() {
  const bundle = JSON.stringify(buildDiagnosticBundle(), null, 2);
  await copyText(bundle, "PII-free diagnostic bundle copied to clipboard.");
}

function downloadDiagnosticBundle() {
  const bundle = JSON.stringify(buildDiagnosticBundle(), null, 2);
  const objectUrl = URL.createObjectURL(new Blob([bundle], { type: "application/json" }));
  triggerDownload(objectUrl, "readme-ux-kit-diagnostic-bundle.json");
  URL.revokeObjectURL(objectUrl);
  setStatus("PII-free diagnostic bundle downloaded.");
}

function buildFeedbackPayload() {
  return {
    schemaVersion: 1,
    app: "readme-ux-kit-showcase",
    appVersion: APP_VERSION,
    timestamp: new Date().toISOString(),
    rating: Number(nodes.feedbackRating?.value || 5),
    category: nodes.feedbackCategory?.value || "UX & Visual Polish",
    comment: (nodes.feedbackComment?.value || "").trim().slice(0, 4000),
    context: {
      activeCategory: state.category,
      activeTheme: state.theme,
      gridColumns: state.cols,
    },
  };
}

async function copyFeedbackPayload() {
  const payload = JSON.stringify(buildFeedbackPayload(), null, 2);
  await copyText(payload, "Structured user feedback JSON copied to clipboard.");
}

function downloadFeedbackPayload() {
  const payload = JSON.stringify(buildFeedbackPayload(), null, 2);
  const objectUrl = URL.createObjectURL(new Blob([payload], { type: "application/json" }));
  triggerDownload(objectUrl, "readme-ux-kit-feedback.json");
  URL.revokeObjectURL(objectUrl);
  setStatus("Structured user feedback JSON downloaded.");
}

function exportUserDataJson() {
  const exportArchive = {
    schemaVersion: 1,
    exportType: "GDPR-Article-15-20-SAR-Data-Export",
    app: "readme-ux-kit-showcase",
    appVersion: APP_VERSION,
    exportedAt: new Date().toISOString(),
    storageInventory: {
      localStorage: {
        [FAVORITES_KEY]: [...state.favorites],
      },
      sessionStorage: {},
      cookies: [],
    },
    preferences: {
      gridColumns: state.cols,
      activeCategory: state.category,
      activeTheme: state.theme,
      favoritesOnly: state.favoritesOnly,
      reducedMotion: state.reducedMotion,
    },
  };
  const jsonText = JSON.stringify(exportArchive, null, 2);
  const objectUrl = URL.createObjectURL(new Blob([jsonText], { type: "application/json" }));
  triggerDownload(objectUrl, "readme-ux-kit-user-data-export.json");
  URL.revokeObjectURL(objectUrl);
  setStatus("Exported local user data archive (JSON).");
}

function purgeAllLocalData() {
  revokeEditorPreviewUrl();
  try {
    localStorage.removeItem(FAVORITES_KEY);
    localStorage.clear();
    sessionStorage.clear();
  } catch {
    // Storage access may be restricted in private sandboxes.
  }
  state.favorites.clear();
  state.flipped.clear();
  state.svgCache.clear();
  state.lastError = null;
  state.editor.item = null;
  state.editor.source = "";
  state.editor.editedSvg = "";
  state.editor.lastOperations = {};
  state.editor.gifFileNameTouched = false;
  state.query = "";
  state.category = "all";
  state.theme = "All Themes";
  state.favoritesOnly = false;
  if (nodes.searchInput) nodes.searchInput.value = "";
  if (nodes.bugDescription) nodes.bugDescription.value = "";
  if (nodes.bugSteps) nodes.bugSteps.value = "";
  if (nodes.feedbackComment) nodes.feedbackComment.value = "";
  if (nodes.interfaceLangSelect) nodes.interfaceLangSelect.value = "en";
  document.documentElement.lang = "en";
  if (nodes.favoritesOnly) {
    nodes.favoritesOnly.setAttribute("aria-pressed", "false");
    nodes.favoritesOnly.classList.remove("primary");
    nodes.favoritesOnly.classList.add("secondary");
  }
  setDensity("3");
  render();
  updateDiagnosticPreview();
  setStatus("Purged all local storage keys and reset showcase preferences to defaults.");
}

function showRuntimeError(error, sourceLabel = "runtime") {
  const message = error instanceof Error ? error.message : String(error || "Unknown runtime error");
  const stack = error instanceof Error && error.stack ? error.stack : `${sourceLabel}: ${message}`;
  state.lastError = { message, stack, sourceLabel, timestamp: new Date().toISOString() };
  if (nodes.errorBannerMessage) {
    nodes.errorBannerMessage.textContent = `A recoverable error occurred (${message}). Use Reset / Recover to restore the default view.`;
  }
  if (nodes.errorTechnicalDetails) {
    nodes.errorTechnicalDetails.textContent = stack;
  }
  if (nodes.errorBanner) {
    nodes.errorBanner.hidden = false;
  }
  setStatus(`Runtime error caught: ${message}`);
}

function recoverFromError() {
  state.lastError = null;
  if (nodes.errorBanner) nodes.errorBanner.hidden = true;
  closeFilterPopovers();
  if (nodes.assetModal?.hasAttribute("open")) closeModal();
  if (nodes.editorModal?.hasAttribute("open")) closeEditor();
  if (nodes.supportModal?.hasAttribute("open")) closeSupportModal();
  state.query = "";
  state.category = "all";
  state.theme = "All Themes";
  state.favoritesOnly = false;
  if (nodes.searchInput) nodes.searchInput.value = "";
  if (nodes.favoritesOnly) {
    nodes.favoritesOnly.setAttribute("aria-pressed", "false");
    nodes.favoritesOnly.classList.remove("primary");
    nodes.favoritesOnly.classList.add("secondary");
  }
  render();
  setStatus("Recovered workspace state cleanly.");
}

boot();
