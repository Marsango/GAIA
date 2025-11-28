import { useState } from "react";
import { useNavigate } from "react-router-dom";
import InputLogin from "../../components/InputLogin";
import { PageContainer, Button, LoginForm, Title } from "./styled";
import Logo_lab_Branco from "../../assets/images/Logo_lab_Branco.svg";
import { login } from "../../api/auth";

const Login = () => {
  const [cpf, setCpf] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!cpf || !password) {
      setError("Os campos devem ser preenchidos.");
      return;
    }

    try {
      const data = await login(cpf, password); // Chama o backend

      if (data && data.access) {
        // Salva o token e, se quiser, os dados do usuário
        localStorage.setItem("token", data.access);
        localStorage.setItem("refresh", data.refresh);
        localStorage.setItem("user", JSON.stringify(data.user));

        navigate("/reports");
        console.log("Login bem-sucedido:", data);
      } else {
        throw new Error("Resposta inesperada do servidor");
      }
    } catch (err) {
      console.error("Erro no login:", err);
      setError("CPF ou senha inválidos.");
    }
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
          onChange={(e) => setCpf(e.target.value)}
          placeholder="CPF"
        />
        <InputLogin
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Senha"
          required
        />

        {error && <p style={{ color: "red" }}>{error}</p>}

        <Button type="submit">Login</Button>
      </LoginForm>
    </PageContainer>
  );
};

export default Login;
