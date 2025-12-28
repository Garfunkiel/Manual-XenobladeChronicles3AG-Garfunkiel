-- put logic functions here using the Lua API: https://github.com/black-sliver/PopTracker/blob/master/doc/PACKS.md#lua-interface
-- don't be afraid to use custom logic functions. it will make many things a lot easier to maintain, for example by adding logging.
-- to see how this function gets called, check: locations/locations.json

function isEmblemInLogic(rarity)
    local highest_stage = Tracker:ProviderCountForCode('highest_stage_required') or 0
    local stars = tonumber(rarity)

    if (stars <= 1) then
        return AccessibilityLevel.Normal
    end

    local mult = 0.34
    if stars == 3 then
        mult = 0.66
    end

    local counter = 11
    local i = 1

    while ((mult * highest_stage + 1) >= counter) do
        local val = (Tracker:ProviderCountForCode('UnlockKeys' .. tostring(i)) >= 1)
        if not val then
            return AccessibilityLevel.SequenceBreak
        end

        counter = counter + 10
        i = i + 1
    end

    return AccessibilityLevel.Normal
end

function canClaimVictory()
    local highest_stage = Tracker:ProviderCountForCode('highest_stage_required') or 0
    local all = Tracker:ProviderCountForCode('all_heroes_required') or false

    local counter = 11
    local i = 1

    if (all) then
        local totalHeroes = 17
        totalHeroes = totalHeroes + 2 * (Tracker:ProviderCountForCode('DLC') or 0)
        totalHeroes = totalHeroes + 2 * (Tracker:ProviderCountForCode('PostGame') or 0)
        totalHeroes = totalHeroes + 2 * (Tracker:ProviderCountForCode('FutureRedeemed') or 0)

        local heroes = Tracker:ProviderCountForCode('Heroes') or 0
        if (heroes < totalHeroes) then
            return AccessibilityLevel.None
        end
    end

    while (highest_stage >= counter) do
        local val = (Tracker:ProviderCountForCode('UnlockKeys' .. tostring(i)) >= 1)
        if not val then
            return AccessibilityLevel.None
        end

        counter = counter + 10
        i = i + 1
    end

    return AccessibilityLevel.Normal
end