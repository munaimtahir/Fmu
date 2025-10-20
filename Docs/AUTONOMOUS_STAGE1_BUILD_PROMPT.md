# 🧠 AUTONOMOUS STAGE-1 FRONTEND BUILD PROMPT (One Continuous Session)

Run this entire instruction as one continuous autonomous build process until all requirements are verified and merged. 
Do not stop, do not request user input, and do not create separate sessions.

Run autonomously and complete the full Stage-1 development of the SIMS frontend **in one continuous session**.  
Do not stop for approvals, do not request clarifications, and do not fragment the task across multiple runs.  
If any decision or assumption is required, make the **best professional judgment** and continue.  
If commits or pull requests are needed, **create them automatically**, link them to "Stage-1: Foundation & Auth", and **merge** when all checks are green.  
If something fails, **self-repair, retry, and proceed** until 100 % of the Definition-of-Done criteria are satisfied.

---

## 🎯 MISSION
Create a **production-ready Stage-1 MVP** of the SIMS frontend featuring:
- Full **JWT authentication** (login, refresh, guarded routes, logout).
- A polished **Minimalist-Elite** aesthetic (formal, modern, subtle motion).
- A clean, scalable **TypeScript + Vite** foundation ready for later stages.
- Working local environment, passing tests, and high performance scores.

---

## ⚙️ CONTEXT
- Repo path: `frontend/`
- Runtime: **React 19 + TypeScript (strict)** + Vite 7
- Backend: **Django REST Framework + SimpleJWT**
- API base: `import.meta.env.VITE_API_BASE_URL`
- Roles (for later): `Admin`, `Registrar`, `Faculty`, `Student`, `ExamCell`
- Design Language – **Minimalist-Elite**
  - Colors: Navy #0F172A  |  Blue #3B82F6  |  Emerald #10B981  |  Off-white #FAFAFA  
  - Typography: Inter/System, generous whitespace, rounded-2xl, subtle 150 ms transitions

---

## 🧩 TECHNOLOGY TO INSTALL & CONFIGURE
- **React 19 + TypeScript (strict mode)**
- **Tailwind CSS + PostCSS + Autoprefixer** (custom theme)
- **React Router v6**
- **Axios** (with access/refresh interceptors + single-flight refresh)
- **@tanstack/react-query**
- **react-hook-form + zod + @hookform/resolvers**
- **react-hot-toast**
- **zustand** (or lightweight context) for auth state
- **ESLint** (with React & hooks) + **Vitest** for unit tests

---

## 🗂️ FILE / FOLDER CONTRACT
```
frontend/
  tsconfig.json
  tailwind.config.ts
  postcss.config.js
  vite.config.ts
  .env.example                   # keeps VITE_API_BASE_URL
  src/
    main.tsx
    styles/globals.css
    lib/{env.ts,tokens.ts}
    api/{axios.ts,auth.ts}
    components/
      ui/{Button.tsx,Input.tsx,Card.tsx,Badge.tsx,Alert.tsx,Spinner.tsx,FormField.tsx}
      layouts/{AuthLayout.tsx,DashboardLayout.tsx}
    features/
      auth/{types.ts,authStore.ts,LoginPage.tsx,ProtectedRoute.tsx,useAuth.ts}
    routes/{index.tsx,appRoutes.tsx}
    pages/{DashboardHome.tsx}
  README.md  # append Stage-1 usage notes
```

---

## 🧱 FUNCTIONAL REQUIREMENTS

### Authentication
- **Login** via email/password → store `access` + `refresh`.
- **Axios interceptors** attach token headers.
- Implement **single-flight refresh** queue: one refresh, replay queued requests, logout on failure.
- Extract **roles** from JWT or `/api/me/`.
- **Logout** clears tokens, invalidates queries, redirects to `/login`.

### Routing & Guards
- `ProtectedRoute` ensures valid/refreshable token.
- Public: `/login`; Protected: `/dashboard`.

### Layout & Aesthetic
- **AuthLayout**: centered card, large heading, muted subtitle, floating-label inputs, inline errors, toast feedback, soft transitions.
- **DashboardLayout**: responsive shell (sidebar placeholder, topbar w/ avatar), clean typography, empty state.
- **UI kit**: Button (primary/ghost), Input, Card, Badge, Alert, Spinner, FormField wrapper.
- Maintain **keyboard accessibility** & ARIA labels.

### Data Layer
- Global `QueryClientProvider`.
- Auth store via zustand/context.
- Query invalidation on logout.

### Validation
- Login form validated with zod schema (email + password required).
- Disabled submit while pending; toast on success/error.

---

## 🔐 CONFIGURATION
- Read `VITE_API_BASE_URL` via `env.ts` (throw friendly error if missing).
- Handle CORS or network errors gracefully with console hint.

---

## 🧪 TEST CRITERIA & QA
**All of the following must pass before merge:**

### ✅ Unit & Integration (Vitest)
1. `axios.ts` refresh logic — simulate 401 → refresh → replay → success.
2. `ProtectedRoute` — redirects unauthenticated to `/login`.
3. `LoginPage` — submits mock credentials, stores tokens, navigates `/dashboard`.
4. UI components render without type errors.

### ✅ Lint & Type Safety
- `npm run lint` → 0 errors  
- `tsc --noEmit` → 0 type errors  

### ✅ Lighthouse (local build)
| Metric | Minimum |
|---------|----------|
| Performance | ≥ 90 |
| Accessibility | ≥ 90 |
| Best Practices | ≥ 90 |
| SEO | ≥ 85 |

### ✅ Manual UX QA
- Focus rings visible, tab order logical.
- Inputs announce labels via screen reader.
- Color contrast meets WCAG AA.
- Motion ≤ 150 ms; consistent spacing.

---

## 🧭 DEFINITION OF DONE
- `npm run dev` launches without errors; `/login` authenticates → `/dashboard`.
- Token refresh tested manually & via unit test.
- Protected routes enforce auth.
- Visual theme matches Minimalist-Elite palette and layout.
- README updated with:
  - Setup & environment steps
  - Commands (`dev`, `build`, `test`, `lint`)
  - Auth flow explanation
- All tests, lint, and type checks pass.
- Local Lighthouse report meets thresholds.

---

## 🧰 COMMANDS TO VERIFY
```
npm install
npm run dev
npm run build
npm run test
npm run lint
```

---

## 🪄 AUTONOMY & PR RULES
- Execute **entire build in one session**.
- If default branch protected → create `feat/stage-1-foundation-auth`.
- Commit progressively with conventional messages:
  - `feat(auth): implement single-flight refresh`
  - `style(ui): finalize minimalist theme`
  - `test(auth): add vitest coverage`
- Open PR automatically; merge when green.
- If any step fails → self-diagnose → fix → re-run.

---

## 🧾 SELF-VERIFICATION CHECKLIST
- [ ] Login works & redirects correctly.  
- [ ] Refresh flow validated (unit + manual).  
- [ ] Unauthorized blocked from protected routes.  
- [ ] UI matches Minimalist-Elite spec.  
- [ ] Keyboard & ARIA accessibility verified.  
- [ ] Lighthouse ≥ 90 scores.  
- [ ] README updated.  
- [ ] All tests/lint/types clean.  
- [ ] PR merged or ready-to-merge.

---

## 🚀 FINAL INSTRUCTION
Run now in a **single continuous autonomous session** until all Definition-of-Done items are complete, verified, committed, and merged.  
Do not pause for approvals or further input.  
Begin execution → build → test → commit → merge.
