var staticCacheName = 'djangopwa-v1';

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll([
        '/', // Ensure the root path is explicitly cached
        '/static/css/style.css', // Example: cache specific assets
        '/static/js/app.js', // Example: cache specific assets
      ]);
    })
  );
});

self.addEventListener('fetch', function(event) {
  var requestUrl = new URL(event.request.url);

  // Handle requests to the root path
  self.addEventListener('fetch', (event) => {
    console.log('Handling fetch event for', event.request.url);
  
    event.respondWith(
      caches.match(event.request).then((response) => {
        if (response) {
          console.log('Found response in cache:', response);
          return response;
        }
  
        console.log('No response found in cache. Fetching from network...');
        return fetch(event.request).catch((error) => {
          console.error('Failed to fetch:', error);
          return new Response('Network error occurred.', {
            status: 408,
            statusText: 'Request Timeout',
          });
        });
      })
    );
  });
})
