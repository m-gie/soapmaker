require "Soapmaker/Logic"

-- Keen Cook (bought, and the free one Chef and Burger Flipper get), Bushcrafter,
-- Rancher and Farmer know Mix Soap. addGrantedRecipe only adds to vanilla's list, so it
-- doesn't clash with other mods. Characters get trait recipes when they are created
-- (on the server in multiplayer), so this runs in shared Lua on both sides.
local function definitions()
    local defs = {}
    local function trait(t)
        if t then defs[#defs + 1] = CharacterTraitDefinition.getCharacterTraitDefinition(t) end
    end
    local function profession(p)
        if p then defs[#defs + 1] = CharacterProfessionDefinition.getCharacterProfessionDefinition(p) end
    end
    trait(CharacterTrait.COOK)
    trait(CharacterTrait.COOK2)
    trait(CharacterTrait.WILDERNESS_KNOWLEDGE)
    profession(CharacterProfession.RANCHER)
    profession(CharacterProfession.FARMER)
    return defs
end

local function grant()
    local n = Soapmaker.grantRecipe(definitions(), "MixSoap")
    if n > 0 then print("[Soapmaker] MixSoap granted to " .. n .. " traits/professions") end
end

-- Safe to run more than once: definitions that already grant it are skipped.
grant()
Events.OnGameBoot.Add(grant)
