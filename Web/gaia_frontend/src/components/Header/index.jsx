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
          <ProfileText>{user ? user.nome : "Visitante"}</ProfileText>
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
