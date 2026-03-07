import styled from "styled-components";
import { gray, black } from "../../config/colors";

export const FooterContainer = styled.footer`
  width: 100%;
  box-sizing: border-box;
  background-color: ${gray};
  color: ${black};
  text-align: center;
  padding: 16px 12px;
  font-family: 'Poppins', sans-serif;
  border-top: 1px solid #ccc;
  overflow-wrap: anywhere;
  
  /* Garante que o footer não encolha num layout flex */
  flex-shrink: 0; 

  @media (min-width: 768px) {
    padding: 20px;
  }
`;

export const ContactText = styled.p`
  margin: 5px 0;
  font-size: 16px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;

  .separator {
    color: #777;
  }

  span {
    white-space: normal;
    word-break: break-word;
  }

  .icon {
    display: inline-block;
    font-size: clamp(16px, 2.4vw, 22px);
    line-height: 1;
    margin-right: 6px;
    vertical-align: -2px;
  }

  @media (min-width: 1024px) {
    font-size: 20px;
    gap: 15px;
  }

  @media (max-width: 768px) {
    flex-direction: column;
    gap: 6px;
    font-size: 18px;

    .separator {
      display: none;
    }

    .icon {
      font-size: 15px;
      margin-right: 4px;
      vertical-align: -1px;
    }
  }
`;

export const CopyText = styled.p`
  margin: 0;
  font-size: 11px;
  color: #555;
  margin-top: 10px;
  line-height: 1.4;

  @media (min-width: 768px) {
    font-size: 12px;
  }
`;