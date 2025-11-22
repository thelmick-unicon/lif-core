export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  tokens?: number;
  cost?: number;
  icon?: keyof typeof import('lucide-react');
}

export interface ChatContextType {
  messages: Message[];
  isTyping: boolean;
  sendMessage: (content: string) => void;
}

export interface UserDetails {
  username: string;
  firstname: string;
  lastname: string;
  identifier: string;
  identifier_type: string;
}