// Service worker CatchClub — mise en cache légère pour un fonctionnement
// "application" (icône, plein écran) et un minimum hors-ligne.
// Volontairement simple : pas de mise en cache des modèles 3D (trop lourds).

const CACHE_NAME = 'catchclub-v1';
const PRECACHE_URLS = [
  '/static/css/style.css',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE_URLS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // On ne touche pas aux requêtes non-GET (formulaires, actions) ni aux
  // modèles 3D (trop volumineux pour être mis en cache côté navigateur).
  if (event.request.method !== 'GET' || url.pathname.startsWith('/static/models/')) {
    return;
  }

  if (url.pathname.startsWith('/static/')) {
    // Fichiers statiques : cache d'abord, réseau en secours.
    event.respondWith(
      caches.match(event.request).then((cached) => cached || fetch(event.request))
    );
  } else if (event.request.mode === 'navigate') {
    // Pages : réseau d'abord (contenu à jour), cache en secours si hors-ligne.
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
  }
});
