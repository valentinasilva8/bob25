-- Create ad_metrics table to store advertising performance data
create table if not exists public.ad_metrics (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  campaign_name text not null,
  impressions integer not null default 0,
  clicks integer not null default 0,
  conversions integer not null default 0,
  spend numeric(10, 2) not null default 0,
  revenue numeric(10, 2) not null default 0,
  date date not null default current_date,
  created_at timestamp with time zone default now()
);

-- Enable RLS
alter table public.ad_metrics enable row level security;

-- RLS Policies
create policy "Users can view their own ad metrics"
  on public.ad_metrics for select
  using (auth.uid() = user_id);

create policy "Users can insert their own ad metrics"
  on public.ad_metrics for insert
  with check (auth.uid() = user_id);

create policy "Users can update their own ad metrics"
  on public.ad_metrics for update
  using (auth.uid() = user_id);

create policy "Users can delete their own ad metrics"
  on public.ad_metrics for delete
  using (auth.uid() = user_id);

-- Create index for faster queries
create index if not exists ad_metrics_user_id_idx on public.ad_metrics(user_id);
create index if not exists ad_metrics_date_idx on public.ad_metrics(date);
