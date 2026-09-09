'use client';

import { createBrowserClient } from '@supabase/ssr';
import type { AuthChangeEvent, Session, SupabaseClient, User } from '@supabase/supabase-js';

type AuthChangeCallback = (event: AuthChangeEvent, session: Session | null) => void | Promise<void>;
type LocalAuthError = {
  name: string;
  message: string;
  status: number;
};
type LocalSupabaseClient = {
  auth: {
    getSession: () => Promise<{ data: { session: Session | null }; error: null }>;
    getUser: () => Promise<{ data: { user: User | null }; error: null }>;
    onAuthStateChange: (callback: AuthChangeCallback) => {
      data: { subscription: { unsubscribe: () => void } };
    };
    signInWithPassword: (credentials: { email: string; password: string }) => Promise<{ data: { user: null; session: null }; error: LocalAuthError }>;
    signUp: (credentials: { email: string; password: string; options?: { data?: Record<string, unknown> } }) => Promise<{ data: { user: null; session: null }; error: LocalAuthError }>;
    signOut: () => Promise<{ error: null }>;
  };
};
type AppSupabaseClient = SupabaseClient | LocalSupabaseClient;

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

function isConfigured(value: string | undefined): value is string {
  return Boolean(value && !value.includes('your-project') && !value.includes('your-anon-key'));
}

function createLocalClient(): LocalSupabaseClient {
  const authError = {
    name: 'AuthApiError',
    message: 'Supabase is not configured for local development.',
    status: 503,
  };

  return {
    auth: {
      getSession: async () => ({ data: { session: null }, error: null }),
      getUser: async () => ({ data: { user: null }, error: null }),
      onAuthStateChange: (callback: AuthChangeCallback) => {
        callback('INITIAL_SESSION', null);
        return {
          data: {
            subscription: {
              id: 'local-supabase-disabled',
              callback,
              unsubscribe: () => undefined,
            },
          },
        };
      },
      signInWithPassword: async () => ({ data: { user: null, session: null }, error: authError }),
      signUp: async () => ({ data: { user: null, session: null }, error: authError }),
      signOut: async () => ({ error: null }),
    },
  } as LocalSupabaseClient;
}

export function createClient(): AppSupabaseClient {
  if (!isConfigured(supabaseUrl) || !isConfigured(supabaseAnonKey)) {
    return createLocalClient();
  }

  return createBrowserClient(
    supabaseUrl,
    supabaseAnonKey
  );
}

export const supabase = createClient();
