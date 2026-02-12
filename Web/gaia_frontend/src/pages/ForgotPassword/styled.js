import { gray, white, lightGray, black, green } from "../../config/colors.js";

export const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    backgroundColor: gray,
    color: black,
    fontFamily: "Poppins, sans-serif",
  },
  box: {
    backgroundColor: white,
    padding: "30px",
    borderRadius: "8px",
    textAlign: "center",
    width: "100%",
    maxWidth: "400px",
    boxShadow: "0 5px 10px 0 rgba(0, 0, 0, 0.10)",
  },
  input: {
    width: "100%",
    padding: "10px",
    marginBottom: "20px",
    borderRadius: "4px",
    border: `1px solid ${lightGray}`,
    fontFamily: "Poppins, sans-serif",
  },
  button: {
    width: "100%",
    padding: "10px",
    backgroundColor: green,
    color: white,
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontWeight: 600,
    fontFamily: "Poppins, sans-serif",
  },
  link: {
    display: "block",
    marginTop: "15px",
    color: lightGray,
    cursor: "pointer",
    fontSize: "0.9rem",
    fontFamily: "Poppins, sans-serif",
  },
};