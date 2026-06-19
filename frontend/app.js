const API = "http://127.0.0.1:8000/api";

let selectedDocType = null;
let templatesData = {};
let selectedFile = null;

// ─────────────────────────────────────────
// INIT
// ─────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  loadTemplates();

  document.getElementById("doc-text").addEventListener("input", function () {
    const words = this.value
      .trim()
      .split(/\s+/)
      .filter((x) => x).length;
    document.getElementById("word-count").textContent =
      `${words.toLocaleString()} words`;
  });
  document
    .getElementById("file-input")
    .addEventListener("change", function (e) {
      const file = e.target.files[0];
      if (file) processFile(file);
    });
  // Drag & drop setup
  const uploadArea = document.getElementById("upload-area");
  if (uploadArea) {
    uploadArea.addEventListener("dragover", (e) => {
      e.preventDefault();
      uploadArea.classList.add("drag-over");
    });
    uploadArea.addEventListener("dragleave", () => {
      uploadArea.classList.remove("drag-over");
    });
    uploadArea.addEventListener("drop", (e) => {
      e.preventDefault();
      uploadArea.classList.remove("drag-over");
      const file = e.dataTransfer.files[0];
      if (file) processFile(file);
    });
  }
});

// ─────────────────────────────────────────
// TEMPLATES
// ─────────────────────────────────────────
async function loadTemplates() {
  try {
    const res = await fetch(`${API}/templates/`);
    const data = await res.json();
    templatesData = data.templates;
    renderDocCards();
  } catch (e) {
    document.getElementById("doc-cards").innerHTML =
      '<p style="color:red;font-size:13px">Backend server chhaina. Django server start garnus: python manage.py runserver</p>';
  }
}

function renderDocCards() {
  const grid = document.getElementById("doc-cards");
  const semLabels = {
    project_1: "4th Semester",
    project_2: "6th Semester",
    internship: "7th Semester",
    project_3: "8th Semester",
  };

  grid.innerHTML = Object.entries(templatesData)
    .map(
      ([key, tmpl]) => `
    <div class="doc-card" onclick="selectDoc('${key}', this)">
      <div class="sem">${semLabels[key] || tmpl.semester + " Semester"}</div>
      <div class="name">${tmpl.name.split("—")[0].split("(")[0].trim()}</div>
      <div class="code">${tmpl.code}</div>
    </div>
  `,
    )
    .join("");
}

function selectDoc(key, el) {
  document
    .querySelectorAll(".doc-card")
    .forEach((c) => c.classList.remove("selected"));
  el.classList.add("selected");
  selectedDocType = key;
  document.getElementById("step1-next").disabled = false;
}

// ─────────────────────────────────────────
// FILE UPLOAD
// ─────────────────────────────────────────
function processFile(file) {
  const ext = file.name.toLowerCase();
  if (!ext.endsWith(".pdf") && !ext.endsWith(".docx")) {
    alert("PDF vaa DOCX matra supported xa.");
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    alert("10MB bhandaa thulo xa.");
    return;
  }
  selectedFile = file;
  const area = document.getElementById("upload-area");
  area.classList.add("file-selected");
  document.getElementById("upload-content").innerHTML = `
    <div class="upload-icon-wrap" style="background:#EAF3E8">
      <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
        <path d="M5 14l6 6L23 8" stroke="#2D6A2D" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    <p class="upload-title" style="color:#2D6A2D">
      ${ext.endsWith(".pdf") ? "📕" : "📘"} ${file.name}
    </p>
    <p class="upload-hint">${(file.size / 1024).toFixed(0)} KB · Click to change</p>
    <span class="upload-btn-label" style="border-color:#2D6A2D;color:#2D6A2D">Change file</span>`;
  document.getElementById("doc-text").value = "";
  document.getElementById("word-count").textContent = "0 words";
}

// ─────────────────────────────────────────
// STEP NAVIGATION
// ─────────────────────────────────────────
function setStep(n) {
  document.getElementById("progress-fill").style.width =
    n === 1 ? "33%" : n === 2 ? "66%" : "100%";

  [1, 2, 3].forEach((i) => {
    const item = document.getElementById(`step${i}-dot`);
    const numEl = item.querySelector(".step-num");
    item.classList.remove("active", "done");
    if (i < n) {
      item.classList.add("done");
      numEl.textContent = "✓";
    } else if (i === n) {
      item.classList.add("active");
      numEl.textContent = String(i).padStart(2, "0");
    } else numEl.textContent = String(i).padStart(2, "0");
  });

  [1, 2, 3].forEach((i) => {
    document.getElementById(`step${i}`).style.display =
      i === n ? "block" : "none";
  });
}

function goToStep1() {
  selectedFile = null;
  const fi = document.getElementById("file-input");
  if (fi) fi.value = "";
  const area = document.getElementById("upload-area");
  if (area) {
    area.classList.remove("file-selected", "drag-over");
    document.getElementById("upload-content").innerHTML = `
      <div class="upload-icon-wrap">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <rect x="4" y="4" width="24" height="24" rx="4" stroke="#C4884A"
                stroke-width="1.5" stroke-dasharray="4 3"/>
          <path d="M16 20v-8M12 16l4-4 4 4" stroke="#C4884A" stroke-width="1.5"
                stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <p class="upload-title">Drop your file here</p>
      <p class="upload-hint">PDF or DOCX · Max 10MB</p>
      <span class="upload-btn-label">Browse files</span>`;
  }
  document.getElementById("doc-text").value = "";
  document.getElementById("word-count").textContent = "0 words";
  setStep(1);
}

function goToStep2() {
  if (!selectedDocType) return;

  // Reference format update
  const refEl = document.getElementById("ref-format");
  if (refEl) {
    refEl.textContent =
      selectedDocType === "internship" ? "APA format" : "IEEE format";
  }

  fetch(`${API}/templates/${selectedDocType}/`)
    .then((res) => res.json())
    .then((data) =>
      renderSectionList(data.required_sections, data.optional_sections),
    )
    .catch((e) => console.error(e));

  setStep(2);
}

function renderSectionList(required, optional) {
  const container = document.getElementById("section-list");
  const all = [
    ...required.map((s) => ({ name: s, opt: false })),
    ...optional.map((s) => ({ name: s, opt: true })),
  ];
  container.innerHTML = all
    .map(
      (s, i) => `
    <div class="section-item">
      <span class="num">${i + 1}.</span>
      <span>${capitalize(s.name)}</span>
      ${s.opt ? '<span class="opt">optional</span>' : ""}
    </div>
  `,
    )
    .join("");
}

// ─────────────────────────────────────────
// ANALYZE
// ─────────────────────────────────────────
const loadMsgs = [
  "Checking document structure...",
  "Verifying TU FOHSS sections...",
  "Analyzing academic language...",
  "Checking IEEE referencing...",
  "Calculating compliance score...",
];

async function analyze() {
  const text = document.getElementById("doc-text").value.trim();
  const hasFile = selectedFile !== null;
  const hasText = text.split(/\s+/).filter((x) => x).length >= 30;

  if (!hasFile && !hasText) {
    alert("File upload garnus vaa document text (min 30 words) paste garnus.");
    return;
  }

  setStep(3);
  document.getElementById("loading").style.display = "flex";
  document.getElementById("results").style.display = "none";

  let msgIdx = 0;
  const msgEl = document.getElementById("load-msg");
  const msgTimer = setInterval(() => {
    msgIdx = (msgIdx + 1) % loadMsgs.length;
    msgEl.textContent = loadMsgs[msgIdx];
  }, 1500);

  // Timeout controller
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 90000); // 90 sec

  try {
    let res;

    if (hasFile) {
      const formData = new FormData();
      formData.append("file", selectedFile);
      formData.append("doc_type", selectedDocType);
      res = await fetch(`${API}/analyze/`, {
        method: "POST",
        body: formData,
        signal: controller.signal,
      });
    } else {
      res = await fetch(`${API}/analyze/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, doc_type: selectedDocType }),
        signal: controller.signal,
      });
    }

    clearTimeout(timeout);
    clearInterval(msgTimer);

    const data = await res.json();

    if (data.error) {
      showError("Server error: " + data.error);
      return;
    }

    renderResults(data);

    document.querySelector(".results-actions").innerHTML = `
      <button class="btn-ghost" onclick="goToStep2()">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M11 7H3M7 3L3 7l4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        Edit document
      </button>
      <button class="btn-ghost" onclick="goToStep1()">Start over</button>
      <button class="btn-primary" onclick="downloadReport()" style="margin-left:auto">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M7 1v8M4 10l3 3 3-3M1 10v2a1 1 0 001 1h10a1 1 0 001-1v-2"
                stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        Download Report
      </button>`;

  } catch (e) {
    clearTimeout(timeout);
    clearInterval(msgTimer);
    if (e.name === "AbortError") {
      showError("Analysis took too long (90s). Try with a smaller file or use plain text.");
    } else {
      showError("Backend connect huna sakena. Django server chalidai xa ki check garnus.");
    }
  }
}

// ─────────────────────────────────────────
// RENDER RESULTS
// ─────────────────────────────────────────
function renderResults(data) {
  document.getElementById("loading").style.display = "none";
  document.getElementById("results").style.display = "block";

  const score = data.score;
  const scoreClass = score >= 75 ? "good" : score >= 50 ? "ok" : "bad";
  const scoreDesc =
    score >= 75
      ? "Well structured document"
      : score >= 50
        ? "Needs some improvements"
        : "Significant issues found";

  // Progress bar update
  document.getElementById("progress-fill").style.width = "100%";

  // Score circle
  document.getElementById("score-num").textContent = score;
  document.getElementById("score-desc").textContent = scoreDesc;
  document.getElementById("score-circle").className =
    `score-circle ${scoreClass}`;

  // Metrics
  document.getElementById("metrics").innerHTML = `
    <div class="metric-card">
      <div class="metric-val">${data.structure.sections_found}/${data.structure.total_required}</div>
      <div class="metric-lbl">Sections<br>detected</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">${(data.total_words || 0).toLocaleString()}</div>
      <div class="metric-lbl">Total<br>words</div>
    </div>
    <div class="metric-card">
      <div class="metric-val ${data.total_issues > 5 ? "bad" : data.total_issues > 2 ? "ok" : "good"}">${data.total_issues}</div>
      <div class="metric-lbl">Issues<br>found</div>
    </div>
    ${
      data.group_info?.member_count
        ? `
    <div class="metric-card">
      <div class="metric-val">${data.group_info.member_count}</div>
      <div class="metric-lbl">Member(s)<br>detected</div>
    </div>`
        : ""
    }
  `;

  const fb = document.getElementById("feedback");
  fb.innerHTML = "";
  // ── 0. DOCUMENT TYPE CHECK ──
  if (data.numbering_issues?.length > 0) {
    const hasError = data.numbering_issues.some((n) => n.type === "error");
    const items = data.numbering_issues
      .map((n) => `<div class="fb-item ${n.type}">${n.message}</div>`)
      .join("");
    fb.innerHTML += buildSection(
      "🚨 Document Type Check",
      hasError ? "error" : "warning",
      items,
    );
  }

  // Proposal bhane score circle red
  const isProposal = data.numbering_issues?.some(
    (n) => n.type === "error" && n.message.includes("PROPOSAL"),
  );
  if (isProposal) {
    document.getElementById("score-circle").className = "score-circle bad";
    document.getElementById("score-desc").textContent =
      "⚠️ This appears to be a proposal — submit your final report";
  }

  // ── 1. GROUP VALIDATION ──
  if (data.group_info?.feedback?.length > 0) {
    const g = data.group_info;
    let html = "";
    if (g.member_count) {
      html += `<div class="fb-item ${g.member_count > 2 ? "error" : "success"}">
        👥 <strong>${g.member_count} member(s) detected</strong>
        ${g.member_names?.length ? ` — ${g.member_names.join(", ")}` : ""}
        ${g.roll_nos?.length ? `<br><span style="font-size:11px;opacity:.7">Roll: ${g.roll_nos.join(", ")}</span>` : ""}
      </div>`;
    }
    g.feedback.forEach((f) => {
      html += `<div class="fb-item ${f.type}">
        ${f.type === "error" ? "❌" : f.type === "warning" ? "⚠️" : f.type === "success" ? "✅" : "ℹ️"}
        ${f.message}
      </div>`;
    });
    fb.innerHTML += buildSection(
      "👥 Group / Member Validation",
      g.feedback.some((f) => f.type === "error")
        ? "error"
        : g.feedback.some((f) => f.type === "warning")
          ? "warning"
          : "success",
      html,
    );
  }

  // ── 2. MISSING SECTIONS ──
  if (data.section_guides?.length > 0) {
    let html = "";
    data.section_guides.forEach((guide) => {
      html += `
        <div class="fb-item error expandable">
          <div class="fb-item-header" onclick="toggleExpand(this)">
            <span>❌ <strong>${guide.section}</strong> — Missing</span>
            <span class="expand-btn">▼ How to fix</span>
          </div>
          <div class="fb-expand-content" style="display:none">
            <p class="fb-label">📝 This section must contain:</p>
            <ul class="fix-list">
              ${guide.must_contain.map((c) => `<li>${c}</li>`).join("")}
            </ul>
            ${guide.word_limit ? `<p class="fb-meta">📏 Suggested: <strong>${guide.word_limit}</strong></p>` : ""}
            ${guide.tip ? `<p class="fb-tip">💡 ${guide.tip}</p>` : ""}
            ${
              guide.template
                ? `<p class="fb-label" style="margin-top:.5rem">✏️ Template:</p>
              <div class="code-block">${guide.template}</div>`
                : ""
            }
          </div>
        </div>`;
    });
    fb.innerHTML += buildSection(
      "📋 Missing Sections — How to Fix",
      "error",
      html,
    );
  } else {
    fb.innerHTML += buildSection(
      "📋 Section Structure",
      "success",
      `<div class="fb-item success">✅ All required sections detected!</div>`,
    );
  }

  // ── 3. CHAPTER SUB-SECTIONS ──
  if (data.structure.subsection_issues?.length > 0) {
    const items = data.structure.subsection_issues
      .map(
        (s) =>
          `<div class="fb-item warning">⚠️ Missing: <strong>${s}</strong></div>`,
      )
      .join("");
    fb.innerHTML += buildSection("📑 Chapter Sub-sections", "warning", items);
  }

  // ── 4. PASSIVE VOICE FIXES ──
  if (data.passive_fixes?.length > 0) {
    let html = `<div class="fb-item error">❌ First-person active voice detected. TU FOHSS requires passive voice / third-person.</div>
      <p class="fb-label" style="margin:.6rem 0 .4rem">🔄 Specific corrections:</p>`;
    data.passive_fixes.forEach((fix) => {
      html += `<div class="fix-card">
        <div class="fix-original">❌ "${fix.sentence || fix.original}"</div>
        <div class="fix-arrow">↓ Suggested fix</div>
        <div class="fix-suggested">✅ "${fix.suggested}"</div>
      </div>`;
    });
    fb.innerHTML += buildSection(
      "✍️ First-Person Language Fixes",
      "error",
      html,
    );
  }

  // ── 5. GRAMMAR ISSUES ──
  if (data.grammar_issues?.length > 0) {
    const high = data.grammar_issues.filter((g) => g.priority === "high");
    const normal = data.grammar_issues.filter((g) => g.priority === "normal");
    let html = "";
    if (high.length > 0) {
      html += `<p class="fb-label" style="margin-bottom:.4rem">🔴 Significant issues:</p>`;
      high.forEach((g) => {
        html += `<div class="fix-card">
          <div class="fix-original">❌ ${g.context}</div>
          <div class="fix-arrow">↓ ${g.message}</div>
          ${g.suggestion ? `<div class="fix-suggested">✅ "${g.suggestion}"</div>` : ""}
        </div>`;
      });
    }
    if (normal.length > 0) {
      html += `<p class="fb-label" style="margin:.6rem 0 .4rem">🟡 Minor suggestions:</p>`;
      normal.forEach((g) => {
        html += `<div class="fb-item warning" style="margin-bottom:4px">
          ⚠️ ${g.message}
          ${g.suggestion ? ` → <strong>"${g.suggestion}"</strong>` : ""}
          <br><span style="font-size:11px;font-style:italic;opacity:.8">${g.context}</span>
        </div>`;
      });
    }
    fb.innerHTML += buildSection(
      "📝 Grammar Analysis",
      high.length > 0 ? "error" : "warning",
      html,
    );
  }

  // ── ACADEMIC TONE ──
  if (data.academic_tone?.length > 0) {
    const items = data.academic_tone
      .map(
        (f) => `
      <div class="fb-item ${f.type}">
        ${f.type === "error" ? "❌" : f.type === "warning" ? "⚠️" : f.type === "success" ? "✅" : "ℹ️"}
        ${f.message}
      </div>`,
      )
      .join("");
    fb.innerHTML += buildSection(
      "🎓 Academic Tone",
      getBadgeType(data.academic_tone),
      items,
    );
  }

  // ── 6. INFORMAL LANGUAGE ──
  if (data.informal_fixes?.length > 0) {
    let html = `<div class="fb-item warning">⚠️ Informal vocabulary found — replace with academic terms:</div>
      <table class="fix-table">
        <thead><tr><th>Informal</th><th>Replace with</th><th>Context</th></tr></thead>
        <tbody>
          ${data.informal_fixes
            .map(
              (f) => `
            <tr>
              <td class="word-bad">"${f.word}"${f.count > 1 ? ` ×${f.count}` : ""}</td>
              <td class="word-good">${f.replace_with}</td>
              <td class="word-context">${f.context}</td>
            </tr>`,
            )
            .join("")}
        </tbody>
      </table>`;
    fb.innerHTML += buildSection("🗣️ Informal Language", "warning", html);
  }

  // ── 7. WORD COUNT ──
  const wcInfo = (data.wordcount || []).filter((w) => w.type === "info");
  const wcSuccess = (data.wordcount || []).filter((w) => w.type === "success");
  if (wcInfo.length > 0 || wcSuccess.length > 0) {
    let html = `<div class="fb-item info" style="margin-bottom:.5rem">
      ℹ️ <strong>Note:</strong> Word counts are <strong>estimates</strong> — 
      not mandatory TU requirements. Content quality matters more.
      ${
        data.file_type === "pdf"
          ? "<br>⚠️ <strong>PDF detected:</strong> Word counts may vary ±20%. Upload <strong>DOCX</strong> for accurate analysis."
          : ""
      }
    </div>`;
    wcInfo.forEach((w) => {
      html += `<div class="fb-item info expandable">
        <div class="fb-item-header" onclick="toggleExpand(this)">
          <span>ℹ️ ${w.message}</span>
          ${w.how_to_fix ? `<span class="expand-btn">▼ Suggestions</span>` : ""}
        </div>
        ${
          w.how_to_fix
            ? `<div class="fb-expand-content" style="display:none">
          <ul class="fix-list">${w.how_to_fix.map((h) => `<li>${h}</li>`).join("")}</ul>
          ${w.tip ? `<p class="fb-tip">💡 ${w.tip}</p>` : ""}
        </div>`
            : ""
        }
      </div>`;
    });
    wcSuccess.forEach((w) => {
      html += `<div class="fb-item success">✅ ${w.message}</div>`;
    });
    fb.innerHTML += buildSection(
      "📏 Word Count",
      wcInfo.length > 0 ? "info" : "success",
      html,
    );
  }

  // ── 8. FORMATTING ──
  if (data.formatting?.length > 0) {
    const items = data.formatting
      .map(
        (f) => `
      <div class="fb-item ${f.type}">
        ${f.type === "error" ? "❌" : f.type === "warning" ? "⚠️" : f.type === "success" ? "✅" : "ℹ️"}
        ${f.message}
      </div>`,
      )
      .join("");
    fb.innerHTML += buildSection(
      "📐 Formatting",
      getBadgeType(data.formatting),
      items,
    );
  }

  // ── Template info ──
  fb.innerHTML += buildSection(
    "ℹ️ Analysis Info",
    "info",
    `
        <div class="fb-item info">
          <strong>Template:</strong> ${data.template_name} ·
          <strong>Code:</strong> ${data.course_code} ·
          <strong>File:</strong> ${(data.file_type || "text").toUpperCase()} ·
          <strong>Referencing:</strong> ${data.doc_type === "internship" ? "APA" : "IEEE"}
        </div>`,
  );
}

// ─────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────
function showError(msg) {
  clearInterval(0); // safety
  document.getElementById("loading").style.display = "none";
  document.getElementById("results").style.display = "block";
  document.getElementById("score-banner").style.display = "none";
  document.getElementById("feedback").innerHTML = `
    <div class="fb-section">
      <div class="fb-section-body">
        <div class="fb-item error">❌ ${msg}</div>
        <div style="margin-top:.75rem;display:flex;gap:8px">
          <button class="btn-ghost" onclick="goToStep2()">← Try again</button>
          <button class="btn-ghost" onclick="goToStep1()">Start over</button>
        </div>
      </div>
    </div>`;
}

function icon(type) {
  return type === "error"
    ? "❌"
    : type === "warning"
      ? "⚠️"
      : type === "success"
        ? "✅"
        : "ℹ️";
}

function buildSection(title, badgeType, content) {
  const badgeText = {
    error: "Action needed",
    warning: "Review",
    success: "Good",
    info: "Info",
  };
  return `
    <div class="fb-section">
      <div class="fb-section-header">
        <span class="fb-section-title">${title}</span>
        <span class="fb-badge ${badgeType}">${badgeText[badgeType] || badgeType}</span>
      </div>
      <div class="fb-section-body">${content}</div>
    </div>`;
}

function getBadgeType(items) {
  if (items.some((i) => i.type === "error")) return "error";
  if (items.some((i) => i.type === "warning")) return "warning";
  return "success";
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function toggleExpand(header) {
  const content = header.nextElementSibling;
  if (!content) return;
  const btn = header.querySelector(".expand-btn");
  if (content.style.display === "none") {
    content.style.display = "block";
    if (btn) btn.textContent = "▲ Hide";
  } else {
    content.style.display = "none";
    if (btn) btn.textContent = "▼ How to fix";
  }
}

function downloadReport() {
  const score = document.getElementById("score-num").textContent;
  const scoreDesc = document.getElementById("score-desc").textContent;
  const metrics = document.getElementById("metrics").innerHTML;
  const feedback = document.getElementById("feedback").innerHTML;

  const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8"/>
  <title>TU Document Analysis Report</title>
  <style>
    body {
      font-family: 'Times New Roman', serif;
      max-width: 750px;
      margin: 0 auto;
      padding: 40px;
      color: #1C1714;
      line-height: 1.6;
    }
    .report-header {
      text-align: center;
      border-bottom: 2px solid #7A2E1A;
      padding-bottom: 20px;
      margin-bottom: 30px;
    }
    .report-header h1 {
      font-size: 20px;
      color: #7A2E1A;
      margin-bottom: 4px;
    }
    .report-header p {
      font-size: 12px;
      color: #666;
    }
    .score-box {
      background: #FAF8F4;
      border: 1px solid #E4DDD8;
      border-radius: 8px;
      padding: 16px 20px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .score-big {
      font-size: 36px;
      font-weight: 700;
      color: #7A2E1A;
      min-width: 80px;
    }
    .metric-card {
      background: #F0EBE3;
      border-radius: 6px;
      padding: 8px 14px;
      text-align: center;
      display: inline-block;
      margin: 4px;
    }
    .metric-val { font-size: 18px; font-weight: 700; }
    .metric-lbl { font-size: 10px; color: #666; }
    .fb-section {
      margin-bottom: 20px;
      border: 1px solid #E4DDD8;
      border-radius: 8px;
      overflow: hidden;
      page-break-inside: avoid;
    }
    .fb-section-header {
      background: #FAF8F4;
      padding: 10px 16px;
      border-bottom: 1px solid #E4DDD8;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .fb-section-title { font-size: 13px; font-weight: 600; }
    .fb-section-body { padding: 12px 16px; }
    .fb-item {
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 11.5px;
      margin-bottom: 5px;
      border-left: 3px solid transparent;
      line-height: 1.55;
    }
    .fb-item.error   { background: #FCEDED; border-left-color: #D63030; color: #4A0A0A; }
    .fb-item.warning { background: #FDF5E0; border-left-color: #E8A000; color: #4A3000; }
    .fb-item.success { background: #EAF3E8; border-left-color: #3D8B3D; color: #0A2A0A; }
    .fb-item.info    { background: #E8EFF9; border-left-color: #3B6FCC; color: #0A1E4A; }
    .fb-badge { font-size: 10px; padding: 2px 8px; border-radius: 10px; font-weight: 600; }
    .fb-badge.error   { background: #FCEDED; color: #8B1A1A; }
    .fb-badge.warning { background: #FDF5E0; color: #7A5500; }
    .fb-badge.success { background: #EAF3E8; color: #2D6A2D; }
    .fb-badge.info    { background: #E8EFF9; color: #1A3D6B; }
    .fix-card {
      background: #fff;
      border: 1px solid #E4DDD8;
      border-radius: 6px;
      padding: 8px 12px;
      margin: 4px 0;
      font-size: 11.5px;
    }
    .fix-original  { color: #8B1A1A; font-style: italic; }
    .fix-suggested { color: #2D6A2D; font-weight: 600; margin-top: 3px; }
    .fix-list { padding-left: 16px; font-size: 11.5px; color: #4A3F38; }
    .fix-list li { margin-bottom: 3px; }
    .fix-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
      margin-top: 6px;
    }
    .fix-table th {
      background: #F0EBE3;
      padding: 6px 8px;
      text-align: left;
      font-size: 10px;
      font-weight: 600;
      text-transform: uppercase;
    }
    .fix-table td {
      padding: 6px 8px;
      border-top: 1px solid #EDE8E3;
    }
    .expand-btn, .fb-item.expandable { display: block; }
    .fb-expand-content { display: block !important; }
    .fb-item-header { display: block; }
    .fb-tip {
      background: #F5E8D6;
      border-left: 3px solid #C4884A;
      padding: 6px 10px;
      border-radius: 0 6px 6px 0;
      font-size: 11px;
      color: #5A4000;
      margin-top: 6px;
    }
    .fb-label { font-size: 11.5px; font-weight: 600; color: #4A3F38; margin-bottom: 4px; }
    .code-block {
      background: #FAF8F4;
      border: 1px solid #E4DDD8;
      border-radius: 4px;
      padding: 8px 10px;
      font-family: 'Courier New', monospace;
      font-size: 10.5px;
      white-space: pre-line;
      margin-top: 4px;
    }
    .report-footer {
      text-align: center;
      font-size: 10px;
      color: #999;
      border-top: 1px solid #E4DDD8;
      padding-top: 16px;
      margin-top: 30px;
    }
    .fb-item.expandable{display:block}
    .fb-expand-content{display:block!important}
    @media print {
      body { padding: 20px; }
      .score-box { page-break-inside: avoid; }
    }
  </style>
</head>
<body>
  <div class="report-header">
    <h1>TU BCA Document Analysis Report</h1>
    <p>Generated by TU Document Assistant · ${new Date().toLocaleDateString(
      "en-US",
      {
        year: "numeric",
        month: "long",
        day: "numeric",
      },
    )}</p>
  </div>

  <div class="score-box">
    <div class="score-big">${score}<span style="font-size:14px;color:#666">/100</span></div>
    <div>
      <div style="font-size:14px;font-weight:600;margin-bottom:6px">${scoreDesc}</div>
      <div>${metrics}</div>
    </div>
  </div>

  ${feedback}

  <div class="report-footer">
    Tribhuvan University · Faculty of Humanities and Social Sciences · BCA Document Assistant
  </div>
</body>
</html>`;

  // Open print dialog — user can Save as PDF
  const win = window.open("", "_blank");
  if (!win) {  // ← null check chhaina!
    alert("Popup blocked! Browser settings ma popup allow garnus.");
    return;
  }
  win.document.write(html);
  win.document.close();
  win.onload = () => {
    win.print();
  };
}
