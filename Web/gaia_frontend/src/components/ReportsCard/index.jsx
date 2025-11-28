import React, { useState } from "react";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";
import { IoMdDownload } from "react-icons/io";
import {
  Card,
  Header,
  Conteudo,
  ButtonRow,
  Button,
  Data,
  Divider,
  NumeroAmostra,
} from "./styled";

const ReportCard = ({ data, amostras }) => {
  const [expandido, setExpandido] = useState(false);

  return (
    <Card>
      <Header onClick={() => setExpandido(!expandido)}>
        <Data>
          <strong>Data da coleta:</strong> {data}
        </Data>
        {expandido ? <FaChevronUp /> : <FaChevronDown />}
      </Header>

      <Conteudo $expandido={expandido}>
        {amostras.map((laudo, index) => (
          <React.Fragment key={laudo.id}>
            <div>
              <NumeroAmostra>
                <strong>Número da amostra:</strong> {laudo.numero}
              </NumeroAmostra>

              <ButtonRow>
                <a
                  href={`${laudo.arquivoUrl}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ textDecoration: "none" }}
                >
                  <Button>Visualizar</Button>
                </a>
                <Button
                  onClick={async () => {
                    try {
                      const response = await fetch(laudo.arquivoUrl, {
                        method: "GET",
                        headers: {
                          Authorization: `Bearer ${localStorage.getItem(
                            "token"
                          )}`,
                        },
                      });

                      const blob = await response.blob();
                      const url = window.URL.createObjectURL(blob);

                      const link = document.createElement("a");
                      link.href = url;
                      link.download = laudo.arquivoUrl.split("/").pop(); // nome do arquivo
                      document.body.appendChild(link);
                      link.click();
                      document.body.removeChild(link);
                    } catch (error) {
                      console.error("Erro ao baixar o PDF:", error);
                    }
                  }}
                >
                  Baixar <IoMdDownload size={20} />
                </Button>
              </ButtonRow>
            </div>
            {index < amostras.length - 1 && <Divider />}
          </React.Fragment>
        ))}
      </Conteudo>
    </Card>
  );
};

export default ReportCard;
