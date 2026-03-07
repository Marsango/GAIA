import React from 'react';
import { FooterContainer, ContactText, CopyText } from './styled';

export default function Footer() {
  return (
    <FooterContainer>
      <ContactText>
        <span><span className="icon" aria-hidden="true">✉️</span> contato@labsolos.com.br</span>
        <span className="separator">|</span>
        <span><span className="icon" aria-hidden="true">📞</span> (43) 3000-0000</span>
      </ContactText>
      <CopyText>
        Laboratório de Solos GAIA © {new Date().getFullYear()} - Todos os direitos reservados.
      </CopyText>
    </FooterContainer>
  );
}