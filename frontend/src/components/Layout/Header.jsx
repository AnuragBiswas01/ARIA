/**
 * Header Component - Top bar with title and status.
 */
import { Menu, Bell, Wifi, WifiOff } from 'lucide-react';

export default function Header({ title, onToggleSidebar, isOnline }) {
    return (
        <div className="flex items-center justify-between w-full h-full">
            <div className="flex items-center gap-(--spacing-md)">
                <button
                    className="bg-transparent border-none text-(--color-text-secondary) p-(--spacing-sm) rounded-(--radius-md) transition-all duration-150 cursor-pointer hover:bg-(--color-bg-glass) hover:text-(--color-text-primary)"
                    onClick={onToggleSidebar}
                >
                    <Menu size={20} />
                </button>
                <h1 className="text-lg font-semibold">{title}</h1>
            </div>

            <div className="flex items-center gap-(--spacing-md)">
                <div className="flex items-center gap-(--spacing-sm) px-(--spacing-md) py-(--spacing-sm) bg-(--color-bg-glass) rounded-full text-sm">
                    <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-(--color-success) animate-pulse' : 'bg-(--color-error)'}`} />
                    <span>{isOnline ? 'Online' : 'Offline'}</span>
                    {isOnline ? <Wifi size={14} /> : <WifiOff size={14} />}
                </div>

                <button className="bg-transparent border-none text-(--color-text-secondary) p-(--spacing-sm) rounded-(--radius-md) transition-all duration-150 cursor-pointer hover:bg-(--color-bg-glass) hover:text-(--color-text-primary)">
                    <Bell size={20} />
                </button>
            </div>
        </div>
    );
}
