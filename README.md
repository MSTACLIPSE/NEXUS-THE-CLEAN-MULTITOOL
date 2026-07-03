

```
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
```
**SIMPLE ARSENAL LAUNCHER — MSTACLIPSE**  
*A unified terminal interface for your red team tools.*

---

## 🔥 Overview

NEXUS is a lightweight, curses‑based launcher that turns a directory of Python scripts into an interactive, searchable, keyboard‑driven arsenal.  
It is designed to sit at the heart of your private toolkit, providing instant access to every module without touching the command line.

- **Keyboard‑driven UI** – arrows, `/` search, `Enter` to launch, `Q` to quit.
- **Auto‑discovery** – scans the `tools/` folder and imports any script with a valid `TOOL_META` and `run()`.
- **Colour‑coded panels** – list on the left, info panel on the right, header and footer bars.
- **Crash‑safe** – if a tool crashes, NEXUS recovers and returns to the menu.
- **Self‑contained** – a single Python file; can even be added to its own `tools/` list.

---

## ⚙️ Installation

### Prerequisites
- **Python 3.8+** (curses is built‑in on Linux/macOS; on Windows, use `windows-curses`)
- **git** (optional, for cloning)

### 1. Clone the repository
```bash
git clone https://github.com/MSTACLIPSE/Nexus.git
cd Nexus
```

### 2. (Windows only) Install the curses library
```bash
pip install windows-curses
```
Linux and macOS ship with curses; no extra step is needed.

### 3. Run the launcher
```bash
python nexus.py
```

The launcher will automatically create a `tools/` folder on first run.  
Drop your tool scripts inside, and they will appear in the menu instantly.

---

## 📦 Tool Integration

Any Python file placed in `tools/` must define two things to be recognised:

```python
TOOL_META = {
    "name":        "My Tool",
    "description": "Does something lethal.",
    "category":    "ATTACK"
}

def run():
    """Entry point called by NEXUS."""
    print("Tool executed!")
    input("Press Enter to return...")
```

**Required fields:**
- `name` – displayed in the menu.
- `description` – shown in the info panel.
- `category` – any string (e.g., `"ATTACK"`, `"RECON"`, `"C2"`).

The `run()` function is called when you press **Enter**.  
It can use `print`, `input`, or even launch its own curses session – NEXUS will pause, run the tool, and re‑initialise its interface afterwards.

---

## 🧠 Architecture

```
nexus.py
 │
 ├── TOOLS_DIR scanner
 │    └── importlib dynamic import
 │
 ├── Curses UI
 │    ├── Header / Footer
 │    ├── Numbered list (left panel)
 │    ├── Info panel (right panel)
 │    └── Search mode (/ key)
 │
 └── Tool launcher
      └── curses.endwin() → tool.run() → curses.initscr()
```

---

## 🎮 Usage

| Key                | Action                                       |
|--------------------|----------------------------------------------|
| `↑` / `↓`          | Navigate tool list                           |
| `Enter`            | Launch selected tool                         |
| `/`                | Start search mode (type to filter)           |
| `Escape`           | Clear search                                 |
| `Backspace`        | Delete last search character                 |
| `Q`                | Quit NEXUS                                   |

After a tool finishes, press `Enter` to return to the launcher.

---

## 🧰 Example Tools

You can drop **PROJECT SUNDIAL** or any other script that follows the integration format.  
The directory structure should look like:

```
Nexus/
├── nexus.py
├── tools/
│   ├── Project Sundial.py
│   ├── reconnaissance.py
│   └── ...
└── README.md
```

---

## 🔒 OPSEC

- NEXUS itself stores no logs – all history and config are managed by the individual tools.
- Keep the `tools/` folder clean; broken scripts are silently skipped.
- Run inside a terminal with a dark background for the best use.

## 🐙 REPOSITORY

<h1 align="center">
  <br>
  PRIVATE — MSTACLIPSE RED TEAM ARSENAL
  <br>
</h1>

<p align="center">
  <b>© 2025 NEXUS LAUNCHER</b><br>
  <sub>Not for public distribution. All rights reserved.</sub>
</p>
