import { useState } from "react";
import InputLogin from "../../components/InputLogin";
import { useNavigate } from "react-router-dom";
import { PageContainer, Button, LoginForm, Title } from "./styled";
import Logo_lab_Branco from "../../assets/images/Logo_lab_Branco.svg";

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
      // Esta é a chamada de API REAL
      const response = await fetch("http://127.0.0.1:8000/api/auth/login/", { // URL completa do Backend
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        // O backend espera "username", que é o que você digita no campo "cpf"
        body: JSON.stringify({ cpf: cpf, password: password }) 
      });

      if (!response.ok) {
        // lê mensagem de erro enviada pelo servidor 
        const errBody = await response.json().catch(() => ({}));
        // Tenta pegar uma mensagem de erro específica do backend
        const detailError = errBody.detail || "Credenciais inválidas";
        throw new Error(detailError);
      }

      const data = await response.json(); 

      // Salva o token
      localStorage.setItem("token", data.token);
      
      // Redireciona para a página de relatórios
      navigate("/reports"); 

    } catch (err) {
      console.error(err); 
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
