import api from '../core/api';

export interface SearchResult {
    id: number;
    name: string;
    model: string;
    category: string;
    icon: string;
    path: string;
}

export const searchService = {
    async query(q: string): Promise<SearchResult[]> {
        const normalizedQuery = q?.trim() || '';
        if (normalizedQuery.length < 2) return [];
        try {
            const response = await api.get('/models/ui/search', {
                params: { q: normalizedQuery }
            });
            return Array.isArray(response.data) ? response.data : [];
        } catch (error) {
            console.error('Search error:', error);
            return [];
        }
    }
};
