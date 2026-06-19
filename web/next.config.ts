import type { NextConfig } from "next";
import path from "path";

// На GitHub Pages (project page) сайт отдаётся по подпути /<repo>.
// Значение приходит из CI (NEXT_PUBLIC_BASE_PATH=/susanino-map); локально пусто.
const basePath = process.env.NEXT_PUBLIC_BASE_PATH || "";

const nextConfig: NextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  outputFileTracingRoot: path.join(__dirname),
  ...(basePath ? { basePath } : {}),
};

export default nextConfig;
