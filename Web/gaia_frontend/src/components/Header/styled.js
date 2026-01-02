import styled from "styled-components";
import {gray, black, green} from "../../config/colors"

export const HeaderContainer = styled.header`
  width: 100%;
  display: flex;
  align-items: flex-start;
  padding: 16px;
  background-color: ${gray};
`;

export const Logo = styled.img`
  height: 70px;
  justify-self: flex-start;
  padding-left: 4px;
`;

export const ProfileIcon = styled.div`
  margin-left: 36px;
  height: 70px;
  display: flex;
  justify-self: flex-start;
  align-items: center;
  padding-right: 20px;
`;

export const ProfileText = styled.span`
  font-size: 26px;
  color: ${black};
  margin-left: 8px;
  font-family: 'Poppins', sans-serif !important;
  align-self: center;
`;

export const LogoutButton = styled.button`
  display: flex;
  margin-left: auto;
  align-items: center;
  align-self: center;
  gap: 3px;
  padding: 10px 20px;
  background: ${green};
  border: 2px solid white;
  color: white;
  border-radius: 6px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 160px;
  justify-content: center;
  
  &:hover {
    background: white;
    color: #2e7d32;
  }
  
  &:active {
    transform: scale(0.98);
  }
`;