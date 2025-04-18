-- 解锁时恢复播放
local unlockWatcher = hs.caffeinate.watcher.new(function(eventType)
    if eventType == hs.caffeinate.watcher.screensDidUnlock then
        hs.applescript.applescript([[
tell application "System Events"
    set isRunning to exists (processes where name is "Music")
end tell

if isRunning then
    tell application "Music" to play
end if
            ]])
    end
end)
unlockWatcher:start()
