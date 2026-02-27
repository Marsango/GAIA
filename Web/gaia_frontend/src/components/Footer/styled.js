import styled from "styled-components";
import { gray, black } from "../../config/colors";

export const FooterContainer = styled.footer`
  width: 100%;
  box-sizing: border-box;
  background-color: ${gray};
  color: ${black};
  text-align: center;
  padding: 20px;
  font-family: 'Poppins', sans-serif;
  border-top: 1px solid #ccc;
  
  /* Garante que o footer não encolha num layout flex */
  flex-shrink: 0; 
`;

export const ContactText = styled.p`
  margin: 5px 0;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;

  @media (max-width: 768px) {
    flex-direction: column;
    gap: 5px;
  }
`;

export const CopyText = styled.p`
  margin: 0;
  font-size: 12px;
  color: #555;
  margin-top: 10px;
`;