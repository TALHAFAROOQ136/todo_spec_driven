# Frontend — Next.js 15 Todo App

## Tech Stack
- Next.js 15 (App Router), TypeScript, Tailwind CSS, Better Auth

## Run
```bash
cd frontend
npm install
npm run dev
```

## Structure
- `src/app/` — App Router pages (layout, signin, signup, dashboard)
- `src/components/` — Reusable UI components
- `src/lib/auth.ts` — Better Auth server config
- `src/lib/auth-client.ts` — Better Auth client for components
- `src/lib/api.ts` — Centralized API client with Bearer token
- `middleware.ts` — Route protection middleware

## Rules
- Better Auth manages all user data (no manual user table)
- JWT issued by Better Auth (EdDSA via JWT plugin), sent as Bearer token to backend
- `BETTER_AUTH_SECRET` must match backend secret
- Use `middleware.ts` for route protection
