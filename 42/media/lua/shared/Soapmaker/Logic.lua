-- Pure rules, no game objects, so they can be tested offline.
Soapmaker = Soapmaker or {}

-- Loot: for every items list under roots that has a source item of map (bare or
-- "Base." name) with weight w, add map[source] with weight w. Vanilla aliases share
-- tables, so each table is visited once; a target already in a list is not added again.
function Soapmaker.mirrorLoot(roots, map)
    local seen, added = {}, 0
    local function walk(t)
        if type(t) ~= "table" or seen[t] then return end
        seen[t] = true
        local items = t.items
        if type(items) == "table" then
            local present, extra = {}, {}
            for i = 1, #items - 1, 2 do
                if type(items[i]) == "string" then present[(items[i]:gsub("^Base%.", ""))] = true end
            end
            for i = 1, #items - 1, 2 do
                local name = type(items[i]) == "string" and (items[i]:gsub("^Base%.", ""))
                local target = name and map[name]
                if target and not present[target] then
                    extra[#extra + 1] = target
                    extra[#extra + 1] = items[i + 1]
                    present[target] = true
                end
            end
            for _, v in ipairs(extra) do items[#items + 1] = v end
            added = added + #extra / 2
        end
        for _, v in pairs(t) do walk(v) end
    end
    for _, root in ipairs(roots) do walk(root) end
    return added
end
