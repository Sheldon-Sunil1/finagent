
-- FinAgent: Phase 1 (Day 1-2) — Supabase/PostgreSQL Schema
-- This script creates minimal tables for user profiles and monthly financial state.
-- Run inside your Supabase project's SQL editor.

-- Extensions (Supabase typically has these; 'IF NOT EXISTS' keeps it idempotent)
create extension if not exists "pgcrypto";

-- ===============
-- 1) profiles
-- ===============
create table if not exists public.profiles (
  id uuid primary key default gen_random_uuid(),
  email text unique not null check (position('@' in email) > 1),
  full_name text not null,
  currency text not null default 'INR',
  monthly_income numeric(12,2) not null default 0,
  risk_tolerance smallint not null default 3 check (risk_tolerance between 1 and 5),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_profiles_email on public.profiles (email);

-- Trigger to keep updated_at fresh
create or replace function public.set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists trg_profiles_updated_at on public.profiles;
create trigger trg_profiles_updated_at
before update on public.profiles
for each row execute function public.set_updated_at();


-- =================================
-- 2) financial_states (monthly rollup)
-- =================================
create table if not exists public.financial_states (
  user_id uuid not null references public.profiles(id) on delete cascade,
  month date not null, -- store the FIRST day of the month (e.g., 2025-08-01)
  income numeric(12,2) not null default 0,
  expenses_fixed numeric(12,2) not null default 0,
  expenses_variable numeric(12,2) not null default 0,
  savings_balance numeric(14,2) not null default 0,
  investments_balance numeric(14,2) not null default 0,
  cash_balance numeric(14,2) not null default 0,
  market_inflation numeric(6,3) default null,
  market_interest_rate numeric(6,3) default null,
  market_index_value numeric(12,3) default null,
  goals_progress jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint financial_states_pk primary key (user_id, month),
  constraint month_is_first_day check (date_trunc('month', month) = month)
);

create index if not exists idx_fin_states_user on public.financial_states (user_id);
create index if not exists idx_fin_states_month on public.financial_states (month);

drop trigger if exists trg_financial_states_updated_at on public.financial_states;
create trigger trg_financial_states_updated_at
before update on public.financial_states
for each row execute function public.set_updated_at();

-- =================================
-- 3) Row Level Security (RLS) — optional if using service_role for backend
-- =================================
alter table public.profiles enable row level security;
alter table public.financial_states enable row level security;

-- If you plan to use Supabase Auth with client-side access, you can scope records to the logged-in user.
-- NOTE: These policies are examples; adjust to your security model.
do $$
begin
  if not exists (
    select 1 from pg_policies where schemaname='public' and tablename='profiles' and policyname='Allow users to view their own profile'
  ) then
    create policy "Allow users to view their own profile"
      on public.profiles for select
      using (auth.uid() = id);
  end if;
  if not exists (
    select 1 from pg_policies where schemaname='public' and tablename='profiles' and policyname='Allow users to manage their profile'
  ) then
    create policy "Allow users to manage their profile"
      on public.profiles for all
      using (auth.uid() = id) with check (auth.uid() = id);
  end if;
  if not exists (
    select 1 from pg_policies where schemaname='public' and tablename='financial_states' and policyname='Allow users to view their own states'
  ) then
    create policy "Allow users to view their own states"
      on public.financial_states for select
      using (auth.uid() = user_id);
  end if;
  if not exists (
    select 1 from pg_policies where schemaname='public' and tablename='financial_states' and policyname='Allow users to manage their own states'
  ) then
    create policy "Allow users to manage their own states"
      on public.financial_states for all
      using (auth.uid() = user_id) with check (auth.uid() = user_id);
  end if;
end $$;

-- ========================
-- 4) Helpful Views (optional)
-- ========================
create or replace view public.v_user_latest_state as
select distinct on (fs.user_id)
  fs.user_id,
  fs.month,
  fs.income,
  (fs.expenses_fixed + fs.expenses_variable) as total_expenses,
  fs.savings_balance,
  fs.investments_balance,
  fs.cash_balance,
  fs.goals_progress,
  fs.updated_at
from public.financial_states fs
order by fs.user_id, fs.month desc;
