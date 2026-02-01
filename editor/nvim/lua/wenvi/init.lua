---@diagnostic disable: undefined-global
local M = {}

function M.setup()
	vim.g.wenvi_version = "0.1"

	vim.api.nvim_create_autocmd("BufWritePost", {
		desc = "Wenvi: BufWritePost",
		callback = function(ev)
			require("wenvi.write").on_write(ev.buf)
		end,
	})

	vim.api.nvim_create_autocmd({ "BufDelete", "BufWipeout" }, {
		desc = "Wenvi: BufDelete/BufWipeout",
		callback = function(ev)
			require("wenvi.write").on_delete(ev.buf)
		end,
	})

	vim.api.nvim_create_autocmd("QuitPre", {
		desc = "Wenvi: QuitPre",
		callback = function()
			require("wenvi.write").on_quit()
		end,
	})
end

M.setup()
return M
