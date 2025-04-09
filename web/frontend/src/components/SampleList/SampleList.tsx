import { useState, useRef, useEffect } from "react";
import styles from "./SampleList.module.css";


const array_test = (): Array<string> => {
  const array_testing: Array<string> = [];
  for (let i = 0; i < 100; i++) {
    array_testing.push(`teste${i}`);
  }
  return array_testing;
};

type SampleListProps = {
    availableHeight: number;
};

export default function SampleList({
    availableHeight
}: SampleListProps) {
  const listRef = useRef<HTMLUListElement>(null);
  const sampleContainerRef = useRef<HTMLDivElement>(null);
  const [itemHeight, setItemHeight] = useState(100);
  const [elementsInList, setElementsInList] = useState(0);
  const isScrolling = useRef(false);
  const scrollTimeoutRef = useRef<number | null>(null);
  const [activeSample, setActiveSample] = useState(0);

  useEffect(() => {
    const updateList = () => {
      if (
        availableHeight
      ) {
        const newElementsInList = Math.floor(availableHeight / 100);
        const newHeight = availableHeight / newElementsInList;

        setElementsInList((prev) => {
          if (prev !== newElementsInList) {
            return newElementsInList;
          }
          return prev;
        });

        setItemHeight((prev) => {
          if (prev !== newHeight) {
            return newHeight;
          }
          return prev;
        });
        if (sampleContainerRef.current){
            sampleContainerRef.current.style.height = `${
                newHeight * newElementsInList + 48
              }px`;
        }

        if (listRef.current) {
          listRef.current.style.gridTemplateRows = `repeat(auto-fill, ${newHeight}px)`;
        }
      }
    };
    updateList();

    window.addEventListener("resize", updateList);

    return () => {
      window.removeEventListener("resize", updateList);
    };
  });
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
    <div ref={sampleContainerRef} className={styles["sample-container"]}>
      <button onClick={() => scroll(-1)} className={styles["move-button-top"]}>
        &and;
      </button>
      <ul ref={listRef} className={styles["sample-list"]} onScroll={onScroll}>
        {array_test().map((text: string, index: number) => (
          <li>
            <button key={index} onClick={(() => setActiveSample(index))} className={`${styles['sample-button']} ${activeSample === index ? styles["active"] : ""}`} style={{ height: `${itemHeight}px` }}>{text}
            </button>
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
  );
}
