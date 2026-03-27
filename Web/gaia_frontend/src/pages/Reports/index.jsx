import React, { useEffect, useState } from "react";
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
  AdminButton,
} from "./styled";

const CentralLaudos = () => {
  const [isAdmin, setIsAdmin] = useState(false);
  const navigate = useNavigate();
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [propriedades, setPropriedades] = useState([]);
  const [laudos, setLaudos] = useState([]);
  const [loading, setLoading] = useState(true);

  const user = JSON.parse(localStorage.getItem("user") || "{}");

  useEffect(() => {
    if (!user.id) {
      navigate("/login", { replace: true });
      return;
    }
    carregarPropriedades();
  }, []);

  useEffect(() => {
    const userStored = localStorage.getItem("user");
    if (userStored) {
      try {
        const user = JSON.parse(userStored);
        if (user.is_staff) setIsAdmin(true);
      } catch (e) {
        console.error("Erro ao verificar permissão:", e);
      }
    }
  }, []);

  const carregarPropriedades = async () => {
    try {
      setLoading(true);
      const response = await api.get("propriedades/");
      const lista = response.data.results || response.data || [];
      setPropriedades(Array.isArray(lista) ? lista : []);

      if (lista.length > 0) setSelectedProperty(lista[0].id);
    } catch (error) {
      console.error("Erro ao carregar propriedades:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedProperty) carregarLaudos(selectedProperty);
  }, [selectedProperty]);

  const carregarLaudos = async (propriedadeId) => {
    try {
      const response = await api.get(
        `laudos/por_propriedade/?propriedade_id=${propriedadeId}`,
      );
      const data = response.data.results || response.data || [];
      setLaudos(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Erro ao carregar laudos:", error);
      setLaudos([]);
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
          <AdminButton onClick={() => navigate("/admin")}>
            ⚙️ Painel do Administrador
          </AdminButton>
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
              <p style={{ color: "#777" }}>Nenhuma propriedade encontrada.</p>
            )}
          </Properties>

          <Reports>
            <Subtitle>Laudos Disponíveis</Subtitle>
            <ReportList>
              {laudos.length > 0 ? (
                Object.entries(agruparPorData(laudos)).map(
                  ([data, laudosDoDia]) => (
                    <ReportsCard
                      key={data}
                      data={data}
                      amostras={laudosDoDia.map((l) => ({
                        id: l.id,
                        numero: l.numero_amostra,
                        arquivoUrl: l.arquivo_url || null,
                      }))}
                    />
                  ),
                )
              ) : (
                <p style={{ color: "#777", fontSize: "20px" }}>
                  {selectedProperty
                    ? "Nenhum laudo cadastrado para esta propriedade."
                    : "Selecione uma propriedade para ver os laudos."}
                </p>
              )}
            </ReportList>
          </Reports>
        </Content>
      </PageContainer>
    </FullPageContainer>
  );
};

export default CentralLaudos;
