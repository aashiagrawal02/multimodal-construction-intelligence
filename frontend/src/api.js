import axios from "axios";

const client = axios.create({ baseURL: import.meta.env.VITE_API_URL || "" });

export const getHealth = () => client.get("/api/health").then((r) => r.data);

export const analyzeImage = (file) => {
  const form = new FormData();
  form.append("file", file);
  return client.post("/api/analyze-image", form).then((r) => r.data);
};

export const estimateProject = (payload) =>
  client.post("/api/estimate", payload).then((r) => r.data);

export const askAssistant = (question, context) =>
  client.post("/api/assistant", { question, context }).then((r) => r.data);

export const visualize = (payload) =>
  client.post("/api/visualize", payload).then((r) => r.data);

export const errorMessage = (err) =>
  err?.response?.data?.detail || err?.message || "Something went wrong";
