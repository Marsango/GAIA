import styled from 'styled-components';

export const Container = styled.div`
  padding: 40px;
  background-color: #2E2E2E;
  min-height: 100vh;
  color: white;
`;

export const Title = styled.h1`
  margin-bottom: 30px;
  border-bottom: 2px solid #444;
  padding-bottom: 10px;
`;

export const TabContainer = styled.div`
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
`;

export const TabButton = styled.button`
  padding: 10px 20px;
  background-color: ${props => props.$active ? '#28a745' : '#444'};
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-weight: bold;
  &:hover { background-color: ${props => props.$active ? '#218838' : '#555'}; }
`;

export const FormBox = styled.div`
  background-color: #3C3C3C;
  padding: 30px;
  border-radius: 8px;
  max-width: 600px;
`;

export const InputGroup = styled.div`
  margin-bottom: 15px;
  label { display: block; margin-bottom: 5px; color: #ccc; }
  input, textarea {
    width: 100%; padding: 10px; border-radius: 5px; border: none;
    background-color: #555; color: white;
  }
  textarea { height: 150px; resize: vertical; }
`;

export const ActionButton = styled.button`
  background-color: #007bff;
  color: white; padding: 12px 20px; border: none; border-radius: 5px;
  cursor: pointer; font-size: 1rem; font-weight: bold; width: 100%;
  &:hover { background-color: #0056b3; }
  &:disabled { background-color: #555; cursor: not-allowed; }
`;

export const Message = styled.div`
  margin-top: 15px;
  padding: 10px;
  border-radius: 5px;
  background-color: ${props => props.$error ? '#ff4d4d' : '#28a745'};
  color: white; text-align: center;
`;