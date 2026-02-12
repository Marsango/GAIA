import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
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
  const [isAdmin, setIsAdmin] = useState(false);
  const navigate = useNavigate();
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [propriedades, setPropriedades] = useState([]);
  const [laudos, setLaudos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const token = localStorage.getItem("token");

  useEffect(() => {
    carregarPropriedades();
  }, []);

  // Verifica se o usuário é Admin ao carregar
  useEffect(() => {
    const userStored = localStorage.getItem("user");
    if (userStored) {
      try {
        const user = JSON.parse(userStored);
        if (user.is_staff) {
          setIsAdmin(true);
        }
      } catch (e) {
        console.error("Erro ao verificar permissão:", e);
      }
    }
  }, []);

  const btnStyle = {
    display: "block",
    margin: "0 auto 15px auto",
    padding: "10px 20px",
    backgroundColor: "#ffc107",
    color: "#000",
    border: "none",
    borderRadius: "5px",
    fontWeight: "bold",
    cursor: "pointer",
  };

  const carregarPropriedades = async () => {
    try {
      setLoading(true);

      const response = await api.get("propriedades/");

      const lista = response.data.results || [];
      setPropriedades(lista);

      if (lista.length > 0) {
        setSelectedProperty(lista[0].id);
      }
    } catch (error) {
      console.error("Erro ao carregar propriedades:", error);
      setError("Não foi possível carregar as propriedades.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedProperty) {
      carregarLaudos(selectedProperty);
    }
  }, [selectedProperty]);

  const carregarLaudos = async (propriedadeId) => {
    try {
      const response = await api.get(
        `laudos/por_propriedade/?propriedade_id=${propriedadeId}`,
      );

      setLaudos(response.data);
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
        {isAdmin && (
          <button style={btnStyle} onClick={() => navigate("/admin")}>
            Ir para Admin Panel
          </button>
        )}
        <Title>Central de Laudos</Title>
        <Content>
          <Properties>
            <Subtitle>Propriedades</Subtitle>
            {Array.isArray(propriedades) && propriedades.length > 0 ? (
              propriedades.map((propriedade) => (
                <PropertiesCard
                  key={propriedade.id}
                  nome={propriedade.name}
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
                ),
              )}
            </ReportList>
          </Reports>
        </Content>
      </PageContainer>
    </FullPageContainer>
  );
};

export default CentralLaudos;
