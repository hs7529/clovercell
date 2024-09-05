import { defineConfig } from "vite";
// import vue from "@vitejs/plugin-vue"; // Vue 플러그인 예시
// import react from "@vitejs/plugin-react"; // React 플러그인 예시
// import { resolve } from "path";

export default defineConfig({
  // 기본적인 설정
  // base: "./", // 모든 경로에 대해 기본 URL
  base: "/clovercell/", // GitHub Pages 배포 시 base 경로 설정
  root: "./src", // 프로젝트의 루트 디렉토리
  // mode: "development", // 'development' | 'production'

  // 서버 설정
  // server: {
  //   host: "localhost", // 개발 서버의 호스트
  //   port: 3000, // 개발 서버의 포트
  //   open: true, // 서버 시작 시 브라우저 자동 열림
  //   https: false, // https 사용 여부
  //   proxy: {
  //     "/api": {
  //       target: "http://localhost:4000", // API 프록시 설정
  //       changeOrigin: true,
  //       rewrite: (path) => path.replace(/^\/api/, ""),
  //     },
  //   },
  // },

  // 빌드 설정
  build: {
    outDir: "../docs", // 빌드 출력 디렉토리
    assetsDir: "assets", // 빌드 자산 디렉토리
    // sourcemap: false, // 소스맵 생성 여부
    // minify: "esbuild", // 코드 압축 방법 ('esbuild' | 'terser' | false)
    // chunkSizeWarningLimit: 500, // 청크 크기 경고 제한 (KB)
    // rollupOptions: {
    //   input: {
    //     main: resolve(__dirname, "index.html"),
    //     nested: resolve(__dirname, "nested/index.html"),
    //   },
    //   output: {
    //     manualChunks: {
    //       vendor: ["vue", "react"], // 분리된 청크 생성
    //     },
    //   },
    // },
  },

  // 플러그인 설정
  // plugins: [
  //   vue(), // Vue 플러그인 사용
  //   react(), // React 플러그인 사용
  // ],

  //경로 별칭 설정
  // resolve: {
  //   alias: {
  //     "@": resolve(__dirname, "src"), // '@/components'로 사용 가능
  //     components: resolve(__dirname, "src/components"),
  //   },
  //   extensions: [".js", ".vue", ".jsx", ".json"], // 확장자 생략 가능
  // },

  // CSS 관련 설정
  // css: {
  //   preprocessorOptions: {
  //     scss: {
  //       additionalData: `@import "@/styles/variables.scss";`, // 글로벌 SCSS 변수
  //     },
  //   },
  //   modules: {
  //     scopeBehaviour: "local", // CSS 모듈의 범위 ('local' | 'global')
  //     generateScopedName: "[name]__[local]___[hash:base64:5]", // 이름 생성 규칙
  //   },
  // },

  // 환경 변수 설정
  // envPrefix: "VITE_", // Vite 환경 변수 접두사

  // 로깅 설정
  // logLevel: "info", // 'info' | 'warn' | 'error' | 'silent'

  // 디버깅 설정
  // clearScreen: true, // 빌드 시 콘솔 클리어 여부

  // HMR(Hot Module Replacement) 설정
  // hmr: {
  //   overlay: true, // 오류 시 화면 오버레이
  // },

  // 기타 설정
  // optimizeDeps: {
  //   include: ["vue", "react"], // 포함할 모듈
  //   exclude: ["@babel/polyfill"], // 제외할 모듈
  // },
});
