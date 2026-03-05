import { useState, useEffect } from 'react';

// Função auxiliar para pegar usuário do localStorage sem erros
const getStoredUser = () => {
  try {
    const userRaw = localStorage.getItem("user");
    // Verifica se não é null, undefined ou string "undefined"
    if (userRaw && userRaw !== "undefined") {
      return JSON.parse(userRaw);
    }
  } catch (error) {
    console.error("Erro ao ler usuário do localStorage:", error);
  }
  return null;
};

// Hook customizado
export function useAuth() {
  // Estado para armazenar o usuário
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Carrega o usuário quando o componente monta
  useEffect(() => {
    const storedUser = getStoredUser();
    setUser(storedUser);
    setLoading(false);
  }, []);

  // Função de login
  const login = (userData) => {
    // ✅ NOVO: Tokens são armazenados em httpOnly cookies pelo servidor
    // Apenas armazenar dados do usuário
    localStorage.setItem("user", JSON.stringify(userData));
    setUser(userData);
  };

  // Função de logout
  const logout = () => {
    // ✅ NOVO: Cookies são removidos pelo endpoint /logout do servidor
    localStorage.removeItem("user");
    setUser(null);
  };

  // Verifica se está autenticado
  const isAuthenticated = !!user;

  return {
    user,
    login,
    logout,
    isAuthenticated,
    loading
  };
}