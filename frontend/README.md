# sims_frontend (React + Vite)

Student Information Management System - Frontend Application

## Tech Stack
- React 18
- Vite (build tool)
- ESLint (code quality)

## Setup for Development

### Local Development (without Docker)

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
# Create a .env.local file
echo "VITE_API_URL=http://localhost:8000" > .env.local
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at http://localhost:5173

### Docker Development

See the main README and docker-compose.yml in the root directory.

## Project Structure

```
frontend/
├── src/                # Source files
│   ├── assets/         # Static assets
│   ├── App.jsx         # Main app component
│   └── main.jsx        # Entry point
├── public/             # Public static files
├── index.html          # HTML template
├── package.json        # Dependencies
├── vite.config.js      # Vite configuration
└── Dockerfile          # Docker configuration
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Environment Variables

Create a `.env.local` file for local development:

```
VITE_API_URL=http://localhost:8000
```
