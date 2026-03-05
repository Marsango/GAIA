// src/api.js
// Configuração axios com suporte a JWT via httpOnly Cookies
// SEGURANÇA: httpOnly Cookies previnem XSS (inacessíveis via JavaScript)
// O navegador automaticamente envia cookies com cada requisição
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/",
  withCredentials: true,  // ✅ Envia cookies automaticamente (httpOnly)
});

// ============================================================
// INTERCEPTADOR: Response - Trata erros de autenticação
// ============================================================

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Se receber 401 (token expirado), tentar refresh automático
    if (error.response?.status === 401) {
      const originalRequest = error.config;
      
      if (!originalRequest._retry) {
        originalRequest._retry = true;
        
        try {
          console.log('[API] 🔄 Token expirado, tentando refresh...');
          
          // Backend vai renovar o refresh_token cookie e retornar novo access_token
          await axios.post(
            'http://localhost:8000/api/token/refresh-cookie/',
            {},
            { withCredentials: true }
          );
          
          // Retry request original com novo token
          console.log('[API] ✅ Token renovado, retentando requisição...');
          return api(originalRequest);
        } catch (refreshError) {
          // Se refresh falhar, fazer logout
          console.error('[API] ❌ Refresh falhou - fazendo logout');
          localStorage.removeItem("user");
          window.location.href = "/login";
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

export default api;
