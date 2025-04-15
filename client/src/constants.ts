export const SECRET = import.meta.env.VITE_SECRET || "";
export const STATIC_ASSETS_BASE_URL =
  import.meta.env.MODE === "development"
    ? "http://localhost:5173/public"
    : "https://localhost";
