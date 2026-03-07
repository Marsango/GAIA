import React, { useState, useEffect } from "react";
import api from "../../api/api"; //  API com interceptors e auto-refresh
import { useNavigate } from "react-router-dom";
import {
  Container,
  Title,
  TabContainer,
  TabButton,
  FormBox,
  InputGroup,
  ActionButton,
  Message,
} from "./styled";

export default function AdminPanel() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("cadastro"); // 'cadastro' ou 'email'
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  // Estados Cadastro
  const [newUser, setNewUser] = useState({
    first_name: "",
    cpf: "",
    email: "",
  });

  // Estados Email Config
  const [emailConfig, setEmailConfig] = useState({ assunto: "", mensagem: "" });

  // Busca configuração de email ao carregar a aba
  useEffect(() => {
    if (activeTab === "email") {
      fetchEmailConfig();
    }
  }, [activeTab]);

  // --- TRAVA DE SEGURANÇA ---
  useEffect(() => {
    // 1. Pega o usuário salvo
    const userStored = localStorage.getItem("user");

    // 2. Se não tiver usuário, vai pro login
    if (!userStored) {
      navigate("/login");
      return;
    }

    const user = JSON.parse(userStored);

    // 3. Se o usuário NÃO for staff (admin), chuta para os relatórios
    if (!user.is_staff) {
      alert("Acesso negado: Apenas administradores podem acessar esta página.");
      navigate("/reports");
    }
  }, [navigate]);

  const fetchEmailConfig = async () => {
    try {
      //  NOVO: Token em httpOnly cookie, axios envia automaticamente
      const response = await api.get("admin/email-config/");
      setEmailConfig(response.data);
    } catch (error) {
      console.error("Erro ao carregar config", error);
    }
  };

  // --- FUNÇÃO: CADASTRAR USUÁRIO ---
  const handleRegisterUser = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    const cpfClean = newUser.cpf.replace(/\D/g, "");

    try {
      //  NOVO: Token em httpOnly cookie, axios envia automaticamente
      await api.post("register/", {
        ...newUser,
        cpf: cpfClean,
      });

      setMessage({
        type: "success",
        text: "Usuário cadastrado e senha enviada por e-mail!",
      });
      setNewUser({ first_name: "", cpf: "", email: "" });
    } catch (error) {
      console.error(error);
      const errorMsg =
        error.response?.data?.error || "Erro ao cadastrar usuário.";
      setMessage({ type: "error", text: errorMsg });
    } finally {
      setLoading(false);
    }
  };

  // --- FUNÇÃO: SALVAR TEMPLATE DE EMAIL ---
  const handleSaveEmailConfig = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      //  NOVO: Token em httpOnly cookie
      // 2. Envia o token automaticamente via api
      await api.post("admin/email-config/", emailConfig);
      setMessage({
        type: "success",
        text: "Template de e-mail atualizado com sucesso!",
      });
    } catch (error) {
      setMessage({ type: "error", text: "Erro ao salvar configuração." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Title>Painel do Administrador</Title>

      <TabContainer>
        <TabButton
          $active={activeTab === "cadastro"}
          onClick={() => {
            setActiveTab("cadastro");
            setMessage(null);
          }}
        >
          Cadastrar Cliente
        </TabButton>
        <TabButton
          $active={activeTab === "email"}
          onClick={() => {
            setActiveTab("email");
            setMessage(null);
          }}
        >
          Configuração de E-mail
        </TabButton>
      </TabContainer>

      {/* --- ABA CADASTRO --- */}
      {activeTab === "cadastro" && (
        <FormBox>
          <h3>Novo Cliente</h3>
          <p style={{ color: "#aaa", marginBottom: "20px", fontSize: "14px" }}>
            O sistema enviará automaticamente as credenciais para o e-mail
            abaixo.
          </p>
          <form onSubmit={handleRegisterUser}>
            <InputGroup>
              <label>Nome Completo</label>
              <input
                required
                value={newUser.first_name}
                onChange={(e) =>
                  setNewUser({ ...newUser, first_name: e.target.value })
                }
              />
            </InputGroup>
            <InputGroup>
              <label>CPF</label>
              <input
                required
                placeholder="000.000.000-00"
                value={newUser.cpf}
                onChange={(e) =>
                  setNewUser({ ...newUser, cpf: e.target.value })
                }
              />
            </InputGroup>
            <InputGroup>
              <label>E-mail</label>
              <input
                required
                type="email"
                value={newUser.email}
                onChange={(e) =>
                  setNewUser({ ...newUser, email: e.target.value })
                }
              />
            </InputGroup>
            <ActionButton type="submit" disabled={loading}>
              {loading ? "Cadastrando..." : "CADASTRAR E ENVIAR SENHA"}
            </ActionButton>
          </form>
        </FormBox>
      )}

      {/* --- ABA E-MAIL CONFIG --- */}
      {activeTab === "email" && (
        <FormBox>
          <h3>Editar Template de E-mail</h3>
          <p style={{ color: "#aaa", marginBottom: "20px", fontSize: "14px" }}>
            Variáveis disponíveis: <b>{"{nome}"}</b>, <b>{"{cpf}"}</b>,{" "}
            <b>{"{senha}"}</b>.
          </p>
          <form onSubmit={handleSaveEmailConfig}>
            <InputGroup>
              <label>Assunto do E-mail</label>
              <input
                required
                value={emailConfig.assunto}
                onChange={(e) =>
                  setEmailConfig({ ...emailConfig, assunto: e.target.value })
                }
              />
            </InputGroup>
            <InputGroup>
              <label>Mensagem</label>
              <textarea
                required
                value={emailConfig.mensagem}
                onChange={(e) =>
                  setEmailConfig({ ...emailConfig, mensagem: e.target.value })
                }
              />
            </InputGroup>
            <ActionButton
              type="submit"
              disabled={loading}
              style={{ backgroundColor: "#6f42c1" }}
            >
              {loading ? "Salvando..." : "SALVAR ALTERAÇÕES"}
            </ActionButton>
          </form>
        </FormBox>
      )}

      {message && (
        <Message $error={message.type === "error"}>{message.text}</Message>
      )}
    </Container>
  );
}
