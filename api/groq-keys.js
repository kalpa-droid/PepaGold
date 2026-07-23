// /api/groq-keys.js — Manejo y rotación de claves API de Groq

function getKeys() {
  const multi = process.env.GROQ_API_KEYS;
  if (multi) {
    return multi.split(",").map((k) => k.trim()).filter(Boolean);
  }
  if (process.env.GROQ_API_KEY) return [process.env.GROQ_API_KEY];
  return [];
}

let rrIndex = 0;
function nextStartIndex(total) {
  const i = rrIndex % total;
  rrIndex++;
  return i;
}

async function fetchGroqWithRotation(url, buildOptions) {
  const keys = getKeys();
  if (keys.length === 0) {
    throw new Error("No hay ninguna GROQ_API_KEY / GROQ_API_KEYS configurada en Vercel");
  }

  const start = nextStartIndex(keys.length);
  let lastResponse;

  for (let i = 0; i < keys.length; i++) {
    const key = keys[(start + i) % keys.length];
    const resp = await fetch(url, buildOptions(key));

    if (resp.status !== 429 && resp.status !== 401) {
      return resp;
    }
    lastResponse = resp;
  }

  return lastResponse;
}

module.exports = { getKeys, fetchGroqWithRotation };
