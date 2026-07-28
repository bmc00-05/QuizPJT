// vite.config.js
import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import { VitePWA } from "vite-plugin-pwa"
import tailwindcss from "@tailwindcss/vite"
import { fileURLToPath, URL } from "node:url"

export default defineConfig({
  // 도메인 루트(https://catlog.bomun.dev/)에 배포하므로 절대경로를 쓴다.
  //
  // 상대경로("./")를 쓰면 /main/map, /main/game/:id 같은 중첩 라우트에서
  // 에셋 경로가 /main/assets/... 로 잘못 해석된다. SPA fallback 때문에
  // 그 요청에 index.html 이 반환되어 MIME 타입 오류로 앱이 뜨지 않는다.
  // (내부 이동은 멀쩡하고 새로고침·직접 링크에서만 깨져 발견이 늦다)
  base: "/",

  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },

  plugins: [
    // ✅ Tailwind v4: 반드시 Vite 플러그인으로 연결
    tailwindcss(),

    vue(),

    VitePWA({
      registerType: "autoUpdate",
      injectRegister: "auto",
      includeAssets: ["favicon.ico", "robots.txt", "apple-touch-icon.png"],

      // base="/" 에 맞춰 절대경로를 사용한다
      manifest: {
        name: "Quiz RPG",
        short_name: "QuizRPG",
        description: "Quiz RPG PWA",
        theme_color: "#0f172a",
        background_color: "#0f172a",
        display: "standalone",

        start_url: "/",
        scope: "/",

        icons: [
          { src: "pwa-192.png", sizes: "192x192", type: "image/png" },
          { src: "pwa-512.png", sizes: "512x512", type: "image/png" },
          {
            src: "pwa-512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "any maskable",
          },
        ],
      },

      workbox: {
        // SPA 라우팅 fallback
        navigateFallback: "/index.html",

        // ⚠️ 제외 목록이 없으면 Workbox 가 '모든' 내비게이션 요청을 가로채
        //    index.html 을 돌려준다. Django admin 처럼 서버가 렌더링하는 경로까지
        //    Vue 앱으로 대체되어, 라우터에 없는 경로라 배경색만 남는 백지가 된다.
        //    브라우저에서만 재현되고 curl 로는 정상이라 원인 파악이 늦어진다.
        navigateFallbackDenylist: [
          /^\/admin/,
          /^\/api/,
          /^\/static/,
          /^\/media/,
        ],

        // ✅ 정적 파일 precache
        globPatterns: ["**/*.{js,css,html,ico,png,svg,webp,woff2}"],

        // ✅ 구 캐시 정리 + 즉시 활성화(업데이트 꼬임 완화)
        cleanupOutdatedCaches: true,
        clientsClaim: true,
        skipWaiting: true,

        runtimeCaching: [
          // ⚠️ API는 보통 캐시 원치 않으면 삭제해도 됨
          {
            urlPattern: ({ url }) => url.pathname.startsWith("/api/"),
            handler: "NetworkFirst",
            options: {
              cacheName: "api-cache",
              networkTimeoutSeconds: 3,
              expiration: { maxEntries: 100, maxAgeSeconds: 60 * 60 },
            },
          },
        ],
      },

      // ✅ 개발 중 SW 캐시로 UI 깨짐 방지
      devOptions: {
        enabled: false,
      },
    }),
  ],
})
