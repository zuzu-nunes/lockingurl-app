// Caches the app shell so lockinGURL opens without internet. Bump VERSION on every release.
const VERSION = 'lockingurl-v17';
const SHELL = ['./', 'index.html', 'manifest.webmanifest?v=12', 'icons/lg-icon-180.png', 'icons/lg-icon-192.png', 'icons/lg-icon-512.png', 'icons/cover.jpg'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== VERSION && /^(lockingurl|lempiraflow)-/.test(k)).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// Network first for the page (so updates arrive), cache first for everything else.
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  // The page's update check asks for a fresh copy; let it reach the network instead of this cache.
  if (req.cache === 'no-store') return;
  if (req.mode === 'navigate') {
    // no-store skips the phone's web cache, which can hold an old page for up to 10 minutes.
    e.respondWith(fetch(req.url, { cache: 'no-store', credentials: 'same-origin' }).then(res => {
      const copy = res.clone();
      caches.open(VERSION).then(c => c.put('index.html', copy));
      return res;
    }).catch(() => caches.match('index.html')));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => {
    if (res.ok && new URL(req.url).origin === location.origin) {
      const copy = res.clone();
      caches.open(VERSION).then(c => c.put(req, copy));
    }
    return res;
  })));
});
