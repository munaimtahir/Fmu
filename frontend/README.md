# SIMS Frontend - React + TypeScript + Vite

Student Information Management System - Frontend Application

## 🎯 Stage-1 Complete: Foundation & Authentication

This is a production-ready Stage-1 MVP featuring:
- ✅ Full JWT authentication with token refresh
- ✅ TypeScript strict mode with comprehensive type safety
- ✅ Minimalist-Elite design system
- ✅ Protected routes and authorization guards
- ✅ Comprehensive test coverage (26 tests passing)
- ✅ Production build optimized and ready

## Tech Stack

- **React 19** - Latest React with concurrent features
- **TypeScript** - Strict mode enabled for maximum type safety
- **Vite 7** - Lightning-fast build tool and dev server
- **Tailwind CSS 3** - Utility-first CSS framework
- **React Router v6** - Client-side routing with protected routes
- **Axios** - HTTP client with request/response interceptors
- **React Query** - Server state management
- **Zustand** - Lightweight state management for auth
- **React Hook Form + Zod** - Form validation with type-safe schemas
- **Vitest** - Fast unit testing framework
- **ESLint** - Code quality and consistency

## Setup for Development

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000` (or configure via `.env.local`)

### Local Development

1. **Install dependencies:**
```bash
npm install
```

2. **Set up environment variables:**
```bash
# Create .env.local file
cp .env.example .env.local

# Edit .env.local and set:
VITE_API_BASE_URL=http://localhost:8000
```

3. **Run the development server:**
```bash
npm run dev
```

The application will be available at http://localhost:5173

### Docker Development

See the main README and docker-compose.yml in the root directory.

## Available Scripts

- `npm run dev` - Start development server (with HMR)
- `npm run build` - Build for production (includes type-checking)
- `npm run type-check` - Run TypeScript type checking without building
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint for code quality
- `npm run test` - Run all tests once
- `npm run test:watch` - Run tests in watch mode

## Project Structure

```
frontend/
├── src/
│   ├── api/                    # API clients and HTTP layer
│   │   ├── axios.ts           # Axios instance with interceptors
│   │   └── auth.ts            # Authentication API methods
│   ├── components/
│   │   ├── ui/                # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Alert.tsx
│   │   │   ├── Spinner.tsx
│   │   │   └── FormField.tsx
│   │   └── layouts/           # Page layouts
│   │       ├── AuthLayout.tsx
│   │       └── DashboardLayout.tsx
│   ├── features/              # Feature-based modules
│   │   └── auth/
│   │       ├── types.ts       # Auth type definitions
│   │       ├── authStore.ts   # Zustand auth state
│   │       ├── useAuth.ts     # Auth hook
│   │       ├── LoginPage.tsx  # Login page component
│   │       └── ProtectedRoute.tsx  # Route guard
│   ├── pages/                 # Page components
│   │   └── DashboardHome.tsx
│   ├── routes/                # Routing configuration
│   │   ├── index.tsx
│   │   └── appRoutes.tsx
│   ├── lib/                   # Shared utilities
│   │   ├── env.ts            # Environment variable access
│   │   └── tokens.ts         # Design system tokens
│   ├── styles/
│   │   └── globals.css       # Global styles and Tailwind
│   ├── test/                 # Test utilities
│   │   └── setup.ts
│   ├── App.tsx               # Root application component
│   ├── main.tsx              # Application entry point
│   └── vite-env.d.ts         # Vite type definitions
├── public/                    # Static assets
├── index.html                 # HTML template
├── package.json               # Dependencies and scripts
├── vite.config.ts             # Vite configuration
├── tsconfig.json              # TypeScript configuration
├── tailwind.config.ts         # Tailwind CSS configuration
└── eslint.config.js           # ESLint configuration
```

## Authentication Flow

### Login Process

1. User enters credentials on `/login` page
2. Form validates inputs using Zod schema
3. On submit, credentials are sent to `/api/auth/token/`
4. Backend returns `access` and `refresh` tokens
5. Tokens are stored in localStorage
6. Auth state is initialized from token
7. User is redirected to `/dashboard`

### Token Refresh (Single-Flight Pattern)

The application implements a sophisticated single-flight token refresh pattern:

1. **Access token** is attached to all API requests via Axios interceptor
2. When a request receives **401 Unauthorized**:
   - If refresh is already in progress, the request is queued
   - Otherwise, a refresh is initiated using the refresh token
3. On successful refresh:
   - New access token is stored
   - All queued requests are replayed with new token
4. On refresh failure:
   - Tokens are cleared
   - User is redirected to login
   - All queued requests are rejected

This ensures:
- Only one refresh request at a time
- No race conditions
- Seamless user experience
- Efficient token management

### Protected Routes

Routes wrapped with `<ProtectedRoute>` component:
- Check authentication state
- Display loading spinner during initialization
- Redirect to `/login` if not authenticated
- Render protected content if authenticated

### Logout

1. User clicks logout button
2. Tokens are cleared from localStorage
3. Auth state is reset
4. React Query cache is invalidated
5. User is redirected to `/login`

## Design System - Minimalist-Elite

The UI follows a Minimalist-Elite aesthetic:

### Colors
- **Primary Blue**: `#3B82F6` - Primary actions and links
- **Emerald Green**: `#10B981` - Success states
- **Gray Scale**: Tailwind's default gray palette
- **Background**: `gray-50` (#F9FAFB)
- **Text**: `gray-900` (#111827)

### Typography
- **Font**: Inter (system fallback)
- **Weights**: 400 (normal), 600 (semibold)
- **Generous whitespace** for breathing room

### Components
- **Rounded corners**: `rounded-2xl` (1rem)
- **Transitions**: 150ms ease-in-out
- **Shadow**: Subtle elevation with `shadow-md` and `shadow-xl`
- **Focus states**: Blue ring on interactive elements

### Accessibility
- WCAG AA compliant color contrast
- Keyboard navigation fully supported
- ARIA labels on all interactive elements
- Screen reader friendly
- Focus visible indicators

## Environment Variables

Create a `.env.local` file for local development:

```env
VITE_API_BASE_URL=http://localhost:8000
```

**Note**: Environment variables must be prefixed with `VITE_` to be exposed to the client.

## Testing

The project uses Vitest with Testing Library for comprehensive test coverage:

### Running Tests

```bash
# Run all tests once
npm run test

# Run tests in watch mode
npm run test:watch
```

### Test Coverage

Current coverage includes:
- ✅ Authentication flow (login, logout, token refresh)
- ✅ Protected route guards
- ✅ UI components (Button, Input, etc.)
- ✅ Form validation
- ✅ API interceptors and token management

### Writing Tests

Tests are colocated with components using `.test.tsx` or `.test.ts` extensions.

Example:
```typescript
import { render, screen } from '@testing-library/react'
import { Button } from './Button'

test('renders button', () => {
  render(<Button>Click me</Button>)
  expect(screen.getByText('Click me')).toBeInTheDocument()
})
```

## Building for Production

```bash
npm run build
```

This will:
1. Run TypeScript type checking
2. Build optimized production bundles
3. Output to `dist/` directory

The built files include:
- Minified JavaScript bundles with code splitting
- Optimized CSS with Tailwind purge
- Asset optimization and fingerprinting

### Preview Production Build

```bash
npm run preview
```

## Code Quality

### Type Safety

- **Strict TypeScript mode** enabled
- **No implicit any** - all types must be explicit
- **Path aliases** configured (`@/*` for `src/*`)
- **Type checking** runs during build

### Linting

ESLint is configured with:
- React hooks rules
- React refresh rules
- Modern JavaScript/TypeScript rules

```bash
npm run lint
```

## Performance

### Lighthouse Scores (Production Build)

The application meets Stage-1 performance requirements:
- ⚡ Performance: 90+
- ♿ Accessibility: 90+
- 🎯 Best Practices: 90+
- 🔍 SEO: 85+

### Optimizations

- Code splitting by route
- Lazy loading for better initial load
- Tailwind CSS purging unused styles
- Modern JavaScript features (ES2020+)
- React 19 concurrent features

## Stage-2 Roadmap

The foundation is ready for Stage-2 features:
- Student management (CRUD operations)
- Course management
- Enrollment workflows
- Role-based access control (Admin, Registrar, Faculty, Student)
- Advanced filtering and search
- Data tables with pagination

## Troubleshooting

### "Cannot find module" errors

Ensure all dependencies are installed:
```bash
rm -rf node_modules package-lock.json
npm install
```

### API connection errors

1. Check that backend is running on correct port
2. Verify `VITE_API_BASE_URL` in `.env.local`
3. Check browser console for CORS errors

### Build fails with type errors

Run type checking to see detailed errors:
```bash
npm run type-check
```

## Contributing

1. Follow the existing code structure
2. Write tests for new features
3. Run `npm run lint` and `npm run type-check` before committing
4. Keep components small and focused
5. Document complex logic with comments

## License

See the main LICENSE file in the repository root.
