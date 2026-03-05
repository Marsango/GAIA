import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api"; // ✅ API com interceptors e auto-refresh
import logo from "../../assets/images/Logo_lab_Branco.svg";
import { styles } from "./styled";
import InputLogin from "../../components/InputLogin";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleReset = async (e) => {
    if (e) {
      e.preventDefault();
    }
    setLoading(true);
    setMessage("");

    const trimmedEmail = email.trim();
    if (!trimmedEmail) {
      setMessage("Informe um e-mail valido.");
      setLoading(false);
      return;
    }

    try {
      // Chama a rota do Django que criamos
      await api.post("/forgot-password/", { email: trimmedEmail });
      setMessage(
        "Se o e-mail estiver cadastrado, uma nova senha foi enviada para ele.",
      );
    } catch (error) {
      setMessage("Erro ao tentar conectar com o servidor.");
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
        <h2 style={{ marginBottom: "20px" }}>Recuperar Senha</h2>

        <p style={{ color: "#aaa", marginBottom: "20px", fontSize: "14px" }}>
          Digite seu e-mail para receber uma senha temporária.
        </p>

        <form onSubmit={handleReset} noValidate>
          <InputLogin
            type="email"
            placeholder="Digite seu e-mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={loading}
            error={message}
          />
          <button
            type="button"
            disabled={loading}
            style={styles.button}
            onClick={handleReset}
          >
            {loading ? "ENVIANDO..." : "ENVIAR NOVA SENHA"}
          </button>
        </form>

        <span style={styles.link} onClick={() => navigate("/login")}>
          Voltar para o Login
        </span>
      </div>
    </div>
  );
}
