import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import type { ChatMessage, ModelInfo } from '../types';
import { sendMessage, getModels } from '../services/api';
import './ChatWidget.css';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [selectedModel, setSelectedModel] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadModels();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadModels = async () => {
    try {
      const response = await getModels();
      setModels(response.models);
      setSelectedModel(response.default_model);
    } catch (error) {
      console.error('Failed to load models:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await sendMessage({
        message: input,
        model: selectedModel,
        chat_history: messages,
      });

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.answer,
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'Sorry, an error occurred. Please try again.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-widget">
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <div className="chat-title">
              <span className="chat-icon">💬</span>
              Ask about my resume
            </div>
            <div className="model-selector">
              <select
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                disabled={isLoading}
              >
                {models.map((model) => (
                  <option
                    key={model.name}
                    value={model.name}
                    disabled={!model.is_available}
                  >
                    {model.display_name} {!model.is_available && '(unavailable)'}
                  </option>
                ))}
              </select>
            </div>
            <button className="close-btn" onClick={() => setIsOpen(false)}>
              &times;
            </button>
          </div>

          <div className="chat-messages">
            {messages.length === 0 && (
              <div className="welcome-message">
                <p>Hi! I'm an AI assistant that can answer questions about Parker's resume.</p>
                <p>Try asking:</p>
                <ul>
                  <li>"What is your work experience?"</li>
                  <li>"What skills do you have?"</li>
                  <li>"Tell me about your education"</li>
                </ul>
              </div>
            )}
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                <div className="message-content">
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-content loading">
                  <span className="dot"></span>
                  <span className="dot"></span>
                  <span className="dot"></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your question..."
              disabled={isLoading}
              rows={1}
            />
            <button onClick={handleSend} disabled={isLoading || !input.trim()}>
              Send
            </button>
          </div>
        </div>
      )}

      <button
        className={`chat-toggle ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? '✕' : '💬'}
      </button>
    </div>
  );
}
