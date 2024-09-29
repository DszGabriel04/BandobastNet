// authentication/static/sw.js

const CACHE_NAME = 'my-pwa-cache-v1';
const urlsToCache = [
    '/',
    '/officer-dashboard/',
    '/supervisor-dashboard/',
    '/static/css/style.css',
    '/static/js/script.js',
    '/static/icons/gpe_192x192.png',
    '/static/icons/gpe_512x512.png',
];

// Install the service worker and cache all the specified resources
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache);
        })
    );
    console.log('Service Worker installed and caching pages...');
});
    path('officer-dashboard/', views.officer_dashboard, name='officer_dashboard'),
    path('supervisor-dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
// Activate the service worker and clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    console.log('Service Worker activated...');
});

// Fetch resources from cache first, then network if unavailable
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            // Return cached resource or fetch from the network if not in cache
            return response || fetch(event.request);
        })
    );
    console.log('Fetching resource:', event.request.url);
});
