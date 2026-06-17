# Contributing to CowxBrowser

Thanks for your interest! Here's how to get started.

## Development setup

```bash
git clone https://github.com/your-username/cowxbrowser.git
cd cowxbrowser
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Code style

- Follow PEP 8
- No comments in code unless the intent is unclear
- Use type hints for function signatures
- Keep functions short and focused
- Use descriptive variable names

## Making changes

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `python -m pytest tests/ -v`
5. Commit with a clear message
6. Push and open a Pull Request

## Adding a new feature

- Add a new file in `cowxbrowser/` if the feature is self-contained
- Wire it into `browser.py` or `main.py` as appropriate
- Add a menu item or keyboard shortcut if user-facing
- Update README.md keyboard shortcuts table if applicable

## Testing

- Run `python -m pytest tests/ -v` to verify your changes don't break anything
- Manual testing: launch with `python run.py` and exercise your feature

## Project structure

```
cowxbrowser/
├── __init__.py              # Package marker
├── main.py                  # Entry point, app setup
├── browser.py               # Main window, nav bar, menu
├── tab_widget.py            # Tabs, web views, per-tab state
├── theme.py                 # Dark + light QSS styles
├── find_bar.py              # Find in page widget
├── bookmarks_manager.py     # Bookmarks data layer
├── bookmarks_bar.py         # Bookmarks toolbar
├── history_manager.py       # History data layer
├── history_dialog.py        # History dialog
├── download_manager.py      # Download manager
├── session_manager.py       # Session save/restore
├── extensions_manager.py    # Extension management
├── extensions_dialog.py     # Extension dialog
├── settings_dialog.py       # Preferences dialog
├── ad_blocker.py            # Ad blocking interceptor
├── reader_mode.py           # Reader mode (CSS)
├── update_checker.py        # Auto-update checker
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
