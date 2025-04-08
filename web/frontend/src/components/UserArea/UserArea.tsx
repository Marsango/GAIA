import styles from "./UserArea.module.css";
import UserAreaHeader from "../UserAreaHeader/UserAreaHeader";
import { useEffect, useRef, useState } from "react";
import PdfJs from "../PDFViewer/PDFViewer";

const array_test = (): Array<string> => {
  const array_testing: Array<string> = [];
  for (let i = 0; i < 100; i++) {
    array_testing.push(`teste${i}`);
  }
  return array_testing;
};

export default function UserArea() {
  const listRef = useRef<HTMLUListElement>(null);
  const sampleContainerRef = useRef<HTMLDivElement>(null);
  const mainContainerRef = useRef<HTMLDivElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const [itemHeight, setItemHeight] = useState(100);
  const [elementsInList, setElementsInList] = useState(0);
  const isScrolling = useRef(false);
  const scrollTimeoutRef = useRef<number | null>(null);
  const pdfViewerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const updateList = () => {
      if (
        sampleContainerRef.current &&
        mainContainerRef.current &&
        headerRef.current
      ) {
        const availableHeight: number =
          mainContainerRef.current.getBoundingClientRect().height -
          headerRef.current.getBoundingClientRect().height -
          48;
        const newElementsInList = Math.floor(availableHeight / 100);
        const newHeight = availableHeight/newElementsInList;

        setElementsInList((prev) => {
          if (prev !== newElementsInList) {
            return newElementsInList;
          }
          return prev;
        });

        setItemHeight((prev) => {
          if (prev !== newHeight){
            return newHeight;
          }
          return prev;
        })

        sampleContainerRef.current.style.height = `${
          newHeight * newElementsInList + 48
        }px`;
        
        if (listRef.current){
          listRef.current.style.gridTemplateRows = `repeat(auto-fill, ${newHeight}px)`;
        }

        if (pdfViewerRef.current) {
          pdfViewerRef.current.style.height = `${
            availableHeight + 48
          }px`;
        }
      }
    };

    updateList();

    window.addEventListener("resize", updateList);

    return () => {
      window.removeEventListener("resize", updateList);
    };
  }, []);

  const handleScrollEnd = () => {
    isScrolling.current = false;
  };

  const onScroll = () => {
    if (scrollTimeoutRef.current) {
      clearTimeout(scrollTimeoutRef.current);
    }
    scrollTimeoutRef.current = setTimeout(handleScrollEnd, 150); // tempo de inatividade
  };

  const scroll = (direction: number) => {
    if (isScrolling.current) {
      return;
    }
    if (listRef.current) {
      isScrolling.current = true;
      listRef.current.scrollTop += direction * itemHeight * elementsInList;
    }
  };

  return (
    <div ref={mainContainerRef} className={styles["main-container"]}>
      <UserAreaHeader headerRef={headerRef}></UserAreaHeader>
      <div className={styles["user-area-body"]}>
        <div ref={sampleContainerRef} className={styles["sample-container"]}>
          <button
            onClick={() => scroll(-1)}
            className={styles["move-button-top"]}
          >
            &and;
          </button>
          <ul
            ref={listRef}
            className={styles["sample-list"]}
            onScroll={onScroll}
          >
            {array_test().map((text: string) => (
              <li>
                <button style={{height: `${itemHeight}px`}}>{text}</button>
              </li>
            ))}
          </ul>
          <button
            onClick={() => scroll(1)}
            className={styles["move-button-bottom"]}
          >
            &or;
          </button>
        </div>
        <PdfJs ref={pdfViewerRef} pdfUrl="src\assets\testing2.pdf"></PdfJs>
      </div>
    </div>
  );
}
