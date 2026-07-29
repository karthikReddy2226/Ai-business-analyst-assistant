import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const askQuestion = (question) =>
  axios.post(`${API_BASE}/ask`, { question }).then((r) => r.data.answer);

export const getSummary = () =>
  axios.get(`${API_BASE}/analytics/summary`).then((r) => r.data);

export const getRevenueByProduct = () =>
  axios.get(`${API_BASE}/analytics/revenue-by-product`).then((r) => r.data);

export const getRevenueByCity = () =>
  axios.get(`${API_BASE}/analytics/revenue-by-city`).then((r) => r.data);

export const getRevenueByDate = () =>
  axios.get(`${API_BASE}/analytics/revenue-by-date`).then((r) => r.data);

export const getChartData = (question) =>
  axios.post(`${API_BASE}/chart-data`, { question }).then((r) => r.data);

export const getQuestionInsights = (question) =>
  axios.post(`${API_BASE}/question-insights`, { question }).then((r) => r.data.insights);