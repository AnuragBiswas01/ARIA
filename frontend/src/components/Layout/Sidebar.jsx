/**
 * Sidebar Component - Navigation sidebar.
 */
import { Link } from '@tanstack/react-router';
import {
    LayoutDashboard,
    MessageSquare,
    Lightbulb,
    Brain,
    Zap,
    Settings
} from 'lucide-react';

const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/chat', icon: MessageSquare, label: 'Chat' },
    { path: '/devices', icon: Lightbulb, label: 'Devices' },
    { path: '/memory', icon: Brain, label: 'Memory' },
    { path: '/automation', icon: Zap, label: 'Automation' },
    { path: '/settings', icon: Settings, label: 'Settings' },
];

export default function Sidebar({ collapsed }) {
    return (
        <nav className="flex flex-col h-full bg-[var(--color-bg-secondary)] border-r border-[var(--color-border)] w-[var(--sidebar-width)] transition-[width] duration-200" style={{ width: collapsed ? '72px' : 'var(--sidebar-width)' }}>
            <div className="flex items-center gap-[var(--spacing-md)] p-[var(--spacing-lg)] border-b border-[var(--color-border)]">
                <div className="w-10 h-10 bg-[linear-gradient(135deg,var(--color-primary),var(--color-accent))] rounded-[var(--radius-lg)] flex items-center justify-center text-white font-bold text-lg shrink-0">
                    A
                </div>
                {!collapsed && (
                    <span className="text-xl font-bold bg-[linear-gradient(135deg,var(--color-primary-light),var(--color-accent))] bg-clip-text text-transparent whitespace-nowrap">
                        ARIA
                    </span>
                )}
            </div>

            <div className="flex-1 p-[var(--spacing-md)] flex flex-col gap-[var(--spacing-xs)] overflow-y-auto">
                {navItems.map(({ path, icon: Icon, label }) => (
                    <Link
                        key={path}
                        to={path}
                        className="flex items-center gap-[var(--spacing-md)] p-[var(--spacing-md)] rounded-[var(--radius-md)] text-[var(--color-text-secondary)] transition-all duration-150 hover:bg-[var(--color-bg-glass)] hover:text-[var(--color-text-primary)] relative group"
                        activeProps={{
                            className: '!bg-[linear-gradient(135deg,rgba(99,102,241,0.2),rgba(6,182,212,0.1))] !text-[var(--color-primary-light)] !border !border-[var(--color-border)]'
                        }}
                    >
                        {({ isActive }) => (
                            <>
                                {isActive && (
                                    <div className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-6 bg-[var(--color-primary)] rounded-r-[var(--radius-sm)]" />
                                )}
                                <Icon size={20} className="shrink-0" />
                                {!collapsed && <span className="text-sm font-medium whitespace-nowrap transition-opacity duration-200">{label}</span>}
                            </>
                        )}
                    </Link>
                ))}
            </div>

            <div className="p-[var(--spacing-md)] border-t border-[var(--color-border)]">
                {!collapsed && (
                    <div className="text-xs text-[var(--color-text-muted)] whitespace-nowrap">
                        ARIA v1.0.0
                    </div>
                )}
            </div>
        </nav>
    );
}
