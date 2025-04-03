import styles from "./UserAreaHeader.module.css"

export default function UserAreaHeader( {headerRef} ){
    return (
        <div ref={headerRef} className={styles["header-container"]}>
            <div className={styles["left-side"]}>Laboratório de Solos da UTFPR</div>
            <div className={styles["right-side"]}>
                <button className={styles["header-button"]}>Laudos</button>
                <button className={styles["header-button"]}>Contato</button>
                <button className={styles["header-button"]}>Minha conta</button>
            </div>
        </div>
    )
}