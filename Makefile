.PHONY: all build run install clean uninstall release dist

SHELL := /bin/bash
VENV  := venv
PYTHON := $(VENV)/bin/python3
VERSION := 0.1.0-alpha

all: build

# --- Run from source ---

run:
	@$(PYTHON) -m cowxbrowser.main

# --- Build standalone binary ---

$(VENV):
	@python3 -m venv $(VENV)
	@$(VENV)/bin/pip install -r requirements.txt

build: $(VENV) cowxbrowser.spec
	@$(PYTHON) -m PyInstaller cowxbrowser.spec --noconfirm
	@echo "✓ Binary: dist/cowxbrowser"

# --- Install ---

install: build
	@$(PYTHON) install.py
	@echo "✓ Installed"

# --- Distribution archive ---

dist: build
	@mkdir -p dist/release
	@cp dist/cowxbrowser dist/release/
	@cp README.md LICENSE dist/release/
	@cp install.py dist/release/
	@cp cowxbrowser.desktop dist/release/
	@cp -r cowxbrowser/ dist/release/cowxbrowser-src/
	@rm -rf dist/release/cowxbrowser-src/__pycache__
	@cd dist && tar czf cowxbrowser-$(VERSION)-linux-x86_64.tar.gz release/
	@rm -rf dist/release
	@echo "✓ Archive: dist/cowxbrowser-$(VERSION)-linux-x86_64.tar.gz"

# --- Clean ---

clean:
	@rm -rf build/ dist/ *.spec
	@rm -rf cowxbrowser/__pycache__ tests/__pycache__
	@echo "✓ Cleaned"

# --- Uninstall ---

uninstall:
	@rm -f $(HOME)/.local/bin/cowxbrowser
	@rm -rf $(HOME)/.local/bin/cowxbrowser
	@rm -f $(HOME)/.local/share/applications/cowxbrowser.desktop
	@echo "✓ Uninstalled"
