import { useEffect, useState } from "react";
import api from "../services/api";

function Reports() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    api
      .get("/report/laudos/")
      .then((res) => {
        console.log(res.data); // <--- aqui você vê os dados no console
        setReports(res.data);
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Meus Laudos</h2>
      <ul>
        {reports.map((r) => (
          <li key={r.id}>
            {r.nome} - {new Date(r.data_criacao).toLocaleDateString()}
            {r.descricao}
            <a href={r.file} target="_blank" rel="noopener noreferrer">
              Ver PDF
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Reports;
