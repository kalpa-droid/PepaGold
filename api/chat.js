// /api/chat.js — Función Serverless de Vercel para el Chat de PepaGold

const fs = require("fs");
const path = require("path");

const GROQ_URL = "https://api.groq.com/openai/v1/chat/completions";
const MODEL = "llama-3.3-70b-versatile";

const { SYSTEM_PROMPT } = require("./context.js");
const { fetchGroqWithRotation } = require("./groq-keys.js");

const MAX_HISTORY_MESSAGES = 10;
const LEADS_FILE = path.join(process.cwd(), "admin", "leads.json");

function autoSaveLeadFromChat(messages) {
  try {
    const userMsgs = messages.filter((m) => m.role === "user").map((m) => m.content);
    if (userMsgs.length === 0) return;

    const fullText = userMsgs.join("\n");
    const hasPhone = /(?:\+?\d{1,3})?[\s.-]?\(?\d{2,5}\)?[\s.-]?\d{3,5}[\s.-]?\d{3,5}/.test(fullText);
    const hasRegKeyword = /(registr|darse de alta|alta|quiero la cuenta|comprar|inscripci|datos)/i.test(fullText);

    if (!hasPhone && !hasRegKeyword) return;

    // Extraer datos aproximados
    const emailMatch = fullText.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/);
    const phoneMatch = fullText.match(/(?:\+?\d{1,3})?[\s.-]?\(?\d{2,5}\)?[\s.-]?\d{3,5}[\s.-]?\d{3,5}/);
    const nameMatch = fullText.match(/(?:me llamo|soy|nombre es)\s+([A-ZÁÉÍÓÚÑa-záéíóúñ\s]+)/i);

    let leads = [];
    if (fs.existsSync(LEADS_FILE)) {
      leads = JSON.parse(fs.readFileSync(LEADS_FILE, "utf-8") || "[]");
    }

    const lastMsg = userMsgs[userMsgs.length - 1];

    // Evitar duplicados recientes
    const isDuplicate = leads.some((l) => l.notes && l.notes.includes(lastMsg.slice(0, 30)));
    if (isDuplicate) return;

    const newLead = {
      id: "lead-" + Date.now(),
      createdAt: new Date().toISOString(),
      name: nameMatch ? nameMatch[1].trim() : "Cliente interesado en Chat",
      birthdate: "",
      email: emailMatch ? emailMatch[0] : "",
      phone: phoneMatch ? phoneMatch[0].trim() : "",
      address: "",
      neighborhood: "",
      zipCode: "",
      province: "",
      country: "Argentina",
      type: "Cliente Gratuito (Green Priority)",
      status: "Pendiente",
      notes: "Capturado automáticamente desde el Chat: " + fullText.slice(-300)
    };

    leads.unshift(newLead);
    fs.writeFileSync(LEADS_FILE, JSON.stringify(leads, null, 2), "utf-8");
  } catch (err) {
    console.error("Error al guardar lead automáticamente desde chat:", err);
  }
}

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.status(405).json({ error: "Método no permitido" });
    return;
  }

  const { messages, locale } = req.body || {};

  if (!Array.isArray(messages) || messages.length === 0) {
    res.status(400).json({ error: "Falta 'messages'" });
    return;
  }

  const MAX_INPUT_CHARS = 6000;
  const lastUserMsg = [...messages].reverse().find((m) => m.role === "user");
  if (lastUserMsg && lastUserMsg.content.length > MAX_INPUT_CHARS) {
    res.status(400).json({
      error: "too_long",
      message:
        locale === "en-us"
          ? "Your message is too long. Please shorten it and try again."
          : "Tu mensaje es demasiado largo. Achicalo un poco e intentá de nuevo.",
    });
    return;
  }

  // Intentar guardar lead si hay datos de registro
  autoSaveLeadFromChat(messages);

  const trimmedHistory = messages.slice(-MAX_HISTORY_MESSAGES);
  const fullMessages = [{ role: "system", content: SYSTEM_PROMPT }, ...trimmedHistory];

  try {
    const answer = await askGroqWithContinuation(fullMessages);
    res.status(200).json({ reply: answer });
  } catch (err) {
    console.error("Error Groq:", err);
    res.status(502).json({ error: "groq_error", message: String(err.message || err) });
  }
};

async function askGroqWithContinuation(fullMessages, maxRounds = 3) {
  let accumulated = "";
  let working = [...fullMessages];

  for (let round = 0; round < maxRounds; round++) {
    const resp = await fetchGroqWithRotation(GROQ_URL, (key) => ({
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${key}`,
      },
      body: JSON.stringify({
        model: MODEL,
        messages: working,
        max_tokens: 1000,
        temperature: 0.5,
      }),
    }));

    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(`Groq ${resp.status}: ${text}`);
    }

    const data = await resp.json();
    const choice = data.choices[0];
    const piece = choice.message.content || "";
    accumulated += piece;

    if (choice.finish_reason !== "length") {
      break;
    }

    working = [
      ...working,
      { role: "assistant", content: piece },
      { role: "user", content: "Continuá exactamente donde te quedaste, sin repetir nada." },
    ];
  }

  return accumulated;
}
