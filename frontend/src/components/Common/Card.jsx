/**
 * Card Component - Container with glassmorphism effect.
 */


export default function Card({
    children,
    title,
    subtitle,
    headerRight,
    hoverable = false,
    glow = false,
    className = '',
    ...props
}) {
    const baseClasses = 'bg-(--color-bg-card) backdrop-blur-md border border-(--color-border) rounded-(--radius-lg) p-(--spacing-lg) transition-all duration-200';
    const hoverClasses = hoverable ? 'hover:border-(--color-border-hover) hover:-translate-y-0.5 hover:shadow-lg' : '';
    const glowClasses = glow ? 'shadow-[var(--shadow-glow)]' : '';

    // Combine classes
    const classes = [
        baseClasses,
        hoverClasses,
        glowClasses,
        className,
    ].filter(Boolean).join(' ');

    return (
        <div className={classes} {...props}>
            {(title || subtitle || headerRight) && (
                <div className="flex items-center justify-between mb-(--spacing-md)">
                    <div>
                        {title && <h3 className="text-lg font-semibold">{title}</h3>}
                        {subtitle && <p className="text-sm text-(--color-text-secondary)">{subtitle}</p>}
                    </div>
                    {headerRight}
                </div>
            )}
            {children}
        </div>
    );
}
