import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import api from "../../api/api";
import logo from "../../assets/images/Logo_lab_Branco.svg";
import InputLogin from "../../components/InputLogin";
import { styles } from "./styled";

export default function ResetPassword() {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);

  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const uid = useMemo(() => searchParams.get("uid") || "", [searchParams]);
  const token = useMemo(() => searchParams.get("token") || "", [searchParams]);

  useEffect(() => {
    const onResize = () => setIsMobile(window.innerWidth <= 768);
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    if (!uid || !token) {
      setError("Link de redefinicao invalido. Solicite um novo email.");
      return;
    }

    if (!newPassword || !confirmPassword) {
      setError("Preencha e confirme a nova senha.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("As senhas nao coincidem.");
      return;
    }

    setLoading(true);

    try {
      await api.post("/reset-password/", {
        uid,
        token,
        new_password: newPassword,
      });

      setMessage(
        "Senha redefinida com sucesso! Redirecionando para o login...",
      );
      setTimeout(() => navigate("/login"), 1800);
    } catch (err) {
      const responseData = err.response?.data;
      setError(responseData?.error || "Nao foi possivel redefinir a senha.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={{ ...styles.box, ...(isMobile ? styles.mobileBox : {}) }}>
        <img
          src={logo}
          alt="Gaia Logo"
          style={{ width: "150px", marginBottom: "20px" }}
        />

        <h2 style={{ marginBottom: "16px" }}>Redefinir Senha</h2>

        <p style={{ color: "#646464", marginBottom: "20px", fontSize: "14px" }}>
          Defina sua nova senha para concluir a recuperacao de acesso.
        </p>

        <form onSubmit={handleSubmit} noValidate>
          <InputLogin
            type="password"
            placeholder="Digite a nova senha"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            disabled={loading}
          />

          <InputLogin
            type="password"
            placeholder="Confirme a nova senha"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            disabled={loading}
          />

          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? "PROCESSANDO..." : "REDEFINIR SENHA"}
          </button>
        </form>

        {message && (
          <div style={{ ...styles.message, ...styles.messageSuccess }}>
            {message}
          </div>
        )}
        {error && (
          <div style={{ ...styles.message, ...styles.messageError }}>
            {error}
          </div>
        )}

        <span style={styles.link} onClick={() => navigate("/login")}>
          Voltar para o Login
        </span>
      </div>
    </div>
  );
}
