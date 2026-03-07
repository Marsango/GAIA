import styled from "styled-components";
import { green, white, gray, black } from "../../config/colors";

export const FullPageContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: ${gray};
  width: 100%;
  overflow-x: hidden; /* Trava mestre: corta o que tentar vazar da tela */
`;

export const PageContainer = styled.div`
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  flex: 1;
  box-sizing: border-box; /* Garante que o padding fique pra dentro */

  @media (max-width: 600px) {
    padding: 10px; /* Menos margem no celular para aproveitar a tela */
  }
`;

export const Title = styled.h1`
  text-align: center;
  color: ${green};
  font-family: 'Poppins', sans-serif;
  margin-bottom: 30px;
  
  @media (max-width: 600px) {
    font-size: 24px;
    margin-bottom: 20px;
  }
`;

export const Content = styled.div`
  display: flex;
  gap: 20px;
  width: 100%;
  box-sizing: border-box;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

export const Properties = styled.div`
  flex: 1;
  background: ${white};
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  
  /* Travas anti-vazamento no mobile */
  width: 100%;
  min-width: 0; 
  box-sizing: border-box;

  @media (max-width: 600px) {
    padding: 15px;
  }
`;

export const Reports = styled.div`
  flex: 2;
  background: ${white};
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  
  /* Travas anti-vazamento no mobile */
  width: 100%;
  min-width: 0; 
  box-sizing: border-box;

  @media (max-width: 600px) {
    padding: 15px;
  }
`;

export const ReportList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

export const Subtitle = styled.h2`
  color: ${black};
  font-size: 1.5rem;
  border-bottom: 2px solid ${green};
  padding-bottom: 10px;
  margin-bottom: 20px;
  font-family: 'Poppins', sans-serif;

  @media (max-width: 600px) {
    font-size: 1.2rem;
  }
`;

export const AdminButton = styled.button`
  display: block;
  margin: 0 auto 20px auto;
  min-height: 44px;
  padding: 10px 20px;
  background-color: #ffc107;
  color: #000;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
  font-size: 16px;
  transition: 0.3s;

  &:hover {
    background-color: #e0a800;
  }

  &:focus-visible {
    outline: 3px solid ${black};
    outline-offset: 2px;
  }
`;