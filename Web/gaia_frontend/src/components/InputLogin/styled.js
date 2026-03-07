import styled from "styled-components";
import { green } from "../../config/colors";

export const InputContainer = styled.div`
  display: flex;
  flex-direction: column;
  position: relative;
  width: 100%;
  margin-bottom: 1.5rem;
  font-family: 'Poppins', sans-serif;
`;

export const Label = styled.label`
  font-size: 1rem;
  color: rgba(85, 85, 85, 0.9);
  font-weight: 500;
  margin-bottom: 0.3rem;
`;

export const InputWrapper = styled.div`
  position: relative;
  display: flex;
  align-items: center;
  min-height: 44px;
  border-bottom: 1px solid ${props => props.$hasError ? '#ff6b6b' : '#ccc'};
  transition: border-color 0.3s ease;

  &:focus-within {
    border-color: ${green};
    box-shadow: 0 2px 0 0 ${green};
  }
`;

export const ErrorText = styled.span`
  color: #d32f2f;
  font-size: 0.9rem;
  margin-top: 0.2rem;
  display: block;
  text-align: left;
`;

export const Input = styled.input`
  flex: 1;
  border: none;
  outline: none;
  padding: 0.8rem 0;
  font-size: 1rem;
  color: #333;
  background: transparent;
`;

export const Icon = styled.div`
  cursor: pointer;
  color: #888;
  position: absolute;
  right: 0; 
  display: flex;
  align-items: center;
  height: 100%;
`;