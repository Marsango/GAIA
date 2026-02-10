import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api'; // Sua configuração do axios
import logo from "../../assets/images/Logo_lab_Branco.svg";

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleReset = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      // Chama a rota do Django que criamos
      await api.post('/auth/forgot-password/', { email });
      setMessage('Se o e-mail estiver cadastrado, uma nova senha foi enviada para ele.');
    } catch (error) {
      setMessage('Erro ao tentar conectar com o servidor.');
    } finally {
      setLoading(false);
    }
  };

  // Estilos simples inline para facilitar (pode mover para styled.js depois)
  const styles = {
    container: {
      display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh',
      backgroundColor: '#2E2E2E', color: '#fff'
    },
    box: {
      backgroundColor: '#3C3C3C', padding: '40px', borderRadius: '10px',
      textAlign: 'center', width: '100%', maxWidth: '400px',
      boxShadow: '0 4px 10px rgba(0,0,0,0.3)'
    },
    input: {
      width: '100%', padding: '10px', marginBottom: '20px', borderRadius: '5px', border: 'none'
    },
    button: {
      width: '100%', padding: '10px', backgroundColor: '#28a745', color: 'white',
      border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold'
    },
    link: {
      display: 'block', marginTop: '15px', color: '#ccc', cursor: 'pointer', fontSize: '0.9rem'
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <img src={logo} alt="Gaia Logo" style={{ width: '80px', marginBottom: '20px' }}/>
        <h2 style={{ marginBottom: '20px' }}>Recuperar Senha</h2>
        
        <p style={{ color: '#aaa', marginBottom: '20px', fontSize: '14px' }}>
          Digite seu e-mail para receber uma senha temporária.
        </p>
        
        <form onSubmit={handleReset}>
          <input 
            type="email" 
            placeholder="Digite seu e-mail" 
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={styles.input}
          />
          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? 'ENVIANDO...' : 'ENVIAR NOVA SENHA'}
          </button>
        </form>

        {message && <p style={{ marginTop: '15px', color: '#00ff00' }}>{message}</p>}
        
        <span style={styles.link} onClick={() => navigate('/login')}>
          Voltar para o Login
        </span>
      </div>
    </div>
  );
}