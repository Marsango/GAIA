import styled from "styled-components";
import {gray, black} from "../../config/colors"

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
  margin-left: auto;
  height: 70px;
  display: flex;
  justify-content: end;
  align-items: center;
  padding-right: 20px;
`;

export const ProfileText = styled.span`
  font-size: 20px;
  color: ${black};
  margin-left: 8px;
  font-family: Poppins, sans-serif;
  align-self: center;
`;
