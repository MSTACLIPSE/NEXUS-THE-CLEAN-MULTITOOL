#!/usr/bin/env python3
"""
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
   SIMPLE ARSENAL LAUNCHER — MSTACLIPSE
"""

import curses
import importlib
import importlib.util
import os
import glob
import sys

TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")


class C:
    """Color pair indices."""
    NORMAL   = 1
    SELECTED = 2
    HEADER   = 3
    FOOTER   = 4
    DIVIDER  = 5


def load_tools():
    """
    Scan the tools/ directory for valid Python files.
    A valid tool must define TOOL_META (dict) and run() (callable).
    """
    if not os.path.exists(TOOLS_DIR):
        os.makedirs(TOOLS_DIR)
        return []

    tools = []
    for filepath in glob.glob(os.path.join(TOOLS_DIR, "*.py")):
        if filepath.endswith("__init__.py"):
            continue

        module_name = os.path.splitext(os.path.basename(filepath))[0]
        try:
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "TOOL_META") and hasattr(module, "run"):
                meta = module.TOOL_META
                tools.append({
                    "name":        meta.get("name", module_name),
                    "description": meta.get("description", ""),
                    "category":    meta.get("category", "OTHER"),
                    "module":      module,
                    "filename":    os.path.basename(filepath),
                })
        except Exception as e:
            # Silently skip broken scripts, but could log for debugging
            pass

    tools.sort(key=lambda t: t["name"].lower())
    return tools


# ───── DRAWING ─────────────────────────────────────────────────────────────

def draw_header(stdscr, width):
    """Draw the fiery NEXUS header."""
    msg = " NEXUS — Your Arsenal "
    try:
        stdscr.attron(curses.color_pair(C.HEADER) | curses.A_BOLD)
        stdscr.addstr(0, 0, msg.center(width)[:width])
        stdscr.attroff(curses.color_pair(C.HEADER) | curses.A_BOLD)
    except curses.error:
        pass


def draw_list(stdscr, tools, selected_idx, start_y, left_width, height):
    """Numbered tool list on the left panel."""
    if not tools:
        try:
            stdscr.addstr(start_y, 2, "No tools found. Drop scripts into tools/")
        except curses.error:
            pass
        return

    for i, tool in enumerate(tools):
        y = start_y + i
        if y >= height - 1:
            break

        line = f"  [{i+1}]  {tool['name']}"
        if len(line) > left_width - 2:
            line = line[:left_width - 5] + "…"

        try:
            if i == selected_idx:
                stdscr.attron(curses.color_pair(C.SELECTED) | curses.A_BOLD)
                stdscr.addstr(y, 2, line)
                stdscr.attroff(curses.color_pair(C.SELECTED) | curses.A_BOLD)
            else:
                stdscr.addstr(y, 2, line)
        except curses.error:
            pass


def draw_info(stdscr, tool, start_y, left_width, width):
    """Info panel on the right side."""
    if not tool:
        return

    x = left_width + 3               # leave room for the divider
    if x >= width - 5:
        return                       # not enough space

    max_len = width - x - 1
    def safe(s):
        return str(s)[:max_len]

    lines = [
        f"Name:        {safe(tool['name'])}",
        f"Description: {safe(tool['description'])}",
        f"Category:    {safe(tool.get('category', '?'))}",
        f"File:        {safe(tool.get('filename', ''))}",
    ]
    for i, text in enumerate(lines):
        try:
            stdscr.addstr(start_y + i, x, text)
        except curses.error:
            pass


def draw_divider(stdscr, left_width, height):
    """Vertical divider line."""
    for y in range(2, height - 1):
        try:
            stdscr.attron(curses.color_pair(C.DIVIDER))
            stdscr.addstr(y, left_width, "│")
            stdscr.attroff(curses.color_pair(C.DIVIDER))
        except curses.error:
            pass


def draw_footer(stdscr, text, width, height):
    """Bottom command bar."""
    if height < 1:
        return
    try:
        stdscr.attron(curses.color_pair(C.FOOTER) | curses.A_DIM)
        stdscr.addstr(height - 1, 0, text.center(width - 1)[:width - 1])
        stdscr.attroff(curses.color_pair(C.FOOTER) | curses.A_DIM)
    except curses.error:
        pass


# ───── MAIN CURSES LOOP ────────────────────────────────────────────────────

def main(stdscr):
    """Curses main loop (called by curses.wrapper)."""
    # Curses initialisation
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(False)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(C.NORMAL,   curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(C.SELECTED, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(C.HEADER,   curses.COLOR_RED,   curses.COLOR_BLACK)
    curses.init_pair(C.FOOTER,   curses.COLOR_RED,   curses.COLOR_BLACK)
    curses.init_pair(C.DIVIDER,  curses.COLOR_RED,   curses.COLOR_BLACK)

    stdscr.bkgd(' ', curses.color_pair(C.NORMAL))

    tools = load_tools()
    if not tools:
        try:
            stdscr.addstr(2, 2, "No valid tools found in tools/ folder.")
            stdscr.addstr(3, 2, "Make sure your scripts define TOOL_META and a run() function.")
        except curses.error:
            pass
        stdscr.refresh()
        stdscr.getch()
        return

    selected = 0
    search_query = ""
    filtered = tools

    while True:
        stdscr.erase()
        height, width = stdscr.getmaxyx()
        left_width = min(40, width // 3)

        # Apply search filter
        if search_query:
            q = search_query.lower()
            filtered = [t for t in tools if q in t["name"].lower() or q in t["description"].lower()]
        else:
            filtered = tools

        # Clamp selection after filter
        if not filtered:
            selected = -1
        else:
            selected = min(selected, len(filtered) - 1)

        selected_tool = filtered[selected] if selected >= 0 else None

        # Draw UI elements (safe against terminal too small)
        draw_header(stdscr, width)
        draw_divider(stdscr, left_width, height)
        draw_list(stdscr, filtered, selected, 2, left_width, height)
        if selected_tool:
            draw_info(stdscr, selected_tool, 2, left_width, width)
        draw_footer(stdscr, "↑↓ Navigate   ENTER Launch   / Search   Q Quit", width, height)

        stdscr.refresh()

        key = stdscr.getch()
        if key == -1:
            continue

        # --- Search mode handling ---
        if search_query:
            if key == 27:                           # Escape clears search
                search_query = ""
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                search_query = search_query[:-1]
            elif key in (curses.KEY_ENTER, 10, 13):
                search_query = ""                   # clear on Enter
            elif 32 <= key <= 126:
                search_query += chr(key)
            continue

        # --- Normal mode ---
        if key == ord('/'):
            search_query = ""
        elif key in (ord('q'), ord('Q')):
            break
        elif key == curses.KEY_UP:
            if filtered:
                selected = (selected - 1) % len(filtered)
        elif key == curses.KEY_DOWN:
            if filtered:
                selected = (selected + 1) % len(filtered)
        elif key in (curses.KEY_ENTER, 10, 13):
            if selected_tool and selected_tool.get("module"):
                # Exit curses temporarily, run the tool, then come back
                stdscr.clear()
                stdscr.refresh()
                curses.endwin()
                os.system('cls' if os.name == 'nt' else 'clear')

                try:
                    selected_tool["module"].run()
                except Exception as e:
                    print(f"Tool crashed: {e}")

                print("\nPress Enter to return to NEXUS...")
                input()

                # Re‑initialise curses (exactly as before)
                stdscr = curses.initscr()
                curses.curs_set(0)
                stdscr.keypad(True)
                stdscr.nodelay(False)
                curses.start_color()
                curses.use_default_colors()
                curses.init_pair(C.NORMAL,   curses.COLOR_WHITE, curses.COLOR_BLACK)
                curses.init_pair(C.SELECTED, curses.COLOR_BLACK, curses.COLOR_YELLOW)
                curses.init_pair(C.HEADER,   curses.COLOR_RED,   curses.COLOR_BLACK)
                curses.init_pair(C.FOOTER,   curses.COLOR_RED,   curses.COLOR_BLACK)
                curses.init_pair(C.DIVIDER,  curses.COLOR_RED,   curses.COLOR_BLACK)
                stdscr.bkgd(' ', curses.color_pair(C.NORMAL))
                # Refresh tool list (in case tools changed on disk)
                tools = load_tools()
                filtered = tools
                selected = 0


# ───── NEXUS INTEGRATION ──────────────────────────────────────────────────

TOOL_META = {
    "name":        "NEXUS Launcher",
    "description": "Interactive arsenal manager – launch your red team tools from a unified interface.",
    "category":    "FRAMEWORK"
}

def run():
    """Entry point called by NEXUS (or standalone)."""
    curses.wrapper(main)


if __name__ == "__main__":
    run()