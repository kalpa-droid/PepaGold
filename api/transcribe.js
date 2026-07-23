// /api/transcribe.js — Función Serverless de Vercel para Transcripción de Voz

const GROQ_TRANSCRIBE_URL = "https://api.groq.com/openai/v1/audio/transcriptions";
const { fetchGroqWithRotation } = require("./groq-keys.js");

module.exports.config = { api: { bodyParser: false } };

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.status(405).json({ error: "Método no permitido" });
    return;
  }

  const MAX_AUDIO_BYTES = 20 * 1024 * 1024;
  const chunks = [];
  let totalBytes = 0;
  let tooLarge = false;

  for await (const chunk of req) {
    totalBytes += chunk.length;
    if (totalBytes > MAX_AUDIO_BYTES) { tooLarge = true; break; }
    chunks.push(chunk);
  }

  if (tooLarge) {
    res.status(400).json({ error: "audio_too_large", message: "El audio es demasiado largo." });
    return;
  }

  const audioBuffer = Buffer.concat(chunks);
  if (audioBuffer.length === 0) {
    res.status(400).json({ error: "empty_audio", message: "No se recibió audio." });
    return;
  }

  try {
    const form = new FormData();
    form.append("file", new Blob([audioBuffer], { type: "audio/webm" }), "audio.webm");
    form.append("model", "whisper-large-v3-turbo");

    const resp = await fetchGroqWithRotation(GROQ_TRANSCRIBE_URL, (key) => ({
      method: "POST",
      headers: { Authorization: `Bearer ${key}` },
      body: form,
    }));

    if (!resp.ok) {
      const text = await resp.text();
      throw new Error(`Groq ${resp.status}: ${text}`);
    }

    const data = await resp.json();
    res.status(200).json({ text: data.text || "" });
  } catch (err) {
    console.error("Error transcribiendo:", err);
    res.status(502).json({ error: "transcribe_error", message: String(err.message || err) });
  }
};
