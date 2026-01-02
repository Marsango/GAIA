import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import {
  InputContainer,
  Label,
  InputWrapper,
  Input,
  ErrorText,
} from "./styled";

export default function InputStyled({ label, type, error, ...props }) {
  const [showPassword, setShowPassword] = useState(false);

  const inputType = type === "password" && showPassword ? "text" : type;

  return (
    <InputContainer>
      <Label>{label}</Label>
      <InputWrapper $hasError={!!error}>
        <Input type={inputType} {...props} />
        {type === "password" && (
          <span
            className="position-absolute top-50 end-0 translate-middle-y me-3 text-muted"
            style={{ cursor: "pointer" }}
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? <FaEyeSlash /> : <FaEye />}
          </span>
        )}
      </InputWrapper>
      {error && <ErrorText>{error}</ErrorText>}
    </InputContainer>
  );
}
