import React, { useState } from "react";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";
import { IoMdDownload } from "react-icons/io";
import api from "../../api/api";
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

  const formatarDataBR = (dataString) => {
    // Se já estiver no formato BR, retorna como está
    if (dataString && dataString.includes("/")) {
      return dataString;
    }

    try {
      // Converte YYYY-MM-DD para DD/MM/YYYY
      if (dataString && dataString.includes("-")) {
        const [ano, mes, dia] = dataString.split("-");
        return `${dia}/${mes}/${ano}`;
      }

      // Tenta converter data ISO
      const date = new Date(dataString);
      if (!isNaN(date.getTime())) {
        return date.toLocaleDateString("pt-BR");
      }

      return dataString || "Data não disponível";
    } catch {
      return dataString || "Data não disponível";
    }
  };

  return (
    <Card>
      <Header onClick={() => setExpandido(!expandido)}>
        <Data>
          <strong>Data da coleta:</strong> {formatarDataBR(data)}
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

              {laudo.arquivoUrl ? (
                <ButtonRow>
                  <a
                    href={laudo.arquivoUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ textDecoration: "none" }}
                  >
                    <Button>Visualizar</Button>
                  </a>
                  <Button
                    onClick={async () => {
                      try {
                        // ✅ NOVO: Usar axios/api com httpOnly cookies ao invés de fetch manual
                        const response = await api.get(laudo.arquivoUrl, {
                          responseType: "blob",
                        });

                        const blob = response.data;
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
              ) : (
                <p style={{ color: "#999", fontSize: "14px" }}>
                  📄 Laudo ainda não possui arquivo PDF anexado
                </p>
              )}
            </div>
            {index < amostras.length - 1 && <Divider />}
          </React.Fragment>
        ))}
      </Conteudo>
    </Card>
  );
};

export default ReportCard;
