import { Navigate } from "react-router-dom";

const PrivateRoute = ({ children }) => {
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  // Se não há usuário logado, redireciona para login
  if (!user.id) {
    return <Navigate to="/login" replace />;
  }

  // Se há usuário, renderiza o componente filho
  return children;
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Se há token, renderiza o componente filho
  return children;
};

export default PrivateRoute;
