import { useState } from "react";
import { useNavigate } from "react-router-dom";
import InputLogin from "../../components/InputLogin";
import {
  PageContainer,
  Button,
  LoginForm,
  Title,
  ErrorMessage,
} from "./styled";
import Logo_lab_Branco from "../../assets/images/Logo_lab_Branco.svg";
import { login, getCurrentUser } from "../../api/auth"; // Adicione getUserInfo

const Login = () => {
  const [cpf, setCpf] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState({ cpf: "", password: "", general: "" });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Função para formatar CPF (remove pontos e traço)
  const formatCPF = (cpf) => {
    return cpf.replace(/\D/g, "");
  };

  // Valida formato do CPF (11 dígitos)
  const isValidCPF = (cpf) => {
    const cleanedCPF = formatCPF(cpf);
    return cleanedCPF.length === 11;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Resetar erros
    setError({ cpf: "", password: "", general: "" });

    let hasError = false;
    const newError = { cpf: "", password: "", general: "" };

    if (!cpf) {
      newError.cpf = "O campo CPF é obrigatório.";
      hasError = true;
    } else if (!isValidCPF(cpf)) {
      newError.cpf = "CPF inválido. Deve conter 11 dígitos.";
      hasError = true;
    }

    if (!password) {
      newError.password = "O campo senha é obrigatório.";
      hasError = true;
    }

    if (hasError) {
      setError(newError);
      setLoading(false);
      return;
    }

    setLoading(true);

    try {
      // Formata CPF antes de enviar
      const formattedCPF = formatCPF(cpf);

      // Chama a API de login
      const data = await login(formattedCPF, password);

      console.log("Dados recebidos do login:", data);

      // Verifica se os dados esperados estão presentes
      if (!data.access || !data.refresh) {
        throw new Error("Dados incompletos recebidos do servidor");
      }

      // Salva no localStorage
      localStorage.setItem("token", data.access);
      localStorage.setItem("refresh", data.refresh);

      // Para debug: verifique no console
      // console.log("Token salvo:", data.access);
      // console.log("Usuário salvo:", data.user);

      const userData = await getCurrentUser(data.access);
      localStorage.setItem("user", JSON.stringify(userData));

      // Verifica se é o primeiro acesso ---
      if (data.user && data.user.primeiro_acesso) {
        console.log("Primeiro acesso detectado! Redirecionando para troca de senha...");
        navigate("/change-password");
      } else {
        console.log("Acesso normal. Redirecionando para relatórios...");
        navigate("/reports");
      }

    } catch (err) {
      console.error("Erro completo no login:", err);

      if (err.response?.status === 401) {
        setError((prev) => ({ ...prev, general: "CPF ou senha incorretos." }));
      } else {
        setError((prev) => ({
          ...prev,
          general: "Erro ao fazer login. Tente novamente.",
        }));
      }
    } finally {
      setLoading(false);
    }
  };

  // Máscara de CPF enquanto digita (opcional)
  const handleCpfChange = (e) => {
    let value = e.target.value.replace(/\D/g, "");

    // Aplica máscara: 000.000.000-00
    if (value.length <= 11) {
      value = value.replace(/(\d{3})(\d)/, "$1.$2");
      value = value.replace(/(\d{3})(\d)/, "$1.$2");
      value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    }

    setCpf(value);
  };

  return (
    <PageContainer>
      <LoginForm onSubmit={handleSubmit}>
        <img
          src={Logo_lab_Branco}
          alt="Logo Lab Solos"
          style={{ marginBottom: "20px", width: "200px" }}
        />
        <Title>Login</Title>

        <InputLogin
          type="text"
          value={cpf}
          onChange={handleCpfChange}
          placeholder="CPF (somente números)"
          disabled={loading}
          error={error.cpf}
        />
        <InputLogin
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Senha"
          disabled={loading}
          error={error.password}
        />

        <Button type="submit" disabled={loading}>
          {loading ? "Entrando..." : "Login"}
        </Button>

        {/* --- ADIÇÃO: BOTÃO ESQUECI MINHA SENHA --- */}
        <div style={{ marginTop: "15px", textAlign: "center" }}>
          <span
            style={{
              color: "#333",
              cursor: "pointer",
              textDecoration: "underline",
              fontSize: "0.9rem",
            }}
            onClick={() => navigate("/forgot-password")}
          >
            Esqueci minha senha
          </span>
        </div>
        {/* ----------------------------------------- */}

        {error && <ErrorMessage>{error.general}</ErrorMessage>}
      </LoginForm>
    </PageContainer>
  );
};

export default Login;
