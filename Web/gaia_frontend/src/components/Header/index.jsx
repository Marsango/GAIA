import { useState } from "react"; // ← ADICIONE ESTA LINHA
import Logo_lab_Branco from "../../assets/images/Logo_lab_Branco.svg";
import {
  Logo,
  HeaderContainer,
  ProfileIcon,
  ProfileText,
  LogoutButton,
  ChangePasswordButton,
} from "./styled.js";
import { CgProfile, CgLogOut } from "react-icons/cg";
import { MdVpnKey } from "react-icons/md";
import { useNavigate } from "react-router-dom";
import LogoutModal from "../LogoutModal"; // Certifique-se que o caminho está correto

export default function Header() {
  const navigate = useNavigate();
  const [showLogoutModal, setShowLogoutModal] = useState(false);
  const [logoutLoading, setLogoutLoading] = useState(false);

  const userRaw = localStorage.getItem("user");
  let user = null;
  try {
    user = userRaw ? JSON.parse(userRaw) : null;
  } catch (error) {
    console.error("Erro ao parsear user:", error);
    localStorage.removeItem("user");
  }

  // Função que abre o modal
  const handleLogoutClick = () => {
    setShowLogoutModal(true);
  };

  // Função que executa o logout (chamada pelo modal)
  const handleLogout = async () => {
    setLogoutLoading(true);

    try {
      // Simula um delay para mostrar loading (opcional)
      await new Promise((resolve) => setTimeout(resolve, 500));

      // Remove todos os dados do localStorage
      localStorage.removeItem("token");
      localStorage.removeItem("refresh");
      localStorage.removeItem("user");

      // Fecha modal
      setShowLogoutModal(false);

      // Redireciona para login
      navigate("/login");
    } catch (error) {
      console.error("Erro ao fazer logout:", error);
    } finally {
      setLogoutLoading(false);
    }
  };

  return (
    <>
      <HeaderContainer>
        {/* <Logo src={Logo_lab_Branco} alt="Logo" /> */}

        <ProfileIcon>
          <CgProfile size={60} />
          <ProfileText>
            {user ? `${user.first_name} ${user.last_name}` : "Visitante"}
          </ProfileText>
        </ProfileIcon>

        {/* Botão para alterar senha */}
        <ChangePasswordButton onClick={() => navigate("/change-password")}>
          <MdVpnKey size={24} />
          Alterar Senha
        </ChangePasswordButton>

        {/* Botão abre o modal, não faz logout direto */}
        <LogoutButton onClick={handleLogoutClick}>
          <CgLogOut size={24} />
          Sair
        </LogoutButton>
      </HeaderContainer>

      {/* Modal de confirmação */}
      <LogoutModal
        isOpen={showLogoutModal}
        onClose={() => !logoutLoading && setShowLogoutModal(false)}
        onConfirm={handleLogout}
        loading={logoutLoading}
      />
    </>
  );
}
