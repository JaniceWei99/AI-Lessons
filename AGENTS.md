# AI-Class — Project Guide

## Quick Start
```bash
python3 serve.py   # Start server at http://localhost:4200
```

## Fixed Port
- **Port**: `4200`
- **Script**: `serve.py`
- Avoid using port 3000 (reserved for my_third/SoloHelm project)
- Avoid using port 4000 (previously used, may conflict)
- Avoid using port 5500 (conflicts with VS Code Live Server)

## Tech Stack
- Pure HTML5 + CSS3 + Vanilla JavaScript (ES6+)
- No build step, no npm, no Node.js required
- Only external dependency: Google Fonts CDN

## Project Structure (Multi-Edition)
```
AI-Class/
├── index.html              # Portal page (edition selector)
├── css/style.css           # Shared global stylesheet
├── js/main.js              # Shared global JavaScript
├── standard-5/             # 5-lesson standard edition
│   ├── index.html          # Edition landing page
│   └── lessons/            # lesson1-5.html
├── standard-15/            # 15-lesson comprehensive edition
│   ├── index.html          # Edition landing page
│   └── lessons/            # lesson1-15.html
├── lab-10/                 # 10-lab hands-on edition
│   ├── index.html          # Edition landing page
│   └── lessons/            # lesson1-10.html
├── test/                   # Test suite
└── docs/                   # Documentation
```

## Path Conventions
- Portal page (root): `css/style.css`, `js/main.js`
- Edition index pages: `../css/style.css`, `../js/main.js`
- Lesson files: `../../css/style.css`, `../../js/main.js`
- Edition index → portal: `../index.html`
- Lesson → edition index: `../index.html`

## Verification
```bash
python3 serve.py &
curl -s -o /dev/null -w "%{http_code}" http://localhost:4200/
# Should return 200
curl -s -o /dev/null -w "%{http_code}" http://localhost:4200/standard-5/index.html
# Should return 200
```

## Run Tests
```bash
uv run test/run_all.py
```
