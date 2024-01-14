-- 键盘输入自动全角符号转半角符号

-- 事件的API https://www.hammerspoon.org/docs/hs.eventtap.event.html
-- 按键(delete)定义表 https://github.com/Hammerspoon/hammerspoon/blob/master/extensions/keycodes/keycodes.lua


-- 预定义生效的应用清单
local app_map = {
    ["Code"] = true,
    ["Drafts"] = true,
    ["Joplin"] = true,
    ["Sublime Text"] = true
}
-- 预定义替换映射表
local replace_map = {
    ["·"] = "`",
    ["“"] = '"',
    ["”"] = '"',
    ["》"] = '>',
    ["《"] = '<',
}

local function keyboardReplaceListener(event)
    -- print("-----")
    -- print(hs.inspect.inspect(event:asData()))
    -- print(event:getButtonState(0))
    -- print(hs.inspect.inspect(event:getCharacters()))
    -- print(hs.inspect.inspect(event:getFlags()))
    -- print(event:getKeyCode())
    -- print(event:getProperty(hs.eventtap.event.properties.eventSourceUserData))
    -- print(event:getRawEventData())
    -- print(event:getTouchDetails())
    -- print(event:getTouches())
    -- print(event:getType())
    -- print(event:getUnicodeString())

    -- 只在指定的应用中生效
    local app_name = hs.application.frontmostApplication():name()
    -- print(app_name)
    if not app_map[app_name] then
        return
    end

    -- 安装替换表执行替换
    local new_char = replace_map[event:getCharacters()]
    if new_char then
        local delete_event = require("hs.eventtap")
        delete_event.keyStroke({}, "delete")
        hs.eventtap.keyStrokes(new_char)
    end
end

tap = hs.eventtap.new({ hs.eventtap.event.types.keyUp }, keyboardReplaceListener)
tap:start()
