import styled from "styled-components";
import { green } from "../../config/colors";

export const InputContainer = styled.div`
  display: flex;
  flex-direction: column;
  position: relative;
  width: 85%;
  margin-bottom: 1.5rem;
  font-family: 'Poppins', sans-serif;
`;

export const Label = styled.label`
  font-size: 30p6;
  color: #rgba(85, 85, 85, 0.64);
  margin-bottom: 0.3rem;
`;

export const InputWrapper = styled.div`
  position: relative;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ccc;
  transition: border-color 0.3s ease;

  &:focus-within {
    border-color: ${green};
  }
`;

export const Input = styled.input`
  flex: 1;
  border: none;
  outline: none;
  padding: 0.6rem 0;
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