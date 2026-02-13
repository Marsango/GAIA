// src/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/", // sua API base
});

// Interceptador: adiciona automaticamente o token em TODAS requisições
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");

    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptador de resposta: redireciona para login se token inválido/expirado
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Se receber 401 (não autorizado), limpa o token e redireciona para login
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
