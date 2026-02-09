/**
 * Layout Component - Main app layout with sidebar and header.
 */
import { useState, useEffect } from 'react';
import { Outlet, useLocation } from '@tanstack/react-router';
import Sidebar from './Sidebar';
import Header from './Header';
import { useSystemStore } from '../../store';
import websocketService from '../../services/websocket';

export default function Layout() {
    const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
    const location = useLocation();
    const { fetchStatus, isOnline } = useSystemStore();

    useEffect(() => {
        // Fetch initial status
        fetchStatus().catch(console.error);

        // Connect WebSocket
        websocketService.connect();

        // Periodic status check
        const interval = setInterval(() => {
            fetchStatus().catch(console.error);
        }, 30000);

        return () => {
            clearInterval(interval);
            websocketService.disconnect();
        };
    }, [fetchStatus]);

    const getPageTitle = () => {
        const path = location.pathname;
        if (path === '/') return 'Dashboard';
        if (path.includes('chat')) return 'Chat with ARIA';
        if (path.includes('devices')) return 'Devices';
        if (path.includes('memory')) return 'Memory';
        if (path.includes('automation')) return 'Automation';
        if (path.includes('settings')) return 'Settings';
        return 'ARIA';
    };

    return (
        <div className="flex min-h-screen relative">
            {/* Sidebar Wrapper */}
            <aside className={`fixed top-0 left-0 bottom-0 z-50 flex flex-col transition-[width] duration-200 bg-(--color-bg-secondary) border-r border-(--color-border) ${sidebarCollapsed ? 'w-18' : 'w-(--sidebar-width)'}`}>
                <Sidebar collapsed={sidebarCollapsed} />
            </aside>

            {/* Main Content Wrapper */}
            <main className={`flex-1 flex flex-col transition-[margin-left] duration-200 ml-(--sidebar-width)`} style={{ marginLeft: sidebarCollapsed ? '72px' : 'var(--sidebar-width)' }}>
                <header className="h-(--header-height) bg-(--color-bg-glass) backdrop-blur-md border-b border-(--color-border) flex items-center px-(--spacing-lg) sticky top-0 z-40">
                    <Header
                        title={getPageTitle()}
                        onToggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)}
                        isOnline={isOnline}
                    />
                </header>

                <div className="flex-1 p-(--spacing-lg) overflow-y-auto">
                    <Outlet />
                </div>
            </main>
        </div>
    );
}
