# CloudFlow Frontend

A modern, responsive user profile management interface built with Next.js 16, React 19, TypeScript, and Tailwind CSS. This frontend application provides a seamless interface for creating, reading, updating, and deleting user profiles.

## Features

- **Modern UI/UX**: Built with Next.js 16 and React 19 for optimal performance
- **Type-Safe**: Full TypeScript support for robust development
- **Responsive Design**: Mobile-first approach using Tailwind CSS 4
- **CRUD Operations**: Complete user profile management (Create, Read, Update, Delete)
- **Real-time Updates**: Instant UI updates after data mutations
- **Form Validation**: Client-side validation with React Hook Form and Zod
- **Beautiful Components**: Pre-built UI components using Radix UI primitives
- **Docker Support**: Containerized deployment ready

## Tech Stack

- **Framework**: Next.js 16.1.4 (App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4
- **UI Components**: Radix UI + shadcn/ui
- **State Management**: React Hooks
- **Form Handling**: React Hook Form + Zod
- **Icons**: Lucide React
- **Build Tool**: Turbopack

## Prerequisites

- Node.js 20+ (LTS recommended)
- npm or yarn
- Docker (optional, for containerized deployment)

## Getting Started

### Local Development

1. **Clone the repository**:

   ```bash
   git clone https://github.com/iAhmedMusa/cloudflow-frontend.git
   cd frontapp
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:

   ```env
   NEXT_PUBLIC_API_URL=http://localhost:3001
   ```

4. **Run the development server**:

   ```bash
   npm run dev
   ```

5. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Docker Development

1. **Build the Docker image**:

   ```bash
   docker build -t cloudflow-frontend .
   ```

2. **Run the container**:

   ```bash
   docker run -d -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:3001 cloudflow-frontend
   ```

3. **Using Docker Compose** (with backend):
   ```bash
   docker compose up -d
   ```

## Project Structure

```
frontapp/
├── src/
│   ├── app/              # Next.js App Router pages
│   │   ├── page.tsx      # Main dashboard (User Profile Management)
│   │   ├── layout.tsx    # Root layout with fonts
│   │   └── globals.css   # Global styles
│   ├── components/       # React components
│   │   ├── ui/          # shadcn/ui components
│   │   └── file-upload.tsx
│   ├── lib/             # Utility functions
│   │   ├── api.ts       # API client for backend communication
│   │   └── utils.ts     # Helper utilities
│   └── types/           # TypeScript type definitions
│       └── index.ts     # User profile types
├── public/              # Static assets
├── Dockerfile           # Docker configuration
├── next.config.ts       # Next.js configuration
├── package.json         # Dependencies and scripts
└── tsconfig.json       # TypeScript configuration
```

## API Integration

The frontend communicates with the CloudFlow backend API. The API client (`src/lib/api.ts`) handles all HTTP requests to the backend service.

### Environment Variables

| Variable              | Description      | Default                 |
| --------------------- | ---------------- | ----------------------- |
| `NEXT_PUBLIC_API_URL` | Backend API URL  | `http://localhost:3001` |
| `NODE_ENV`            | Environment mode | `development`           |
| `PORT`                | Server port      | `3000`                  |

### API Endpoints

The frontend consumes the following API endpoints:

- `GET /api/profiles` - Fetch all user profiles
- `POST /api/profiles` - Create a new profile
- `PATCH /api/profiles/:id` - Update an existing profile
- `DELETE /api/profiles/:id` - Delete a profile

## Available Scripts

- `npm run dev` - Start development server with Turbopack
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Docker Deployment

### Building for Production

```bash
# Build the image
docker build -t yourusername/cloudflow-frontend:latest .

# Run with production API URL
docker run -d \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://api:3001 \
  -e NODE_ENV=production \
  yourusername/cloudflow-frontend:latest
```

### Docker Compose

The frontend is designed to work seamlessly with the CloudFlow backend using Docker Compose. See the main `cloudflow-compose.yml` in the project root for the complete setup.

## Backend Integration

This frontend is designed to work with the [CloudFlow Backend](https://github.com/iAhmedMusa/cloudflow_api). The backend provides:

- RESTful API for user profile management
- MongoDB database integration
- Express.js server
- Full CRUD operations

### Full Stack Setup

1. Clone both repositories:

   ```bash
   # Backend
   git clone https://github.com/iAhmedMusa/cloudflow_api.git

   # Frontend
   git clone https://github.com/iAhmedMusa/cloudflow-frontend.git
   ```

2. Use Docker Compose to run the entire stack:
   ```bash
   docker compose -f cloudflow-compose.yml up -d
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Author

**Ahmed Musa** - [@iAhmedMusa](https://github.com/iAhmedMusa)

## Acknowledgments

- Built with [Next.js](https://nextjs.org/)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- Icons by [Lucide](https://lucide.dev/)
