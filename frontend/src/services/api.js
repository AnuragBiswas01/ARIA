/**
 * ARIA API Service
 * Axios client for backend communication.
 */
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});

// --- Chat ---
export const sendMessage = async (
  message,
  sessionId = null,
  stream = false,
) => {
  const response = await api.post("/chat", {
    message,
    session_id: sessionId,
    stream,
  });
  return response.data;
};

// --- System ---
export const getSystemStatus = async () => {
  const response = await api.get("/system/status");
  return response.data;
};

export const getSystemHealth = async () => {
  const response = await api.get("/system/health");
  return response.data;
};

export const getSystemLogs = async (lines = 100) => {
  const response = await api.get("/system/logs", { params: { lines } });
  return response.data;
};

// --- Devices ---
export const getDevices = async () => {
  const response = await api.get("/devices/list");
  return response.data;
};

export const controlDevice = async (entityId, action, value = null) => {
  const response = await api.post("/devices/action", {
    entity_id: entityId,
    action,
    value,
  });
  return response.data;
};

// --- Events ---
export const getRecentEvents = async (limit = 20) => {
  const response = await api.get("/events/recent", { params: { limit } });
  return response.data;
};

export const logEvent = async (eventType, source = null, data = null) => {
  const response = await api.post("/events", {
    event_type: eventType,
    source,
    data,
  });
  return response.data;
};

// --- Memory ---
export const searchMemory = async (
  query,
  collection = "conversations",
  nResults = 5,
) => {
  const response = await api.post("/memory/search", {
    query,
    collection,
    n_results: nResults,
  });
  return response.data;
};

export const getMemoryStats = async () => {
  const response = await api.get("/memory/stats");
  return response.data;
};

export const clearWorkingMemory = async () => {
  const response = await api.post("/memory/clear-working");
  return response.data;
};

// --- Context ---
export const getHomeState = async () => {
  const response = await api.get("/context/home-state");
  return response.data;
};

export const getWorkingMemory = async () => {
  const response = await api.get("/context/working-memory");
  return response.data;
};

export default api;
