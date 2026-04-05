// ======================================================
// ★ API Gateway の URL をここに設定してください ★
// ======================================================
const API_URL = "https://kuejdkujf9.execute-api.ap-northeast-1.amazonaws.com/prod/rant";
// ======================================================

const messagesEl = document.getElementById("messages");
const inputEl    = document.getElementById("user-input");
const sendBtn    = document.getElementById("send-btn");

let exchangeCount = 0;

const SPINNER_FRAMES = ["\u2807","\u2819","\u2839","\u2838","\u283c","\u2834","\u2826","\u2827","\u2807","\u280f"];
const THINKING_MSGS  = ["ふむ...", "考えておる...", "若いもんのことを思うと...", "ワシの時代はのう..."];

function scrollBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function addSeparator() {
  const hr = document.createElement("hr");
  hr.className = "separator";
  messagesEl.appendChild(hr);
}

function addUserMessage(text) {
  const row = document.createElement("div");
  row.className = "msg-user";
  row.innerHTML = `<span class="label">あなた</span><span class="text">${escHtml(text)}</span>`;
  messagesEl.appendChild(row);
  addSeparator();
  scrollBottom();
}

function escHtml(s) {
  return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function startThinking() {
  const row = document.createElement("div");
  row.className = "msg-thinking";

  const spinnerEl = document.createElement("span");
  spinnerEl.className = "spinner-char";
  spinnerEl.style.color = "#e8a020";

  const msgEl = document.createElement("span");

  row.appendChild(spinnerEl);
  row.appendChild(msgEl);
  messagesEl.appendChild(row);
  scrollBottom();

  let fi = 0, mi = 0;
  const timer = setInterval(() => {
    spinnerEl.textContent = SPINNER_FRAMES[fi % SPINNER_FRAMES.length];
    if (fi % 10 === 0) { msgEl.textContent = THINKING_MSGS[mi % THINKING_MSGS.length]; mi++; }
    fi++;
  }, 80);

  return () => { clearInterval(timer); row.remove(); };
}

function showAngryMessage() {
  addSeparator();
  const row = document.createElement("div");
  row.className = "msg-angry";
  row.innerHTML = `
    <span class="angry-text">バカモノ！<br>いつまでAIに頼ってるんだ！</span>
    <span class="angry-sub">— 玄人より渾身の一言 —</span>
  `;
  messagesEl.appendChild(row);
  addSeparator();
  scrollBottom();
}

function typewriterRant(text, onDone) {
  addSeparator();
  const row = document.createElement("div");
  row.className = "msg-kurouto";
  const label = document.createElement("span");
  label.className = "label";
  label.textContent = "玄人";
  const textEl = document.createElement("span");
  textEl.className = "text";
  row.appendChild(label);
  row.appendChild(textEl);
  messagesEl.appendChild(row);

  const codeMatch = text.match(/^([\s\S]*?)(#include[\s\S]+return 0;\n\})([\s\S]*)$/);
  if (codeMatch) {
    const before = codeMatch[1];
    const code   = codeMatch[2];
    const after  = codeMatch[3];
    const fullText = before + "\x00CODE\x00" + after;
    let i = 0;
    let codeInserted = false;
    function tick() {
      if (i >= fullText.length) { addSeparator(); scrollBottom(); if (onDone) onDone(); return; }
      const ch = fullText[i++];
      if (ch === "\x00" && fullText.slice(i, i+4) === "CODE") {
        i += 5;
        const pre = document.createElement("pre");
        pre.textContent = code;
        textEl.appendChild(pre);
        codeInserted = true;
        scrollBottom();
        setTimeout(tick, 30);
        return;
      }
      if (ch === "\n") {
        textEl.appendChild(document.createTextNode("\n"));
      } else {
        const last = textEl.lastChild;
        if (last && last.nodeType === Node.TEXT_NODE && !codeInserted) {
          last.textContent += ch;
        } else {
          textEl.appendChild(document.createTextNode(ch));
          codeInserted = false;
        }
      }
      scrollBottom();
      const delay = "。、\n".includes(ch) ? 80 + Math.random() * 120 : 15 + Math.random() * 30;
      setTimeout(tick, delay);
    }
    tick();
    return;
  }

  let i = 0;
  function tick() {
    if (i >= text.length) { addSeparator(); scrollBottom(); if (onDone) onDone(); return; }
    const ch = text[i++];
    textEl.textContent += ch;
    scrollBottom();
    const delay = "。、\n".includes(ch)
      ? 80 + Math.random() * 120
      : 15 + Math.random() * 30;
    setTimeout(tick, delay);
  }
  tick();
}

async function send() {
  const prompt = inputEl.value.trim();
  if (!prompt) return;

  inputEl.value = "";
  inputEl.disabled = true;
  sendBtn.disabled = true;

  exchangeCount++;
  addUserMessage(prompt);

  const stopThinking = startThinking();

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, exchange_count: exchangeCount }),
    });
    const data = await res.json();
    stopThinking();
    typewriterRant(data.rant, () => {
      if (data.angry) showAngryMessage();
    });
  } catch (e) {
    stopThinking();
    typewriterRant("……ネットワークがつながらん。\nワシが若い頃はオフラインでも仕事をしたもんじゃ。\n根性が足りんのじゃ。");
  } finally {
    inputEl.disabled = false;
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

sendBtn.addEventListener("click", send);
inputEl.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
});

inputEl.focus();

// ── ダーク / ライト切替 ──
const themeBtn = document.getElementById("theme-btn");

function applyTheme(light) {
  document.body.classList.toggle("light", light);
  themeBtn.textContent = light ? "\u2600\ufe0f" : "\ud83c\udf19";
}

const saved = localStorage.getItem("theme");
const preferLight = saved
  ? saved === "light"
  : window.matchMedia("(prefers-color-scheme: light)").matches;
applyTheme(preferLight);

themeBtn.addEventListener("click", () => {
  const isLight = document.body.classList.toggle("light");
  themeBtn.textContent = isLight ? "\u2600\ufe0f" : "\ud83c\udf19";
  localStorage.setItem("theme", isLight ? "light" : "dark");
});
