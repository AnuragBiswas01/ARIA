/**
 * MessageInput Component - Chat input field.
 */
import { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

export default function MessageInput({ onSend, disabled }) {
    const [message, setMessage] = useState('');
    const textareaRef = useRef(null);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (message.trim() && !disabled) {
            onSend(message);
            setMessage('');
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    // Auto-resize textarea
    useEffect(() => {
        const textarea = textareaRef.current;
        if (textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
        }
    }, [message]);

    return (
        <form className="p-(--spacing-md) bg-(--color-bg-glass) backdrop-blur-md border-t border-(--color-border) rounded-b-(--radius-lg)" onSubmit={handleSubmit}>
            <div className="flex gap-(--spacing-md) items-end">
                <textarea
                    ref={textareaRef}
                    className="flex-1 bg-(--color-bg-secondary) border border-(--color-border) rounded-(--radius-lg) p-(--spacing-md) text-(--color-text-primary) text-base resize-none min-h-[48px] max-h-[200px] transition-colors duration-150 focus:outline-none focus:border-(--color-primary) focus:ring-[3px] focus:ring-[rgba(99,102,241,0.1)] placeholder:text-(--color-text-muted)"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask ARIA anything..."
                    rows={1}
                    disabled={disabled}
                />
                <button
                    type="submit"
                    className="p-(--spacing-md) bg-[linear-gradient(135deg,var(--color-primary),var(--color-primary-dark))] border-none rounded-(--radius-lg) text-white cursor-pointer transition-all duration-150 flex items-center justify-center hover:-translate-y-0.5 hover:shadow-[var(--shadow-glow)] disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={!message.trim() || disabled}
                >
                    <Send size={20} />
                </button>
            </div>
        </form>
    );
}
