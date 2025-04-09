import styles from "./UserAreaHeader.module.css"
import { RefObject } from 'react'

type UserAreaHeaderProps = {
    headerRef: RefObject<HTMLDivElement | null>
    setActiveButton: React.Dispatch<React.SetStateAction<number>>;
    activeButton: number;
}

export default function UserAreaHeader( {headerRef, setActiveButton, activeButton}: UserAreaHeaderProps ){
    const buttonsText = ['Laudos', 'Minha conta'];

    return (
        <div ref={headerRef} className={styles["header-container"]}>
            <div className={styles["left-side"]}>Laboratório de Solos da UTFPR</div>
            <div className={styles["right-side"]}>
                <button className={`${styles["header-button"]} ${styles["download"]}`} style={{visibility: `${activeButton === 0 ? 'visible' : 'hidden'}`}}>Download</button>
                {buttonsText.map((buttonText, index) => <button key={index} onClick={() => setActiveButton(index)} className={`${styles["header-button"]} ${activeButton === index ? styles["active"] : ""}`}>{buttonText}</button>)}
                <div>Bem-vindo, fulano!</div>
            </div>
        </div>
    )
}