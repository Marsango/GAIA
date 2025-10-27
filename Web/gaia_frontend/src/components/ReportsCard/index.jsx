import React, { useState } from "react";
import { FaChevronDown, FaChevronUp } from "react-icons/fa";
import { IoMdDownload } from "react-icons/io";
import { Card, Header, Conteudo, ButtonRow, Button, Data } from "./styled";

const ReportCard = ({ laudo }) => {
  const [expandido, setExpandido] = useState(false);

  return (
    <Card>
      <Header onClick={() => setExpandido(!expandido)}>
        <Data>
          <strong>Número da amostra:</strong> {laudo.amostra} <br />
          <small>Data da coleta: {laudo.data}</small>
        </Data>
        {expandido ? <FaChevronUp /> : <FaChevronDown />}
      </Header>

      <Conteudo $expandido={expandido}>
        <ButtonRow>
          <a
            href={laudo.arquivoUrl}
            target="_blank"
            rel="noopener noreferrer"
            style={{ textDecoration: "none" }}
          >
            <Button>Visualizar</Button>
          </a>
          <Button $secundario>
            Baixar <IoMdDownload size={20} />
          </Button>
        </ButtonRow>
      </Conteudo>
    </Card>
  );
};

export default ReportCard;
