import React from "react";
import { MdHome } from "react-icons/md";
import { FaMapMarkedAlt } from "react-icons/fa";
import { Card, Name, Location } from "./styled";

const PropertyCard = ({ nome, local, ativo, onClick }) => (
  <Card type="button" $ativo={ativo} onClick={onClick} aria-pressed={ativo}>
    <Name>
      <MdHome size={30} />
      <span>{nome}</span>
    </Name>
    <Location>
      <FaMapMarkedAlt size={30} />
      <span>{local}</span>
    </Location>
  </Card>
);

export default PropertyCard;
