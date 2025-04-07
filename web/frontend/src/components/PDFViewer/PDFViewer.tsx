import React, { RefObject, useEffect, useRef } from "react";
import * as pdfjsLib from "pdfjs-dist";
import type { RenderParameters } from "pdfjs-dist/types/src/display/api";
import styles from "./PDFViewer.module.css"

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url
).toString();

interface PDFViewerProps {
  pdfUrl: string;
  ref: RefObject<HTMLDivElement | null>;
}

const PDFViewer: React.FC<PDFViewerProps> = ({ pdfUrl, ref }) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const loadingTask = pdfjsLib.getDocument(pdfUrl);

    loadingTask.promise
      .then((pdf: pdfjsLib.PDFDocumentProxy) => {
        pdf.getPage(1).then((page: pdfjsLib.PDFPageProxy) => {
          const viewport = page.getViewport({ scale: 1.5 });
          const canvas = canvasRef.current;

          if (!canvas) return;
          const context = canvas.getContext("2d");
          if (!context) return;

          canvas.height = viewport.height;
          canvas.width = viewport.width;

          const renderContext: RenderParameters = {
            canvasContext: context,
            viewport: viewport,
          };

          return page.render(renderContext).promise;
        });
      })
      .catch((error) => {
        console.error("Erro ao carregar o PDF:", error);
      });
  }, [pdfUrl]);

  return (
    <div ref={ref} className={styles["pdf-container"]}>
      <canvas ref={canvasRef}/>
    </div>
  );
};

export default PDFViewer;
