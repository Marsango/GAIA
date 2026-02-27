import { useState } from "react";
import {
  Logo,
  HeaderContainer,
  ProfileIcon,
  ProfileText,
  LogoutButton,
  ChangePasswordButton,
  ButtonGroup 
} from "./styled.js";
import { CgProfile, CgLogOut } from "react-icons/cg";
import { MdVpnKey } from "react-icons/md";
import { useNavigate } from "react-router-dom";
import LogoutModal from "../LogoutModal"; 

export default function Header() {
  const navigate = useNavigate();
  const [showLogoutModal, setShowLogoutModal] = useState(false);
  const [logoutLoading, setLogoutLoading] = useState(false);

  const userRaw = localStorage.getItem("user");
  let user = null;
  try {
    user = userRaw ? JSON.parse(userRaw) : null;
  } catch (error) {
    localStorage.removeItem("user");
  }

  const handleLogoutClick = () => setShowLogoutModal(true);

  const handleLogout = async () => {
    setLogoutLoading(true);
    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      localStorage.removeItem("token");
      localStorage.removeItem("refresh");
      localStorage.removeItem("user");
      setShowLogoutModal(false);
      navigate("/login");
    } finally {
      setLogoutLoading(false);
    }
  };

  return (
    <>
      <HeaderContainer>
        <ProfileIcon>
          <CgProfile size={50} /> 
          <ProfileText>
            {user ? `${user.first_name} ${user.last_name}` : "Visitante"}
          </ProfileText>
        </ProfileIcon>
        <ButtonGroup>
          <ChangePasswordButton onClick={() => navigate("/change-password")}>
            <MdVpnKey size={20} />
            Alterar Senha
          </ChangePasswordButton>
          <LogoutButton onClick={handleLogoutClick}>
            <CgLogOut size={20} />
            Sair
          </LogoutButton>
        </ButtonGroup>
      </HeaderContainer>
      <LogoutModal isOpen={showLogoutModal} onClose={() => !logoutLoading && setShowLogoutModal(false)} onConfirm={handleLogout} loading={logoutLoading} />
    </>
  );
}