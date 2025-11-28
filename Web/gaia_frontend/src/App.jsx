import { useState } from "react";
import viteLogo from "/vite.svg";
import "./App.css";
import test from "./pages/test";
import Login from "./pages/Login";
import Reports from "./pages/Reports";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

// rotas da aplicação
function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
