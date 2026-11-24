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

local MAX_BEGINNER = 30
local MAX_INTERMEDIATE = 50
local MAX_PRO = 140

local BASE_HERO_COUNT = 17

local maxRequiredKeys = {
    [BEGINNER] = 1,
    [INTERMEDIATE] = 1,
    [PRO] = 1,
    [BEGINNER_INTERMEDIATE] = 2,
    [INTERMEDIATE_PRO] = 2,
    [BEGINNER_PRO] = 2,
    [ALL] = 3
}

-- RULES USED ON LOCATIONS:

function canAccessStage(stage, gauntlet_level)
    local stage_num = tonumber(stage)
    local keys = tonumber(_keysRequiredForStage(tonumber(gauntlet_level)))
    local highest_stage = _getClampedStageRequirement()

    if (highest_stage > 0 and stage_num > highest_stage) then
        return AccessibilityLevel.None
    end

    for i = 1, ((stage_num - 1) // 10), 1 do
        local has_keys = Tracker:ProviderCountForCode('UnlockKeys' .. tostring(i)) >= keys
        if not has_keys then
            return AccessibilityLevel.None
        end
    end

    -- if stage_num is after or at the stage that requires Nopwatch Refills, return SequenceBreak if the player doesn't have it:
    local nopwatch_refill_stage = tonumber(Tracker:ProviderCountForCode('nopwatch_refill_stage') or 0)
    if stage_num >= nopwatch_refill_stage then
        local has_nopwatch_refill = (Tracker:ProviderCountForCode('NopwatchRefills') or 0) > 0
        if not has_nopwatch_refill then
            return AccessibilityLevel.SequenceBreak
        end
    end

    return AccessibilityLevel.Normal
end

function isEmblemInLogic(rarity)
    local highest_stage = _getClampedStageRequirement()
    local stars = tonumber(rarity)

    if (stars <= 1) then
        return AccessibilityLevel.Normal
    end

    local mult = 0.34
    if stars == 3 then
        mult = 0.66
    end

    return canAccessStage((mult * highest_stage + 1), _getHighestGauntlet())
end

function CanClaimVictory()
    local highest_stage = _getClampedStageRequirement()

    if (_areHeroesRequired() and not _hasAllHeroesAvailable()) then
        return AccessibilityLevel.None
    else
        return canAccessStage(highest_stage, _getHighestGauntlet())
    end
end

-- INTERNAL HELPER FUNCTIONS
function _areHeroesRequired()
    return Tracker:ProviderCountForCode('all_heroes_required') or false
end

function _getIncludedGauntlets()
    return tonumber(Tracker:ProviderCountForCode('gauntlets_included') or 7)
end

function _getClampedStageRequirement()
    local highest_stage = tonumber(Tracker:ProviderCountForCode('highest_stage_required') or 0)

    if _isProIncluded() then
        return math.min(highest_stage, MAX_PRO)
    elseif _isIntermediateIncluded() then
        return math.min(highest_stage, MAX_INTERMEDIATE)
    else
        return math.min(highest_stage, MAX_BEGINNER)
    end
end

function _isBeginnerIncluded()
    local gauntlets_included = _getIncludedGauntlets()
    return gauntlets_included == BEGINNER or gauntlets_included == BEGINNER_INTERMEDIATE or gauntlets_included == BEGINNER_PRO or gauntlets_included == ALL
end

function _isIntermediateIncluded()
    local gauntlets_included = _getIncludedGauntlets()
    return gauntlets_included == INTERMEDIATE or gauntlets_included == BEGINNER_INTERMEDIATE or gauntlets_included == INTERMEDIATE_PRO or gauntlets_included == ALL
end

function _isProIncluded()
    local gauntlets_included = _getIncludedGauntlets()
    return gauntlets_included == PRO or gauntlets_included == BEGINNER_PRO or gauntlets_included == INTERMEDIATE_PRO or gauntlets_included == ALL
end

function _getMaxRequiredKeyCount()
    return maxRequiredKeys[_getIncludedGauntlets()] or 1
end

function _keysRequiredForStage(gauntlet_level)
    local gauntlets_included = _getIncludedGauntlets()

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

function _getTotalHeroes()
    local totalHeroes = BASE_HERO_COUNT
    totalHeroes = totalHeroes + 2 * (Tracker:ProviderCountForCode('DLC') or 0)            -- Ino and Masha
    totalHeroes = totalHeroes + 2 * (Tracker:ProviderCountForCode('PostGame') or 0)       -- Nia and Melia
    totalHeroes = totalHeroes + 2 * (Tracker:ProviderCountForCode('FutureRedeemed') or 0) -- Shulk and Rex
    totalHeroes = totalHeroes + 1 * (Tracker:ProviderCountForCode('Switch2') or 0)        -- Shimmer
    return totalHeroes
end

function _hasAllHeroesAvailable()
    return ((Tracker:ProviderCountForCode('Heroes') or 0) >= _getTotalHeroes())
end

function _getHighestGauntlet()
    if _isProIncluded() then
        return 3
    elseif _isIntermediateIncluded() then
        return 2
    else
        return 1
    end
end