import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Paperclip, Mic, MoreHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { useDemoStore } from '@/stores/demoStore';
import { cn, formatDate } from '@/lib/utils';
import { api, Message } from '@/lib/api';

interface DemoChatProps {
  mode?: 'marketing' | 'app';
  className?: string;
}

const DemoChat = ({ mode = 'marketing', className }: DemoChatProps) => {
  const [input, setInput] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const { messages, isTyping, addMessage, setTyping, reset } = useDemoStore();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setIsLoading(true);
    
    // Add user message
    addMessage({
      author: 'user',
      content: userMessage
    });

    try {
      // Send message to AI API
      const response = await api.sendMessage(userMessage);
      
      // Add AI response
      if (response.conversation && response.conversation.length > 0) {
        // Get the latest AI message
        const latestMessages = response.conversation.slice(-2); // Get last 2 messages (user + AI)
        const aiMessage = latestMessages.find(msg => msg.author === 'ai');
        
        if (aiMessage) {
          addMessage({
            author: 'ai',
            content: aiMessage.content
          });
        }
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      // Add error message
      addMessage({
        author: 'ai',
        content: "I apologize, but I'm experiencing technical difficulties. Please try again later."
      });
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

  const quickActions = [
    "I need custom phone cases",
    "Find electronics suppliers",
    "Quote for 10K units",
    "Set up escrow payment"
  ];

  return (
    <Card className={cn(
      "flex flex-col overflow-hidden",
      mode === 'marketing' ? "h-[500px]" : "h-full",
      className
    )}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-surface-border">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-full bg-gradient-accent flex items-center justify-center">
            <span className="text-white text-sm font-semibold">AI</span>
          </div>
          <div>
            <h3 className="font-semibold text-text-primary">Sourcing Assistant</h3>
            <p className="text-xs text-text-secondary flex items-center">
              <div className="w-2 h-2 bg-success rounded-full mr-1" />
              Online
            </p>
          </div>
        </div>
        <Button variant="ghost" size="icon">
          <MoreHorizontal className="h-4 w-4" />
        </Button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.3 }}
              className={cn(
                "flex",
                message.author === 'user' ? 'justify-end' : 'justify-start'
              )}
            >
              <div className={cn(
                "max-w-[85%] rounded-2xl px-4 py-2 text-sm",
                message.author === 'user' 
                  ? "bg-gradient-accent text-white ml-4" 
                  : "glass-effect text-text-primary mr-4"
              )}>
                {message.author === 'ai' && message.content ? (
                  <div className="whitespace-pre-wrap">
                    {message.content}
                  </div>
                ) : (
                  <div>{message.content}</div>
                )}
                <p className={cn(
                  "text-xs mt-1 opacity-70",
                  message.author === 'user' ? "text-right" : "text-left"
                )}>
                  {formatDate(message.timestamp).split(',')[1]}
                </p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Typing Indicator */}
        <AnimatePresence>
          {(isTyping || isLoading) && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="flex justify-start"
            >
              <div className="glass-effect rounded-2xl px-4 py-3 mr-4">
                <div className="flex space-x-1">
                  {[0, 1, 2].map((i) => (
                    <motion.div
                      key={i}
                      className="w-2 h-2 bg-text-accent rounded-full"
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{
                        duration: 0.6,
                        repeat: Infinity,
                        delay: i * 0.2
                      }}
                    />
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      {mode === 'marketing' && !isExpanded && (
        <div className="px-4 py-2 border-t border-surface-border">
          <div className="flex flex-wrap gap-2">
            {quickActions.map((action, index) => (
              <Button
                key={index}
                variant="outline"
                size="sm"
                className="text-xs"
                onClick={() => {
                  setInput(action);
                  setIsExpanded(true);
                }}
              >
                {action}
              </Button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="p-4 border-t border-surface-border">
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="icon" className="shrink-0">
            <Paperclip className="h-4 w-4" />
          </Button>
          <div className="flex-1 relative">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your sourcing request..."
              className="pr-10"
              disabled={isLoading}
            />
            <Button
              variant="ghost"
              size="icon"
              className="absolute right-1 top-1/2 -translate-y-1/2 h-7 w-7"
            >
              <Mic className="h-4 w-4" />
            </Button>
          </div>
          <Button 
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            size="icon"
            className="shrink-0"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </Card>
  );
};

export default DemoChat;