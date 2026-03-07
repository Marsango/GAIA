import styled from "styled-components";
import { gray, white, lightGray, black, green } from "../../config/colors.js";

export const PageContainer = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100%;
    font-family: 'Poppins', sans-serif;
`;
export const LoginForm = styled.form`
    display: flex;
    flex-direction: column;
    width: 400px;
    min-height: 520px;
    height: auto;
    gap: 12px;
    padding: 30px;
    padding-top: 30px;
    border-radius: 8px;
    background: ${white};
    box-shadow: 0 5px 10px 0 rgba(0, 0, 0, 0.10);
    align-items: center;
    transition: min-height 0.2s ease, padding 0.2s ease;

        @media (max-width: 768px) {
            box-shadow: none;
            border-radius: 0;
        }
`;

export const Button = styled.button`
    padding: 10px;
    border: none;
    border-radius: 4px;
    background: ${green};
    color: ${white};
    cursor: pointer;
    width: 60%;
    font-weight: 600;
    font-size: 15px;

    &:hover {
        background: darken(${green}, 10%);
    }
`;

export const Title = styled.h1`
    font-size: 24px;
    margin-bottom: 16px;
    color: ${black};
    text-align: center;
`;

export const Logo = styled.img`
    width: 150px;
    height: auto;
`;

export const ErrorMessage = styled.p`
    font-family: 'Poppins', sans-serif;
    color: #d32f2f; /* Vermelho */
    font-size: 17px;
    text-align: center;
    min-height: 20px;
    font-weight: 500;
    padding: 8px;
    width: 100%;
`;