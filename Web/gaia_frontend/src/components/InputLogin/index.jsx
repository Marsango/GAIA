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

export default function InputStyled({ label, type, error, id, ...props }) {
  const [showPassword, setShowPassword] = useState(false);

  const inputType = type === "password" && showPassword ? "text" : type;
  const inputId = id || props.name || props.placeholder || "input-field";

  return (
    <InputContainer>
      {label && <Label htmlFor={inputId}>{label}</Label>}
      <InputWrapper $hasError={!!error}>
        <Input
          id={inputId}
          type={inputType}
          aria-invalid={!!error}
          aria-describedby={error ? `${inputId}-error` : undefined}
          {...props}
        />
        {type === "password" && (
          <button
            type="button"
            className="position-absolute top-50 end-0 translate-middle-y me-1 text-muted"
            style={{
              cursor: "pointer",
              background: "transparent",
              border: "none",
            }}
            onClick={() => setShowPassword(!showPassword)}
            aria-label={showPassword ? "Ocultar senha" : "Mostrar senha"}
          >
            {showPassword ? <FaEyeSlash /> : <FaEye />}
          </button>
        )}
      </InputWrapper>
      {error && <ErrorText id={`${inputId}-error`}>{error}</ErrorText>}
    </InputContainer>
  );
}
