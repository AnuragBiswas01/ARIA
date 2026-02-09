/**
 * MessageList Component - Renders list of messages.
 */
import MessageBubble from './MessageBubble';

export default function MessageList({ messages }) {
    return (
        <>
            {messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
            ))}
        </>
    );
}
