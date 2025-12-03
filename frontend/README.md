# LưuGọn - Frontend

This is the Next.js frontend for LưuGọn application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Copy environment variables:
```bash
cp .env.local.example .env.local
```

3. Update `.env.local` with your backend API URL.

4. Run development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Build for Production

```bash
npm run build
npm start
```

## Project Structure

- `app/` - Next.js app directory with pages and layouts
- `components/` - React components
- `lib/` - Utility functions, API client, and Zustand store
- `public/` - Static assets

## Technologies

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Shadcn/UI
- Zustand (state management)
- Zod (validation)
- Axios (HTTP client)
