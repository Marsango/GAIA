import React from "react";
import { CgLogOut, CgClose } from "react-icons/cg";
import {
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalTitle,
  ModalCloseButton,
  ModalBody,
  ModalText,
  ModalWarning,
  ModalActions,
  CancelButton,
  ConfirmButton,
} from "./styled";

const LogoutModal = ({ isOpen, onClose, onConfirm, loading = false }) => {
  if (!isOpen) return null;

  return (
    <ModalOverlay onClick={onClose}>
      <ModalContent onClick={(e) => e.stopPropagation()}>
        <ModalHeader>
          <ModalTitle>Confirmar Saída</ModalTitle>
          <ModalCloseButton onClick={onClose}>
            <CgClose />
          </ModalCloseButton>
        </ModalHeader>

        <ModalBody>
          <ModalText>Tem certeza que deseja sair da sua conta?</ModalText>
          <ModalWarning>
            Você será redirecionado para a página de login e precisará entrar
            novamente para acessar o sistema.
          </ModalWarning>
        </ModalBody>

        <ModalActions>
          <CancelButton onClick={onClose} disabled={loading}>
            Cancelar
          </CancelButton>
          <ConfirmButton onClick={onConfirm} disabled={loading}>
            {loading ? (
              "Saindo..."
            ) : (
              <>
                <CgLogOut size={18} />
                Sair
              </>
            )}
          </ConfirmButton>
        </ModalActions>
      </ModalContent>
    </ModalOverlay>
  );
};

export default LogoutModal;
