import { create } from 'zustand';
import { Message, mockMessages } from '@/lib/mockData';

interface DemoState {
  messages: Message[];
  isTyping: boolean;
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void;
  setTyping: (typing: boolean) => void;
  reset: () => void;
  simulateTyping: (content: string) => Promise<void>;
}

export const useDemoStore = create<DemoState>((set, get) => ({
  messages: [...mockMessages],
  isTyping: false,
  
  addMessage: (message) => {
    const newMessage: Message = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date()
    };
    
    set((state) => ({
      messages: [...state.messages, newMessage]
    }));
  },
  
  setTyping: (typing) => set({ isTyping: typing }),
  
  reset: () => set({ messages: [...mockMessages], isTyping: false }),
  
  simulateTyping: async (content: string) => {
    set({ isTyping: true });
    
    // Simulate typing delay
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
    
    const { addMessage, setTyping } = get();
    addMessage({
      author: 'ai',
      content
    });
    
    setTyping(false);
  }
}));