// Glycine Lab: funciona offline. Página: rede primeiro (pega atualizações), cache se não houver sinal.
// Arquivos estáticos, fontes e bibliotecas: cache primeiro. Firestore cuida dos próprios dados offline.
const V = 'gl-v14';
const SHELL = ['./', './index.html', './config.js', './manifest.webmanifest', './icons/apple-touch-icon.png', './icons/icon-192.png', './icons/icon-512.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  if (/open-meteo\.com|firestore\.googleapis|identitytoolkit|securetoken|googleapis\.com\/(identitytoolkit|v1)/.test(u.href)) return;
  const isPage = e.request.mode === 'navigate' || (u.origin === location.origin && /(\/|index\.html|config\.js)$/.test(u.pathname));
  if (isPage){
    e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(V).then(x => x.put(e.request, c)); return r; }).catch(() => caches.match(e.request).then(r => r || caches.match('./index.html'))));
    return;
  }
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => { if (res && (res.ok || res.type === 'opaque')){ const c = res.clone(); caches.open(V).then(x => x.put(e.request, c)); } return res; })));
});
