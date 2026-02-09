/**
 * MessageBubble Component - Single message display.
 */
import { Wrench } from 'lucide-react';
import { format } from 'date-fns';
import ReactMarkdown from 'react-markdown';

export default function MessageBubble({ message }) {
    const { role, content, metadata, timestamp } = message;
    const isUser = role === 'user';
    const isSystem = role === 'system';

    const containerClasses = `flex gap-(--spacing-md) max-w-[80%] animate-[fadeIn_0.3s_ease] ${isUser ? 'self-end flex-row-reverse' : isSystem ? 'self-center max-w-full' : 'self-start'}`;
    const avatarClasses = `w-9 h-9 rounded-full flex items-center justify-center shrink-0 font-semibold text-sm ${isUser ? 'bg-[linear-gradient(135deg,var(--color-accent),var(--color-accent-dark))] text-white' : 'bg-[linear-gradient(135deg,var(--color-primary),var(--color-primary-dark))] text-white'}`;
    const bubbleClasses = `p-(--spacing-md) rounded-(--radius-lg) leading-relaxed ${isUser ? 'bg-[linear-gradient(135deg,var(--color-primary),var(--color-primary-dark))] text-white rounded-br-sm' : isSystem ? 'bg-(--color-bg-glass) text-(--color-text-secondary) text-sm px-(--spacing-md) py-(--spacing-sm)' : 'bg-(--color-bg-card) border border-(--color-border) text-(--color-text-primary) rounded-bl-sm'}`;

    return (
        <div className={containerClasses}>
            {!isSystem && (
                <div className={avatarClasses}>
                    {isUser ? 'U' : 'A'}
                </div>
            )}

            <div>
                <div className={bubbleClasses}>
                    <ReactMarkdown>{content}</ReactMarkdown>

                    {metadata?.toolCalls?.length > 0 && (
                        <div className="mt-(--spacing-sm) p-(--spacing-sm) bg-[rgba(6,182,212,0.1)] rounded-(--radius-md) text-sm border-l-3 border-(--color-accent)">
                            <div className="flex items-center gap-(--spacing-xs) text-(--color-accent) font-medium mb-(--spacing-xs)">
                                <Wrench size={14} />
                                Tools Used
                            </div>
                            {metadata.toolCalls.map((call, idx) => (
                                <div key={idx} className="text-xs">
                                    • {call.tool}
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {timestamp && (
                    <div className="text-xs text-(--color-text-muted) mt-(--spacing-xs)">
                        {format(new Date(timestamp), 'HH:mm')}
                    </div>
                )}
            </div>
        </div>
    );
}
