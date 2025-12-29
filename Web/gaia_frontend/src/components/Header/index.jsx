import Logo_lab_Branco from "../../assets/images/Logo_lab_Branco.svg";
import { Logo, HeaderContainer, ProfileIcon, ProfileText } from "./styled.js";
import { CgProfile } from "react-icons/cg";

export default function Header() {
  const userRaw = localStorage.getItem("user");
  let user = null;

  try {
    user = userRaw ? JSON.parse(userRaw) : null;
  } catch (error) {
    console.error("Erro ao parsear user:", error);
    // Limpa o localStorage se o dado estiver corrompido
    localStorage.removeItem("user");
  }
  return (
    <HeaderContainer>
      <Logo src={Logo_lab_Branco} alt="Logo" />
      <ProfileIcon>
        <CgProfile size={60} />
        <ProfileText>
          {user ? `${user.first_name} ${user.last_name}` : "visitante"}
        </ProfileText>
      </ProfileIcon>
    </HeaderContainer>
  );
}
