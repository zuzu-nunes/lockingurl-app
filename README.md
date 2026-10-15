# lockinGURL

Personal finance app in Honduran lempiras (budget, spending by category, net worth, goals, insights). A Home Screen web app: open the site in Safari on iPhone, tap Share, then Add to Home Screen.

First launch walks through a 3-step setup (name, monthly income, recommended budget). The budget helper splits income into savings (10-20%) and per-category limits, using the last 3 months of spending when available; rent and utilities are never planned below what they actually cost.

Data stays on the device (localStorage). Use Settings, then Save a backup, to keep a copy.

Icons and the in-app cover come from `icons/cover.jpg` (square crops around the text). `tools/make_icons.py` draws the older ring icon. Bump `VERSION` in `sw.js` on each release so phones pick up the update.
