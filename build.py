# Gera a versão PWA (GitHub Pages + Firebase) a partir do app principal /home/claude/soja/index.html
import re, sys
src = open('/home/claude/soja/index.html').read()
s = src
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

# cabeçalho: manifest, ícones iOS, Firebase
rep('<meta name="theme-color" content="#123321">', '''<meta name="theme-color" content="#123321">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Glycine Lab">
<script src="config.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.14.1/firebase-firestore-compat.js"></script>''')
s = re.sub(r'<meta name="viewport" content="([^"]*)">', lambda m: '<meta name="viewport" content="' + (m.group(1) if 'viewport-fit' in m.group(1) else m.group(1) + ', viewport-fit=cover') + '">', s, count=1)

# tela de login
rep('<div id="splash" hidden', '''<div id="login" hidden style="position:fixed;inset:0;z-index:90;background:var(--bg);display:flex;align-items:center;justify-content:center;padding:24px">
  <form id="fLogin" class="ccard" style="width:100%;max-width:360px;display:grid;gap:12px" novalidate>
    <div class="brand" style="margin:0"><span class="glogo" style="width:38px;height:38px"></span><b>Glycine Lab</b></div>
    <div class="cs">Entre com a conta criada no Firebase para sincronizar os dados entre aparelhos.</div>
    <label class="fl">E-mail<input id="lgMail" type="email" autocomplete="username" inputmode="email"></label>
    <label class="fl">Senha<input id="lgPass" type="password" autocomplete="current-password"></label>
    <p class="ferr" id="lgErr" role="alert"></p>
    <button type="submit" class="btn" style="min-height:52px">Entrar</button>
    <button type="button" class="btn ghost" id="lgLocal">Usar só neste aparelho</button>
  </form>
</div>
<div id="splash" hidden''')

# camada de dados: Firebase no lugar do armazenamento do Claude
a = s.index("  if (window.claude && typeof window.claude.use === 'function'){")
end_marker = "  } else { clearTimeout(loadTimer); startLocal('Salvando só neste aparelho.'); }"
b = s.index(end_marker, a) + len(end_marker)
fb = r"""  // Firebase (Firestore + login por e-mail). Sem configuração: dados só neste aparelho.
  var FB = window.GL_FIREBASE, subscribed = false;
  function fbSubscribe(db){
    if (subscribed) return; subscribed = true; store = db; store.isFb = true;
    ['talhoes','projetos','areas','clima','safras'].forEach(function(c){ db.collection(c).onSnapshot({ includeMetadataChanges: false }, onSnapCol(c), onSnapErr); });
  }
  if (FB && FB.apiKey && window.firebase){
    try {
      firebase.initializeApp(FB);
      var fdb = firebase.firestore();
      fdb.enablePersistence({ synchronizeTabs: true }).catch(function(){});
      firebase.auth().onAuthStateChanged(function(u){
        if (u){ document.getElementById('login').hidden = true; fbSubscribe(fdb); }
        else if (!subscribed){ clearTimeout(loadTimer); document.getElementById('login').hidden = false; }
      });
      document.getElementById('fLogin').addEventListener('submit', function(e){
        e.preventDefault(); var em = document.getElementById('lgMail').value.trim(), pw = document.getElementById('lgPass').value, er = document.getElementById('lgErr');
        er.textContent = ''; if (!em || !pw){ er.textContent = 'Informe e-mail e senha.'; return; }
        firebase.auth().signInWithEmailAndPassword(em, pw).catch(function(x){ er.textContent = /network/i.test(x.code || '') ? 'Sem internet: o primeiro login precisa de conexão.' : 'E-mail ou senha incorretos.'; });
      });
      document.getElementById('lgLocal').addEventListener('click', function(){ document.getElementById('login').hidden = true; startLocal('Salvando só neste aparelho (sem login).'); });
    } catch(err){ clearTimeout(loadTimer); startLocal('Firebase não iniciou: salvando só neste aparelho.'); }
  } else { clearTimeout(loadTimer); startLocal('Salvando só neste aparelho: Firebase ainda não configurado (arquivo config.js).'); }
  window.glLogout = function(){ if (window.firebase && firebase.apps && firebase.apps.length) firebase.auth().signOut().then(function(){ location.reload(); }); };"""
s = s[:a] + fb + s[b:]
rep("'Salvo na página: projetos e talhões aparecem em qualquer aparelho com acesso a ela.'", "'Sincronizado com o Firebase: os dados aparecem em qualquer aparelho com o seu login.'")

# Ajustes: sair da conta
rep('    <div class="ccard"><h2>Sobre o modelo</h2>', '    <div class="ccard"><h2>Conta</h2><div class="cs">Dados sincronizados pelo Firebase quando você está conectado.</div><button type="button" class="btn ghost" onclick="window.glLogout && window.glLogout()">Sair da conta</button></div>\n    <div class="ccard"><h2>Sobre o modelo</h2>')

# service worker
rep('</body>', '''<script>
if ('serviceWorker' in navigator) window.addEventListener('load', function(){ navigator.serviceWorker.register('sw.js').catch(function(){}); });
</script>
</body>''')
open('/home/claude/glycine-pwa/index.html', 'w').write(s)
print('PWA gerado', len(s))
