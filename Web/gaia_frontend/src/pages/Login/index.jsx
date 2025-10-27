import { useState } from "react";
import InputLogin from "../../components/InputLogin";
//import useNavigate from "react-router-dom";
import { PageContainer, Button, LoginForm, Title } from "./styled";
import Logo_lab_Branco from "../../assets/images/Logo_lab_Branco.svg";

const Login = () => {
  const [cpf, setCpf] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");
    if (!cpf || !password) {
      setError("Os campos devem ser preenchidos.");
      return;
    }

    // try {
    //   const response = await fetch("/api/login", { // endpoint do backend
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json"
    //     },
    //     body: JSON.stringify({ email, password })
    //   });

    //   if (!response.ok) {
    //     // lê mensagem de erro enviada pelo servidor (se houver)
    //     const errBody = await response.json().catch(() => ({}));
    //     throw new Error(errBody.message || `Erro ${response.status}`);
    //   }

    //   const data = await response.json(); // ex: { token: "...", user: {...} }

    //   // Exemplo de armazenamento simples (ver observações de segurança abaixo)
    //   localStorage.setItem("token", data.token);
    //   // você pode salvar dados do usuário em um context/global store também

    //   // redirecionar após login
    //   navigate("/dashboard");
    // }
    try {
      // Simulação de chamada de API
      if (cpf === "123" && password === "123") {
        // Login bem-sucedido
        localStorage.setItem("token", "token_simulado");
        //navigate("/dashboard");
        console.log("Login bem-sucedido");
      } else {
        throw new Error("Credenciais inválidas");
      }
    } catch (err) {
      console.error(err); // importante: não logue senhas
      setError(err.message || "Erro ao fazer login");
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
