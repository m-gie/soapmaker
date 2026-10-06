require "Soapmaker/Logic"

local S = Soapmaker

-- Fake trait/profession definitions with the two methods grantRecipe uses.
local function def(granted)
    local d = {list = granted or {}}
    function d:isGrantedRecipe(r) for _, v in ipairs(self.list) do if v == r then return true end end return false end
    function d:addGrantedRecipe(r) self.list[#self.list + 1] = r end
    return d
end

local cook, bush, rancher = def({"MakePizza"}), def(), def({"MixSoap"})
local n = S.grantRecipe({cook, bush, rancher}, "MixSoap")
check(n == 2, "adds to the two that lack it: " .. tostring(n))
check(cook:isGrantedRecipe("MixSoap") and #cook.list == 2, "keeps existing recipes and adds MixSoap")
check(#rancher.list == 1, "already granted is not added twice")
check(S.grantRecipe({cook, bush, rancher}, "MixSoap") == 0, "second run adds nothing")
check(S.grantRecipe({nil, bush}, "MixSoap") == 0, "missing definitions are skipped")
check(S.grantRecipe({}, "MixSoap") == 0, "no definitions, nothing added")
