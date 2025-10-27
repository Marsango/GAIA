import React, { useEffect, useState } from "react";
import axios from "axios";
import Header from "../../components/Header";
import PropertiesCard from "../../components/PropertiesCard";
import ReportsCard from "../../components/ReportsCard";
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

  axios.defaults.withCredentials = true;

  useEffect(() => {
    carregarPropriedades();
  }, []);

  const carregarPropriedades = async () => {
    try {
      const response = await axios.get(
        "http://localhost:8000/api/propriedades/"
      );

      console.log("Resposta completa:", response.data);

      if (response.data && Array.isArray(response.data.results)) {
        setPropriedades(response.data.results); // ← MUDE PARA .results
        if (response.data.results.length > 0) {
          setSelectedProperty(response.data.results[0].id);
        }
      } else {
        setError("Estrutura da resposta inesperada");
        setPropriedades([]);
      }
    } catch (error) {
      console.error("Erro ao carregar propriedades:", error);
      setError("Erro ao carregar propriedades: " + error.message);
      setPropriedades([]);
    }
  };

  useEffect(() => {
    if (selectedProperty) {
      carregarLaudos(selectedProperty);
    }
  }, [selectedProperty]);

  const carregarLaudos = async (PropertyId) => {
    setLoading(true);
    try {
      const response = await axios.get(
        `http://localhost:8000/api/laudos/?propriedade=${PropertyId}`
      );

      console.log("Resposta Laudos:", response.data);

      if (response.data && Array.isArray(response.data.results)) {
        setLaudos(response.data.results); // ← MUDE PARA .results
      } else {
        setLaudos([]);
      }
    } catch (error) {
      console.error("Erro ao carregar laudos:", error);
      setLaudos([]);
    } finally {
      setLoading(false);
    }
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
              {Array.isArray(laudos) && laudos.length > 0
                ? laudos.map((laudo) => (
                    <ReportsCard
                      key={laudo.id}
                      laudo={{
                        id: laudo.id,
                        amostra: laudo.numero_amostra,
                        data: laudo.data_coleta,
                        arquivoUrl: `http://localhost:8000${laudo.arquivo_pdf}`,
                      }}
                    />
                  ))
                : !loading && <p>Nenhum laudo encontrado</p>}
            </ReportList>
          </Reports>
        </Content>
      </PageContainer>
    </FullPageContainer>
  );
};

export default CentralLaudos;
