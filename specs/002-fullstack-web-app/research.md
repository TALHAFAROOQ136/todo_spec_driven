# Research: Full-Stack Web Todo App

**Feature**: 002-fullstack-web-app
**Date**: 2026-02-17
**Status**: Complete

## Research Questions

### RQ-1: Better Auth configuration for JWT issuance

**Decision**: Use Better Auth v1.x with the JWT plugin configured for HS256 signing using `BETTER_AUTH_SECRET`.

**Rationale**: Better Auth is a TypeScript-first authentication framework with native Next.js support. Its JWT plugin can issue tokens upon login. The constitution mandates a shared secret (`BETTER_AUTH_SECRET`), so HS256 is the correct algorithm. Better Auth also manages user registration, sessions, and account storage via its built-in PostgreSQL database adapter.

**Alternatives considered**:
- **NextAuth.js / Auth.js**: Now consolidated under Better Auth ecosystem. Better Auth is the current standard.
- **Custom JWT issuance**: Over-engineering. Better Auth handles this natively.
- **Asymmetric keys (RS256)**: Better Auth's default, but adds complexity (key management) without benefit for a single-service architecture. HS256 with shared secret is simpler and sufficient.

**Key configuration**:
```typescript
import { betterAuth } from "better-auth"
import { jwt } from "better-auth/plugins"

export const auth = betterAuth({
  database: { /* Neon PostgreSQL connection */ },
  plugins: [jwt({
    jwks: { disabled: true },  // Disable JWKS, use shared secret
  })]
})
```

**Gotchas**:
- Must call `router.refresh()` in `onSessionChange` to clear Next.js router cache
- Next.js 16 renames middleware to "proxy" (`proxy.ts` with `proxy` function)
- Better Auth manages its own tables (user, session, account, verification) — no manual user table needed

---

### RQ-2: Backend JWT verification with PyJWT

**Decision**: Use PyJWT (not python-jose) to verify JWT tokens on the FastAPI backend.

**Rationale**: FastAPI's official documentation has moved from `python-jose` to PyJWT. `python-jose` is nearly abandoned (last release ~3 years ago). PyJWT is actively maintained, secure, and works as a drop-in replacement.

**Alternatives considered**:
- **python-jose**: Previously recommended by FastAPI, now abandoned. Security risk.
- **authlib**: More comprehensive but heavier. Violates YAGNI for simple JWT verification.

**Key implementation**:
```python
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Gotchas**:
- Always hard-code the `algorithms` list — never derive from the token header
- Install `pyjwt` (not `jwt`) — the package name differs from the import name

---

### RQ-3: SQLModel async with Neon Serverless PostgreSQL

**Decision**: Use SQLModel with `asyncpg` driver via `create_async_engine` for non-blocking database access to Neon.

**Rationale**: Neon is serverless PostgreSQL that closes idle connections automatically. Async access via `asyncpg` aligns with FastAPI's async nature. SQLModel extends SQLAlchemy's async support cleanly.

**Alternatives considered**:
- **Synchronous psycopg2**: Blocks the event loop. Not suitable for FastAPI async.
- **SQLAlchemy directly**: SQLModel wraps SQLAlchemy with Pydantic integration, reducing boilerplate. Better fit with FastAPI.
- **Prisma (Python)**: Experimental. Not mature enough for production.

**Key configuration**:
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = "postgresql+asyncpg://user:pass@ep-xxx.neon.tech/dbname?ssl=require"

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,    # Check connection health before use
    pool_recycle=300,       # Recreate connections every 5 minutes (Neon lifecycle)
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

**Gotchas**:
- `pool_pre_ping=True` is essential — Neon closes idle connections
- `pool_recycle=300` aligns with Neon's connection lifecycle
- `expire_on_commit=False` prevents lazy loading issues in async contexts
- Connection string must use `postgresql+asyncpg://` prefix and `?ssl=require`

---

### RQ-4: Schema migration strategy

**Decision**: Use SQLModel's `create_all()` for initial deployment. Include Alembic in the project structure for future schema changes, but do not configure it for Phase 2.

**Rationale**: Phase 2 is a greenfield deployment — there's no existing schema to migrate from. `create_all()` creates all tables at startup. Alembic adds complexity that's not needed until we have schema evolution requirements.

**Alternatives considered**:
- **Alembic from day one**: Proper but premature for initial deployment. We'd generate a single "initial" migration that does the same as `create_all()`.
- **Raw SQL migrations**: Manual and error-prone. No benefit over SQLModel's built-in.

---

### RQ-5: Next.js 16 App Router patterns

**Decision**: Use Next.js 16 App Router with server components for data fetching, client components for interactivity, and `proxy.ts` for route protection.

**Rationale**: App Router is the standard for Next.js 16. Server components reduce client-side JavaScript. The proxy (middleware) pattern protects routes before rendering.

**Key patterns**:
- **Route protection**: `proxy.ts` checks for Better Auth session cookie, redirects unauthenticated users to `/signin`
- **API calls**: Centralized API client in `lib/api.ts` that attaches Bearer token to all backend requests
- **Session management**: Better Auth's `nextCookies` plugin for automatic cookie handling in server components
- **Data fetching**: Client components use the API client to fetch from the FastAPI backend

**Gotchas**:
- Next.js 16 renames `middleware.ts` → `proxy.ts` and `middleware()` → `proxy()`
- Proxy runs in Edge runtime — cannot use Node.js APIs directly
- Must use `fetch` to `/api/auth/get-session` for session checks in proxy

---

### RQ-6: Better Auth database storage

**Decision**: Better Auth uses the same Neon PostgreSQL database as the application, via its built-in PostgreSQL adapter.

**Rationale**: Single database simplifies infrastructure. Better Auth manages its own tables (user, session, account, verification) independently. The backend's Task table references `user_id` from Better Auth's user table (by storing the user ID extracted from the JWT — no foreign key needed since auth is managed separately).

**Alternatives considered**:
- **Separate database**: Adds infrastructure complexity. No benefit for this scale.
- **SQLite for auth**: Not compatible with serverless deployment. Neon is already available.

---

### RQ-7: Frontend-backend communication pattern

**Decision**: The Next.js frontend calls the FastAPI backend via REST API with Bearer token authentication. All API calls go through a centralized `lib/api.ts` client.

**Rationale**: The constitution mandates REST API communication between frontend and backend. A centralized API client ensures consistent token attachment and error handling.

**Key flow**:
1. User logs in → Better Auth creates session + issues JWT
2. Frontend reads JWT from Better Auth session
3. `lib/api.ts` attaches JWT as `Authorization: Bearer <token>` to all requests
4. Backend's `auth.py` middleware verifies JWT, extracts `user_id`
5. Route handlers scope all queries to `user_id`
