import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";
import logo from "../../assets/images/Logo_lab_Branco.svg";
import { styles } from "./styled";
import { lightGray, black } from "../../config/colors.js";
import InputLogin from "../../components/InputLogin";

export default function ChangePassword() {
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [errorFields, setErrorFields] = useState({
    oldPassword: "",
    newPassword: "",
    confirmPassword: "",
  });
  const [loading, setLoading] = useState(false);
  const [isFirstAccess, setIsFirstAccess] = useState(false);
  const navigate = useNavigate();

  // Verificar se é primeiro acesso
  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) {
      try {
        const userData = JSON.parse(user);
        setIsFirstAccess(userData.primeiro_acesso === true);
      } catch (e) {
        console.error("Erro ao parsear dados do usuário:", e);
      }
    }
  }, []);

  // --- FUNÇÃO PADRÃO: TROCAR SENHA ---
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setErrorFields({ oldPassword: "", newPassword: "", confirmPassword: "" });

    let hasError = false;
    const newFieldErrors = {
      oldPassword: "",
      newPassword: "",
      confirmPassword: "",
    };

    if (!oldPassword) {
      newFieldErrors.oldPassword = "Digite a senha atual.";
      hasError = true;
    }

    if (!newPassword) {
      newFieldErrors.newPassword = "Digite uma nova senha.";
      hasError = true;
    } else if (newPassword.length < 6) {
      newFieldErrors.newPassword = "A senha deve ter pelo menos 6 caracteres.";
      hasError = true;
    }

    if (!confirmPassword) {
      newFieldErrors.confirmPassword = "Confirme a senha.";
      hasError = true;
    } else if (newPassword !== confirmPassword) {
      newFieldErrors.confirmPassword = "As senhas não coincidem.";
      hasError = true;
    }

    if (hasError) {
      setErrorFields(newFieldErrors);
      return;
    }

    // Chama a função que conecta com a API
    await sendChangePasswordRequest(oldPassword, newPassword);
  };

  // --- FUNÇÃO COMPARTILHADA DE REQUISIÇÃO ---
  const sendChangePasswordRequest = async (currentPass, newPass) => {
    setLoading(true);
    try {
      const token = localStorage.getItem("token");

      if (!token) {
        setError("Sessão expirada. Faça login novamente.");
        setTimeout(() => navigate("/login"), 2000);
        return;
      }

      await api.post(
        "/change-password/",
        {
          old_password: currentPass,
          new_password: newPass,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      setMessage("Senha definida com sucesso! Redirecionando...");

      localStorage.removeItem("token");
      localStorage.removeItem("user");
      localStorage.removeItem("refresh");

      setTimeout(() => {
        navigate("/login");
      }, 2000);
    } catch (err) {
      console.error("Erro ao mudar senha:", err);

      const responseData = err.response?.data;
      let errorMessage = "Erro ao processar. Tente novamente.";

      if (err.response?.status === 400) {
        // Tratamento específico para erro de senha fraca
        if (responseData?.motivos && Array.isArray(responseData.motivos)) {
          // Exibir motivos específicos de rejeição
          const motivos = responseData.motivos.join("\n");
          const requisitos = responseData.requisitos
            ? "\n\nRequisitos de segurança:\n" +
              responseData.requisitos.map((r) => `• ${r}`).join("\n")
            : "";

          errorMessage = responseData.error + "\n" + motivos + requisitos;
        } else {
          errorMessage = responseData?.error || "Erro ao mudar a senha.";
        }

        setError(errorMessage);
      } else if (err.response?.status === 401) {
        setError("Sessão expirada. Faça login novamente.");
        setTimeout(() => navigate("/login"), 2000);
      } else {
        setError(responseData?.error || errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <img
          src={logo}
          alt="Gaia Logo"
          style={{ width: "150px", marginBottom: "20px" }}
        />
        <h2
          style={{
            marginBottom: "16px",
            fontSize: "24px",
            color: black,
            fontFamily: "Poppins, sans-serif",
          }}
        >
          {isFirstAccess ? "Primeiro Acesso" : "Alterar Senha"}
        </h2>

        <p style={{ color: lightGray, marginBottom: "20px", fontSize: "14px" }}>
          {isFirstAccess
            ? "Bem-vindo! Para continuar, você precisa definir uma nova senha de acesso."
            : "Defina uma nova senha para continuar."}
        </p>

        {isFirstAccess && (
          <div style={styles.alertBox}>
            A mudança de senha é <strong>obrigatória</strong> no primeiro
            acesso.
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <InputLogin
            type="password"
            placeholder="Digite sua senha atual"
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
            error={errorFields.oldPassword}
          />

          <InputLogin
            type="password"
            placeholder="Digite uma nova senha"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            disabled={loading}
            error={errorFields.newPassword}
          />

          <InputLogin
            type="password"
            placeholder="Confirme a nova senha"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            disabled={loading}
            error={errorFields.confirmPassword}
          />

          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? "Processando..." : "Salvar Senha"}
          </button>
        </form>

        {message && (
          <p style={{ ...styles.message, ...styles.messageSuccess }}>
            ✓ {message}
          </p>
        )}
        {error && (
          <div
            style={{
              ...styles.message,
              ...styles.messageError,
              whiteSpace: "pre-wrap",
              textAlign: "left",
            }}
          >
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
