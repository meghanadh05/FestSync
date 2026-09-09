-- Workspace foundation for collaborative event planning.

create table if not exists workspaces (
    id uuid primary key default gen_random_uuid(),
    name varchar(255) not null,
    organization varchar(255),
    country varchar(100) not null default 'India',
    currency varchar(10) not null default 'INR',
    timezone varchar(100) not null default 'Asia/Kolkata',
    created_by text not null,
    created_at timestamp not null default now(),
    updated_at timestamp not null default now(),
    deleted_at timestamp
);

create table if not exists workspace_members (
    id uuid primary key default gen_random_uuid(),
    workspace_id uuid not null references workspaces(id) on delete cascade,
    user_id text not null,
    email varchar(255),
    role varchar(20) not null default 'MEMBER',
    created_at timestamp not null default now(),
    updated_at timestamp not null default now(),
    constraint uq_workspace_member_user unique (workspace_id, user_id),
    constraint workspace_members_role_check check (role in ('OWNER', 'ADMIN', 'PLANNER', 'MEMBER', 'VIEWER'))
);

create index if not exists idx_workspaces_created_by on workspaces(created_by);
create index if not exists idx_workspaces_created_at on workspaces(created_at);
create index if not exists idx_workspace_members_workspace_id on workspace_members(workspace_id);
create index if not exists idx_workspace_members_user_id on workspace_members(user_id);
