-- put logic functions here using the Lua API: https://github.com/black-sliver/PopTracker/blob/master/doc/PACKS.md#lua-interface
-- don't be afraid to use custom logic functions. it will make many things a lot easier to maintain, for example by adding logging.
-- to see how this function gets called, check: locations/locations.json

local BEGINNER = 1
local INTERMEDIATE = 2
local BEGINNER_INTERMEDIATE = 3
local PRO = 4
local BEGINNER_PRO = 5
local INTERMEDIATE_PRO = 6
local ALL = 7

function getMaxRequiredKeyCount()
    local gauntlets_included = tonumber(Tracker:ProviderCountForCode('gauntlets_included') or 7)
    if gauntlets_included == ALL then
        return 3
    elseif gauntlets_included == BEGINNER_INTERMEDIATE or gauntlets_included == INTERMEDIATE_PRO or gauntlets_included == BEGINNER_PRO then
        return 2
    else
        return 1
    end
end

function keysRequiredForStage(stage, gauntlet_level)
    local gauntlets_included = tonumber(Tracker:ProviderCountForCode('gauntlets_included') or 7)

    if gauntlet_level == 3 then
        if gauntlets_included == PRO then
            return 1
        elseif gauntlets_included == BEGINNER_PRO or gauntlets_included == INTERMEDIATE_PRO then
            return 2
        else
            return 3
        end
    elseif gauntlet_level == 2 then
        if gauntlets_included == INTERMEDIATE or gauntlets_included == INTERMEDIATE_PRO then
            return 1
        else
            return 2
        end
    else
        return 1
    end
end

function canAccessStage(stage, gauntlet_level)
    local stage_num = tonumber(stage)
    local keys = tonumber(keysRequiredForStage(stage, gauntlet_level))
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

    local requiredkeys = getMaxRequiredKeyCount()

    while ((mult * highest_stage + 1) >= counter) do
        local val = (Tracker:ProviderCountForCode('UnlockKeys' .. tostring(i)) >= requiredkeys)
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

    local requiredkeys = getMaxRequiredKeyCount()

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