const CACHE_NAME = 'ai-resume-v2';
const ASSETS_TO_CACHE = [
  '/',
  '/manifest.json',
  '/static/css/style.css',
  '/static/js/app.js',
  '/static/manifest.json',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png'
];

// 1. Service Worker 설치 및 안전한 캐싱 (일부 리소스 실패 시에도 설치 보장)
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      for (const asset of ASSETS_TO_CACHE) {
        try {
          await cache.add(asset);
        } catch (err) {
          console.warn('[SW] Cache skip for:', asset, err);
        }
      }
    })
  );
  self.skipWaiting();
});

// 2. Service Worker 활성화 및 이전 캐시 정리
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// 3. 네트워크 요청 가로채기 (PWA 오프라인 지원 필수 fetch 핸들러)
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // POST 요청 및 AI 생성 API 요청은 캐싱하지 않고 네트워크로 직접 전달
  if (event.request.method !== 'GET' || url.pathname.startsWith('/generate') || url.pathname.startsWith('/api/generate')) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      }).catch(() => {
        return caches.match('/');
      });
    })
  );
});
