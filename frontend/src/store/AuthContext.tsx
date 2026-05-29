import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api } from '../api/client';
import type { User } from '../types';

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (phone: string, code: string) => Promise<void>;
  register: (phone: string, code: string, agree: boolean) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api.init().then((token) => {
      if (token) {
        api.getUserInfo()
          .then(setUser)
          .catch(() => api.setToken(null))
          .finally(() => setIsLoading(false));
      } else {
        setIsLoading(false);
      }
    });
  }, []);

  const login = async (phone: string, code: string) => {
    const res = await api.login(phone, code);
    await api.setToken(res.access_token);
    setUser(res.user);
  };

  const register = async (phone: string, code: string, agree: boolean) => {
    const res = await api.register(phone, code, agree);
    await api.setToken(res.access_token);
    setUser(res.user);
  };

  const logout = async () => {
    await api.setToken(null);
    setUser(null);
  };

  const refreshUser = async () => {
    const u = await api.getUserInfo();
    setUser(u);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        register,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
