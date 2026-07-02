# CloudFlow Frontend

A modern, responsive user profile management interface built with Next.js 16, React 19, TypeScript, and Tailwind CSS. This frontend application provides a seamless interface for creating, reading, updating, and deleting user profiles.

Part of the `devops-assessment` monorepo — see the root [README.md](../README.md) for full-stack setup with Docker Compose.

## Features

- **Modern UI/UX**: Built with Next.js 16 and React 19 for optimal performance
- **Type-Safe**: Full TypeScript support for robust development
- **Responsive Design**: Mobile-first approach using Tailwind CSS 4
- **CRUD Operations**: Complete user profile management (Create, Read, Update, Delete)
- **Real-time Updates**: Instant UI updates after data mutations
- **Form Validation**: Client-side validation with React Hook Form and Zod
- **Beautiful Components**: Pre-built UI components using Radix UI primitives
- **Docker Support**: Containerized deployment ready (standalone production build)

## Tech Stack

- **Framework**: Next.js 16.1.4 (App Router, `output: "standalone"`)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4
- **UI Components**: Radix UI + shadcn/ui
- **State Management**: React Hooks
- **Form Handling**: React Hook Form + Zod
- **Icons**: Lucide React
- **Build Tool**: Turbopack

## Prerequisites

- Node.js 20+ (LTS recommended)
- npm
- Docker (optional, for containerized deployment)

## Getting Started

### Local Development

1. **Install dependencies**:

   ```bash
   npm install
   ```

2. **Run the development server**:

   ```bash
   npm run dev
   ```

3. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

   In local dev without the backend running behind a rewrite, API calls to `/api/*` will 404 — run the full stack via Docker Compose (root README) or point a dev proxy at a running backend.

### Docker

The frontend ships a single production multi-stage `Dockerfile` (deps → builder → runner, `node:20-alpine`, non-root user). It requires `BACKEND_URL` at runtime (see below) — build and run it directly, or via the root `docker-compose.yml` (recommended):

```bash
docker build -t cloudflow-frontend .
docker run -d -p 3000:3000 -e BACKEND_URL=http://backend:8080 cloudflow-frontend
```

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js App Router pages
│   │   ├── page.tsx      # Main dashboard (User Profile Management)
│   │   ├── layout.tsx    # Root layout with fonts
│   │   └── globals.css   # Global styles
│   ├── components/       # React components
│   │   ├── ui/          # shadcn/ui components
│   │   └── file-upload.tsx
│   ├── lib/             # Utility functions
│   │   ├── api.ts       # API client (calls relative "/api", proxied server-side)
│   │   └── utils.ts     # Helper utilities
│   └── types/           # TypeScript type definitions
│       └── index.ts     # User profile types
├── public/              # Static assets
├── Dockerfile           # Production multi-stage build
├── next.config.ts       # output: "standalone" + /api/:path* rewrite to BACKEND_URL
├── package.json         # Dependencies and scripts
└── tsconfig.json        # TypeScript configuration
```

## API Integration

The frontend never calls the backend directly from the browser. `src/lib/api.ts` issues requests to the relative path `/api`, and `next.config.ts` rewrites `/api/:path*` server-side to `${BACKEND_URL}/api/:path*`. This keeps the backend's network location a server-side runtime concern — see the root README's "Design decisions" section for why.

### Environment Variables

| Variable      | Description                                             | Default |
| ------------- | --------------------------------------------------------- | ------- |
| `BACKEND_URL` | Backend base URL for the Next.js rewrite (server-side only, **not** `NEXT_PUBLIC_*`) | none — required at build and runtime |
| `NODE_ENV`    | Environment mode                                          | `production` (set in Dockerfile) |
| `PORT`        | Server port                                                | `3000`  |

### API Endpoints

The frontend consumes the following backend endpoints (proxied through `/api`):

- `GET /api/profiles` - Fetch all user profiles
- `POST /api/profiles` - Create a new profile
- `PATCH /api/profiles/:id` - Update an existing profile
- `DELETE /api/profiles/:id` - Delete a profile

## Available Scripts

- `npm run dev` - Start development server with Turbopack
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Full Stack Setup

This app is meant to run alongside the `backend/` FastAPI service and a PostgreSQL database, orchestrated by the root `docker-compose.yml`:

```bash
cd ..
cp .env.example .env
docker compose up -d --build
```

See the root [README.md](../README.md) for architecture, verification steps, and the full environment variable reference.

## License

This project is licensed under the MIT License.

## Author

**Ahmed Musa** - [@iAhmedMusa](https://github.com/iAhmedMusa)

## Acknowledgments

- Built with [Next.js](https://nextjs.org/)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- Icons by [Lucide](https://lucide.dev/)
