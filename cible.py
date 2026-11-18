name: Build exe

on:
  workflow_dispatch:
  push:
    branches: [main]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pyinstaller
      - run: pyinstaller --onefile --noconsole cible.py
      - uses: actions/upload-artifact@v4
        with:
          name: cible-exe
          path: dist/cible.exe
