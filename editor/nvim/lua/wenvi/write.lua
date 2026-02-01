---@diagnostic disable: undefined-global
local M = {}


local WENVI_LOG_FILE = vim.env.WENVI_LOG_FILE
local WENVI_HOME = vim.env.WENVI_HOME
local WENVI_FILE_PATTERN = "%.wenvi.txt$"

local function log_debug(msg)
	if WENVI_LOG_FILE then
		local now = os.date("*t")
		local ms = math.floor((vim.loop.hrtime() / 1e6) % 1000)
		local timestamp = string.format("%02d:%02d.%03d", now.min, now.sec, ms)
		local message = string.format("[%s][vm][DEBUG]", timestamp) .. msg
		vim.fn.writefile({ message }, WENVI_LOG_FILE, "a")
	end
end

local function is_valid_buf(buf)
	return vim.api.nvim_buf_is_valid(buf) and vim.bo[buf].buflisted
end

local function get_buf_name(buf)
	local name = vim.api.nvim_buf_get_name(buf)
	if name == "" then
		return
	end
	return name
end

local function get_wenvi_file_name(buf)
	if not is_valid_buf(buf) then
		return
	end
	local text_file = get_buf_name(buf)
	if not text_file then
		return
	end
	if text_file:match(WENVI_FILE_PATTERN) == nil then
		return
	end
	WENVI_LOG_FILE = text_file:gsub("%.txt$", ".log")
	return text_file
end

local function should_skip()
	return vim.g.wenvi_skip_writeback == true
end

local function run_wenvi_write(text_file, save)
	log_debug("wenvi-write started for " .. text_file)
	vim.fn.jobstart({
		WENVI_HOME .. "/bin/wenvi-write",
		text_file,
		save,
	}, { detach = true })
end

local function set_write_flag(buf)
	vim.b[buf].wenvi_written = true
end

local function has_write_flag(buf)
	return vim.b[buf].wenvi_written == true
end

local function clear_write_flag(buf)
	vim.b[buf].wenvi_written = nil
end

local function process_buffer(buf, text_file)
	local save = "on"
	if should_skip() then
		log_debug("skip: wenvi_skip_writeback")
		return
	end
	log_debug(text_file)
	if vim.bo[buf].modified then
		log_debug("skip: buffer modified")
		save = "off"
	elseif not has_write_flag(buf) then
		log_debug("skip: not written")
		save = "off"
	else
		save = "on"
	end
	clear_write_flag(buf)
	run_wenvi_write(text_file, save)
end

function M.on_write(buf)
	local text_file = get_wenvi_file_name(buf)
	if text_file then
		log_debug("===+===+===+=== on_write START ===+===+===+===")
		set_write_flag(buf)
		log_debug("===+===+===+=== on_write END ===+===+===+===")
	end
end

function M.on_delete(buf)
	local text_file = get_wenvi_file_name(buf)
	if text_file then
		log_debug("===+===+===+=== on_delete START ===+===+===+===")
		process_buffer(buf, text_file)
		log_debug("===+===+===+=== on_delete END ===+===+===+===")
	end
end

function M.on_quit()
	if should_skip() then
		log_debug("skip: quit (wenvi)")
		return
	end
	for _, buf in ipairs(vim.api.nvim_list_bufs()) do
		local text_file = get_wenvi_file_name(buf)
		if text_file then
			log_debug("===+===+===+=== on_quit START ===+===+===+===")
			process_buffer(buf, text_file)
			log_debug("===+===+===+=== on_quit END ===+===+===+===")
		end
	end
end

return M
