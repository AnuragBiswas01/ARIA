/**
 * Settings Page - App configuration.
 */
import { Settings as SettingsIcon, Volume2, Bell, Moon } from 'lucide-react';
import Card from '../components/Common/Card';
import { useSettingsStore } from '../store';

export default function SettingsPage() {
    const {
        notifications,
        soundEnabled,
        setNotifications,
        setSoundEnabled
    } = useSettingsStore();

    return (
        <div className="grid gap-(--spacing-lg)">
            <Card title="Preferences" subtitle="Customize your experience">
                <div className="flex flex-col gap-(--spacing-lg)">
                    <label className="flex items-center justify-between cursor-pointer">
                        <div className="flex items-center gap-(--spacing-md)">
                            <Bell size={20} />
                            <span>Enable Notifications</span>
                        </div>
                        <input
                            type="checkbox"
                            checked={notifications}
                            onChange={(e) => setNotifications(e.target.checked)}
                            className="w-5 h-5 accent-(--color-primary)"
                        />
                    </label>

                    <label className="flex items-center justify-between cursor-pointer">
                        <div className="flex items-center gap-(--spacing-md)">
                            <Volume2 size={20} />
                            <span>Sound Effects</span>
                        </div>
                        <input
                            type="checkbox"
                            checked={soundEnabled}
                            onChange={(e) => setSoundEnabled(e.target.checked)}
                            className="w-5 h-5 accent-(--color-primary)"
                        />
                    </label>

                    <label className="flex items-center justify-between opacity-70 cursor-not-allowed">
                        <div className="flex items-center gap-(--spacing-md)">
                            <Moon size={20} />
                            <span>Dark Mode</span>
                        </div>
                        <input
                            type="checkbox"
                            checked={true}
                            disabled
                            className="w-5 h-5 accent-(--color-primary)"
                        />
                    </label>
                </div>
            </Card>

            <Card title="About ARIA">
                <div className="text-(--color-text-secondary)">
                    <p><strong>Version:</strong> 1.0.0</p>
                    <p><strong>AI Model:</strong> llama3.2:3b-instruct-q4_K_M</p>
                    <p className="mt-(--spacing-md)">
                        ARIA is your Adaptive Residential Intelligence Assistant -
                        a fully local, privacy-focused AI home automation system.
                    </p>
                </div>
            </Card>
        </div>
    );
}
