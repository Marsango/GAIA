import axios from "axios";

const API_URL = "http://localhost:8000/api"; // URL base do seu backend

export async function login(cpf, password) {
  try {
    const response = await axios.post(`${API_URL}/auth/login/cpf/`, {
      cpf,
      password,
    });
    console.log("Usuário logado:", response.data);
    return response.data; // Retorna os dados do usuário
  } catch (error) {
    console.error("Erro no login:", error.response?.data || error.message);
    throw error;
  }
}

// Função para refresh token (opcional)
export async function refreshToken(refresh) {
  try {
    const response = await axios.post(`${API_URL}/token/refresh/`, {
      refresh
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao refresh token:", error);
    throw error;
  }
}

export async function getCurrentUser(token) {
  try {
    const response = await axios.get(`${API_URL}/auth/user-info/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    console.error("Erro ao buscar dados do usuário:", error);
    throw error;
  }
}