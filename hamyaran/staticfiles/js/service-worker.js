const staticCacheName = 'djangopwa-v1';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(staticCacheName).then((cache) => {
      return cache.addAll([
        '/', // Cache the homepage
        '/static/css/style.css', // Replace with actual paths
        '/static/js/app.js',
        '/static/images/icons/icon-192x192.png',
      ]).catch((error) => {
        console.error('Failed to cache files during install:', error);
      });
    })
  );
});

self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);

  if (requestUrl.origin === location.origin) {
    // Handle specific cases like the root path
    if (requestUrl.pathname === '/') {
      event.respondWith(caches.match('/'));
      return;
    }
  }

  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request).catch((error) => {
        console.error('Failed to fetch or match cache:', error);
      });
    })
  );
});
