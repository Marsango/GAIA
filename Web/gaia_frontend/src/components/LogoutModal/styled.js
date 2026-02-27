import styled from 'styled-components';

// Overlay (fundo escuro)
export const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease;
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
`;

// Conteúdo do modal
export const ModalContent = styled.div`
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 450px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  animation: slideIn 0.3s ease;
  
  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

// Cabeçalho do modal
export const ModalHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 30px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
`;

export const ModalTitle = styled.h3`
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0;
  color: #2c3e50;
  font-size: 20px;
  font-weight: 600;
`;

export const ModalCloseButton = styled.button`
  background: transparent;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  
  &:hover {
    background: #f8f9fa;
    color: #495057;
  }
  
  svg {
    width: 20px;
    height: 20px;
  }
`;

// Corpo do modal
export const ModalBody = styled.div`
  padding: 30px;
`;

export const ModalText = styled.p`
  font-size: 16px;
  color: #2c3e50;
  margin: 0 0 15px 0;
  line-height: 1.5;
`;

export const ModalWarning = styled.div`
  background: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 12px 15px;
  border-radius: 4px;
  font-size: 14px;
  color: #856404;
  line-height: 1.4;
`;

// Ações (botões)
export const ModalActions = styled.div`
  display: flex;
  gap: 15px;
  padding: 20px 30px;
  background: #f8f9fa;
  border-top: 1px solid #dee2e6;
  
  @media (max-width: 480px) {
    flex-direction: column;
  }
`;

export const CancelButton = styled.button`
  flex: 1;
  padding: 12px 24px;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover:not(:disabled) {
    background: #5a6268;
    transform: translateY(-1px);
  }
  
  &:active:not(:disabled) {
    transform: translateY(0);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

export const ConfirmButton = styled.button`
  flex: 1;
  padding: 12px 24px;
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s ease;
  
  &:hover:not(:disabled) {
    background: linear-gradient(135deg, #c0392b 0%, #a93226 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
  }
  
  &:active:not(:disabled) {
    transform: translateY(0);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;