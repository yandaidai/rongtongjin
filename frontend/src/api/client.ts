import AsyncStorage from '@react-native-async-storage/async-storage';

// 可根据实际部署修改 BASE_URL
const BASE_URL = 'http://localhost:8000/api';

const TOKEN_KEY = '@rongtongjin_token';

class ApiClient {
  private token: string | null = null;

  async init(): Promise<string | null> {
    const saved = await AsyncStorage.getItem(TOKEN_KEY);
    if (saved) {
      this.token = saved;
    }
    return this.token;
  }

  async setToken(token: string | null): Promise<void> {
    this.token = token;
    if (token) {
      await AsyncStorage.setItem(TOKEN_KEY, token);
    } else {
      await AsyncStorage.removeItem(TOKEN_KEY);
    }
  }

  getToken(): string | null {
    return this.token;
  }

  private async request<T>(
    path: string,
    options: RequestInit = {},
  ): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const res = await fetch(`${BASE_URL}${path}`, {
      ...options,
      headers,
    });

    if (!res.ok) {
      const body = await res.json().catch(() => ({ detail: '请求失败' }));
      throw new Error(body.detail || `HTTP ${res.status}`);
    }

    // 204 No Content
    if (res.status === 204) {
      return undefined as T;
    }

    return res.json();
  }

  // --- Auth ---
  login(phone: string, code: string) {
    return this.request<import('../types').TokenResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ phone, code }),
    });
  }

  loginViaPassword(phone: string, password: string, agree_protocol: boolean) {
    return this.request<import('../types').TokenResponse>('/auth/login/password', {
      method: 'POST',
      body: JSON.stringify({ phone, password, agree_protocol }),
    });
  }

  register(phone: string, code: string, agree_protocol: boolean) {
    return this.request<import('../types').TokenResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ phone, code, agree_protocol }),
    });
  }

  getUserInfo() {
    return this.request<import('../types').User>('/auth/user/info');
  }

  updateAvatar(avatar: string) {
    return this.request<import('../types').User>('/auth/user/avatar', {
      method: 'PATCH',
      body: JSON.stringify({ avatar }),
    });
  }

  updateNickname(nickname: string) {
    return this.request<import('../types').User>('/auth/user/nickname', {
      method: 'PATCH',
      body: JSON.stringify({ nickname }),
    });
  }

  setPassword(password: string) {
    return this.request<{ message: string }>('/auth/user/password', {
      method: 'POST',
      body: JSON.stringify({ password }),
    });
  }

  deactivateAccount() {
    return this.request<{ message: string }>('/auth/user/account', {
      method: 'DELETE',
    });
  }

  // --- Products ---
  getProducts() {
    return this.request<import('../types').MetalProduct[]>('/products/');
  }

  // --- Quotes ---
  getQuotes() {
    return this.request<import('../types').MetalProductQuote[]>('/quotes/');
  }

  getDomesticQuotes() {
    return this.request<import('../types').MetalProductQuote[]>('/quotes/domestic');
  }

  getInternationalQuotes() {
    return this.request<import('../types').MetalProductQuote[]>('/quotes/international');
  }

  getQuoteHistory(product_id: number, limit = 10) {
    return this.request<import('../types').MetalQuote[]>(
      `/quotes/history?product_id=${product_id}&limit=${limit}`,
    );
  }

  // --- Klines ---
  getKlines(product_id: number, k_type: string, limit = 100) {
    return this.request<import('../types').MetalKline[]>(
      `/klines/?product_id=${product_id}&k_type=${k_type}&limit=${limit}`,
    );
  }

  getLatestKlines(product_id: number, k_type: string, limit = 10) {
    return this.request<import('../types').MetalKline[]>(
      `/klines/latest?product_id=${product_id}&k_type=${k_type}&limit=${limit}`,
    );
  }

  // --- Global Config ---
  getGlobalConfigs() {
    return this.request<import('../types').GlobalConfig[]>('/global/config/');
  }

  getGlobalConfigByProduct(product_id: number) {
    return this.request<import('../types').GlobalConfig>(`/global/config/${product_id}`);
  }

  updateGlobalConfig(product_id: number, data: import('../types').GlobalConfigUpdate) {
    return this.request<import('../types').GlobalConfig>(`/global/config/${product_id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  // --- User Config ---
  getUserConfigs() {
    return this.request<import('../types').UserConfig[]>('/user/config/');
  }

  upsertUserConfig(data: import('../types').UserConfigUpdate) {
    return this.request<import('../types').UserConfig>('/user/config/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // --- Warn ---
  getUserWarns() {
    return this.request<import('../types').MetalWarn[]>('/user/warn/');
  }

  getWarn(warn_id: number) {
    return this.request<import('../types').MetalWarn>(`/user/warn/${warn_id}`);
  }

  createWarn(data: import('../types').WarnCreate) {
    return this.request<import('../types').MetalWarn>('/user/warn/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  updateWarn(warn_id: number, data: import('../types').WarnUpdate) {
    return this.request<import('../types').MetalWarn>(`/user/warn/${warn_id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  deleteWarn(warn_id: number) {
    return this.request<void>(`/user/warn/${warn_id}`, {
      method: 'DELETE',
    });
  }
}

export const api = new ApiClient();
