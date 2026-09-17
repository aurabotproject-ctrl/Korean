#!/bin/bash
# Builds index.html (for GitHub Pages / Netlify) and artifact.html (for the Claude preview)
cd "$(dirname "$0")"
{ echo '<!doctype html>'; echo '<html lang="en">'; echo '<head>';
  echo '<meta charset="utf-8">'; echo '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">';
  echo '<link rel="icon" href="assets/icon-192.webp">'; echo '<link rel="apple-touch-icon" href="assets/icon-192.webp">';
  echo '<meta name="theme-color" content="#FBF6EC">';
  cat src/head.html; echo '</head>'; echo '<body>'; cat src/body.html; echo '</body>'; echo '</html>'; } > index.html
python3 - <<'PY'
s = open('src/head.html').read() + open('src/body.html').read()
s = s.replace('<button class="btn small ghost" id="bk-dl">Download file</button>', '')
s = s.replace("$('#bk-dl', main).onclick = ", "if (0) ")
open('artifact.html', 'w').write(s)
PY
