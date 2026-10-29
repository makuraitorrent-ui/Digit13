/* ERT INVENTORY — Service Worker de remplacement
 * Navigation : réseau d'abord pour recevoir les mises à jour Vercel.
 * Ressources locales : cache pour accélérer le lancement.
 * Supabase / API : jamais mises en cache.
 */

const CACHE_NAME = 'ert-inventory-v4-17-recovery-1';
const OFFLINE_FILES = ['/', '/index.html'];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => Promise.allSettled(OFFLINE_FILES.map(url => cache.add(url))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(names => Promise.all(
      names.filter(name => name.startsWith('ert-inventory-') && name !== CACHE_NAME)
        .map(name => caches.delete(name))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const request = event.request;

  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  if (url.origin !== self.location.origin) return;

  if (
    url.pathname.startsWith('/api/') ||
    url.pathname.startsWith('/auth/') ||
    url.pathname.startsWith('/rest/') ||
    url.pathname.startsWith('/storage/')
  ) return;

  // Pages : priorité à la dernière version disponible sur Vercel.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then(response => {
          if (response.ok) {
            const copy = response.clone();

            event.waitUntil(
              caches.open(CACHE_NAME)
                .then(cache => cache.put('/index.html', copy))
            );
          }

          return response;
        })
        .catch(async () =>
          (await caches.match('/index.html')) ||
          new Response('ERT INVENTORY indisponible hors connexion.', {
            status: 503,
            headers: {
              'Content-Type': 'text/plain; charset=utf-8'
            }
          })
        )
    );

    return;
  }

  // Images, icônes et manifest : réseau d'abord,
  // puis utilisation du cache si nécessaire.
  event.respondWith(
    fetch(request)
      .then(response => {
        if (response.ok && response.type === 'basic') {
          const copy = response.clone();

          event.waitUntil(
            caches.open(CACHE_NAME)
              .then(cache => cache.put(request, copy))
          );
        }

        return response;
      })
      .catch(async () =>
        (await caches.match(request)) || Response.error()
      )
  );
});
