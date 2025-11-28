import styled from "styled-components";

export const Card = styled.div`
  border: 2px solid #ccc;
  border-radius: 10px;
  padding: 12px;
  margin-bottom: 10px;
  background: white;
  width: 550px;
  font-family: "Poppins", sans-serif;
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
  max-height: ${(p) => (p.$expandido ? "200px" : "0")};
  opacity: ${(p) => (p.$expandido ? "1" : "0")};
  overflow: hidden;
  transition: all 0.4s ease;
  margin-top: ${(p) => (p.$expandido ? "10px" : "0")};
`;

export const ButtonRow = styled.div`
  display: flex;
  gap: 10px;
  margin-top: 10px;
  justify-content: center;
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
  width: 250px;
  font-size: 20px;
  justify-content: center;
`;

export const Data = styled.div`
  font-size: 25px;
`;

export const NumeroAmostra = styled.div`
  font-size: 20px;
  font-family: "Poppins", sans-serif;
`;