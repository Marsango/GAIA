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

export default api;
