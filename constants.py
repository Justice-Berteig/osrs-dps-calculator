ENEMIES = {
    "ogress_warrior": {
        "max_health"    : 82,
        "defense_level" : 82,
        "ranged_defence": 16,
        "gp_per_kill"   : 0.01 * (24960 + 21120 + 11520),
        "pretty_name"   : "Ogress Warrior",
        "line_colour"   : "blue"
    },
    "ogress_shaman": {
        "max_health"    : 82,
        "defense_level" : 82,
        "ranged_defence": 8,
        "gp_per_kill"   : 0.01 * (24960 + 21120 + (11520 * 2.5)),
        "pretty_name"   : "Ogress Shaman",
        "line_colour"   : "green"
    }
}

ATTACK_STYLES = {
    "accurate" : {
        "bonus"                : 3,
        "attack_period_seconds": 2.4
    },
    "rapid"    : {
        "bonus"                : 0,
        "attack_period_seconds": 1.8
    },
    "longrange": {
        "bonus"                : 0,
        "attack_period_seconds": 2.4
    },
}

ARROWS = {
    "bronze" : {
        "base_price"     : 1,
        "ranged_strength": 7,
        "line_colour"    : "brown"
    },
    "iron"   : {
        "base_price"     : 3,
        "ranged_strength": 10,
        "line_colour"    : "black"
    },
    "steel"  : {
        "base_price"     : 12,
        "ranged_strength": 16,
        "line_colour"    : "grey"
    },
    "mithril": {
        "base_price"     : 32,
        "ranged_strength": 20,
        "line_colour"    : "darkblue"
    },
    "adamant": {
        "base_price"     : 80,
        "ranged_strength": 31,
        "line_colour"    : "darkgreen"
    }
}

PRAYER_MULTIPLIERS = {
    "none"    : 1,
    "sharpeye": 1.05,
    "hawkeye" : 1.10,
    "eagleeye": 1.15
}

ARROW_LOSS_RATE        = 0.2;
ARROW_PRICE_CHANGE_PER = 1.01;

MIN_LEVEL = 1
MAX_LEVEL = 99

NUMBER_PRECISION = 3
