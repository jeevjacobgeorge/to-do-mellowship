import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_URL,
});

// Add request interceptor to include token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth services
export const login = async (username, password) => {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  const response = await axios.post(`${API_URL}/token`, formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('/register', userData);
  return response.data;
};

// Todo services
export const getTodos = async () => {
  const response = await api.get('/todos/');
  return response.data;
};

export const createTodo = async (todoData) => {
  const response = await api.post('/todos/', todoData);
  return response.data;
};

export const completeTodo = async (todoId) => {
  const response = await api.patch(`/todos/${todoId}/complete`);
  return response.data;
};

export const updateTodo = async (todoId, todoData) => {
  const response = await api.put(`/todos/${todoId}`, todoData);
  return response.data;
};

export const deleteTodo = async (todoId) => {
  const response = await api.delete(`/todos/${todoId}`);
  return response.data;
};

export default {
  login,
  register,
  getTodos,
  createTodo,
  completeTodo,
  updateTodo,
  deleteTodo,
};