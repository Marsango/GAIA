import styled from "styled-components";

export const Card = styled.div`
  border: 2px solid #ccc;
  border-radius: 10px;
  padding: 12px;
  margin-bottom: 10px;
  background: white;
  width: 100%;
  box-sizing: border-box; 
  font-family: "Poppins", sans-serif;
  overflow: hidden;
`;

export const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
`;

export const Divider = styled.hr`
  border: none;
  border-top: 1px solid #ddd;
  margin: 12px 0;
  font-family: "Poppins", sans-serif;
`;

export const Conteudo = styled.div`
  max-height: ${(p) => (p.$expandido ? "500px" : "0")};
  opacity: ${(p) => (p.$expandido ? "1" : "0")};
  overflow-y: ${(p) => (p.$expandido ? "auto" : "hidden")};
  overflow-x: hidden;
  transition: all 0.4s ease;
  margin-top: ${(p) => (p.$expandido ? "10px" : "0")};
  padding-right: ${(p) => (p.$expandido ? "4px" : "0")};

  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
  }
`;

export const ButtonRow = styled.div`
  display: flex;
  gap: 10px;
  margin-top: 10px;
  justify-content: center;
  
  @media (max-width: 600px) {
    gap: 5px; 
  }
`;

export const Button = styled.button`
  background: ${(p) => (p.secundario ? "#2e7d32" : "#4caf50")};
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  width: 100%;
  
  /* Reduzimos de 20px para 16px no Desktop! */
  font-size: 16px; 
  justify-content: center;

  @media (max-width: 600px) {
    font-size: 14px; 
    padding: 8px;
  }
`;

export const Data = styled.div`
  /* Reduzimos de 25px para 18px! (Mesmo tamanho do nome da Fazenda) */
  font-size: 18px; 
  font-weight: 500; 
  
  @media (max-width: 600px) {
    font-size: 14px; 
  }
`;

export const NumeroAmostra = styled.div`
  /* Reduzimos de 20px para 16px no Desktop! */
  font-size: 16px; 
  font-family: "Poppins", sans-serif;

  @media (max-width: 600px) {
    font-size: 14px; 
  }
`;