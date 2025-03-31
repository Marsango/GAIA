import React, { useState } from "react";
import styles from "./LoginForm.module.css";

export default function LoginForm() {
  const [user, setUser] = useState("");
  const [password, setPassword] = useState("");
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    console.log(user);
    console.log(password);
  };
  return (
    <form onSubmit={(e) => handleSubmit(e)} className={styles["login-form"]}>
      <input
        placeholder={"Usuário"}
        type={"text"}
        id={"user"}
        value={user}
        onChange={(e) => setUser(e.target.value)}
      ></input>
      <input
        placeholder={"Senha"}
        type={"password"}
        id={"password"}
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      ></input>
      <button className="submit-button">LOGIN</button>
    </form>
  );
}
