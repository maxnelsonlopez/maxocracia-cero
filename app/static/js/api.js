/**
 * Centralized API Module for Maxocracia-Cero
 * Handles token management and standardized API requests.
 */

const API_BASE = ''; // Relative path, same origin

class ApiService {
    constructor() {
        this.tokenKey = 'mc_token';
        this.baseUrl = ''; // Relative path
    }

    // Token Management
    getToken() {
        return localStorage.getItem(this.tokenKey) || localStorage.getItem('access_token');
    }

    setToken(token) {
        if (token) {
            localStorage.setItem(this.tokenKey, token);
            localStorage.setItem('access_token', token); // Compatibility
        } else {
            this.removeToken();
        }
    }

    removeToken() {
        localStorage.removeItem(this.tokenKey);
        localStorage.removeItem('access_token');
    }

    isAuthenticated() {
        return !!this.getToken();
    }

    // Generic Request Handler
    async request(endpoint, options = {}) {
        const url = `${API_BASE}${endpoint}`;

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        // Auto-inject Authorization header if token exists
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            ...options,
            headers
        };

        try {
            const response = await fetch(url, config);

            // Handle 401 Unauthorized (Token expired/invalid)
            if (response.status === 401) {
                // Optional: Attempt refresh logic here or redirect to login
                // For now, we just let the caller handle it or logout
                console.warn('Unauthorized access. Token might be invalid.');
            }

            return response;
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    // Auth Services
    async login(email, password) {
        const res = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
            credentials: 'include'
        });
        const data = await res.json();
        if (res.ok && data.access_token) {
            this.setToken(data.access_token);
        }
        return { ok: res.ok, data };
    }

    async register(name, email, password) {
        const res = await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password })
        });
        const data = await res.json();
        if (res.ok && data.access_token) {
            this.setToken(data.access_token);
        }
        return { ok: res.ok, data };
    }

    logout() {
        this.removeToken();
        // Optional: Call backend logout endpoint
        // this.request('/auth/logout', { method: 'POST' });
    }

    async getProfile() {
        if (!this.isAuthenticated()) return null;
        const res = await this.request('/auth/me');
        if (!res.ok) return null;
        return await res.json();
    }

    // Dashboard Services
    async getDashboardStats() {
        const res = await this.request('/forms/dashboard/stats');
        if (!res.ok) throw new Error('Failed to fetch stats');
        return await res.json();
    }

    async getDashboardAlerts() {
        const res = await this.request('/forms/dashboard/alerts');
        if (!res.ok) throw new Error('Failed to fetch alerts');
        return await res.json();
    }

    async getNetworkFlow() {
        const res = await this.request('/forms/dashboard/network');
        if (!res.ok) throw new Error('Failed to fetch network flow');
        return await res.json();
    }

    async authFetch(url, options = {}) {
        return this.request(url.replace(this.baseUrl, ''), options);
    }

    async getDashboardTrends(period = 30) {
        const res = await this.request(`/forms/dashboard/trends?days=${period}`);
        if (!res.ok) throw new Error('Failed to fetch trends');
        return await res.json();
    }

    async getCommunityStats() {
        const response = await fetch(`${this.baseUrl}/tvi/community-stats`);
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        return response.json();
    }

    async getDashboardCategories() {
        const res = await this.request('/forms/dashboard/categories');
        return res;
    }

    async getDashboardResolution() {
        const res = await this.request('/forms/dashboard/resolution');
        return res;
    }

    // Participant Services (Form Cero)
    async registerParticipant(data) {
        const res = await this.request('/forms/participant', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error || 'Participant registration failed');
        }
        return await res.json();
    }

    // TVI Services
    async logTVI(data) {
        const res = await this.request('/tvi', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error || 'TVI logging failed');
        }
        return await res.json();
    }

    async getTVIs(limit = 50, offset = 0) {
        const res = await this.request(`/tvi?limit=${limit}&offset=${offset}`);
        if (!res.ok) throw new Error('Failed to fetch TVIs');
        return await res.json();
    }

    // Forms Services (A & B)
    async registerInterchange(data) {
        const res = await this.request('/forms/interchange', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error || 'Interchange registration failed');
        }
        return await res.json();
    }

    async registerFollowup(data) {
        const res = await this.request('/forms/followup', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error || 'Follow-up registration failed');
        }
        return await res.json();
    }

    // VHV Services
    async calculateVHV(data) {
        const res = await this.request('/vhv/calculate', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error || 'VHV Calculation failed');
        }
        return await res.json();
    }

    async getVHVParameters() {
        const res = await this.request('/vhv/parameters');
        if (!res.ok) throw new Error('Failed to fetch parameters');
        return await res.json();
    }

    async getVHVProducts() {
        const res = await this.request('/vhv/products');
        if (!res.ok) throw new Error('Failed to fetch products');
        return await res.json();
    }

    async getVHVCaseStudies() {
        const res = await this.request('/vhv/case-studies');
        if (!res.ok) throw new Error('Failed to fetch case studies');
        return await res.json();
    }

    // Maxo Services
    async getBalance(userId) {
        const res = await this.request(`/maxo/${userId}/balance`);
        if (!res.ok) throw new Error('Failed to fetch balance');
        return await res.json();
    }

    async transferMaxo(fromId, toId, amount) {
        const res = await this.request('/maxo/transfer', {
            method: 'POST',
            body: JSON.stringify({ from_user_id: fromId, to_user_id: toId, amount })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error || 'Transfer failed');
        }
        return await res.json();
    }
}

// Export singleton instance
const api = new ApiService();
