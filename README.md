# wenvi

Edit browser text areas using Neovim. Copy & paste is automated.

## Features

* Edit text in Neovim and sync back to the browser automatically.
* Saves edits in `dataHome` (default: `~/.cache/wenvi`) for search or diff.
* Organizes files by domain with filenames including page title.

## Requirements

* macOS, Neovim, Hammerspoon, Chromium browser, Python toml module

## Installation

```bash
git clone https://github.com/USER/wenvi.git ~/wenvi
cp examples/hammerspoon/wenvi_config.lua.example ~/.hammerspoon/wenvi_config.lua
mkdir -p ~/.config/wenvi/
cp examples/config.toml.example ~/.config/wenvi/config.toml
```

> Edit the paths inside wenvi_config.lua to match your environment.

Neovim init example:

```lua
vim.opt.runtimepath:append('/path/to/wenvi_home/editor/nvim')
require 'wenvi'
```

> Replace `/path/to/wenvi_home/` with your environment path.

## Usage

* Open the browser page and press ⌘E (shortcut configurable).
* Edit text in Neovim. Closing the buffer writes changes back automatically.

## License

MIT License. See LICENSE file.