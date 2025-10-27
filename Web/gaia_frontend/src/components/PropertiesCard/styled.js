import styled from "styled-components";

export const Card = styled.div`
  border: 2px solid ${(props) => (props.$ativo ? "#2e7d32" : "#ccc")};
  background: ${(props) => (props.$ativo ? "#e8f5e9" : "#fff")};
  border-radius: 10px;
  padding: 10px;
  cursor: pointer;
  width: 400px;
  font-size: 25px;
  align-items: center;
  font-family: "Poppins", sans-serif;
  transition: 0.2s;
  &:hover {
    background: #f5f5f5;
  }
`;

export const IconContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;
