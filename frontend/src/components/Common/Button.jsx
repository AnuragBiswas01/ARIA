/**
 * Button Component - Reusable button with variants.
 */


export default function Button({
    children,
    variant = 'primary',
    size = 'md',
    icon,
    disabled = false,
    onClick,
    className = '',
    ...props
}) {
    const baseClasses = 'inline-flex items-center justify-center gap-(--spacing-sm) border-none rounded-(--radius-md) font-medium cursor-pointer transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed';

    const variants = {
        primary: 'bg-[linear-gradient(135deg,var(--color-primary),var(--color-primary-dark))] text-white shadow-[var(--shadow-glow)] hover:-translate-y-px hover:shadow-[0_0_30px_rgba(99,102,241,0.4)]',
        secondary: 'bg-(--color-bg-glass) text-(--color-text-primary) border border-(--color-border) hover:bg-(--color-bg-tertiary) hover:border-(--color-border-hover)',
        ghost: 'bg-transparent text-(--color-text-secondary) hover:bg-(--color-bg-glass) hover:text-(--color-text-primary)',
        danger: 'bg-(--color-error) text-white'
    };

    const sizes = {
        sm: 'px-(--spacing-sm) py-(--spacing-xs) text-xs',
        md: 'px-(--spacing-md) py-(--spacing-sm) text-sm',
        lg: 'px-(--spacing-lg) py-(--spacing-md) text-base'
    };

    const iconClass = (icon && !children) ? 'p-(--spacing-sm)' : '';

    const classes = [
        baseClasses,
        variants[variant],
        sizes[size],
        iconClass,
        className,
    ].filter(Boolean).join(' ');

    return (
        <button className={classes} disabled={disabled} onClick={onClick} {...props}>
            {icon}
            {children}
        </button>
    );
}
