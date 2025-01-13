const staticCacheName = 'djangopwa-v2';

// کش کردن فایل‌ها هنگام نصب Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(staticCacheName).then((cache) => {
      return cache.addAll([
        '/', // صفحه اصلی
        '/static/css/style.css', // مسیر فایل‌های CSS
        '/static/js/app.js', // مسیر فایل‌های جاوااسکریپت
        '/static/images/icons/icon-192x192.png', // آیکون‌ها
      ]).catch((error) => {
        console.error('خطا در کش کردن فایل‌ها در زمان نصب:', error);
      });
    })
  );
});

// حذف کش‌های قدیمی هنگام فعال شدن Service Worker
self.addEventListener('activate', (event) => {
  const cacheWhitelist = [staticCacheName];

  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// مدیریت درخواست‌های fetch
self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);

  if (requestUrl.origin === location.origin) {
    // برای صفحه اصلی، همیشه درخواست از سرور
    if (requestUrl.pathname === '/') {
      event.respondWith(fetch(event.request).catch((error) => {
        console.error('خطا در بارگذاری صفحه اصلی:', error);
      }));
      return;
    }
  }

  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request).catch((error) => {
        console.error('خطا در fetch یا مطابقت کش:', error);
      });
    })
  );
});

// مدیریت Push Notifications
self.addEventListener('push', (event) => {
  let data = {};

  // بررسی داده‌های ارسال شده از سرور
  if (event.data) {
    data = event.data.json();
  }

  const title = data.title || 'پیام جدید';
  const options = {
    body: data.body || 'شما یک اعلان جدید دارید.',
    icon: '/static/images/icons/icon-192x192.png', // آیکون اعلان
    badge: '/static/images/icons/icon-192x192.png', // نشان اعلان
    data: data.url || '/', // لینک مربوط به اعلان
  };

  // نمایش نوتیفیکیشن
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// مدیریت کلیک روی نوتیفیکیشن
self.addEventListener('notificationclick', (event) => {
  event.notification.close(); // بستن نوتیفیکیشن

  event.waitUntil(
    clients.matchAll({ type: 'window' }).then((clientList) => {
      // باز کردن یا متمرکز کردن صفحه مرتبط با اعلان
      for (const client of clientList) {
        if (client.url === event.notification.data && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(event.notification.data);
      }
    })
  );
});

// مدیریت پیام‌ها از سمت اپلیکیشن برای پاک کردن کش پس از لاگ اوت
self.addEventListener('message', (event) => {
  if (event.data === 'logout') {
    caches.delete(staticCacheName).then(() => {
      console.log('کش‌ها پس از لاگ اوت پاک شدند');
    });
  }
});
