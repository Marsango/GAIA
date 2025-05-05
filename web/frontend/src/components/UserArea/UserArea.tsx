import styles from "./UserArea.module.css";
import UserAreaHeader from "../UserAreaHeader/UserAreaHeader";
import { useEffect, useRef, useState } from "react";
import PDFViewer from "../PDFViewer/PDFViewer";
import SampleList from "../SampleList/SampleList";
import MyAccountArea from "../MyAccountArea/MyAccountArea";

export default function UserArea() {
  const mainContainerRef = useRef<HTMLDivElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const pdfViewerRef = useRef<HTMLDivElement>(null);
  const [activeButton, setActiveButton] = useState(0);
  const [availableHeight, setAvailableHeight] = useState(0);

  useEffect(() => {

    const updateList = () => {
      if (
        mainContainerRef.current &&
        headerRef.current
      ) {
        const newAvailableHeight: number =
          mainContainerRef.current.getBoundingClientRect().height -
          headerRef.current.getBoundingClientRect().height -
          48;

        setAvailableHeight(newAvailableHeight);

        if (pdfViewerRef.current) {
          pdfViewerRef.current.style.height = `${
            newAvailableHeight + 48
          }px`;
        }
      }
    };

    if (activeButton === 0) {
      updateList();
    }

    window.addEventListener("resize", updateList);

    return () => {
      window.removeEventListener("resize", updateList);
    };
  }, [activeButton]);


  return (
    <div ref={mainContainerRef} className={styles["main-container"]}>
      <UserAreaHeader setActiveButton={setActiveButton} activeButton={activeButton} headerRef={headerRef}></UserAreaHeader>
      {activeButton === 0 ? <div className={styles["user-area-body"]}>
        <SampleList availableHeight={availableHeight}></SampleList>
        <PDFViewer ref={pdfViewerRef} pdfUrl="src\assets\testing2.pdf"></PDFViewer>
      </div> : <MyAccountArea></MyAccountArea>} 
    </div>
  );
}
