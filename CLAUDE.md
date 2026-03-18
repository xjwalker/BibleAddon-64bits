# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BibleAddon-64bits is an NVDA screen reader addon for reading the Bible with chapter/verse navigation. It's a 64-bit compatible fork of the original BibleAddon by Carlos Pacheco. The addon UI and documentation are in Spanish.

## Build Commands

```bash
# Build the addon (produces BibleAddon-<version>.nvda-addon)
scons

# Requires: Python 3.11+, SCons, markdown package
```

The output `.nvda-addon` file is a ZIP archive installable in NVDA. Build configuration lives in `buildVars.py` (version, NVDA compatibility range, metadata). The build system is SCons (`sconstruct`).

## Architecture

### Core Modules (addon/globalPlugins/BibleAddon/)

- **`__init__.py`** — Main plugin entry point. Contains `GlobalPlugin` (NVDA integration, keyboard shortcuts) and `BibleDialog` (wxPython UI with testament/book/chapter selectors and verse display). Persists user's last-read position to `settings.json`.
- **`daoBible.py`** — `DaoBible` class providing SQLite access to `.bbl` Bible database files. Uses Python's standard `sqlite3` module (the 64-bit migration removed bundled 32-bit SQLite binaries).
- **`varsBible.py`** — Constants: testament names, 66-book metadata (ID, name, chapter count, covenant). Books split into `booksOt` (39) and `booksNt` (27).
- **`NTV.bbl`** — SQLite database with tables `Bible` (Book, Chapter, Verse, Scripture as RTF) and `Details` (Description, Abbreviation).

### RTF Processing (addon/globalPlugins/BibleAddon/striprtf/)

Bible verses are stored in RTF format in the database. The `striprtf.rtf_to_text()` function converts RTF to plain text for accessible display.

## Key Design Decisions

- **Standard sqlite3**: Uses Python's built-in `sqlite3` instead of bundled 32-bit binaries — this is the core 64-bit migration change.
- **RTF storage**: The `.bbl` database format stores verses as RTF for compatibility with existing Bible database files; text is stripped at display time.
- **Localization**: Uses `addonHandler.initTranslation()` for i18n readiness, though currently only Spanish is implemented.

## NVDA Addon Conventions

- Keyboard shortcuts are bound via NVDA's `scriptHandler` decorators with `gesture` strings (e.g., `kb:alt+1`).
- The addon targets NVDA 2024.1+ on 64-bit Windows with Python 3.11+.
- Manifest metadata is generated from `manifest.ini.tpl` + `buildVars.py` during build.
