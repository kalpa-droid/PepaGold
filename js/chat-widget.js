/*
  Widget de Chat Inteligente PepaGold — Asistente Pepa
  - Bienvenida de Pepa única (sin duplicar 3 veces al abrir).
  - El botón Enviar (flecha ➤) envía el texto escrito y si estás grabando audio también detiene y envía el audio inmediatamente.
  - Avatar de Pepa con animación de habla al leer respuestas por voz.
  - Botón de micrófono con estado VERDE LATIENDO (escuchando) y ROJO QUIETO (cortado/enviando).
  - Botón de micrófono y botón de enviar uno al lado del otro.
  - Íconos planos y simbólicos.
  - Traducción 100% multilingüe en los 10 locales.
*/
(function () {
  "use strict";

  const API_ENDPOINT = "/api/chat";
  const MAX_CHARS = 1500;
  const REFERRAL_LINK = "https://greenwayglobal.ar/shop/brands/fiber/08093?gw=uZv7Gi0Ep5";

  const LANG_MAP = {
    "es-ar": "es-AR", "es-mx": "es-MX", "es-es": "es-ES", "en-us": "en-US",
    "fr-fr": "fr-FR", "de-de": "de-DE", "it-it": "it-IT", "pt-br": "pt-BR",
    "ru-ru": "ru-RU", "zh-hans": "zh-CN"
  };

  const STRINGS = {
    "es-ar": {
      title: "Pepa · ¿Tenés dudas?", placeholder: "Escribí tu pregunta…", send: "Enviar",
      greeting: "¡Hola! 👋 Soy Pepa. Puedo ayudarte a comprar, a registrarte en la plataforma de Greenway y a descubrir nuestros productos ecológicos. Si vas a Greenway, ¡allí en el icono del teléfono te atenderá mi hermana asistente! ¿En qué te ayudo hoy? 😊",
      navBtn: "Chat", tooLong: "Achicá un poco el mensaje, por favor.", error: "Algo falló. Intentá de nuevo en un momento.",
      close: "Cerrar", soundOn: "Voz activada", soundOff: "Voz desactivada", micTitle: "Grabar mensaje de voz",
      micRecording: "Escuchando... Toca de nuevo o la flecha para enviar", micStopping: "Enviando mensaje...", sendTitle: "Enviar mensaje"
    },
    "es-mx": {
      title: "Pepa · ¿Tienes dudas?", placeholder: "Escribe tu pregunta…", send: "Enviar",
      greeting: "¡Hola! 👋 Soy Pepa. Puedo ayudarte a comprar, a registrarte en la plataforma de Greenway y a descubrir nuestros productos ecológicos. Si vas a Greenway, ¡allí en el icono del teléfono te atenderá mi hermana asistente! ¿En qué te ayudo hoy? 😊",
      navBtn: "Chat", tooLong: "Acorta un poco tu mensaje, por favor.", error: "Algo falló. Intenta de nuevo en un momento.",
      close: "Cerrar", soundOn: "Voz activada", soundOff: "Voz desactivada", micTitle: "Grabar mensaje de voz",
      micRecording: "Escuchando... Toca de nuevo o la flecha para enviar", micStopping: "Enviando mensaje...", sendTitle: "Enviar mensaje"
    },
    "es-es": {
      title: "Pepa · ¿Tienes dudas?", placeholder: "Escribe tu pregunta…", send: "Enviar",
      greeting: "¡Hola! 👋 Soy Pepa. Puedo ayudarte a comprar, a registrarte en la plataforma de Greenway y a descubrir nuestros productos ecológicos. Si vas a Greenway, ¡allí en el icono del teléfono te atenderá mi hermana asistente! ¿En qué te ayudo hoy? 😊",
      navBtn: "Chat", tooLong: "Acorta un poco tu mensaje, por favor.", error: "Algo falló. Intenta de nuevo en un momento.",
      close: "Cerrar", soundOn: "Voz activada", soundOff: "Voz desactivada", micTitle: "Grabar mensaje de voz",
      micRecording: "Escuchando... Toca de nuevo o la flecha para enviar", micStopping: "Enviando mensaje...", sendTitle: "Enviar mensaje"
    },
    "en-us": {
      title: "Pepa · Questions?", placeholder: "Type your question…", send: "Send",
      greeting: "Hi! 👋 I'm Pepa. I can help you buy, register on the Greenway platform, and discover our eco-friendly products. If you go to Greenway, my sister assistant will help you there at the phone icon! How can I help you today? 😊",
      navBtn: "Chat", tooLong: "Please shorten your message.", error: "Something went wrong. Please try again.",
      close: "Close", soundOn: "Voice enabled", soundOff: "Voice disabled", micTitle: "Record voice message",
      micRecording: "Listening... Tap again or arrow to send", micStopping: "Sending message...", sendTitle: "Send message"
    },
    "fr-fr": {
      title: "Pepa · Des questions ?", placeholder: "Posez votre question…", send: "Envoyer",
      greeting: "Bonjour ! 👋 Je suis Pepa. Je peux vous aider à acheter, à vous inscrire sur Greenway et à découvrir nos produits. Sur Greenway, ma sœur assistante vous accueillera sur l'icône du téléphone ! 😊",
      navBtn: "Chat", tooLong: "Veuillez raccourcir votre message.", error: "Une erreur est survenue. Veuillez réessayer.",
      close: "Fermer", soundOn: "Voix activée", soundOff: "Voix désactivée", micTitle: "Enregistrer un message vocal",
      micRecording: "Écoute en cours... Appuyez sur la flèche pour envoyer", micStopping: "Envoi en cours...", sendTitle: "Envoyer le message"
    },
    "de-de": {
      title: "Pepa · Fragen?", placeholder: "Stellen Sie Ihre Frage…", send: "Senden",
      greeting: "Hallo! 👋 Ich bin Pepa. Ich kann Ihnen beim Kauf, der Registrierung bei Greenway und dem Entdecken aller Produkte helfen. Bei Greenway hilft Ihnen meine Assistenten-Schwester am Telefon-Icon! 😊",
      navBtn: "Chat", tooLong: "Bitte kürzen Sie Ihre Nachricht.", error: "Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.",
      close: "Schließen", soundOn: "Sprache aktiv", soundOff: "Sprache deaktiviert", micTitle: "Sprachnachricht aufnehmen",
      micRecording: "Hört zu... Pfeil zum Senden tippen", micStopping: "Senden...", sendTitle: "Nachricht senden"
    },
    "it-it": {
      title: "Pepa · Domande?", placeholder: "Scrivi la tua domanda…", send: "Invia",
      greeting: "Ciao! 👋 Sono Pepa. Posso aiutarti ad acquistare, registrarti su Greenway e scoprire tutti i nostri prodotti. Sulla piattaforma Greenway troverai mia sorella assistente all'icona del telefono! 😊",
      navBtn: "Chat", tooLong: "Per favore accorcia il tuo messaggio.", error: "Si è verificato un errore. Riprova tra poco.",
      close: "Chiudi", soundOn: "Voce attiva", soundOff: "Voce disattivata", micTitle: "Registra messaggio vocale",
      micRecording: "Ascolto... Tocca la freccia per inviare", micStopping: "Invio in corso...", sendTitle: "Invia messaggio"
    },
    "pt-br": {
      title: "Pepa · Dúvidas?", placeholder: "Digite sua pergunta…", send: "Enviar",
      greeting: "Olá! 👋 Sou a Pepa. Posso ajudar você a comprar, se cadastrar na Greenway e conhecer nossos produtos. Na plataforma da Greenway, minha irmã assistente vai te atender no ícone do telefone! 😊",
      navBtn: "Chat", tooLong: "Por favor encurte sua mensagem.", error: "Ocorreu um erro. Tente novamente em instantes.",
      close: "Fechar", soundOn: "Voz ativada", soundOff: "Voz desativada", micTitle: "Gravar mensagem de voz",
      micRecording: "Ouvindo... Toque na seta para enviar", micStopping: "Enviando mensagem...", sendTitle: "Enviar mensagem"
    },
    "ru-ru": {
      title: "Пепа · Есть вопросы?", placeholder: "Напишите ваш вопрос…", send: "Отправить",
      greeting: "Привет! 👋 Я Пепа. Помогу оформить покупку, зарегистрироваться на Greenway и узнать обо всех эко-товарах. На платформе Greenway на иконке телефона вас встретит моя сестра-ассистент! 😊",
      navBtn: "Чат", tooLong: "Пожалуйста, сократите сообщение.", error: "Произошла ошибка. Попробуйте еще раз.",
      close: "Закрыть", soundOn: "Голос включен", soundOff: "Голос выключен", micTitle: "Записать голосовое сообщение",
      micRecording: "Слушаю... Нажмите стрелку для отправки", micStopping: "Отправка...", sendTitle: "Отправить сообщение"
    },
    "zh-hans": {
      title: "Pepa · 有疑问吗？", placeholder: "请输入您的问题…", send: "发送",
      greeting: "您好！👋 我是 Pepa。我可以帮您购买商品、在 Greenway 平台注册并了解所有环保产品。去 Greenway 平台时，我的姐妹助手会在电话图标处为您服务！😊",
      navBtn: "聊天", tooLong: "请缩短您的消息。", error: "出错了，请稍后再试。",
      close: "关闭", soundOn: "语音已开启", soundOff: "语音已关闭", micTitle: "录制语音消息",
      micRecording: "正在聆听... 点击箭头发送", micStopping: "发送中...", sendTitle: "发送消息"
    }
  };

  function detectPageLocale() {
    const path = window.location.pathname.toLowerCase();
    if (path.startsWith("/mx/") || path.includes("/es-mx/")) return "es-mx";
    if (path.startsWith("/es/") || path.includes("/es-es/")) return "es-es";
    if (path.startsWith("/us/") || path.startsWith("/en/") || path.includes("/en-us/")) return "en-us";
    if (path.startsWith("/fr/") || path.includes("/fr-fr/")) return "fr-fr";
    if (path.startsWith("/de/") || path.includes("/de-de/")) return "de-de";
    if (path.startsWith("/it/") || path.includes("/it-it/")) return "it-it";
    if (path.startsWith("/pt/") || path.includes("/pt-br/")) return "pt-br";
    if (path.startsWith("/ru/") || path.includes("/ru-ru/")) return "ru-ru";
    if (path.startsWith("/zh/") || path.includes("/zh-hans/")) return "zh-hans";

    const docLang = (document.documentElement.lang || "").toLowerCase();
    if (STRINGS[docLang]) return docLang;
    if (docLang.startsWith("es")) return "es-ar";

    return "es-ar";
  }

  const pageLang = detectPageLocale();
  const speechLang = LANG_MAP[pageLang] || "es-AR";
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
    #pg-chat-head { background: linear-gradient(135deg, #111827 0%, #1f2937 100%); color: #f3f4f6; padding: 14px 16px; font-weight: 600; font-size: 14px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #c9a24b; }
    #pg-chat-head .head-left { display: flex; align-items: center; gap: 8px; }
    #pg-chat-head .head-right { display: flex; align-items: center; gap: 10px; }
    
    /* Avatar Animado de Pepa */
    .pepa-avatar { font-size: 20px; transition: transform 0.2s ease; display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 50%; background: rgba(201,162,75,0.2); border: 1px solid #c9a24b; }
    .pepa-avatar.speaking { animation: pepaTalk 0.4s infinite alternate cubic-bezier(0.45, 0.05, 0.55, 0.95); background: rgba(201,162,75,0.4); border-color: #ffd700; }
    @keyframes pepaTalk {
      0% { transform: scale(1) translateY(0); }
      50% { transform: scale(1.22) translateY(-2px) rotate(-4deg); }
      100% { transform: scale(1.1) translateY(1px) rotate(4deg); }
    }

    #pg-chat-sound, #pg-chat-close { background: none; border: none; color: #d1d5db; font-size: 18px; cursor: pointer; padding: 2px 4px; transition: color 0.15s, transform 0.15s; }
    #pg-chat-sound:hover, #pg-chat-close:hover { color: #ffffff; transform: scale(1.1); }
    #pg-chat-log { flex: 1; overflow-y: auto; padding: 14px; font-size: 14px; background: #f9fafb; display: flex; flex-direction: column; gap: 10px; }
    .pg-msg { padding: 10px 14px; border-radius: 14px; max-width: 85%; line-height: 1.45; font-size: 13.5px; word-wrap: break-word; }
    .pg-msg.user { background: linear-gradient(135deg, #c9a24b 0%, #b38b34 100%); color: #ffffff; margin-left: auto; border-bottom-right-radius: 2px; box-shadow: 0 2px 8px rgba(201,162,75,0.25); }
    .pg-msg.bot { background: #ffffff; color: #1f2937; border: 1px solid #e5e7eb; border-bottom-left-radius: 2px; box-shadow: 0 2px 6px rgba(0,0,0,0.04); }
    .pg-msg a { color: #2563eb !important; font-weight: 600; text-decoration: underline; transition: opacity 0.15s; }
    .pg-msg a:hover { opacity: 0.8; }
    #pg-chat-inputrow { display: flex; align-items: center; border-top: 1px solid #f3f4f6; padding: 10px; gap: 8px; background: #ffffff; }
    #pg-chat-text { flex: 1; border: 1px solid #e5e7eb; border-radius: 10px; padding: 9px 12px; font-size: 13.5px; resize: none; outline: none; transition: border-color 0.15s; font-family: inherit; }
    #pg-chat-text:focus { border-color: #c9a24b; box-shadow: 0 0 0 3px rgba(201,162,75,0.15); }
    
    /* Botones de Entrada Planos Uno al Lado del Otro */
    .pg-btn-group { display: flex; gap: 6px; align-items: center; }
    
    #pg-chat-mic { border: 1px solid #c9a24b; background: #111827; color: #ffffff; width: 38px; height: 38px; border-radius: 10px; font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.15); }
    #pg-chat-mic:hover { background: #1f2937; color: #ffffff; transform: translateY(-1px); border-color: #e5c158; }
    
    /* Estado VERDE LATIENDO (Escuchando) */
    #pg-chat-mic.listening { background: #22c55e !important; color: #ffffff !important; border-color: #16a34a !important; box-shadow: 0 0 14px rgba(34,197,94,0.8); animation: pgGreenPulse 0.9s infinite alternate cubic-bezier(0.4, 0, 0.2, 1); }
    @keyframes pgGreenPulse { 0% { transform: scale(1); box-shadow: 0 0 6px rgba(34,197,94,0.5); } 100% { transform: scale(1.12); box-shadow: 0 0 16px rgba(34,197,94,0.95); } }

    /* Estado ROJO QUIETO (Cortado/Enviando) */
    #pg-chat-mic.stopping { background: #dc2626 !important; color: #ffffff !important; border-color: #991b1b !important; animation: none !important; transform: scale(1) !important; box-shadow: 0 2px 6px rgba(220,38,38,0.4) !important; }

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
        <div id="pepa-avatar" class="pepa-avatar" title="Pepa">😊</div>
        <span>${t.title}</span>
      </div>
      <div class="head-right">
        <button id="pg-chat-sound" title="${t.soundOn}" aria-label="${t.soundOn}">🔊</button>
        <button id="pg-chat-close" title="${t.close}" aria-label="${t.close}">✕</button>
      </div>
    </div>
    <div id="pg-chat-log"></div>
    <div id="pg-chat-counter">0 / ${MAX_CHARS}</div>
    <div id="pg-chat-inputrow">
      <textarea id="pg-chat-text" rows="1" maxlength="${MAX_CHARS}" placeholder="${t.placeholder}"></textarea>
      <div class="pg-btn-group">
        <button id="pg-chat-mic" title="${t.micTitle}" aria-label="Micrófono">📞</button>
        <button id="pg-chat-send" title="${t.sendTitle}" aria-label="Enviar">➤</button>
      </div>
    </div>
  `;
  document.body.appendChild(btn);
  document.body.appendChild(win);

  const pepaAvatar = win.querySelector("#pepa-avatar");
  const soundBtn = win.querySelector("#pg-chat-sound");
  const closeBtn = win.querySelector("#pg-chat-close");
  const log = win.querySelector("#pg-chat-log");
  const textEl = win.querySelector("#pg-chat-text");
  const counterEl = win.querySelector("#pg-chat-counter");
  const micBtn = win.querySelector("#pg-chat-mic");
  const sendBtn = win.querySelector("#pg-chat-send");

  let history = [];
  let opened = false;
  let hasWelcomed = false;
  let voiceOutputEnabled = true;

  // Variables globales de Grabación de Audio
  let mediaRecorder = null;
  let audioChunks = [];
  let recording = false;
  let autoStopTimer = null;

  soundBtn.addEventListener("click", () => {
    voiceOutputEnabled = !voiceOutputEnabled;
    soundBtn.textContent = voiceOutputEnabled ? "🔊" : "🔇";
    soundBtn.title = voiceOutputEnabled ? t.soundOn : t.soundOff;
    if (!voiceOutputEnabled && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
      setAvatarSpeaking(false);
    }
  });

  function setAvatarSpeaking(state) {
    if (!pepaAvatar) return;
    if (state) {
      pepaAvatar.classList.add("speaking");
      pepaAvatar.textContent = "🗣️";
    } else {
      pepaAvatar.classList.remove("speaking");
      pepaAvatar.textContent = "😊";
    }
  }

  function formatMessageHtml(text) {
    let escaped = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // Reemplazar Markdown [Texto](https://...) -> <a href="..." target="_blank">Texto</a>
    escaped = escaped.replace(/\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)/g, (match, anchor, url) => {
      return `<a href="${url}" target="_blank" rel="noopener noreferrer">${anchor}</a>`;
    });

    // Reemplazar URLs sueltas de Greenway Global -> <a href="..." target="_blank">Greenway Global</a>
    escaped = escaped.replace(/(^|[^"])https?:\/\/greenwayglobal\.ar\/[^\s<]+/g, (match, prefix) => {
      return `${prefix}<a href="${REFERRAL_LINK}" target="_blank" rel="noopener noreferrer">Greenway Global</a>`;
    });

    return escaped.replace(/\n/g, "<br>");
  }

  function addBubble(text, who) {
    const div = document.createElement("div");
    div.className = "pg-msg " + who;
    div.innerHTML = formatMessageHtml(text);
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
    return div;
  }

  function toggleChatWindow(state) {
    opened = typeof state === "boolean" ? state : !opened;
    win.classList.toggle("open", opened);
    if (opened && !hasWelcomed) {
      hasWelcomed = true;
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
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSendAction(); }
  });

  sendBtn.addEventListener("click", handleSendAction);

  function handleSendAction() {
    // Si se está grabando audio y se presiona la flecha, detiene y envía el audio inmediatamente
    if (recording && mediaRecorder) {
      stopRecordingAndSend();
      return;
    }
    send();
  }

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
        thinking.innerHTML = formatMessageHtml(data.message || t.error);
        return;
      }

      thinking.innerHTML = formatMessageHtml(data.reply);
      history.push({ role: "assistant", content: data.reply });
      if (voiceOutputEnabled) speak(data.reply);
    } catch (err) {
      thinking.innerHTML = formatMessageHtml(t.error);
    }
  }

  // --------------------------------------------------------- Voz Entrada (Verde Latiendo / Rojo Cortado)
  const MAX_RECORDING_MS = 60000;

  function stopRecordingAndSend() {
    if (!recording || !mediaRecorder) return;
    micBtn.classList.remove("listening");
    micBtn.classList.add("stopping");
    micBtn.textContent = "🛑";
    micBtn.title = t.micStopping;
    mediaRecorder.stop();
  }

  if (navigator.mediaDevices && window.MediaRecorder) {
    micBtn.addEventListener("click", async () => {
      if (recording) {
        stopRecordingAndSend();
        return;
      }

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", (e) => audioChunks.push(e.data));
        mediaRecorder.addEventListener("start", () => {
          recording = true;
          micBtn.classList.remove("stopping");
          micBtn.classList.add("listening");
          micBtn.textContent = "📞";
          micBtn.title = t.micRecording;
          autoStopTimer = setTimeout(() => {
            if (recording) stopRecordingAndSend();
          }, MAX_RECORDING_MS);
        });
        mediaRecorder.addEventListener("stop", async () => {
          recording = false;
          micBtn.classList.remove("listening");
          micBtn.classList.add("stopping");
          micBtn.textContent = "🛑";
          micBtn.title = t.micStopping;
          clearTimeout(autoStopTimer);
          stream.getTracks().forEach((track) => track.stop());

          const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
          await transcribeAndSend(audioBlob);

          // Volver a estado normal reposado
          micBtn.classList.remove("stopping");
          micBtn.textContent = "📞";
          micBtn.title = t.micTitle;
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

  // ---------------------------------------------------------- Voz Salida con Avatar Hablando
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

    let cleanText = text
      .replace(/\[([^\]]+)\]\(https?:\/\/[^\s\)]+\)/g, "$1")
      .replace(/https?:\/\/greenwayglobal\.ar[^\s]*/g, "Greenway Global")
      .replace(/https?:\/\/[^\s]+/g, "en la tienda")
      .replace(/[*_#~]/g, "")
      .replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, "")
      .trim();

    if (!cleanText) return;

    window.speechSynthesis.cancel();
    setAvatarSpeaking(false);

    setTimeout(() => {
      const utter = new SpeechSynthesisUtterance(cleanText);
      utter.lang = speechLang;
      utter.rate = 1.0;
      utter.pitch = 1.0;

      if (availableVoices.length === 0) availableVoices = window.speechSynthesis.getVoices();
      const targetLang = speechLang.toLowerCase();
      const matchVoice = availableVoices.find(v => v.lang.toLowerCase().replace("_", "-") === targetLang) ||
                         availableVoices.find(v => v.lang.toLowerCase().startsWith(targetLang.split("-")[0]));
      
      if (matchVoice) utter.voice = matchVoice;

      utter.onstart = () => setAvatarSpeaking(true);
      utter.onend = () => setAvatarSpeaking(false);
      utter.onerror = () => setAvatarSpeaking(false);

      window.speechSynthesis.speak(utter);
    }, 60);
  }
})();
