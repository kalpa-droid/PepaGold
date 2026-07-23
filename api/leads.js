// /api/leads.js — Función Serverless para Gestionar Solicitudes de Registro en Greenway

const fs = require("fs");
const path = require("path");

const LEADS_FILE = path.join(process.cwd(), "admin", "leads.json");

function readLeads() {
  try {
    if (!fs.existsSync(LEADS_FILE)) return [];
    const data = fs.readFileSync(LEADS_FILE, "utf-8");
    return JSON.parse(data || "[]");
  } catch (err) {
    console.error("Error leyendo leads:", err);
    return [];
  }
}

function writeLeads(leads) {
  try {
    fs.writeFileSync(LEADS_FILE, JSON.stringify(leads, null, 2), "utf-8");
    return true;
  } catch (err) {
    console.error("Error escribiendo leads:", err);
    return false;
  }
}

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    res.status(200).end();
    return;
  }

  // GET: Obtener todas las solicitudes
  if (req.method === "GET") {
    const leads = readLeads();
    res.status(200).json(leads);
    return;
  }

  // POST: Crear nueva solicitud de registro
  if (req.method === "POST") {
    const body = req.body || {};
    if (!body.name || !body.phone) {
      res.status(400).json({ error: "Faltan datos obligatorios (nombre o teléfono)" });
      return;
    }

    const leads = readLeads();
    const newLead = {
      id: "lead-" + Date.now(),
      createdAt: new Date().toISOString(),
      name: body.name || "",
      birthdate: body.birthdate || "",
      email: body.email || "",
      phone: body.phone || "",
      address: body.address || "",
      neighborhood: body.neighborhood || "",
      zipCode: body.zipCode || "",
      province: body.province || "",
      country: body.country || "Argentina",
      type: body.type || "Cliente Gratuito (Green Priority)",
      status: "Pendiente",
      notes: body.notes || "Solicitud enviada desde la web"
    };

    leads.unshift(newLead);
    writeLeads(leads);

    res.status(201).json({ success: true, lead: newLead });
    return;
  }

  // PUT: Actualizar estado o datos de una solicitud
  if (req.method === "PUT") {
    const body = req.body || {};
    if (!body.id) {
      res.status(400).json({ error: "Falta el ID del lead" });
      return;
    }

    let leads = readLeads();
    const index = leads.findIndex((l) => l.id === body.id);
    if (index === -1) {
      res.status(404).json({ error: "Lead no encontrado" });
      return;
    }

    leads[index] = { ...leads[index], ...body };
    writeLeads(leads);

    res.status(200).json({ success: true, lead: leads[index] });
    return;
  }

  // DELETE: Eliminar una solicitud
  if (req.method === "DELETE") {
    const { id } = req.query || req.body || {};
    if (!id) {
      res.status(400).json({ error: "Falta el ID del lead" });
      return;
    }

    let leads = readLeads();
    leads = leads.filter((l) => l.id !== id);
    writeLeads(leads);

    res.status(200).json({ success: true });
    return;
  }

  res.status(405).json({ error: "Método no permitido" });
};
