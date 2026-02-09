/**
 * Memory Page - View and search ARIA's memory.
 */
import { useState } from 'react';
import { Search, Brain, Clock, Trash2 } from 'lucide-react';
import Card from '../components/Common/Card';
import Button from '../components/Common/Button';
import { searchMemory, clearWorkingMemory, getMemoryStats } from '../services/api';

export default function MemoryPage() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [stats, setStats] = useState(null);
    const [isSearching, setIsSearching] = useState(false);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        setIsSearching(true);
        try {
            const response = await searchMemory(query, 'conversations', 10);
            setResults(response.results || []);
        } catch (error) {
            console.error('Search failed:', error);
        }
        setIsSearching(false);
    };

    const handleClearWorking = async () => {
        try {
            await clearWorkingMemory();
            alert('Working memory cleared!');
        } catch (error) {
            console.error('Failed to clear:', error);
        }
    };

    const loadStats = async () => {
        try {
            const response = await getMemoryStats();
            setStats(response);
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    };

    return (
        <div className="grid gap-(--spacing-lg)">
            <div className="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-(--spacing-md) mb-(--spacing-lg)">
                <div className="flex items-center gap-(--spacing-md) p-(--spacing-lg) bg-(--color-bg-card) backdrop-blur-md border border-(--color-border) rounded-(--radius-lg) transition-all duration-200 hover:border-(--color-border-hover) hover:-translate-y-0.5 cursor-pointer" onClick={loadStats}>
                    <div className="w-12 h-12 rounded-(--radius-md) flex items-center justify-center shrink-0 bg-[linear-gradient(135deg,rgba(99,102,241,0.2),rgba(99,102,241,0.1))] text-(--color-primary-light)">
                        <Brain size={24} />
                    </div>
                    <div className="flex-1">
                        <div className="text-2xl font-bold text-(--color-text-primary)">
                            {stats?.semantic?.conversations_count ?? '—'}
                        </div>
                        <div className="text-sm text-(--color-text-secondary)">Stored Memories</div>
                    </div>
                </div>

                <div className="flex items-center gap-(--spacing-md) p-(--spacing-lg) bg-(--color-bg-card) backdrop-blur-md border border-(--color-border) rounded-(--radius-lg) transition-all duration-200 hover:border-(--color-border-hover) hover:-translate-y-0.5">
                    <div className="w-12 h-12 rounded-(--radius-md) flex items-center justify-center shrink-0 bg-[linear-gradient(135deg,rgba(6,182,212,0.2),rgba(6,182,212,0.1))] text-(--color-accent)">
                        <Clock size={24} />
                    </div>
                    <div className="flex-1">
                        <div className="text-2xl font-bold text-(--color-text-primary)">
                            {stats?.short_term?.item_count ?? '—'}
                        </div>
                        <div className="text-sm text-(--color-text-secondary)">Short-term Items</div>
                    </div>
                </div>
            </div>

            <Card title="Semantic Search" subtitle="Search through ARIA's memory">
                <form onSubmit={handleSearch} className="mb-(--spacing-lg)">
                    <div className="flex gap-(--spacing-md)">
                        <input
                            type="text"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Search memories..."
                            className="flex-1 p-(--spacing-md) bg-(--color-bg-secondary) border border-(--color-border) rounded-(--radius-md) text-(--color-text-primary)"
                        />
                        <Button type="submit" icon={<Search size={16} />} disabled={isSearching}>
                            Search
                        </Button>
                    </div>
                </form>

                {results.length > 0 && (
                    <div>
                        {results.map((result, idx) => (
                            <div key={idx} className="flex items-start gap-(--spacing-md) p-(--spacing-md) border-b border-(--color-border) last:border-0">
                                <div className="mt-1 text-(--color-text-secondary)">
                                    <Brain size={16} />
                                </div>
                                <div className="flex-1">
                                    <div className="text-sm text-(--color-text-primary) leading-relaxed">{result.document}</div>
                                    <div className="text-xs text-(--color-text-muted) mt-1">
                                        Distance: {result.distance?.toFixed(3)}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </Card>

            <Card title="Memory Management">
                <Button variant="danger" icon={<Trash2 size={16} />} onClick={handleClearWorking}>
                    Clear Working Memory
                </Button>
            </Card>
        </div>
    );
}
