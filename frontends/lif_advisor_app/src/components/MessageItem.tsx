import React from 'react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Message } from '../types';
import { formatTime } from '../utils/helpers';
import { User } from 'lucide-react';
import assistantIcon from '../assets/assistant-icon copy.png';

interface MessageItemProps {
  message: Message;
  isTyping?: boolean;
}

const MessageItem: React.FC<MessageItemProps> = ({ message, isTyping = false }) => {
  const isBot = message.sender === 'bot';
  
  return (
    <div 
      className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-4`}
      style={{ 
        animation: 'fadeIn 0.3s ease-out forwards',
      }}
    >
      <div 
        className={`max-w-[80%] md:max-w-[70%] rounded-2xl px-4 py-3 ${
          isBot 
            ? 'bg-gray-100 text-gray-800 rounded-tl-none' 
            : 'bg-blue-500 text-white rounded-tr-none'
        }`}
        data-testid="message-item"
        data-isbot={isBot}
      >
        <div className="flex items-center gap-2 mb-2">
          <div className={`p-1 rounded-full ${isBot ? 'bg-gray-200' : 'bg-blue-400'}`}>
            {isBot ? (
              <img src={assistantIcon} alt="Assistant" className="w-[20px] h-[20px] object-contain" />
            ) : (
              <User size={16} />
            )}
          </div>
          <span className="text-sm font-medium">{isBot ? <i><strong>LIF</strong>fy</i> : 'You'}</span>
        </div>
        <div className="text-sm md:text-base">
          {isTyping ? (
            <div className="flex space-x-1" data-testid="typing">
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
          ) : (
            // <div dangerouslySetInnerHTML={{ __html: message.content }} />
            <div>
              {isBot ? (
              <article className="prose" data-testid="message-content-bot">
              <Markdown remarkPlugins={[remarkGfm]}>{message.content}</Markdown>
              </article>
              
            ) : (
              <div data-testid="message-content-user">{message.content}</div>
            )}
            </div>
          )}
        </div>
        <div 
          className={`text-xs mt-1 flex justify-between items-center ${
            isBot ? 'text-gray-500' : 'text-blue-100'
          }`}
        >
          <span>{formatTime(message.timestamp)}</span>
          {isBot && message.tokens && message.cost && !isTyping && message.tokens > 0 && message.cost > 0 ? (
            <span className="ml-4">
              {message.tokens} tokens (${message.cost.toFixed(6)})
            </span>
          ) : (
            null
          )}
        </div>
      </div>
    </div>
  );
};

export default MessageItem;