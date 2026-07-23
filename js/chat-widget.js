/*
  Widget de Chat Inteligente PepaGold — Soporte Multilingüe en 10 Locales
  Incluye integración con botón en la barra superior de navegación y chat flotante inferior derecho.
*/
(function () {
  "use strict";

  const API_ENDPOINT = "/api/chat";
  const MAX_CHARS = 1500;

  const LANG_MAP = {
    "es-ar": "es-AR", "es-mx": "es-MX", "es-es": "es-ES", "en-us": "en-US",
    "fr-fr": "fr-FR", "de-de": "de-DE", "it-it": "it-IT", "pt-br": "pt-BR",
    "ru-ru": "ru-RU", "zh-hans": "zh-CN"
  };

  const rawLang = (document.documentElement.lang || "es-ar").toLowerCase();
  const pageLang = LANG_MAP[rawLang] ? rawLang : (rawLang.startsWith("es") ? "es-ar" : (rawLang.startsWith("en") ? "en-us" : "es-ar"));
  const speechLang = LANG_MAP[pageLang] || "es-AR";

  const STRINGS = {
    "es-ar": { title: "¿Tenés dudas?", placeholder: "Escribí tu pregunta…", send: "Enviar", greeting: "¡Hola! 👋 Puedo ayudarte a comprar, a registrarte en la plataforma de Greenway y a descubrir todos los productos ecológicos de la tienda. ¡Preguntame lo que quieras! 😊", navBtn: "Chat", tooLong: "Achicá un poco el mensaje, por favor.", error: "Algo falló. Intentá de nuevo en un momento." },
    "es-mx": { title: "¿Tienes dudas?", placeholder: "Escribe tu pregunta…", send: "Enviar", greeting: "¡Hola! 👋 Puedo ayudarte a comprar, a registrarte en la plataforma de Greenway y a descubrir todos los productos ecológicos de la tienda. ¡Pregúntame lo que quieras! 😊", navBtn: "Chat", tooLong: "Acorta un poco tu mensaje, por favor.", error: "Algo falló. Intenta de nuevo en un momento." },
    "es-es": { title: "¿Tienes dudas?", placeholder: "Escribe tu pregunta…", send: "Enviar", greeting: "¡Hola! 👋 Puedo ayudarte a comprar, a registrarte en la plataforma de Greenway y a descubrir todos los productos ecológicos de la tienda. ¡Pregúntame lo que quieras! 😊", navBtn: "Chat", tooLong: "Acorta un poco tu mensaje, por favor.", error: "Algo falló. Intenta de nuevo en un momento." },
    "en-us": { title: "Questions?", placeholder: "Type your question…", send: "Send", greeting: "Hi! 👋 I can help you buy, register on the Greenway platform, and discover all the eco-friendly products in our store. Ask me anything! 😊", navBtn: "Chat", tooLong: "Please shorten your message.", error: "Something went wrong. Please try again." },
    "fr-fr": { title: "Des questions ?", placeholder: "Posez votre question…", send: "Envoyer", greeting: "Bonjour ! 👋 Je peux vous aider à acheter, à vous inscrire sur la plateforme Greenway et à découvrir tous les produits écologiques. Posez-moi vos questions ! 😊", navBtn: "Chat", tooLong: "Veuillez raccourcir votre message.", error: "Une erreur est survenue. Veuillez réessayer." },
    "de-de": { title: "Fragen?", placeholder: "Stellen Sie Ihre Frage…", send: "Senden", greeting: "Hallo! 👋 Ich kann Ihnen beim Kauf, der Registrierung auf der Greenway-Plattform und beim Entdecken aller Produkte helfen. Fragen Sie mich alles! 😊", navBtn: "Chat", tooLong: "Bitte kürzen Sie Ihre Nachricht.", error: "Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut." },
    "it-it": { title: "Domande?", placeholder: "Scrivi la tua domanda…", send: "Invia", greeting: "Ciao! 👋 Posso aiutarti ad acquistare, registrarti sulla piattaforma Greenway e scoprire tutti i prodotti ecologici del negozio. Chiedimi qualsiasi cosa! 😊", navBtn: "Chat", tooLong: "Per favore accorcia il tuo messaggio.", error: "Si è verificato un errore. Riprova tra poco." },
    "pt-br": { title: "Dúvidas?", placeholder: "Digite sua pergunta…", send: "Enviar", greeting: "Olá! 👋 Posso ajudar você a comprar, se cadastrar na plataforma da Greenway e conhecer todos os produtos ecológicos da loja. Pergunte o que quiser! 😊", navBtn: "Chat", tooLong: "Por favor encurte sua mensagem.", error: "Ocorreu um erro. Tente novamente em instantes." },
    "ru-ru": { title: "Есть вопросы?", placeholder: "Напишите ваш вопрос…", send: "Отправить", greeting: "Привет! 👋 Я помогу вам оформить покупку, зарегистрироваться на платформе Greenway и узнать обо всех эко-товарах. Спросите меня о чем угодно! 😊", navBtn: "Чат", tooLong: "Пожалуйста, сократите сообщение.", error: "Произошла ошибка. Попробуйте еще раз." },
    "zh-hans": { title: "有疑问吗？", placeholder: "请输入您的问题…", send: "发送", greeting: "您好！👋 我可以帮助您购买商品、在 Greenway 平台注册，并了解商城中的所有环保产品。有任何问题随时问我！😊", navBtn: "聊天", tooLong: "请缩短您的消息。", error: "出错了，请稍后再试。" }
  };

  const t = STRINGS[pageLang] || STRINGS["es-ar"];

  // ---------------------------------------------------------------- Estilos PepaGold
  const style = document.createElement("style");
  style.textContent = `
    #pg-chat-btn { position: fixed; bottom: 20px; right: 20px; width: 58px; height: 58px;
      border-radius: 50%; background: linear-gradient(135deg, #c9a24b 0%, #a67c1e 100%); color: #fff; border: 2px solid rgba(255,255,255,0.4); cursor: pointer;
      box-shadow: 0 8px 24px rgba(201,162,75,0.4); font-size: 26px; z-index: 9999; transition: transform 0.2s ease, box-shadow 0.2s ease; display: flex; align-items: center; justify-content: center; }
    #pg-chat-btn:hover { transform: scale(1.08); box-shadow: 0 10px 28px rgba(201,162,75,0.6); }
    #pg-chat-win { position: fixed; bottom: 90px; right: 20px; width: 350px; max-width: 92vw;
      height: 490px; max-height: 75vh; background: #ffffff; border-radius: 18px;
      box-shadow: 0 12px 40px rgba(0,0,0,0.25); display: none; flex-direction: column;
      overflow: hidden; font-family: 'Inter', system-ui, -apple-system, sans-serif; z-index: 9999; border: 1px solid rgba(201,162,75,0.3); }
    #pg-chat-win.open { display: flex; animation: pgPopIn 0.25s cubic-bezier(0.16, 1, 0.3, 1); }
    @keyframes pgPopIn { from { opacity: 0; transform: translateY(12px) scale(0.96); } to { opacity: 1; transform: translateY(0) scale(1); } }
    #pg-chat-head { background: linear-gradient(135deg, #111827 0%, #1f2937 100%); color: #f3f4f6; padding: 14px 16px; font-weight: 600; font-size: 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #c9a24b; }
    #pg-chat-head .head-left { display: flex; align-items: center; gap: 8px; }
    #pg-chat-head .head-right { display: flex; align-items: center; gap: 10px; }
    #pg-chat-sound, #pg-chat-close { background: none; border: none; color: #d1d5db; font-size: 18px; cursor: pointer; padding: 2px 4px; transition: color 0.15s, transform 0.15s; }
    #pg-chat-sound:hover, #pg-chat-close:hover { color: #ffffff; transform: scale(1.1); }
    #pg-chat-log { flex: 1; overflow-y: auto; padding: 14px; font-size: 14px; background: #f9fafb; display: flex; flex-direction: column; gap: 10px; }
    .pg-msg { padding: 10px 14px; border-radius: 14px; max-width: 85%; line-height: 1.45; font-size: 13.5px; word-wrap: break-word; }
    .pg-msg.user { background: linear-gradient(135deg, #c9a24b 0%, #b38b34 100%); color: #ffffff; margin-left: auto; border-bottom-right-radius: 2px; box-shadow: 0 2px 8px rgba(201,162,75,0.25); }
    .pg-msg.bot { background: #ffffff; color: #1f2937; border: 1px solid #e5e7eb; border-bottom-left-radius: 2px; box-shadow: 0 2px 6px rgba(0,0,0,0.04); }
    #pg-chat-inputrow { display: flex; align-items: center; border-top: 1px solid #f3f4f6; padding: 10px; gap: 8px; background: #ffffff; }
    #pg-chat-text { flex: 1; border: 1px solid #e5e7eb; border-radius: 10px; padding: 9px 12px; font-size: 13.5px; resize: none; outline: none; transition: border-color 0.15s; font-family: inherit; }
    #pg-chat-text:focus { border-color: #c9a24b; box-shadow: 0 0 0 3px rgba(201,162,75,0.15); }
    
    /* Botón de Micrófono de Alto Contraste */
    #pg-chat-mic { border: 1px solid #c9a24b; background: #111827; color: #f3f4f6; width: 38px; height: 38px; border-radius: 10px; font-size: 17px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.15); }
    #pg-chat-mic:hover { background: #1f2937; color: #ffffff; transform: translateY(-1px); border-color: #e5c158; }
    #pg-chat-mic.listening { background: #dc2626 !important; color: #ffffff !important; border-color: #991b1b !important; box-shadow: 0 0 12px rgba(220,38,38,0.7); animation: pgMicPulse 1s infinite; }
    @keyframes pgMicPulse { 0%, 100% { transform: scale(1); box-shadow: 0 0 8px rgba(220,38,38,0.5); } 50% { transform: scale(1.12); box-shadow: 0 0 16px rgba(220,38,38,0.9); } }

    #pg-chat-send { border: none; background: #c9a24b; color: #ffffff; width: 38px; height: 38px; border-radius: 10px; font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background 0.15s, transform 0.15s; box-shadow: 0 2px 6px rgba(201,162,75,0.3); }
    #pg-chat-send:hover { background: #b38b34; transform: translateY(-1px); }
    #pg-chat-counter { font-size: 10.5px; color: #9ca3af; text-align: right; padding: 0 14px 4px; background: #ffffff; }
  `;
  document.head.appendChild(style);

  // ---------------------------------------------------------------- DOM
  const btn = document.createElement("button");
  btn.id = "pg-chat-btn";
  btn.textContent = "💬";
  btn.setAttribute("aria-label", t.title);

  const win = document.createElement("div");
  win.id = "pg-chat-win";
  win.innerHTML = `
    <div id="pg-chat-head">
      <div class="head-left">
        <span>✨ ${t.title}</span>
      </div>
      <div class="head-right">
        <button id="pg-chat-sound" title="Voz activada/desactivada" aria-label="Audio">🔊</button>
        <button id="pg-chat-close" title="Cerrar" aria-label="Cerrar">✕</button>
      </div>
    </div>
    <div id="pg-chat-log"></div>
    <div id="pg-chat-counter">0 / ${MAX_CHARS}</div>
    <div id="pg-chat-inputrow">
      <button id="pg-chat-mic" title="Grabar mensaje de voz" aria-label="Grabar voz">🎙️</button>
      <textarea id="pg-chat-text" rows="1" maxlength="${MAX_CHARS}" placeholder="${t.placeholder}"></textarea>
      <button id="pg-chat-send" title="${t.send}" aria-label="${t.send}">➤</button>
    </div>
  `;
  document.body.appendChild(btn);
  document.body.appendChild(win);

  const soundBtn = win.querySelector("#pg-chat-sound");
  const closeBtn = win.querySelector("#pg-chat-close");
  const log = win.querySelector("#pg-chat-log");
  const textEl = win.querySelector("#pg-chat-text");
  const counterEl = win.querySelector("#pg-chat-counter");
  const micBtn = win.querySelector("#pg-chat-mic");
  const sendBtn = win.querySelector("#pg-chat-send");

  let history = [];
  let opened = false;
  let voiceOutputEnabled = true;

  soundBtn.addEventListener("click", () => {
    voiceOutputEnabled = !voiceOutputEnabled;
    soundBtn.textContent = voiceOutputEnabled ? "🔊" : "🔇";
    soundBtn.title = voiceOutputEnabled ? "Voz activada" : "Voz desactivada";
    if (!voiceOutputEnabled && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
  });

  function addBubble(text, who) {
    const div = document.createElement("div");
    div.className = "pg-msg " + who;
    div.textContent = text;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
    return div;
  }

  function toggleChatWindow(state) {
    opened = typeof state === "boolean" ? state : !opened;
    win.classList.toggle("open", opened);
    if (opened && history.length === 0) {
      addBubble(t.greeting, "bot");
      if (voiceOutputEnabled) speak(t.greeting);
    }
  }

  btn.addEventListener("click", () => toggleChatWindow());
  closeBtn.addEventListener("click", () => toggleChatWindow(false));

  document.addEventListener("click", (e) => {
    const navBtn = e.target.closest("#pg-chat-nav-btn, .pg-chat-nav-btn");
    if (navBtn) {
      e.preventDefault();
      toggleChatWindow(true);
    }
  });

  textEl.addEventListener("input", () => {
    counterEl.textContent = `${textEl.value.length} / ${MAX_CHARS}`;
  });
  textEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
  });
  sendBtn.addEventListener("click", send);

  async function send() {
    const content = textEl.value.trim();
    if (!content) return;
    if (content.length > MAX_CHARS) { addBubble(t.tooLong, "bot"); return; }

    addBubble(content, "user");
    textEl.value = "";
    counterEl.textContent = `0 / ${MAX_CHARS}`;
    history.push({ role: "user", content });

    const thinking = addBubble("…", "bot");

    try {
      const resp = await fetch(API_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history, locale: pageLang }),
      });
      const data = await resp.json();

      if (!resp.ok) {
        thinking.textContent = data.message || t.error;
        return;
      }

      thinking.textContent = data.reply;
      history.push({ role: "assistant", content: data.reply });
      if (voiceOutputEnabled) speak(data.reply);
    } catch (err) {
      thinking.textContent = t.error;
    }
  }

  // --------------------------------------------------------- Voz Entrada
  const MAX_RECORDING_MS = 60000;

  if (navigator.mediaDevices && window.MediaRecorder) {
    let mediaRecorder = null;
    let audioChunks = [];
    let recording = false;
    let autoStopTimer = null;

    micBtn.addEventListener("click", async () => {
      if (recording) { mediaRecorder.stop(); return; }

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", (e) => audioChunks.push(e.data));
        mediaRecorder.addEventListener("start", () => {
          recording = true;
          micBtn.classList.add("listening");
          micBtn.title = "Grabando... Hacé clic para enviar";
          autoStopTimer = setTimeout(() => mediaRecorder.stop(), MAX_RECORDING_MS);
        });
        mediaRecorder.addEventListener("stop", async () => {
          recording = false;
          micBtn.classList.remove("listening");
          micBtn.title = "Grabar mensaje de voz";
          clearTimeout(autoStopTimer);
          stream.getTracks().forEach((track) => track.stop());

          const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
          await transcribeAndSend(audioBlob);
        });

        mediaRecorder.start();
      } catch (err) {
        addBubble(t.error, "bot");
      }
    });
  } else {
    micBtn.style.display = "none";
  }

  async function transcribeAndSend(audioBlob) {
    const thinking = addBubble("…", "bot");
    try {
      const resp = await fetch(`/api/transcribe?lang=${pageLang.split("-")[0]}`, {
        method: "POST",
        headers: { "Content-Type": "audio/webm" },
        body: audioBlob,
      });
      const data = await resp.json();
      thinking.remove();

      if (!resp.ok || !data.text) {
        addBubble(t.error, "bot");
        return;
      }
      textEl.value = data.text.slice(0, MAX_CHARS);
      counterEl.textContent = `${textEl.value.length} / ${MAX_CHARS}`;
      send();
    } catch (err) {
      thinking.remove();
      addBubble(t.error, "bot");
    }
  }

  // ---------------------------------------------------------- Voz Salida Robustecida
  let availableVoices = [];
  function loadVoices() {
    if ("speechSynthesis" in window) {
      availableVoices = window.speechSynthesis.getVoices();
    }
  }

  if ("speechSynthesis" in window) {
    loadVoices();
    if (speechSynthesis.onvoiceschanged !== undefined) {
      speechSynthesis.onvoiceschanged = loadVoices;
    }
  }

  function speak(text) {
    if (!("speechSynthesis" in window)) return;

    // Limpiar texto para una voz natural (quitar URLs, asteriscos y emojis pesados)
    let cleanText = text
      .replace(/https?:\/\/[^\s]+/g, "en el enlace de la tienda")
      .replace(/[*_#~]/g, "")
      .replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, "")
      .trim();

    if (!cleanText) return;

    window.speechSynthesis.cancel(); // Detener cualquier audio previo

    setTimeout(() => {
      const utter = new SpeechSynthesisUtterance(cleanText);
      utter.lang = speechLang;
      utter.rate = 1.0;
      utter.pitch = 1.0;

      // Buscar mejor voz en el navegador según el idioma
      if (availableVoices.length === 0) availableVoices = window.speechSynthesis.getVoices();
      const targetLang = speechLang.toLowerCase();
      const matchVoice = availableVoices.find(v => v.lang.toLowerCase().replace("_", "-") === targetLang) ||
                         availableVoices.find(v => v.lang.toLowerCase().startsWith(targetLang.split("-")[0]));
      
      if (matchVoice) utter.voice = matchVoice;

      window.speechSynthesis.speak(utter);
    }, 60);
  }
})();
