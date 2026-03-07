import styled from "styled-components";
import { gray, black, green } from "../../config/colors";

export const HeaderContainer = styled.header`
  width: 100%;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background-color: ${gray};
  flex-wrap: wrap;
  gap: 15px;

  @media (max-width: 600px) {
    flex-direction: column;
    justify-content: center;
    padding: 15px;
  }
`;

export const Logo = styled.img`
  height: 70px;
  @media (max-width: 600px) { height: 50px; }
`;

export const ProfileIcon = styled.div`
  display: flex;
  align-items: center;
  margin-left: 35px;

  @media (max-width: 600px) {
    margin-left: 0;
  }
`;

export const ProfileText = styled.span`
  font-size: 26px;
  color: ${black};
  margin-left: 12px;
  font-family: 'Poppins', sans-serif !important;

  @media (max-width: 600px) {
    font-size: 16px; /* Reduzi de 20px para 16px no celular! */
  }
`;

export const ButtonGroup = styled.div`
  display: flex;
  gap: 10px;
  margin-right: 35px;

  @media (max-width: 600px) {
    width: 100%;
    margin-right: 0;
  }
`;

export const ChangePasswordButton = styled.button`
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 44px;
  padding: 10px 20px;
  background: #2196f3;
  border: 2px solid white;
  color: white;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  justify-content: center;
  
  &:hover { background: white; color: #2196f3; }
  &:active { transform: scale(0.98); }
  &:focus-visible {
    outline: 3px solid ${black};
    outline-offset: 2px;
  }

  @media (max-width: 600px) {
    flex: 1; padding: 8px 10px; font-size: 14px;
  }
`;

export const LogoutButton = styled.button`
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 44px;
  padding: 10px 20px;
  background: ${green};
  border: 2px solid white;
  color: white;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  justify-content: center;
  
  &:hover { background: white; color: #2e7d32; }
  &:active { transform: scale(0.98); }
  &:focus-visible {
    outline: 3px solid ${black};
    outline-offset: 2px;
  }

  @media (max-width: 600px) {
    flex: 1; padding: 8px 10px; font-size: 14px; width: auto;
  }
`;