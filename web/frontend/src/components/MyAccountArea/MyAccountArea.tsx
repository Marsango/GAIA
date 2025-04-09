import { useState } from "react";
import styles from "./MyAccountArea.module.css";

export default function MyAccountArea() {
  const [user, setUser] = useState("marsango");
  const [password, setPassword] = useState("teste");
  const [cpf, setCpf] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [cep, setCep] = useState("");

  const handleCpfChange = (e) => {
    let value = e.target.value.replace(/\D/g, "");

    if (value.length > 11) value = value.slice(0, 11);

    value = value.replace(/(\d{3})(\d)/, "$1.$2");
    value = value.replace(/(\d{3})(\d)/, "$1.$2");
    value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

    setCpf(value);
  };

  const handlePhoneNumberChange = (e) => {
    let value = e.target.value.replace(/\D/g, "");

    value = value.replace(/(\d{2})(\d)/, "($1)$2");
    value = value.replace(/\)(\d{1})/, ") $1");
    value = value.replace(/(\d{5})(\d{4})$/, "$1-$2");

    setPhoneNumber(value);
  };

  const currentDate = () => {
    const date = new Date();
    var day = date.getDate().toString();
    var month = date.getMonth().toString();
    const year = date.getFullYear();
    if (Number(day) < 10) {
      day = "0" + day;
    }
    if (Number(month) < 10) {
      month = "0" + month;
    }
    return `${year}-${month}-${day}`;
  };

  const handleCepChange = (e) => {
    let value = e.target.value.replace(/\D/g, "");

    value = value.replace(/(\d{5})(\d{3})$/, "$1-$2");

    setCep(value);
  }

  return (
    <form className={styles["form-container"]}>
      <div className={styles["left-side"]}>
        <div className={styles["label-container"]}>
          <p className={styles["information-title"]}>Informações Gerais</p>
        </div>

        <div className={styles["label-container"]}>
          <label htmlFor="name">Nome:</label>
          <input id="name" placeholder="Nome" />
        </div>

        <div className={styles["label-container"]}>
          <label htmlFor="email">Email:</label>
          <input id="email" type="email" placeholder="Email" />
        </div>

        <div className={styles["label-container"]}>
          <label htmlFor="cpf">CPF</label>
          <input
            id="cpf"
            placeholder="000.000.000-00"
            value={cpf}
            onChange={handleCpfChange}
          />
        </div>

        <div className={styles["label-container"]}>
          <label htmlFor="birthDate">Data de Nascimento:</label>
          <input id="birthDate" type="date" max={currentDate()} />
        </div>

        <div className={styles["label-container"]}>
          <label htmlFor="phoneNumber">Telefone:</label>
          <input
            id="phoneNumber"
            type="tel"
            value={phoneNumber}
            onChange={handlePhoneNumberChange}
            placeholder="(00) 00000-0000"
          />
        </div>
      </div>
      <div className={styles["right-side"]}>
        <div className={styles["label-container"]}>
          <p className={styles["information-title"]}>Endereço</p>
        </div>

        <div className={styles["label-container"]}>
          <label htmlFor="country">País:</label>
          <input id="country" placeholder="País" />
        </div>

        <div className={styles["label-container"]}>
          <label htmlFor="state">Estado:</label>
          <input id="state" placeholder="Estado" />
        </div>

        <div className={styles["label-container"]}>
          <label htmlFor="city">Cidade:</label>
          <input
            id="city"
            placeholder="Cidade"
          />
        </div>

        <div className={styles["label-container"]}>
          <label htmlFor="cep">CEP:</label>
          <input id="cep" placeholder="00000-000" value={cep} onChange={handleCepChange}/>
        </div>

        <div className={styles["double-label-container"]}>
        <div className={styles["label-container"]}>          <label htmlFor="street">Rua</label>
          <input
            id="street"
            placeholder="Rua"
          /></div>
        <div className={styles["label-container"] + " " + styles["label-container-right"]}>          <label htmlFor="streetNumber">Número</label>
          <input
            id="streetNumber"
            type="text"
            placeholder="Número"
          /></div>

        </div>
        <button className={styles["submit-button"]}>Salvar alterações</button>
      </div>
    </form>
  );
}
