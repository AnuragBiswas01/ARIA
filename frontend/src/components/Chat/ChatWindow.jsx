/**
 * ChatWindow Component - Main chat interface.
 */
import { useRef, useEffect } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { useChatStore } from '../../store';


export default function ChatWindow() {
    const messagesEndRef = useRef(null);
    const { messages, isLoading, sendUserMessage } = useChatStore();

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (message) => {
        if (!message.trim()) return;
        try {
            await sendUserMessage(message);
        } catch (error) {
            console.error('Failed to send message:', error);
        }
    };

    return (
        <div className="flex flex-col h-[calc(100vh-var(--header-height)-var(--spacing-lg)*2)] max-w-[900px] mx-auto">
            <div className="flex-1 overflow-y-auto p-(--spacing-md) flex flex-col gap-(--spacing-md)">
                {messages.length === 0 ? (
                    <div className="text-center p-(--spacing-2xl) text-(--color-text-secondary)">
                        <h2 className="mb-(--spacing-md) text-2xl font-semibold">👋 Hello! I'm ARIA</h2>
                        <p>Your intelligent home assistant. Ask me anything!</p>
                    </div>
                ) : (
                    <MessageList messages={messages} />
                )}

                {isLoading && (
                    <div className="flex gap-(--spacing-md) max-w-[80%] animate-[fadeIn_0.3s_ease] self-start">
                        <div className="w-9 h-9 rounded-full flex items-center justify-center shrink-0 font-semibold text-sm bg-[linear-gradient(135deg,var(--color-primary),var(--color-primary-dark))] text-white">A</div>
                        <div className="p-(--spacing-md) rounded-(--radius-lg) leading-relaxed bg-(--color-bg-card) border border-(--color-border) text-(--color-text-primary) rounded-bl-sm">
                            <div className="flex gap-1 p-(--spacing-md)">
                                <div className="w-2 h-2 bg-(--color-primary) rounded-full animate-bounce [animation-delay:0s]" />
                                <div className="w-2 h-2 bg-(--color-primary) rounded-full animate-bounce [animation-delay:0.2s]" />
                                <div className="w-2 h-2 bg-(--color-primary) rounded-full animate-bounce [animation-delay:0.4s]" />
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            <MessageInput onSend={handleSend} disabled={isLoading} />
        </div>
    );
}
