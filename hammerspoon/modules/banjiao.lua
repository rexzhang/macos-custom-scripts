-- 键盘输入自动全角符号转半角符号

-- 事件的API https://www.hammerspoon.org/docs/hs.eventtap.event.html
-- 按键(delete)定义表 https://github.com/Hammerspoon/hammerspoon/blob/master/extensions/keycodes/keycodes.lua


-- 预定义生效的应用清单
local app_map = {
    ["com.microsoft.VSCode"] = true,
    ["com.agiletortoise.Drafts-OSX"] = true,
    ["net.cozic.joplin-desktop"] = true,
    ["com.sublimetext.4"] = true
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
    -- 只在指定的应用中生效
    local app_bundle_id = hs.application.frontmostApplication():bundleID()
    -- print(app_name)
    if not app_map[app_bundle_id] then
        return
    end

    -- 安装替换表执行替换
    local new_char = replace_map[event:getCharacters()]
    if new_char then
        hs.eventtap.keyStrokes(new_char)

        return true -- 阻止原事件
    end
end

-- keyUp 会看到原始输入,并可能破坏原有输入(比如键入时被选中的文字)
-- KeyDown 不会显示原始输入,对输入无干扰
tap = hs.eventtap.new({ hs.eventtap.event.types.keyDown }, keyboardReplaceListener)
tap:start()
