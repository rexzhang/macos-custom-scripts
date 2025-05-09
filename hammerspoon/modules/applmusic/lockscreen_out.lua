-- 监听锁屏事件
local lockWatcher = hs.caffeinate.watcher.new(function(eventType)
    if eventType == hs.caffeinate.watcher.screensDidLock then
        -- 暂停 Apple Music
        hs.applescript.applescript([[
tell application "System Events"
    set isRunning to exists (processes where name is "Music")
end tell

if isRunning then
    tell application "Music" to pause
end if
            ]])
        -- end
    end
end)
lockWatcher:start()
