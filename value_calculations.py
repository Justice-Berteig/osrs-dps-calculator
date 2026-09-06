"""Functions to calculate gold/xp estimates
"""

import math

import constants


def get_avg_arrow_price(
    arrow_type,
    purchase_quantity
):
    basePrice = constants.ARROWS[arrow_type]["base_price"]
    priceSum = (
        (
            basePrice
            * (1 - math.pow(constants.ARROW_PRICE_CHANGE_PER, purchase_quantity))
        ) / (1 - constants.ARROW_PRICE_CHANGE_PER)
    )
    avgPrice = priceSum / purchase_quantity
    return avgPrice


def get_gp_per_hour(time_to_kill, target_enemy):
    gpPerHour = constants.ENEMIES[target_enemy]["gp_per_kill"] * (360 / time_to_kill)
    return gpPerHour


def get_cost_per_hour(
    equipped_arrow_type,
    active_attack_style,
    arrow_purchase_quantity
):
    avgArrowPrice = get_avg_arrow_price(equipped_arrow_type, arrow_purchase_quantity)
    secondsBetweenAttacks = constants.ATTACK_STYLES[active_attack_style]["attack_period_seconds"]
    costPerHour = avgArrowPrice * (360 / secondsBetweenAttacks * constants.ARROW_LOSS_RATE)
    return costPerHour
