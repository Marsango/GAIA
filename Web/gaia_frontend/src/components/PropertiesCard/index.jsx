import React from "react";
import { MdHome } from "react-icons/md";
import { FaMapMarkedAlt } from "react-icons/fa";
import { Card, IconContainer } from "./styled";

const PropertyCard = ({ nome, local, ativo, onClick }) => (
  <Card $ativo={ativo} onClick={onClick}>
    <IconContainer>
      <MdHome size={30} /> {nome}
    </IconContainer>
    <IconContainer>
      <FaMapMarkedAlt size={30} /> {local}
    </IconContainer>
  </Card>
);

export default PropertyCard;
