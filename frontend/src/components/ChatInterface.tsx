import { useState, useRef, useEffect } from 'react';
import { chatWithAI } from '../services/api';
import type { ChatMessage } from '../services/api';
import './ChatInterface.css';

interface ChatInterfaceProps {
  isOpen: boolean;
  onToggle: () => void;
}

export default function ChatInterface({ isOpen, onToggle }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: inputMessage.trim(),
    };

    // Add user message immediately
    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await chatWithAI({
        message: userMessage.content,
        message_history: messages,
      });

      // Add AI response
      setMessages(response.message_history);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  if (!isOpen) {
    return (
      <button className="chat-toggle-button" onClick={onToggle} title="Open AI Chat">
        💬
      </button>
    );
  }

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>♟️ Chess AI Assistant</h3>
        <div className="chat-controls">
          <button className="clear-chat-button" onClick={clearChat} title="Clear chat">
            🗑️
          </button>
          <button className="close-chat-button" onClick={onToggle} title="Close chat">
            ✕
          </button>
        </div>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <p>👋 Hello! I'm your chess assistant. Ask me about:</p>
            <ul>
              <li>♟️ Chess rules and strategies</li>
              <li>📊 Position analysis</li>
              <li>🎯 Opening ideas</li>
              <li>🏆 Tips for improvement</li>
            </ul>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.role === 'user' ? 'user-message' : 'ai-message'}`}
          >
            <div className="message-content">{message.content}</div>
          </div>
        ))}

        {isLoading && (
          <div className="message ai-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <textarea
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me about chess..."
          disabled={isLoading}
          rows={1}
        />
        <button
          onClick={handleSendMessage}
          disabled={!inputMessage.trim() || isLoading}
          className="send-button"
        >
          ➤
        </button>
      </div>
    </div>
  );
}
