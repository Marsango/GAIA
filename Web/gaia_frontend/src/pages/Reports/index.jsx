import React, { useEffect, useState } from "react";
import axios from "axios";
import Header from "../../components/Header";
import PropertiesCard from "../../components/PropertiesCard";
import ReportsCard from "../../components/ReportsCard";
import api from "../../api/api";
import {
  PageContainer,
  Title,
  Content,
  Properties,
  Reports,
  ReportList,
  FullPageContainer,
  Subtitle,
} from "./styled";

const CentralLaudos = () => {
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [propriedades, setPropriedades] = useState([]);
  const [laudos, setLaudos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const token = localStorage.getItem("token");

  useEffect(() => {
    carregarPropriedades();
  }, []);

  const carregarPropriedades = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await api.get("propriedades/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setPropriedades(response.data.results || []);
      if (response.data.results?.length > 0) {
        setSelectedProperty(response.data.results[0].id);
      }
    } catch (error) {
      console.error("Erro ao carregar propriedades:", error);
      setError("Não foi possível carregar as propriedades.");
    }
  };

  useEffect(() => {
    if (selectedProperty) {
      carregarLaudos(selectedProperty);
    }
  }, [selectedProperty]);

  const carregarLaudos = async (propriedadeId) => {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.get(
        `http://localhost:8000/api/laudos/por_propriedade/?propriedade_id=${propriedadeId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setLaudos(response.data); // <-- SÓ OS LAUDOS DA PROPRIEDADE
    } catch (error) {
      console.error("Erro ao carregar laudos:", error);
    }
  };

  const agruparPorData = (laudos) => {
    return laudos.reduce((acc, laudo) => {
      const data = laudo.data_coleta;

      if (!acc[data]) acc[data] = [];
      acc[data].push(laudo);

      return acc;
    }, {});
  };

  return (
    <FullPageContainer>
      <Header />
      <PageContainer>
        <Title>Central de Laudos</Title>
        <Content>
          <Properties>
            <Subtitle>Propriedades</Subtitle>
            {Array.isArray(propriedades) && propriedades.length > 0 ? (
              propriedades.map((propriedade) => (
                <PropertiesCard
                  key={propriedade.id}
                  nome={propriedade.nome}
                  local={propriedade.localizacao}
                  ativo={propriedade.id === selectedProperty}
                  onClick={() => setSelectedProperty(propriedade.id)}
                />
              ))
            ) : (
              <p>Nenhuma propriedade encontrada</p>
            )}
          </Properties>

          <Reports>
            <Subtitle>Laudos</Subtitle>
            <ReportList>
              {Object.entries(agruparPorData(laudos)).map(
                ([data, laudosDoDia]) => (
                  <ReportsCard
                    key={data}
                    data={data}
                    amostras={laudosDoDia.map((l) => ({
                      id: l.id,
                      numero: l.numero_amostra,
                      arquivoUrl: `${l.arquivo_pdf}`,
                    }))}
                  />
                )
              )}
            </ReportList>
          </Reports>
        </Content>
      </PageContainer>
    </FullPageContainer>
  );
};

export default CentralLaudos;
