// Service worker CatchClub — mise en cache légère pour un fonctionnement
// "application" (icône, plein écran) et un minimum hors-ligne.
// Volontairement simple : pas de mise en cache des modèles 3D (trop lourds).
//
// IMPORTANT : le numéro de version ci-dessous doit être incrémenté à
// chaque fois qu'on modifie ce fichier (ou qu'on veut forcer les
// téléphones à réévaluer leur cache). Le nom de fichier sw.js ne
// change jamais, donc c'est ce numéro qui permet au navigateur de
// détecter qu'il y a une nouvelle version à installer.
const CACHE_NAME = 'catchclub-v2';
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
    // Fichiers statiques : on sert le cache immédiatement s'il existe
    // (rapide), MAIS on relance systématiquement une requête réseau en
    // arrière-plan pour rafraîchir le cache — ainsi, une mise à jour du
    // CSS ou d'une icône est visible dès le rechargement suivant, sans
    // rester bloqué sur une version périmée indéfiniment ("stale-while-
    // revalidate").
    event.respondWith(
      caches.open(CACHE_NAME).then((cache) =>
        cache.match(event.request).then((cached) => {
          const enReseau = fetch(event.request)
            .then((response) => {
              if (response.ok) cache.put(event.request, response.clone());
              return response;
            })
            .catch(() => cached);
          return cached || enReseau;
        })
      )
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
