# wenvi

Edit browser-editable content using Neovim.
Copy & paste is fully automated.

**wenvi** temporarily extracts the content of an editable element
(textareas, inputs, or contenteditable regions),
opens it in Neovim, and writes the result back when editing is finished.

No browser extensions required.
No manual copy & paste.
Just Neovim, outside the browser.

## Features

* Edit browser-editable elements (textareas, inputs, contenteditable regions) in Neovim.
* Automatically sync edited content back to the browser when you finish editing.
* Save edit buffers in `dataHome` (default: `~/.cache/wenvi`) for search or diff.
* Organize files by domain, with filenames that include page titles.

## Requirements

* macOS, Neovim, Hammerspoon, Chromium-based browser, Python (toml module)

## Installation

```bash
git clone https://github.com/kibi2/wenvi.git ~/wenvi
cd ~/wenvi
cp examples/hammerspoon/wenvi_config.lua.example ~/.hammerspoon/wenvi_config.lua
mkdir -p ~/.config/wenvi/
cp examples/config.toml.example ~/.config/wenvi/config.toml
```

> Edit the paths inside `wenvi_config.lua` to match your environment.
> Also, adjust the contents of `config.toml` as needed for your setup.

### Neovim init example

```lua
vim.opt.runtimepath:append('/path/to/wenvi_home/editor/nvim')
require 'wenvi'
```

> Replace `/path/to/wenvi_home/` with the path for your environment.

## Usage

* Open a browser page and press ⌘E (shortcut is configurable).

  * See: `~/wenvi/platforms/macos/hammerspoon/wenvi/init.lua`
* Neovim launches and automatically loads the text.
* Edit the text in Neovim. Closing the buffer writes the changes back to the browser.

## License

MIT License. See the LICENSE file for details.
