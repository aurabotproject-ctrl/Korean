# 한글 Quest

A Korean alphabet and vocabulary app for two young learners heading to Korea.

## Files
- `index.html`: the app (open this / host this)
- `data.js`: letters, mnemonics, lessons and words. Edit this to change content.
- `assets/`: logo, mascot, avatars and mnemonic pictures
- `src/` + `build.sh`: source used to build `index.html` (not needed for hosting)

## Adding the mnemonic pictures
Save each picture into `assets/mnemonics/` using the names from the image-prompt list,
e.g. `mn-giyeok.png`, `mn-a.png`. Stamps live in `assets/stamps/`, the map and passport cover in `assets/`. The app uses `.webp` if present, otherwise `.png`,
and shows an emoji until the picture is added.

## Hosting
Upload the whole folder to a GitHub repo and turn on GitHub Pages (or drag it into Netlify).
Progress is saved in each browser. Use Grown-ups → Backup to move progress between devices.
