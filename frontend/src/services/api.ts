import type { ChatRequest, ChatResponse, ModelsResponse, HealthResponse } from '../types';

const API_BASE = '/api';

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export async function getModels(): Promise<ModelsResponse> {
  const response = await fetch(`${API_BASE}/models`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE}/health`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}
