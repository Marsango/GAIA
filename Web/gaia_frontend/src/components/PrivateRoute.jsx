import { Navigate } from "react-router-dom";

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem("token");

  // Se não há token, redireciona para login
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Se há token, renderiza o componente filho
  return children;
};

export default PrivateRoute;
