import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api"; 
import "./styles.css";

export default function Amostras() {
  const navigate = useNavigate();
  const [amostras, setAmostras] = useState([]);
  const [loading, setLoading] = useState(false);
  const [convenio, setConvenio] = useState("UTFPR");
  const [error, setError] = useState(null);
  // Verifica autenticação ao carregar
  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");

    if (!user.id) {
      navigate("/login", { replace: true });
      return;
    }
    carregarAmostras();
  }, []);

  const carregarAmostras = async () => {
    try {
      setLoading(true);
      setError(null);

      //  NOVO: Token em httpOnly cookie, axios envia automaticamente
      const response = await api.get("/amostras/");

      setAmostras(response.data.results || response.data);
    } catch (err) {
      console.error("Erro ao carregar amostras:", err);
      setError("Erro ao carregar amostras. Faça login novamente.");
    } finally {
      setLoading(false);
    }
  };

  const baixarLaudo = async (amostraId, numeroAmostra, dataColeta) => {
    try {
      setLoading(true);
      setError(null);
      
      // Fazer requisição para gerar PDF
      const response = await api.get(
        `/amostras/${amostraId}/gerar_laudo/?convenio=${encodeURIComponent(convenio)}`,
        {
          responseType: "blob", // Importante para baixar arquivo
        },
      );

      // Criar URL temporária para download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        `Laudo_Amostra_${numeroAmostra}_${dataColeta}.pdf`,
      );
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      alert("Laudo baixado com sucesso!");
    } catch (err) {
      console.error("Erro ao baixar laudo:", err);
      setError(
        err.response?.data?.error || "Erro ao gerar laudo. Tente novamente.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="amostras-container">
      <div className="amostras-header">
        <h1>Amostras Cadastradas</h1>
        <button onClick={carregarAmostras} disabled={loading}>
          {loading ? "Carregando..." : "Atualizar"}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="convenio-input">
        <label>
          Convênio para o Laudo:
          <input
            type="text"
            value={convenio}
            onChange={(e) => setConvenio(e.target.value)}
            placeholder="Ex: UTFPR, Sistema Web GAIA"
          />
        </label>
      </div>

      {loading && <p>Carregando...</p>}

      <div className="amostras-table">
        <table>
          <thead>
            <tr>
              <th>Nº Amostra</th>
              <th>Descrição</th>
              <th>Data Coleta</th>
              <th>Profundidade (cm)</th>
              <th>pH</th>
              <th>Fósforo</th>
              <th>Potássio</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {amostras.length === 0 && !loading && (
              <tr>
                <td colSpan="8" style={{ textAlign: "center" }}>
                  Nenhuma amostra encontrada
                </td>
              </tr>
            )}
            {amostras.map((amostra) => (
              <tr key={amostra.id}>
                <td>{amostra.numero_amostra}</td>
                <td>{amostra.descricao || "-"}</td>
                <td>{amostra.data_coleta}</td>
                <td>{amostra.profundidade || "-"}</td>
                <td>{amostra.ph || "-"}</td>
                <td>{amostra.fosforo || "-"}</td>
                <td>{amostra.potassio || "-"}</td>
                <td>
                  <button
                    onClick={() =>
                      baixarLaudo(
                        amostra.id,
                        amostra.numero_amostra,
                        amostra.data_coleta,
                      )
                    }
                    disabled={loading}
                    className="btn-download"
                  >
                    Baixar Laudo
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
