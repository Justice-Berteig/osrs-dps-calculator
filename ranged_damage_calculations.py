"""Functions for calculating ranged damage
"""

import math
import random

import constants


def get_effective_ranged_strength(
    ranged_level,
    active_prayer,
    active_attack_style
):
    """Get the effective ranged strength

    Calculated with the formula at
    https://oldschool.runescape.wiki/w/Damage_per_second/Ranged
    using a given ranged level, active prayer, and active attack style.
    """

    prayer_multiplier  = constants.PRAYER_MULTIPLIERS[active_prayer]
    attack_style_bonus = constants.ATTACK_STYLES[active_attack_style]["bonus"]

    effective_ranged_strength = math.floor(
        (ranged_level * prayer_multiplier)
        + attack_style_bonus
        + 8
    )

    return effective_ranged_strength


def get_max_hit(
    effective_ranged_strength,
    equipped_arrow_type
):
    """Get the maximum hit

    Calculated with the formula at
    https://oldschool.runescape.wiki/w/Damage_per_second/Ranged
    using a given effective ranged strength end equipped arrow.
    """

    equipment_ranged_strength = (
        constants.ARROWS[equipped_arrow_type]["ranged_strength"]
    )

    max_hit = math.floor(
        0.5 + (
            (
                effective_ranged_strength
                * (equipment_ranged_strength + 64)
            ) / 640
        )
    )

    return max_hit


def get_hit_chance(
    effective_ranged_attack,
    equipment_ranged_attack_bonus,
    target_enemy
):
    """Get the chance of landing a successful hit

    Calculated with the formula at
    https://oldschool.runescape.wiki/w/Damage_per_second/Ranged
    using a given effective ranged attack, equipment ranged attack bonus, and
    a target enemy.
    """

    # Start by calculating the attack and defense rolls.
    attack_roll = math.floor(
        effective_ranged_attack
        * (equipment_ranged_attack_bonus + 64)
    )

    defense_roll = (
        (constants.ENEMIES[target_enemy]["defense_level"] + 9)
        * (constants.ENEMIES[target_enemy]["ranged_defence"] + 64)
    )

    # Then calculate the hit chance
    hit_chance = None
    if attack_roll > defense_roll:
        hit_chance = (
            1 - (
                (defense_roll + 2)
                / (2 * (attack_roll + 1))
            )
        )
    else:
        hit_chance = (
            attack_roll
            / (2 * (defense_roll + 1))
        )

    return hit_chance
