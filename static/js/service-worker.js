// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
  "/offline", // Offline page
  "/css/django-pwa-app.css", // CSS for your PWA
  "/", // Home page
  "/static/css/styles.css", // Your main CSS file
  "/static/js/main.js", // Your main JS file
  "/authorization/login", // Login page
  "/authorization/logout", // Logout page (if applicable)
  "/excel_upload/", // Excel upload page
  "/map/", // Main map app route
  "/static/icons/icon-192x192.png", // 192x192 icon
  "/static/icons/icon-512x512.png", // 512x512 icon
];

// Additional routes for caching
filesToCache = filesToCache.concat([
  "/authorization/signup", // Sign-up page if applicable
  "/map/view", // View map page (add specific routes as needed)
  "/map/edit", // Edit map page (add specific routes as needed)
  "/static/css/*.css", // All CSS files (manually list if needed)
  "/static/js/*.js", // All JS files (manually list if needed)
  "/static/images/*", // All images
  "/static/fonts/*", // All font files
]);

// Cache on install
self.addEventListener("install", (event) => {
  this.skipWaiting();
  event.waitUntil(
    caches.open(staticCacheName).then((cache) => {
      return cache.addAll(filesToCache);
    }),
  );
});

// Clear cache on activate
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((cacheName) => cacheName.startsWith("django-pwa-"))
          .filter((cacheName) => cacheName !== staticCacheName)
          .map((cacheName) => caches.delete(cacheName)),
      );
    }),
  );
});

// Serve from Cache
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches
      .match(event.request)
      .then((response) => {
        return response || fetch(event.request);
      })
      .catch(() => {
        return caches.match("offline");
      }),
  );
});
