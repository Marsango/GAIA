import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import logo from '../../assets/images/Logo_lab_Branco.svg';

export default function ChangePassword() {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // --- FUNÇÃO PADRÃO: TROCAR SENHA ---
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    if (newPassword !== confirmPassword) {
      setError('As novas senhas não coincidem.');
      return;
    }

    if (!newPassword) {
        setError('Digite uma nova senha.');
        return;
    }

    // Chama a função que conecta com a API
    await sendChangePasswordRequest(oldPassword, newPassword);
  };

  // --- NOVA FUNÇÃO: MANTER SENHA ---
  const handleKeepPassword = async (e) => {
    e.preventDefault(); // Evita recarregar a página
    setError('');
    setMessage('');

    if (!oldPassword) {
      setError('Para manter a senha, digite a Senha Atual no primeiro campo.');
      return;
    }

    // Envia a senha antiga como se fosse a nova!
    await sendChangePasswordRequest(oldPassword, oldPassword);
  };

  // --- FUNÇÃO COMPARTILHADA DE REQUISIÇÃO ---
  const sendChangePasswordRequest = async (currentPass, newPass) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      
      if (!token) {
        setError('Sessão expirada. Faça login novamente.');
        setTimeout(() => navigate('/login'), 2000);
        return;
      }

      await api.post('/auth/change-password/', {
        old_password: currentPass,
        new_password: newPass
      }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      setMessage('Senha definida com sucesso! Redirecionando...');
      
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      localStorage.removeItem('refresh');

      setTimeout(() => {
        navigate('/login');
      }, 2000);

    } catch (err) {
      console.error(err);
      if (err.response?.status === 401) {
         setError('Sessão inválida ou senha atual incorreta.');
      } else {
         setError('Erro ao processar. Verifique sua senha atual.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Estilos
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
      width: '100%', padding: '12px', marginBottom: '15px', borderRadius: '5px', border: 'none',
      backgroundColor: '#555', color: '#fff'
    },
    button: {
      width: '100%', padding: '12px', backgroundColor: '#28a745', color: 'white',
      border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold', marginTop: '10px'
    },
    // Estilo do botão novo (Cinza / Secundário)
    secondaryButton: {
      width: '100%', padding: '12px', backgroundColor: 'transparent', color: '#ccc',
      border: '1px solid #555', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold', marginTop: '10px',
      transition: '0.3s'
    },
    label: {
        display: 'block', textAlign: 'left', marginBottom: '5px', color: '#ccc', fontSize: '0.9rem'
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <img src={logo} alt="Gaia Logo" style={{ width: '150px', marginBottom: '20px' }}/>
        <h2 style={{ marginBottom: '20px' }}>Definir Senha</h2>
        
        <p style={{ color: '#ccc', marginBottom: '20px', fontSize: '14px' }}>
          Defina uma nova senha ou confirme a atual para liberar seu acesso.
        </p>
        
        <form onSubmit={handleSubmit}>
          
          <label style={styles.label}>Senha Atual (Obrigatório)</label>
          <input 
            type="password" 
            placeholder="Senha que você usou para entrar" 
            required
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
            style={styles.input}
          />

          <label style={styles.label}>Nova Senha</label>
          <input 
            type="password" 
            placeholder="Nova senha (opcional se manter a atual)" 
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            style={styles.input}
          />

          <label style={styles.label}>Confirmar Nova Senha</label>
          <input 
            type="password" 
            placeholder="Repita a nova senha" 
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            style={styles.input}
          />

          {/* Botão Principal: Mudar Senha */}
          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? 'PROCESSANDO...' : 'SALVAR NOVA SENHA'}
          </button>

          {/* Botão Secundário: Manter Senha */}
          <button 
            type="button" // Importante ser type="button" para não submeter o form principal
            onClick={handleKeepPassword} 
            disabled={loading} 
            style={styles.secondaryButton}
            onMouseOver={(e) => e.target.style.borderColor = '#aaa'}
            onMouseOut={(e) => e.target.style.borderColor = '#555'}
          >
            MANTER SENHA ATUAL
          </button>

        </form>

        {message && <p style={{ marginTop: '15px', color: '#28a745', fontWeight: 'bold' }}>{message}</p>}
        {error && <p style={{ marginTop: '15px', color: '#ff4d4d', fontWeight: 'bold' }}>{error}</p>}
        
      </div>
    </div>
  );
}