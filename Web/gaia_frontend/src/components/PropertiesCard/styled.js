import styled from "styled-components";
import { green, black } from "../../config/colors";

export const Card = styled.button`
  background-color: ${(props) => (props.$ativo ? "#e8f5e9" : "#fff")};
  border: 2px solid ${(props) => (props.$ativo ? green : "#e0e0e0")};
  border-radius: 8px;
  min-height: 44px;
  padding: 15px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden; /* Evita que o texto vaze pra fora da caixa */
  text-align: left;

  &:hover {
    border-color: ${green};
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  &:focus-visible {
    outline: 3px solid ${black};
    outline-offset: 2px;
  }

  @media (max-width: 600px) {
    padding: 12px;
  }
`;

/* Adicionamos o IconContainer que estava faltando! */
export const IconContainer = styled.span`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px; /* Dá um espacinho entre o ícone e o texto */
  font-size: 1.1em;
`;

export const Name = styled.h3`
  font-size: 20px;
  color: ${black};
  margin: 0 0 5px 0;
  font-family: 'Poppins', sans-serif;
  display: flex;
  align-items: center;
  gap: 10px;
  
  /* Faz com que o texto longo não quebre a tela */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;

  svg {
    flex-shrink: 0;
  }

  @media (max-width: 600px) {
    font-size: 14px;
  }
`;

export const Location = styled.p`
  font-size: 20px;
  color: ${black};
  margin: 0;
  font-family: 'Poppins', sans-serif;
  display: flex;
  align-items: center;
  gap: 10px;
  
  /* Coloca "..." no final se a localização for muito grande */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;

  svg {
    flex-shrink: 0;
  }

  @media (max-width: 600px) {
    font-size: 12px;
  }
`;