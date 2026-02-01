property isDebugFromScriptEditor : false

on run argv
	if (count of argv) < 1 then
		set isDebugFromScriptEditor to true
		debugValue("debug mode in script editor")
		debugValue("Check the log output in the message tab.(⌘+3)")
		-- set argv to {"display-dialog", "[DEBUG] : debug mode in script editor"}
		-- set argv to {"get-editable-info"}
		-- set argv to {"get-editable-text"}
		-- set argv to {"execute-javascript"}
		set argv to {"activate-browser"}
		-- set argv to {"activate-browser-tab"}
		-- set argv to {"set-editable-text"}
	end if
	return runWithArgv(argv)
end run

on runWithArgv(argv)
	try
		set cmd to item 1 of argv as text
		debugValue("==================== " & cmd & " ====================")
		debugValue(argv)
		set outValue to doMain(argv)
		debugValue("==================== RETURN ====================")
		debugValue(outValue)
		return outValue
	on error errMsg number errNum
		checkAndThrow(errMsg, errNum)
	end try
end runWithArgv

on checkAndThrow(errMsg, errNum)
	if 1000 <= errNum  and errNum < 2000 then
		error "[warn] " & errMsg number errNum
	else
		error "[error] " & errMsg number errNum
	end if
end checkAndThrow

on doMain(argv)
	if (count of argv) < 1 then
		error "No command" number 2001
	end if
	set cmd to item 1 of argv as text
	set args to rest of argv
	if cmd is "display-dialog" then
		handleDisplayDialog(args)
	else if cmd is "get-editable-info" then
		handleGetEditableInfo()
	else if cmd is "get-editable-text" then
		handleGetEditableText()
	else if cmd is "execute-javascript" then
		handleExecuteJavascript((item 1 of args) as text)
	else if cmd is "activate-browser" then
		handleActivateBrowser()
	else if cmd is "activate-browser-tab" then
		handleActivateBrowserTab((item 1 of args) as text)
	else if cmd is "set-editable-text" then
		handleSetEditableText((item 1 of args) as text)
	else
		error "Unknown command: " & cmd number 2002
	end if
end doMain

on handleDisplayDialog(args)
	set message to (item 1 of args) as text
	if (count of args) = 1 then
		debugValue("OK CANCEL")
		display dialog message
	else
		debugValue("OK")
		display dialog message buttons {"OK"} default button "OK"
	end if
end handleDisplayDialog

on handleExecuteJavascript(jsCode)
	set jsCode to jsCode as text
	tell application "__APP_NAME__"
		if (count of windows) = 0 then return
		tell front window
			tell active tab
				return execute javascript jsCode
			end tell
		end tell
	end tell
end handleExecuteJavascript

on handleGetEditableInfo()
	try
		tell application "System Events"
			set frontApp to first application process whose frontmost is true
			set bundleId to bundle identifier of frontApp
			set appName to name of frontApp
			set activeURL to ""
			tell frontApp
				set frontWin to first window whose value of attribute "AXMain" is true
				set activeURL to value of attribute "AXDocument" of frontWin
				if activeURL is missing value then
					error "activeURL is missing value"
				end if
				return bundleId & tab & appName & tab & activeURL
			end tell
		end tell
	on error
		error "No active URL" number 1003
	end try
end handleGetEditableInfo

on handleActivateBrowser()
	tell application "System Events"
		repeat with p in (application processes whose visible is true)
			try
				if (count of windows of p) = 0 then error "no window"
				set w to front window of p
				set docValue to value of attribute "AXDocument" of w
				if my isURL(docValue) then
					tell application (name of p as text)
						activate
					end tell
					exit repeat
				end if
			on error errMsg number errNum
			end try
		end repeat
	end tell
	return ""
end handleActivateBrowser

on handleActivateBrowserTab(activeURL)
	set activeURL to activeURL as text
	raiseTabByURL(activeURL)
	return "OK"
end handleActivateBrowserTab

on isURL(docValue)
	if docValue is missing value then return false
	if class of docValue is not text then return false
	return (docValue starts with "http://" or ¬
		docValue starts with "https://")
end isURL


on raiseTabByURL(activeURL)
	try
		tell application "__APP_NAME__"
			activate
			repeat with win in windows
				set iTab to 1
				repeat with tb in tabs of win
					if (URL of tb as text) = activeURL then
						set index of win to 1
						delay 0.2
						set active tab index of window 1 to iTab
						delay 0.1
						return "OK"
					end if
					set iTab to iTab + 1
				end repeat
			end repeat
			error "active Url does not exit." & activeURL number 1001
		end tell
	on error
		error "active Url does not exit." & activeURL number 1001
	end try
end raiseTabByURL

on handleGetEditableText()
  set previousClipboard to the clipboard
  set the clipboard to "}"

  tell application "System Events"
    keystroke "a" using command down
    delay 0.05
    keystroke "c" using command down
  end tell

  repeat 500 times
    delay 0.01
    try
      if the clipboard is not "}" then exit repeat
    end try
  end repeat

  try
    return the clipboard as text
  on error
    return ""
  end try
end handleGetEditableText

on handleSetEditableText(text_b64)
	set text_b64 to text_b64 as text
	set the clipboard to text_b64
	delay 0.05
	tell application "System Events"
		keystroke "a" using command down
		delay 0.05
		keystroke "v" using command down
	end tell
	return ""
end handleSetEditableText

on debugValue(v)
	try
		if isDebugFromScriptEditor then
			debugLog("[SCRIPT EDITOR]", v)
		else
			do shell script "printf '%s
' " & ¬
				quoted form of ("[APPLE] " & formatValue(v)) & ¬
				" >> /tmp/wenvi.osascript.log"
		end if
	end try
end debugValue

on isDebugEnabled()
	set lvl to my getLogLevel()
	if lvl is "" then return false
	if lvl is "debug" then return true
	return true
end isDebugEnabled

on getLogLevel()
	if isDebugFromScriptEditor then
		return "trace"
	end if
	try
		return do shell script "echo \"$WENVI_LOG_LEVEL\""
	on error
		return ""
	end try
end getLogLevel

on debugLog(label, val)
	if not isDebugFromScriptEditor then
		return
	end if
	try
		log label & formatValue(val)
	on error
		log label & val
	end try
end debugLog

on formatValue(v)
	if class of v is list then
		return formatList(v)
	else if class of v is record then
		return formatRecord(v)
	else
		return v as text
	end if
end formatValue

on formatList(xs)
	set out to "["
	repeat with i from 1 to count xs
		set out to out & formatValue(item i of xs)
		if i < (count xs) then set out to out & ", "
	end repeat
	return out & "]"
end formatList

on formatRecord(r)
	set out to "{"
	set ks to keys of r
	repeat with i from 1 to count ks
		set k to item i of ks
		set out to out & k & ": " & (r's k as text)
		if i < (count ks) then set out to out & ", "
	end repeat
	return out & "}"
end formatRecord

