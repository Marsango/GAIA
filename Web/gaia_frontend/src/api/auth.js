import axios from "axios";

const API_URL = "http://localhost:8000/api"; // URL base do seu backend

export async function login(cpf, password) {
  try {
    const response = await axios.post(`${API_URL}/login/`, {
      cpf,
      password,
    });
    console.log("Usuário logado:", response.data);
    return response.data; // Retorna os dados do usuário
  } catch (error) {
    console.error("Erro no login:", error.response?.data || error.message);
    throw error;
  }


    //   // Se o backend retornar um token, salve no localStorage
    //   if (response.data.token) {
    //     localStorage.setItem("token", response.data.token);
    //   }

    // } catch (error) {
    //   console.error("Erro no login:", error.response?.data || error.message);
    //   throw error;
}
