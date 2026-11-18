# Glycine Lab: instalação gratuita no iPhone

Esta pasta é o Glycine Lab como app instalável (PWA). Ele fica hospedado de graça no GitHub Pages, e os dados ficam no Firebase, também grátis. São três etapas; a 1 e a 2 levam uns 15 minutos.

## Arquivos

| Arquivo | O que é |
|---|---|
| `index.html` | o app |
| `config.js` | onde entra a configuração do seu Firebase (etapa 2) |
| `manifest.webmanifest`, `icons/` | nome e ícone do app na tela inicial |
| `sw.js` | faz o app abrir sem internet |
| `firestore.rules` | regras de segurança do banco (etapa 2) |
| `dados/glycine-lab-backup-2026-11-17.json` | seus dados atuais (S.L, L1, S.lucia1, projetos, safra 2026/27 e clima importado) |
| `build.py` | uso interno: gera o `index.html` a partir da versão que eu edito |

---

## Etapa 1: hospedar no GitHub Pages

1. Crie uma conta grátis em **github.com**.
2. Toque em **New repository**. Nome: `glycine-lab`. Marque **Public**. Toque em **Create repository**.
3. Na página do repositório, toque em **uploading an existing file** e arraste **todo o conteúdo desta pasta**, incluindo as pastas `icons` e `dados`. Toque em **Commit changes**.
4. Vá em **Settings → Pages**. Em *Branch*, escolha `main` e a pasta `/ (root)`. Toque em **Save**.
5. Depois de 1 ou 2 minutos, o endereço aparece no topo da página. Vai ser algo como `https://SEU-USUARIO.github.io/glycine-lab/`.

O repositório público deixa o **código** do app visível, mas **não os seus dados**. Os dados ficam no Firebase, protegidos pela sua senha.

---

## Etapa 2: criar o banco no Firebase

1. Entre em **console.firebase.google.com** com uma conta Google e toque em **Adicionar projeto**. Nome: `glycine-lab`. O Google Analytics pode ficar desligado.
2. **Login:** no menu, abra **Build → Authentication → Get started**.
   - Em *Sign-in method*, ative **E-mail/senha**.
   - Em *Users*, toque em **Add user** e crie o seu e-mail e uma senha.
   - Na lista de usuários, copie o **User UID**, um código longo. Ele é usado no passo 4.
3. **Banco de dados:** abra **Build → Firestore Database → Criar banco de dados**.
   - Local: **southamerica-east1 (São Paulo)**.
   - Modo: **produção**.
4. **Regras de segurança:** na aba **Regras** do Firestore, apague o que estiver lá e cole o conteúdo do arquivo `firestore.rules`. Troque `SEU_UID` pelo UID copiado no passo 2. Toque em **Publicar**. Com isso, só a sua conta lê e grava os dados.
5. **Ligar o app ao Firebase:**
   - Em **Configurações do projeto** (engrenagem) → *Seus apps*, toque no ícone **</>** (Web). Apelido: `glycine-lab`. Não marque o Hosting.
   - O Firebase mostra um bloco `const firebaseConfig = { apiKey: ..., ... }`. Copie só o que está **entre as chaves**.
6. No GitHub, abra o arquivo `config.js` e toque no lápis para editar. Troque a linha `window.GL_FIREBASE = null;` por:

```js
window.GL_FIREBASE = {
  apiKey: "...",
  authDomain: "...",
  projectId: "...",
  storageBucket: "...",
  messagingSenderId: "...",
  appId: "..."
};
```

   Toque em **Commit changes**. A `apiKey` do Firebase pode ficar visível: quem protege os dados são as regras do passo 4.

O plano gratuito (Spark) sobra para o seu uso, e não pede cartão.

---

## Etapa 3: instalar no iPhone e trazer os dados

1. Abra o endereço do GitHub Pages no **Safari**.
2. Entre com o e-mail e a senha criados no Firebase.
3. Toque em **Compartilhar → Adicionar à Tela de Início**. O ícone do Glycine Lab aparece.
4. Abra o app pelo ícone, vá em **Ajustes → Backup dos dados → Importar backup** e escolha o arquivo `glycine-lab-backup-2026-11-17.json`.
   - Antes, passe o arquivo para o iPhone por AirDrop, iCloud Drive ou e-mail, para ele aparecer no app Arquivos.
5. Pronto. No computador, é só abrir o mesmo endereço e entrar com o mesmo login, que os dados aparecem iguais.

**Sem internet no campo:** o app abre e salva normalmente. Quando o sinal volta, ele sincroniza sozinho. O primeiro login precisa de internet.

---

## Atualizações

Eu continuo editando o app nas nossas conversas. Para atualizar:

- **Jeito simples:** eu te mando o `index.html` novo, e você sobe por cima do antigo no GitHub (**Add file → Upload files**).
- **Jeito automático:** se você ligar o repositório `glycine-lab` a uma conversa comigo, eu mesmo envio as atualizações.

No iPhone, a versão nova chega na próxima vez que o app abrir com internet. Às vezes leva duas aberturas.

**Backup:** de tempos em tempos, use **Ajustes → Exportar backup** e guarde o arquivo no iCloud Drive.
