import axios from 'axios';
import config from '../config';

interface CreateAccountingEntryPayload {
  date: string;
  document_type: string;
  description: string;
  amount: number;
  vat: number;
  recorder_id: string;
  remarks?: string;
  attach_proof_base64: string;
}

interface AccountingEntryResponse {
  id: string;
  date: string;
  document_type: string;
  description: string;
  amount: number;
  vat: number;
  recorder_id: string;
  remarks?: string;
  proof_attachment_link?: string;
  pdf_unique_ref_number?: string;
  gcs_pdf_link?: string;
  created_at: string;
}

const apiClient = axios.create({
  baseURL: config.apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('jwt_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const createAccountingEntry = async (payload: CreateAccountingEntryPayload): Promise<AccountingEntryResponse> => {
  const response = await apiClient.post<AccountingEntryResponse>('/accounting-entries', payload);
  return response.data;
};
