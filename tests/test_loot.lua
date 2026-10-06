require "Soapmaker/Logic"

local S = Soapmaker

-- mirrorLoot: copy CookingMag1/Book_Fiction entries to our items at the same weight.
local MAP = {CookingMag1 = "CookingMagSoap", Book_Fiction = "Book_FightClub"}
local function has(items, name, weight)
    for i = 1, #items - 1, 2 do if items[i] == name and items[i + 1] == weight then return true end end
    return false
end
local shop = {items = {"Pen", 1, "CookingMag1", 2, "Book_Fiction", 4}}
local shared = {items = {"Base.CookingMag1", 0.1}}
local procedural = {list = {BookstoreCooking = shop, AliasA = shared, AliasB = shared}}
local rooms = {kitchen = {counter = {rolls = 1, items = {"Book_Fiction", 0.5}, junk = {items = {"CookingMag1", 0.2}}}}}
local plain = {items = {"Pen", 1}}
local n = S.mirrorLoot({procedural, rooms, plain}, MAP)
check(has(shop.items, "CookingMagSoap", 2), "magazine mirrored at weight 2")
check(has(shop.items, "Book_FightClub", 4), "book mirrored at weight 4")
check(has(shared.items, "CookingMagSoap", 0.1), "Base.-prefixed name mirrored")
check(#shared.items == 4, "shared alias table mirrored once")
check(has(rooms.kitchen.counter.items, "Book_FightClub", 0.5), "nested container mirrored")
check(has(rooms.kitchen.counter.junk.items, "CookingMagSoap", 0.2), "junk list mirrored")
check(#plain.items == 2, "lists without the source items are untouched")
check(n == 5, "returns entries added: " .. tostring(n))
local again = {items = {"CookingMag1", 1, "CookingMagSoap", 3}}
check(S.mirrorLoot({again}, MAP) == 0 and #again.items == 4, "already listed target is not added twice")
