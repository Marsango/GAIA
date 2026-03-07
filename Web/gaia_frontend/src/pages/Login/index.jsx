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
import { loginSecureCPF, loginWithCNPJ } from "../../api/auth";

const Login = () => {
  const [cpf, setCpf] = useState("");
  const [password, setPassword] = useState("");
  const [captchaChallenge, setCaptchaChallenge] = useState("");
  const [captchaToken, setCaptchaToken] = useState("");
  const [captchaAnswer, setCaptchaAnswer] = useState("");
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
        : await loginSecureCPF(
            formattedDoc,
            password,
            captchaToken || null,
            captchaAnswer || null,
          );

      console.log(" Resposta do backend:", data); // ← NOVO: Debug

      // Verifica se os dados esperados estão presentes
      if (!data.user) {
        throw new Error("Dados incompletos recebidos do servidor");
      }

      //  httpOnly Cookies já são enviados automaticamente pelo navegador
      // Não precisamos mais salvar o token em sessionStorage
      // O axios com withCredentials: true vai gerenciar isso para nós

      // Armazenar dados do usuário (não-sensível)
      const userData = data.user;
      localStorage.setItem("user", JSON.stringify(userData));

      if (data.user && data.user.primeiro_acesso) {
        navigate("/change-password");
      } else {
        navigate("/reports");
      }
    } catch (err) {
      console.error("Erro completo no login:", err);

      const responseData = err.response?.data;

      // Verificar se requer CAPTCHA
      if (responseData?.require_captcha && responseData?.captcha) {
        setCaptchaChallenge(
          responseData.captcha.challenge || "Resolva o CAPTCHA",
        );
        setCaptchaToken(responseData.captcha.token || "");
        setCaptchaAnswer("");

        const failedAttempts = responseData.failed_attempts || 0;
        const mensagem = ` Muitas tentativas falhadas (${failedAttempts}). Por favor, resolva o CAPTCHA para continuar.`;

        setError((prev) => ({
          ...prev,
          general: mensagem,
        }));
        return;
      }

      // Erro 403: CAPTCHA errado
      if (err.response?.status === 403) {
        // CAPTCHA continua visível, mas mostra erro
        setCaptchaAnswer(""); // Limpa a resposta anterior

        const errorMsg =
          responseData?.error || "Resposta do CAPTCHA incorreta.";
        const failedAttempts = responseData?.failed_attempts || 0;

        let mensagem = ` ${errorMsg}`;
        if (failedAttempts > 0) {
          mensagem += ` (Tentativa ${failedAttempts})`;
        }

        setError((prev) => ({
          ...prev,
          general: mensagem,
        }));
        return;
      }

      // Erro 429: Conta bloqueada temporariamente
      if (err.response?.status === 429) {
        setError((prev) => ({
          ...prev,
          general:
            " Muitas tentativas. Sua conta foi bloqueada temporariamente. Tente novamente em alguns minutos.",
        }));
        return;
      }

      // Erro 401: Credenciais inválidas
      if (err.response?.status === 401) {
        const failedAttempts = responseData?.failed_attempts || 0;
        const maxAttempts = responseData?.max_attempts_before_captcha || 5;

        let mensagem = " CPF/CNPJ ou senha incorretos.";

        if (failedAttempts > 0) {
          const tentativasRestantes = maxAttempts - failedAttempts;
          if (tentativasRestantes > 0) {
            mensagem += ` (Tentativa ${failedAttempts}/${maxAttempts}. Restam ${tentativasRestantes} antes do CAPTCHA)`;
          } else {
            mensagem += ` (${failedAttempts} tentativas falhadas. Próxima tentativa exigirá CAPTCHA)`;
          }
        }

        setError((prev) => ({
          ...prev,
          general: mensagem,
        }));
        return;
      }

      // Erro 400: Validação
      if (err.response?.status === 400) {
        const errorMsg = responseData?.error || "Dados inválidos";
        setError((prev) => ({
          ...prev,
          general: ` ${errorMsg}`,
        }));
        return;
      }

      // Erro genérico (5xx, network, etc)
      if (err.code === "ERR_NETWORK") {
        setError((prev) => ({
          ...prev,
          general:
            " Erro de conexão. Verifique sua internet e tente novamente.",
        }));
        return;
      }

      // Fallback para qualquer outro erro
      setError((prev) => ({
        ...prev,
        general:
          responseData?.error ||
          "Erro ao fazer login. Tente novamente mais tarde.",
      }));
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

        {captchaChallenge && (
          <>
            <p style={{ margin: "4px 0 0", fontWeight: 600 }}>
              {captchaChallenge}
            </p>
            <InputLogin
              type="text"
              value={captchaAnswer}
              onChange={(e) => {
                setCaptchaAnswer(e.target.value);
                // Limpar erro anterior quando usuário digita a resposta novamente
                setError((prev) => ({
                  ...prev,
                  general: "",
                }));
              }}
              placeholder="Resposta do CAPTCHA"
              disabled={loading}
            />
          </>
        )}

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
