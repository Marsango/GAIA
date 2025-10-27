import Logo_lab_Branco from "../../assets/images/Logo_lab_Branco.svg";
import { Logo, HeaderContainer, ProfileIcon, ProfileText } from "./styled.js";
import { CgProfile } from "react-icons/cg";

export default function Header() {
  return (
    <HeaderContainer>
      <Logo src={Logo_lab_Branco} alt="Logo" />
      <ProfileIcon>
        <CgProfile size={60} />
        <ProfileText>Bruno Nunes</ProfileText>
      </ProfileIcon>
    </HeaderContainer>
  );
}
