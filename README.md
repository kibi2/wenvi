# wenvi

Edit browser editable content using Neovim.
Copy & paste is fully automated.

**wenvi** temporarily extracts the content of a focused editable element
(textareas, inputs, or contenteditable regions),
opens it in Neovim, and writes the result back when you finish editing.

No browser extensions.
No manual copy & paste.
Just Neovim, outside the browser.

## Features

* Edit browser editable elements (textarea, input, contenteditable) in Neovim.
* Automatically sync edits back to the browser on exit.
* Saves edit buffers in `dataHome` (default: `~/.cache/wenvi`) for search or diff.
* Organizes files by domain, with filenames including page titles.

## Requirements

* macOS, Neovim, Hammerspoon, Chromium-based browser, Python (toml module)

## Installation

```bash
git clone https://github.com/USER/wenvi.git ~/wenvi
cp examples/hammerspoon/wenvi_config.lua.example ~/.hammerspoon/wenvi_config.lua
mkdir -p ~/.config/wenvi/
cp examples/config.toml.example ~/.config/wenvi/config.toml
```

> Edit the paths inside `wenvi_config.lua` to match your environment.
> Also, adjust the contents of `config.toml` as needed for your setup.

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
