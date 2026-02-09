/**
 * StatusBadge Component - Status indicator.
 */


export default function StatusBadge({ status, text }) {
    const variants = {
        online: 'bg-[rgba(16,185,129,0.2)] text-(--color-success)',
        offline: 'bg-[rgba(239,68,68,0.2)] text-(--color-error)',
        warning: 'bg-[rgba(245,158,11,0.2)] text-(--color-warning)'
    };

    const statusKey = status === 'online' ? 'online' : status === 'warning' ? 'warning' : 'offline';

    return (
        <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-xs font-medium ${variants[statusKey]}`}>
            <span className="w-1.5 h-1.5 rounded-full bg-current" />
            {text || status}
        </span>
    );
}
