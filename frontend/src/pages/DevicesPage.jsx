/**
 * Devices Page - Device management view.
 */
import { useEffect } from 'react';
import { Lightbulb, Fan, Lock, Thermometer, RefreshCw } from 'lucide-react';
import Card from '../components/Common/Card';
import Button from '../components/Common/Button';
import Loading from '../components/Common/Loading';
import { useDeviceStore } from '../store';


const getDeviceIcon = (entityId) => {
    if (entityId.includes('light')) return Lightbulb;
    if (entityId.includes('fan') || entityId.includes('switch')) return Fan;
    if (entityId.includes('lock')) return Lock;
    if (entityId.includes('climate')) return Thermometer;
    return Lightbulb;
};

export default function DevicesPage() {
    const { devices, isLoading, fetchDevices, controlDevice } = useDeviceStore();

    useEffect(() => {
        fetchDevices().catch(console.error);
    }, [fetchDevices]);

    const toggleDevice = async (device) => {
        const action = device.state === 'on' ? 'turn_off' : 'turn_on';
        await controlDevice(device.entity_id, action);
    };

    if (isLoading) {
        return <Loading text="Loading devices..." />;
    }

    return (
        <div className="grid gap-(--spacing-lg)">
            <Card
                title="Smart Home Devices"
                subtitle={`${devices.length} devices available`}
                headerRight={
                    <Button
                        variant="ghost"
                        icon={<RefreshCw size={16} />}
                        onClick={() => fetchDevices()}
                    >
                        Refresh
                    </Button>
                }
            >
                <div className="grid grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-(--spacing-md)">
                    {devices.map((device) => {
                        const Icon = getDeviceIcon(device.entity_id);
                        const isActive = device.state === 'on';

                        return (
                            <div
                                key={device.entity_id}
                                className={`bg-(--color-bg-secondary) rounded-(--radius-lg) p-(--spacing-md) flex flex-col items-center gap-(--spacing-sm) border border-(--color-border) cursor-pointer transition-all duration-200 hover:border-(--color-border-hover) hover:-translate-y-0.5 ${isActive ? 'bg-[linear-gradient(135deg,rgba(99,102,241,0.1),rgba(99,102,241,0.05))] border-(--color-primary) shadow-[0_4px_12px_rgba(99,102,241,0.1)]' : ''}`}
                                onClick={() => toggleDevice(device)}
                            >
                                <div className={`w-10 h-10 rounded-full flex items-center justify-center mb-(--spacing-xs) ${isActive ? 'bg-(--color-primary) text-white' : 'bg-(--color-bg-tertiary) text-(--color-text-secondary)'}`}>
                                    <Icon size={24} />
                                </div>
                                <div className="font-medium text-center text-sm truncate w-full">{device.name || device.entity_id}</div>
                                <div className={`text-xs capitalize ${isActive ? 'text-(--color-primary)' : 'text-(--color-text-muted)'}`}>{device.state}</div>
                            </div>
                        );
                    })}
                </div>
            </Card>
        </div>
    );
}
