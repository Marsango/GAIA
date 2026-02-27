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
import { login, getCurrentUser, loginWithCNPJ } from "../../api/auth"; // Adicione getUserInfo

const Login = () => {
  const [cpf, setCpf] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState({ cpf: "", password: "", general: "" });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Função para formatar CPF/CNPJ (remove pontos, traço e barra)
  const formatCPF = (cpf) => {
    return cpf.replace(/\D/g, "");
  };

  // Valida formato do CPF (11 dígitos) ou CNPJ (14 dígitos)
  const isValidCPF = (cpf) => {
    const cleanedCPF = formatCPF(cpf);
    return cleanedCPF.length === 11 || cleanedCPF.length === 14;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Resetar erros
    setError({ cpf: "", password: "", general: "" });

    let hasError = false;
    const newError = { cpf: "", password: "", general: "" };

    if (!cpf) {
      newError.cpf = "O campo CPF/CNPJ é obrigatório.";
      hasError = true;
    } else if (!isValidCPF(cpf)) {
      newError.cpf = "CPF/CNPJ inválido. CPF: 11 dígitos, CNPJ: 14 dígitos.";
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
      // Formata CPF/CNPJ antes de enviar
      const formattedDoc = formatCPF(cpf);

      // Detecta se é CPF (11 dígitos) ou CNPJ (14 dígitos)
      const isCNPJ = formattedDoc.length === 14;

      // Chama a API de login apropriada
      const data = isCNPJ
        ? await loginWithCNPJ(formattedDoc, password)
        : await login(formattedDoc, password);

      // Verifica se os dados esperados estão presentes
      if (!data.access || !data.refresh) {
        throw new Error("Dados incompletos recebidos do servidor");
      }

      // Salva no localStorage
      localStorage.setItem("token", data.access);
      localStorage.setItem("refresh", data.refresh);

      const userData = await getCurrentUser(data.access);
      localStorage.setItem("user", JSON.stringify(userData));
      if (data.user && data.user.primeiro_acesso) {
        navigate("/change-password");
      } else {
        navigate("/reports");
      }
    } catch (err) {
      console.error("Erro completo no login:", err);

      if (err.response?.status === 401) {
        setError((prev) => ({
          ...prev,
          general: "CPF/CNPJ ou senha incorretos.",
        }));
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

  // Máscara de CPF ou CNPJ enquanto digita
  const handleCpfChange = (e) => {
    let value = e.target.value.replace(/\D/g, "");

    // Aplica máscara baseado no tamanho
    if (value.length <= 11) {
      // Máscara CPF: 000.000.000-00
      value = value.replace(/(\d{3})(\d)/, "$1.$2");
      value = value.replace(/(\d{3})(\d)/, "$1.$2");
      value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    } else {
      // Máscara CNPJ: 00.000.000/0000-00
      value = value.substring(0, 14); // Limita a 14 dígitos
      value = value.replace(/(\d{2})(\d)/, "$1.$2");
      value = value.replace(/(\d{3})(\d)/, "$1.$2");
      value = value.replace(/(\d{3})(\d)/, "$1/$2");
      value = value.replace(/(\d{4})(\d{1,2})$/, "$1-$2");
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
          placeholder="CPF/CNPJ (somente números)"
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
              fontFamily: "Poppins, sans-serif",
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
