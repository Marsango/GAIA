import styles from "./ContentContainer.module.css"
import LoginForm from "../LoginForm/LoginForm.js"

export default function ContentContainer(){
    return (
        <div className={styles["content-container"]}>
            <div className={styles["left-content"]}>
            <h1>Entrar</h1>
            <LoginForm></LoginForm>
            </div>
            <div className={styles["right-content"]}>
            <img src={"UTFPR_logo.svg.png"} ></img>
            </div>
        </div>
    )
}