export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  model: string;
  chat_history?: ChatMessage[];
}

export interface ChatResponse {
  answer: string;
  model: string;
  sources: string[];
  timestamp: string;
}

export interface ModelInfo {
  name: string;
  display_name: string;
  description: string;
  is_available: boolean;
}

export interface ModelsResponse {
  models: ModelInfo[];
  default_model: string;
}

export interface HealthResponse {
  status: string;
  ollama_connected: boolean;
  vectorstore_ready: boolean;
  documents_loaded: number;
}
