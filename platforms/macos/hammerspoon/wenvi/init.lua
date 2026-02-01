---@diagnostic disable: undefined-global
local cfg = require("wenvi_config")
local last_run = 0
hs.hotkey.bind({ "ctrl" }, "E", function()
    local now = hs.timer.secondsSinceEpoch()
    if now - last_run < 2.0 then
        print("wenvi_read: suppressed")
        return
    end
    last_run = now

    assert(cfg.home, "cfg.home missing")
    assert(cfg.path, "cfg.path missing")
    assert(cfg.log_level, "cfg.log_level missing")
    hs.task.new("/usr/bin/env",
        function(code, out, err)
            if out ~= "" then
                print("stdout:", out)
            end
            if err ~= "" then
                print("stderr:", err)
            end
        end,
        {
            "WENVI_HOME=" .. cfg.home,
            "WENVI_LOG_LEVEL=" .. cfg.log_level,
            "WENVI_LOG_FILE=" .. cfg.log_file,
            "python3",
            cfg.path .. "/wenvi-read"
        }
    ):start()
end)

hs.urlevent.bind("sendkey", function(eventName, params)
    local key = params["key"]
    local app = hs.application.frontmostApplication()
    if not app then
        return
    end
    hs.eventtap.keyStroke({ "cmd" }, key)
end)

hs.urlevent.bind("cmd_ac_safe", function()
    local app = hs.application.frontmostApplication()
    if not app then
        return
    end

    local before = hs.pasteboard.getContents()
    app:activate(true)

    local after = nil
    for _ = 1, 3 do
        app:activate(true)
        hs.eventtap.keyStroke({ "cmd" }, "a")
        hs.timer.usleep(30 * 1000)
        hs.eventtap.keyStroke({ "cmd" }, "c")
        hs.timer.usleep(50 * 1000)

        after = hs.pasteboard.getContents()
        if after and after ~= before then
            break
        end
    end

    local tmp = "/tmp/wenvi_hammerspoon.tmp"
    local final = "/tmp/wenvi_hammerspoon.txt"

    local f = io.open(tmp, "w")
    if f then
        f:write(after or "")
        f:close()
        os.rename(tmp, final)
    end

    hs.pasteboard.setContents(before)
end)

hs.urlevent.bind("cmd_av_safe", function(_, params)
    local text = params.text
    if not text then
        return
    end

    local pb = hs.pasteboard
    local oldClipboard = pb.getContents()

    local ok, err = xpcall(function()
        pb.setContents(text)

        local app = hs.application.frontmostApplication()
        if not app then return end

        app:activate(true)
        hs.eventtap.keyStroke({ "cmd" }, "a")
        hs.timer.usleep(30 * 1000)
        hs.eventtap.keyStroke({ "cmd" }, "v")
    end, debug.traceback)

    pb.setContents(oldClipboard)

    if not ok then
        hs.notify.new({
            title = "cmd_av_safe failed",
            informativeText = err,
        }):send()
    end
end)
