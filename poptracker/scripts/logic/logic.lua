-- put logic functions here using the Lua API: https://github.com/black-sliver/PopTracker/blob/master/doc/PACKS.md#lua-interface
-- don't be afraid to use custom logic functions. it will make many things a lot easier to maintain, for example by adding logging.
-- to see how this function gets called, check: locations/locations.json

function canAccessStage(stage, required_keys)
    local stage_num = tonumber(stage)
    local keys = tonumber(required_keys)
    local highest_stage = Tracker:ProviderCountForCode('highest_stage_required') or 0

    if (highest_stage > 0 and stage_num > highest_stage) then
        return AccessibilityLevel.None
    end

    if (stage_num <= 10) then
        return AccessibilityLevel.Normal
    end

    local i = 1
    local counter = 11

    while (stage_num >= counter) do
        local val = (Tracker:ProviderCountForCode('UnlockKeys' .. tostring(i)) >= keys)
        if not val then
            return AccessibilityLevel.None
        end

        counter = counter + 10
        i = i + 1
    end

    return AccessibilityLevel.Normal
end

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
    local highest_stage = tonumber(Tracker:ProviderCountForCode('highest_stage_required') or 0)
    local all = Tracker:ProviderCountForCode('all_heroes_required') or false
    local gauntlets_included = tonumber(Tracker:ProviderCountForCode('gauntlets_included') or 7)

    local counter = 11
    local i = 1

    if (all) then
        local totalHeroes = 17
        totalHeroes = totalHeroes + 2 * (Tracker:ProviderCountForCode('DLC') or 0)            -- Ino and Masha
        totalHeroes = totalHeroes + 2 * (Tracker:ProviderCountForCode('PostGame') or 0)       -- Nia and Melia
        totalHeroes = totalHeroes + 2 * (Tracker:ProviderCountForCode('FutureRedeemed') or 0) -- Shulk and Rex
        totalHeroes = totalHeroes + 1 * (Tracker:ProviderCountForCode('Switch2') or 0)        -- Shimmer

        local heroes = Tracker:ProviderCountForCode('Heroes') or 0
        if (heroes < totalHeroes) then
            return AccessibilityLevel.None
        end
    end

    local requiredkeys = 1
    if gauntlets_included == 4 or gauntlets_included == 5 or gauntlets_included == 7 then
        requiredkeys = 3
    elseif gauntlets_included == 2 or gauntlets_included == 3 or gauntlets_included == 6 then
        requiredkeys = 2
    end

    while (highest_stage >= counter) do
        local val = (Tracker:ProviderCountForCode('UnlockKeys' .. tostring(i)) >= requiredkeys)
        if not val then
            return AccessibilityLevel.None
        end

        counter = counter + 10
        i = i + 1
    end

    return AccessibilityLevel.Normal
end