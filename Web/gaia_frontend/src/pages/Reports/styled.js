import styled from "styled-components";

export const FullPageContainer = styled.div`
  font-family: "K2D", sans-serif;
  color: #222;
`;

export const Title = styled.h1`
  text-align: center;
  margin-bottom: 1rem;
  padding-bottom: 40px;
`;

export const Content = styled.div`
  display: flex;
  justify-content: center;
  align-items: start;
  background-color: #f9f9f9;
  height: 450px;
  width: fit-content;
  margin: 0 auto;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #2e7d32;
`;

export const Properties = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 450px; /* altura máxima visível */
  overflow-y: auto;
  padding-right: 10px; /* evita o texto encostar na barra */

  width: 450px;
`;

export const Reports = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

export const ReportList = styled.div`
  overflow-y: auto;
  max-height: 400px;
  padding-right: 10px;
  height: 450px;
`;

export const PageContainer = styled.div`
  padding: 20px;
  padding-left: 40px;
  padding-right: 40px;
`;

export const Subtitle = styled.h3`
  font-weight: 600;
  font-size: 1.5rem;
  color: #333;
  font-family: "Poppins", sans-serif;
`;
