--- 权限问题: 系统设置 > 隐私与安全 > 辅助功能，勾选 Hammerspoon
---          如果不勾选不会主动触发权限请求

-- 1. 监听锁屏事件
local lockWatcher = hs.caffeinate.watcher.new(function(eventType)
    if eventType == hs.caffeinate.watcher.screensDidLock then
        -- 2. 暂停 Apple Music
        if hs.application.get("Music") then -- 检查应用是否运行
            hs.applescript.applescript([[
                tell application "Music" to pause
            ]])
        end
    end
end)
lockWatcher:start()

-- 3. 解锁时恢复播放（可选）
local unlockWatcher = hs.caffeinate.watcher.new(function(eventType)
    if eventType == hs.caffeinate.watcher.screensDidUnlock then
        if hs.application.get("Music") then
            hs.applescript.applescript([[
                tell application "Music" to play
            ]])
        end
    end
end)
unlockWatcher:start()

