import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function NotFound() {
  const navigate = useNavigate();
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', padding: '50px', textAlign: 'center' }}>
      <h1 style={{ fontSize: '4rem', color: '#2e7d32', margin: '0' }}>404</h1>
      <h2 style={{ color: '#333', marginBottom: '20px' }}>Página não encontrada</h2>
      <p style={{ color: '#666', marginBottom: '30px' }}>A página que você está procurando não existe ou foi movida.</p>
      <button 
        onClick={() => navigate('/login')}
        style={{ padding: '10px 20px', backgroundColor: '#2e7d32', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold' }}
      >
        Voltar para o Início
      </button>
    </div>
  );
}