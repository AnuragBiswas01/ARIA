/**
 * Automation Page - Placeholder for automation rules.
 */
import { Zap, Clock, Plus } from 'lucide-react';
import Card from '../components/Common/Card';
import Button from '../components/Common/Button';

export default function AutomationPage() {
    return (
        <div className="grid gap-(--spacing-lg)">
            <Card
                title="Automations"
                subtitle="Create rules for ARIA to follow"
                headerRight={
                    <Button icon={<Plus size={16} />}>
                        New Automation
                    </Button>
                }
            >
                <div className="text-center p-(--spacing-2xl) text-(--color-text-secondary)">
                    <Zap size={48} className="mb-(--spacing-md) opacity-50 mx-auto" />
                    <h3 className="mb-(--spacing-sm) text-lg font-semibold">No Automations Yet</h3>
                    <p>Create your first automation rule to get started.</p>
                    <p className="text-xs mt-(--spacing-md)">
                        Examples: "Turn off lights at midnight", "Alert when motion detected"
                    </p>
                </div>
            </Card>

            <Card title="Scheduled Tasks">
                <div className="text-center p-(--spacing-lg) text-(--color-text-muted)">
                    <Clock size={32} className="mb-(--spacing-sm) opacity-50 mx-auto" />
                    <p>No scheduled tasks</p>
                </div>
            </Card>
        </div>
    );
}
