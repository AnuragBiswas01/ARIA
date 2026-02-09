/**
 * Loading Component - Spinner indicator.
 */


export default function Loading({ size = 'md', text = 'Loading...' }) {
    const spinnerSize = size === 'sm' ? 'w-4 h-4' : size === 'lg' ? 'w-10 h-10 border-[3px]' : 'w-6 h-6 border-2';

    return (
        <div className="flex items-center justify-center gap-(--spacing-md) p-(--spacing-xl)">
            <div className={`rounded-full border-(--color-border) border-t-(--color-primary) animate-spin ${spinnerSize}`} />
            {text && <span>{text}</span>}
        </div>
    );
}
