import styles from "./UserArea.module.css";
import UserAreaHeader from "../UserAreaHeader/UserAreaHeader";
import { useEffect, useRef, useState } from "react";

const array_test = (): Array<string> => {
  const array_testing: Array<string> = [];
  for (let i = 0; i < 13; i++) {
    array_testing.push(`teste${i}`);
  }
  return array_testing;
};

export default function UserArea() {
  const listRef = useRef<HTMLUListElement>(null);
  const sampleContainerRef = useRef<HTMLDivElement>(null);
  const mainContainerRef = useRef<HTMLDivElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const itemHeight = 100;
  const [elementsInList, setElementsInList] = useState(0);

  useEffect(() => {
    const updateList = () => {
      if (sampleContainerRef.current && mainContainerRef.current && headerRef.current){
        const availableHeight: number = mainContainerRef.current.getBoundingClientRect().height - headerRef.current.getBoundingClientRect().height - 20 - 48;
        const newElementsInList = Math.floor(availableHeight / itemHeight);

        setElementsInList((prev) => {
          if (prev !== newElementsInList) {
            return newElementsInList;
          }
          return prev;
        });

        sampleContainerRef.current.style.height = `${Math.floor(availableHeight/100) * 100 + 48}px`;
      }
    };

    updateList();

    window.addEventListener('resize', updateList);

    return () => {
      window.removeEventListener('resize', updateList);
    };

  }, [])

  const scroll = (direction: number) => {
    if (listRef.current) {
      listRef.current.scrollTop += direction * itemHeight * elementsInList;
    }
  };

  return (
    <div ref={mainContainerRef} className={styles["main-container"]}>
      <UserAreaHeader headerRef={headerRef}></UserAreaHeader>
      <div ref={sampleContainerRef} className={styles["sample-container"]}>
        <button
          onClick={() => scroll(-1)}
          className={styles["move-button-top"]}
        >
          &and;
        </button>
        <ul ref={listRef} className={styles["sample-list"]}>
          {array_test().map((text: string) => (
            <li>
              <button>{text}</button>
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
    </div>
  );
}
