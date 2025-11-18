import axios from "axios";

// Get base API URL and ensure it ends with /api
const getApiBaseUrl = () => {
  const baseUrl = process.env.REACT_APP_API_URL || "http://localhost:8000";
  return baseUrl.endsWith('/api') ? baseUrl : `${baseUrl}/api`;
};

const API_BASE_URL = getApiBaseUrl();

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${API_BASE_URL}/upload/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const processQuery = async (query, filePath = null) => {
  const response = await api.post("/query/", {
    query,
    file_path: filePath,
  });

  return response.data;
};

export const getAvailableAreas = async (filePath = null) => {
  const params = filePath ? { file_path: filePath } : {};
  const response = await api.get("/areas/", { params });

  return response.data;
};

export const exportData = async (area, filePath = null) => {
  const response = await api.post("/export/", {
    area,
    file_path: filePath,
  });

  return response.data;
};

export default api;
