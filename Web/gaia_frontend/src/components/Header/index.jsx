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
import LogoutModal from "../LogoutModal"; // Certifique-se que o caminho está correto
import api from "../../api/api"; // ← ADICIONE IMPORTAÇÃO

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
      // 1. PRIMEIRO: Chamar endpoint de logout no servidor
      //    Backend vai limpar os httpOnly cookies e sessão
      try {
        await api.post("logout/");
        console.log("✓ Logout no servidor realizado");
      } catch (e) {
        console.error("⚠ Erro ao fazer logout no servidor:", e.message);
        // Continua mesmo com erro (logout local sempre funciona)
      }

      // 2. DEPOIS: Limpar dados locais (user data - não-sensível)
      localStorage.removeItem("user");
      console.log("✓ Dados locais limpos");

      // Simula um delay para mostrar loading (opcional)
      await new Promise((resolve) => setTimeout(resolve, 300));

      // Fecha modal
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