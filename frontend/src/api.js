import axios from "axios";

const API = axios.create({
  baseURL: "https://rag-document-q-a-1.onrender.com"
});

export default API;