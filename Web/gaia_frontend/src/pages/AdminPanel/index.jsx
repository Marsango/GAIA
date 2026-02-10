import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';

// --- ESTILOS (Pode mover para styled.js depois) ---
const Container = styled.div`
  padding: 40px;
  background-color: #2E2E2E;
  min-height: 100vh;
  color: white;
`;

const Title = styled.h1`
  margin-bottom: 30px;
  border-bottom: 2px solid #444;
  padding-bottom: 10px;
`;

const TabContainer = styled.div`
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
`;

const TabButton = styled.button`
  padding: 10px 20px;
  background-color: ${props => props.$active ? '#28a745' : '#444'};
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-weight: bold;
  &:hover { background-color: ${props => props.$active ? '#218838' : '#555'}; }
`;

const FormBox = styled.div`
  background-color: #3C3C3C;
  padding: 30px;
  border-radius: 8px;
  max-width: 600px;
`;

const InputGroup = styled.div`
  margin-bottom: 15px;
  label { display: block; margin-bottom: 5px; color: #ccc; }
  input, textarea {
    width: 100%; padding: 10px; border-radius: 5px; border: none;
    background-color: #555; color: white;
  }
  textarea { height: 150px; resize: vertical; }
`;

const ActionButton = styled.button`
  background-color: #007bff;
  color: white; padding: 12px 20px; border: none; border-radius: 5px;
  cursor: pointer; font-size: 1rem; font-weight: bold; width: 100%;
  &:hover { background-color: #0056b3; }
  &:disabled { background-color: #555; cursor: not-allowed; }
`;

const Message = styled.div`
  margin-top: 15px;
  padding: 10px;
  border-radius: 5px;
  background-color: ${props => props.$error ? '#ff4d4d' : '#28a745'};
  color: white; text-align: center;
`;

// --- COMPONENTE PRINCIPAL ---
export default function AdminPanel() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('cadastro'); // 'cadastro' ou 'email'
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  
  // Estados Cadastro
  const [newUser, setNewUser] = useState({ first_name: '', cpf: '', email: '' });
  
  // Estados Email Config
  const [emailConfig, setEmailConfig] = useState({ assunto: '', mensagem: '' });

  // Busca configuração de email ao carregar a aba
  useEffect(() => {
    if (activeTab === 'email') {
      fetchEmailConfig();
    }
  }, [activeTab]);

  // --- TRAVA DE SEGURANÇA ---
  useEffect(() => {
    // 1. Pega o usuário salvo
    const userStored = localStorage.getItem('user');
    
    // 2. Se não tiver usuário, vai pro login
    if (!userStored) {
      navigate('/login');
      return;
    }

    const user = JSON.parse(userStored);

    // 3. Se o usuário NÃO for staff (admin), chuta para os relatórios
    if (!user.is_staff) {
      alert('Acesso negado: Apenas administradores podem acessar esta página.');
      navigate('/reports');
    }
  }, [navigate]);

  const fetchEmailConfig = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await api.get('/auth/admin/email-config/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
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
    const token = localStorage.getItem('token'); // 1. Pega o token

    try {
      // 2. Envia o token no header
      await api.post('/auth/register/', {
        ...newUser,
        cpf: cpfClean
      }, {
        headers: {
          'Authorization': `Bearer ${token}` 
        }
      });

      setMessage({ type: 'success', text: 'Usuário cadastrado e senha enviada por e-mail!' });
      setNewUser({ first_name: '', cpf: '', email: '' }); 
    } catch (error) {
      console.error(error);
      const errorMsg = error.response?.data?.error || 'Erro ao cadastrar usuário.';
      setMessage({ type: 'error', text: errorMsg });
    } finally {
      setLoading(false);
    }
  };

  // --- FUNÇÃO: SALVAR TEMPLATE DE EMAIL ---
  const handleSaveEmailConfig = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    const token = localStorage.getItem('token'); // 1. Pega o token

    try {
      // 2. Envia o token no header
      await api.post('/auth/admin/email-config/', emailConfig, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setMessage({ type: 'success', text: 'Template de e-mail atualizado com sucesso!' });
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro ao salvar configuração.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Title>Painel do Administrador</Title>

      <TabContainer>
        <TabButton $active={activeTab === 'cadastro'} onClick={() => { setActiveTab('cadastro'); setMessage(null); }}>
          Cadastrar Cliente
        </TabButton>
        <TabButton $active={activeTab === 'email'} onClick={() => { setActiveTab('email'); setMessage(null); }}>
          Configuração de E-mail
        </TabButton>
      </TabContainer>

      {/* --- ABA CADASTRO --- */}
      {activeTab === 'cadastro' && (
        <FormBox>
          <h3>Novo Cliente</h3>
          <p style={{color: '#aaa', marginBottom: '20px', fontSize: '14px'}}>
            O sistema enviará automaticamente as credenciais para o e-mail abaixo.
          </p>
          <form onSubmit={handleRegisterUser}>
            <InputGroup>
              <label>Nome Completo</label>
              <input 
                required 
                value={newUser.first_name}
                onChange={e => setNewUser({...newUser, first_name: e.target.value})}
              />
            </InputGroup>
            <InputGroup>
              <label>CPF</label>
              <input 
                required 
                placeholder="000.000.000-00"
                value={newUser.cpf}
                onChange={e => setNewUser({...newUser, cpf: e.target.value})}
              />
            </InputGroup>
            <InputGroup>
              <label>E-mail</label>
              <input 
                required 
                type="email" 
                value={newUser.email}
                onChange={e => setNewUser({...newUser, email: e.target.value})}
              />
            </InputGroup>
            <ActionButton type="submit" disabled={loading}>
              {loading ? 'Cadastrando...' : 'CADASTRAR E ENVIAR SENHA'}
            </ActionButton>
          </form>
        </FormBox>
      )}

      {/* --- ABA E-MAIL CONFIG --- */}
      {activeTab === 'email' && (
        <FormBox>
          <h3>Editar Template de E-mail</h3>
          <p style={{color: '#aaa', marginBottom: '20px', fontSize: '14px'}}>
            Variáveis disponíveis: <b>{'{nome}'}</b>, <b>{'{cpf}'}</b>, <b>{'{senha}'}</b>.
          </p>
          <form onSubmit={handleSaveEmailConfig}>
            <InputGroup>
              <label>Assunto do E-mail</label>
              <input 
                required 
                value={emailConfig.assunto}
                onChange={e => setEmailConfig({...emailConfig, assunto: e.target.value})}
              />
            </InputGroup>
            <InputGroup>
              <label>Mensagem</label>
              <textarea 
                required 
                value={emailConfig.mensagem}
                onChange={e => setEmailConfig({...emailConfig, mensagem: e.target.value})}
              />
            </InputGroup>
            <ActionButton type="submit" disabled={loading} style={{backgroundColor: '#6f42c1'}}>
              {loading ? 'Salvando...' : 'SALVAR ALTERAÇÕES'}
            </ActionButton>
          </form>
        </FormBox>
      )}

      {message && (
        <Message $error={message.type === 'error'}>
          {message.text}
        </Message>
      )}

    </Container>
  );
}