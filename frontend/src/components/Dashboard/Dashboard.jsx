/**
 * Dashboard Component - Main dashboard view.
 */
import { useEffect } from 'react';
import { Link } from '@tanstack/react-router';
import {
    MessageSquare,
    Lightbulb,
    Brain,
    Activity,
    Cpu,
    Database,
    Wifi
} from 'lucide-react';
import Card from '../Common/Card';
import { useSystemStore, useDeviceStore } from '../../store';

export default function Dashboard() {
    const { status, fetchStatus } = useSystemStore();
    const { devices, fetchDevices, controlDevice } = useDeviceStore();

    useEffect(() => {
        fetchStatus().catch(console.error);
        fetchDevices().catch(console.error);
    }, [fetchStatus, fetchDevices]);

    const toggleDevice = async (device) => {
        const action = device.state === 'on' ? 'turn_off' : 'turn_on';
        await controlDevice(device.entity_id, action);
    };

    return (
        <div className="grid gap-(--spacing-lg)">
            {/* Stats */}
            <div className="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-(--spacing-md) mb-(--spacing-lg)">
                <div className="flex items-center gap-(--spacing-md) p-(--spacing-lg) bg-(--color-bg-card) backdrop-blur-md border border-(--color-border) rounded-(--radius-lg) transition-all duration-200 hover:border-(--color-border-hover) hover:-translate-y-0.5">
                    <div className="w-12 h-12 rounded-(--radius-md) flex items-center justify-center shrink-0 bg-[linear-gradient(135deg,rgba(99,102,241,0.2),rgba(99,102,241,0.1))] text-(--color-primary-light)">
                        <Cpu size={24} />
                    </div>
                    <div className="flex-1">
                        <div className="text-2xl font-bold text-(--color-text-primary)">
                            {status?.ollama_connected ? 'Active' : 'Offline'}
                        </div>
                        <div className="text-sm text-(--color-text-secondary)">AI Engine</div>
                    </div>
                </div>

                <div className="flex items-center gap-(--spacing-md) p-(--spacing-lg) bg-(--color-bg-card) backdrop-blur-md border border-(--color-border) rounded-(--radius-lg) transition-all duration-200 hover:border-(--color-border-hover) hover:-translate-y-0.5">
                    <div className="w-12 h-12 rounded-(--radius-md) flex items-center justify-center shrink-0 bg-[linear-gradient(135deg,rgba(6,182,212,0.2),rgba(6,182,212,0.1))] text-(--color-accent)">
                        <Database size={24} />
                    </div>
                    <div className="flex-1">
                        <div className="text-2xl font-bold text-(--color-text-primary)">
                            {status?.database_connected ? 'Connected' : 'Offline'}
                        </div>
                        <div className="text-sm text-(--color-text-secondary)">Memory DB</div>
                    </div>
                </div>

                <div className="flex items-center gap-(--spacing-md) p-(--spacing-lg) bg-(--color-bg-card) backdrop-blur-md border border-(--color-border) rounded-(--radius-lg) transition-all duration-200 hover:border-(--color-border-hover) hover:-translate-y-0.5">
                    <div className="w-12 h-12 rounded-(--radius-md) flex items-center justify-center shrink-0 bg-[linear-gradient(135deg,rgba(16,185,129,0.2),rgba(16,185,129,0.1))] text-(--color-success)">
                        <Wifi size={24} />
                    </div>
                    <div className="flex-1">
                        <div className="text-2xl font-bold text-(--color-text-primary)">{devices.length}</div>
                        <div className="text-sm text-(--color-text-secondary)">Devices</div>
                    </div>
                </div>

                <div className="flex items-center gap-(--spacing-md) p-(--spacing-lg) bg-(--color-bg-card) backdrop-blur-md border border-(--color-border) rounded-(--radius-lg) transition-all duration-200 hover:border-(--color-border-hover) hover:-translate-y-0.5">
                    <div className="w-12 h-12 rounded-(--radius-md) flex items-center justify-center shrink-0 bg-[linear-gradient(135deg,rgba(245,158,11,0.2),rgba(245,158,11,0.1))] text-(--color-warning)">
                        <Activity size={24} />
                    </div>
                    <div className="flex-1">
                        <div className="text-2xl font-bold text-(--color-text-primary)">
                            {status?.uptime_seconds ? Math.floor(status.uptime_seconds / 60) : 0}m
                        </div>
                        <div className="text-sm text-(--color-text-secondary)">Uptime</div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-(--spacing-lg)">
                {/* Quick Actions */}
                <Card title="Quick Actions">
                    <div className="grid grid-cols-3 gap-(--spacing-md)">
                        <Link to="/chat" className="flex flex-col items-center gap-(--spacing-sm) p-(--spacing-lg) bg-(--color-bg-glass) border border-(--color-border) rounded-(--radius-lg) cursor-pointer transition-all duration-150 text-(--color-text-primary) no-underline hover:bg-(--color-bg-tertiary) hover:border-(--color-primary) hover:-translate-y-0.5">
                            <div className="w-12 h-12 rounded-full bg-[linear-gradient(135deg,var(--color-primary),var(--color-accent))] flex items-center justify-center text-white">
                                <MessageSquare size={24} />
                            </div>
                            <span className="text-sm font-medium">Chat</span>
                        </Link>

                        <Link to="/devices" className="flex flex-col items-center gap-(--spacing-sm) p-(--spacing-lg) bg-(--color-bg-glass) border border-(--color-border) rounded-(--radius-lg) cursor-pointer transition-all duration-150 text-(--color-text-primary) no-underline hover:bg-(--color-bg-tertiary) hover:border-(--color-primary) hover:-translate-y-0.5">
                            <div className="w-12 h-12 rounded-full bg-[linear-gradient(135deg,var(--color-primary),var(--color-accent))] flex items-center justify-center text-white">
                                <Lightbulb size={24} />
                            </div>
                            <span className="text-sm font-medium">Devices</span>
                        </Link>

                        <Link to="/memory" className="flex flex-col items-center gap-(--spacing-sm) p-(--spacing-lg) bg-(--color-bg-glass) border border-(--color-border) rounded-(--radius-lg) cursor-pointer transition-all duration-150 text-(--color-text-primary) no-underline hover:bg-(--color-bg-tertiary) hover:border-(--color-primary) hover:-translate-y-0.5">
                            <div className="w-12 h-12 rounded-full bg-[linear-gradient(135deg,var(--color-primary),var(--color-accent))] flex items-center justify-center text-white">
                                <Brain size={24} />
                            </div>
                            <span className="text-sm font-medium">Memory</span>
                        </Link>
                    </div>
                </Card>

                {/* Devices */}
                <Card title="Devices" subtitle="Tap to toggle">
                    <div className="grid grid-cols-[repeat(auto-fill,minmax(160px,1fr))] gap-(--spacing-md)">
                        {devices.map((device) => (
                            <div
                                key={device.entity_id}
                                className={`flex flex-col items-center gap-(--spacing-sm) p-(--spacing-lg) bg-(--color-bg-card) border border-(--color-border) rounded-(--radius-lg) cursor-pointer transition-all duration-150 hover:border-(--color-primary) ${device.state === 'on' ? 'border-(--color-success) shadow-[0_0_20px_rgba(16,185,129,0.2)]' : ''}`}
                                onClick={() => toggleDevice(device)}
                            >
                                <div className={`w-12 h-12 rounded-full flex items-center justify-center bg-(--color-bg-glass) text-(--color-text-secondary) transition-all duration-150 ${device.state === 'on' ? 'bg-[linear-gradient(135deg,var(--color-success),#059669)] text-white' : ''}`}>
                                    <Lightbulb size={24} />
                                </div>
                                <div className="text-sm font-medium text-center text-(--color-text-primary) line-clamp-2">{device.name || device.entity_id}</div>
                                <div className="text-xs text-(--color-text-muted)">{device.state}</div>
                            </div>
                        ))}
                    </div>
                </Card>
            </div>
        </div>
    );
}
