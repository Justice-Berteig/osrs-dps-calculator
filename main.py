import os
import itertools
import math
import random
import re
import time

import matplotlib.pyplot as plt
import numpy as np

import constants
import damage_calculations
import ranged_damage_calculations
import value_calculations
from matrix import Matrix


def plot_profit_by_level():
    equipped_arrow = "adamant"
    equipment_ranged_attack_bonus = 68

    active_attack_style = "rapid"
    active_prayer = "none"

    target_enemy = "ogress_shaman"

    min_level = 50
    max_level = 99

    increments = 200

    levels = []
    ideal_values = []
    regen_values = []

    for level in range(min_level, max_level + 1):
        levels.append(level)

        effective_ranged_strength = ranged_damage_calculations.get_effective_ranged_strength(
            level,
            active_prayer,
            active_attack_style
        )
        max_hit = ranged_damage_calculations.get_max_hit(
            effective_ranged_strength,
            equipped_arrow
        )
        hit_chance = ranged_damage_calculations.get_hit_chance(
            effective_ranged_strength,
            equipment_ranged_attack_bonus,
            target_enemy
        )

        # Get various DPH estimates
        ideal_avg_dph = damage_calculations.get_ideal_avg_damage_per_attack(
            hit_chance,
            max_hit
        )
        ideal_values.append(damage_calculations.get_avg_dps(
            ideal_avg_dph,
            active_attack_style
        ))

        regen_avg_dph = damage_calculations.get_markov_avg_damage_per_attack_regen(
            hit_chance,
            max_hit,
            constants.ATTACK_STYLES[active_attack_style]["attack_period_seconds"],
            increments,
            constants.ENEMIES[target_enemy]["max_health"]
        )
        regen_values.append(damage_calculations.get_avg_dps(
            regen_avg_dph,
            active_attack_style
        ))

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.set(
        xlabel = "Ranged Level",
        ylabel = "DPS"
    )

    ax1.plot(
        levels,
        ideal_values,
        label="Ideal DPS",
        linestyle=(0, (5, 5)),
        color=constants.ENEMIES[target_enemy]["line_colour"],
        alpha=0.2
    )
    ax1.plot(
        levels,
        regen_values,
        label="True DPS",
        linestyle="solid",
        color=constants.ENEMIES[target_enemy]["line_colour"]
    )

    ax1.legend()

    levels_profit = []
    enemies = ["ogress_warrior", "ogress_shaman"]
    ideal_profit = {}
    true_profit = {}
    for enemy in enemies:
        ideal_profit[enemy] = []
        true_profit[enemy] = []

    for level in range(min_level, max_level + 1):
        levels_profit.append(level)
        for target_enemy in enemies:

            effective_ranged_strength = ranged_damage_calculations.get_effective_ranged_strength(
                level,
                active_prayer,
                active_attack_style
            )
            max_hit = ranged_damage_calculations.get_max_hit(
                effective_ranged_strength,
                equipped_arrow
            )
            hit_chance = ranged_damage_calculations.get_hit_chance(
                effective_ranged_strength,
                equipment_ranged_attack_bonus,
                target_enemy
            )

            # Get cost per hour of arrows
            cost_per_hour = value_calculations.get_cost_per_hour(
                equipped_arrow,
                active_attack_style,
                100
            )

            # Get various profit estimates
            ideal_avg_dph = damage_calculations.get_ideal_avg_damage_per_attack(
                hit_chance,
                max_hit
            )
            ideal_dps = ideal_avg_dph / constants.ATTACK_STYLES[active_attack_style]["attack_period_seconds"]
            ideal_ttk = damage_calculations.get_avg_time_to_kill(ideal_dps, target_enemy)
            ideal_gph = value_calculations.get_gp_per_hour(ideal_ttk, target_enemy)
            ideal_pph = ideal_gph - cost_per_hour
            ideal_profit[target_enemy].append(ideal_pph)

            regen_avg_dph = damage_calculations.get_markov_avg_damage_per_attack_regen(
                hit_chance,
                max_hit,
                constants.ATTACK_STYLES[active_attack_style]["attack_period_seconds"],
                increments,
                constants.ENEMIES[target_enemy]["max_health"]
            )
            true_dps = regen_avg_dph / constants.ATTACK_STYLES[active_attack_style]["attack_period_seconds"]
            true_ttk = damage_calculations.get_avg_time_to_kill(true_dps, target_enemy)
            true_gph = value_calculations.get_gp_per_hour(true_ttk, target_enemy)
            true_pph = true_gph - cost_per_hour
            true_profit[target_enemy].append(true_pph)

    ax2.set(
        xlabel = "Ranged Level",
        ylabel = "Profit/Hour"
    )

    min_y = 0
    max_y = 0
    for enemy in enemies:
        if ideal_profit[enemy][0] < min_y:
            min_y = ideal_profit[enemy][0]
        if true_profit[enemy][0] < min_y:
            min_y = true_profit[enemy][0]
        if ideal_profit[enemy][-1] > max_y:
            max_y = ideal_profit[enemy][-1]
        if true_profit[enemy][-1] > max_y:
            max_y = true_profit[enemy][-1]

        ax2.plot(
            levels_profit,
            ideal_profit[enemy],
            label="Ideal Profit/Hour Killing " + constants.ENEMIES[enemy]["pretty_name"],
            linestyle=(0, (5, 5)),
            color=constants.ENEMIES[enemy]["line_colour"],
            alpha=0.3
        )
        ax2.plot(
            levels_profit,
            true_profit[enemy],
            label="True Profit/Hour Killing " + constants.ENEMIES[enemy]["pretty_name"],
            linestyle="solid",
            color=constants.ENEMIES[enemy]["line_colour"],
        )

    ax2.set_ylim([min_y - 500, max_y + 500])
    ax2.axhspan(0, min_y - 500, color="red", alpha=0.2)

    ax2.legend()

    plt.show()


def main():
    arrow_types = list(constants.ARROWS.keys())
    equipment_ranged_attack_bonus = 68

    active_attack_style = "rapid"
    active_prayer = "none"

    target_enemies = list(constants.ENEMIES.keys())

    min_level = 50
    max_level = 99

    increments = 200

    levels = list(range(min_level, max_level + 1))
    data = {}
    for equipped_arrow in arrow_types:
        for target_enemy in target_enemies:
            data[equipped_arrow + " " + target_enemy] = []

    for level in levels:
        effective_ranged_strength = ranged_damage_calculations.get_effective_ranged_strength(
            level,
            active_prayer,
            active_attack_style
        )

        for equipped_arrow in arrow_types:
            max_hit = ranged_damage_calculations.get_max_hit(
                effective_ranged_strength,
                equipped_arrow
            )

            for target_enemy in target_enemies:
                hit_chance = ranged_damage_calculations.get_hit_chance(
                    effective_ranged_strength,
                    equipment_ranged_attack_bonus,
                    target_enemy
                )

                avg_dph = damage_calculations.get_markov_avg_damage_per_attack_regen(
                    hit_chance,
                    max_hit,
                    constants.ATTACK_STYLES[active_attack_style]["attack_period_seconds"],
                    increments,
                    constants.ENEMIES[target_enemy]["max_health"]
                )
                avg_dps = damage_calculations.get_avg_dps(
                    avg_dph,
                    active_attack_style
                )

                data[equipped_arrow + " " + target_enemy].append(avg_dps)

    fig, axs = plt.subplots(1, 2)

    for i in range(0, len(target_enemies)):
        axs[i].set_title(constants.ENEMIES[target_enemies[i]]["pretty_name"])

        axs[i].set(
            xlabel = "Ranged Level",
            ylabel = "DPS"
        )

        for equipped_arrow in arrow_types:
            axs[i].plot(
                levels,
                data[equipped_arrow + " " + target_enemies[i]],
                label=equipped_arrow.capitalize(),
                linestyle="solid",
                color=constants.ARROWS[equipped_arrow]["line_colour"]
            )

        axs[i].legend()

    for ax in axs:
        limits = ax.get_ylim()
        min_val = math.ceil(limits[0])
        max_val = math.floor(limits[1])
        y = min_val
        while y <= max_val:
            ax.axhline(y=y, color="lightgrey", linestyle=(0, (5, 5)), alpha=0.5, zorder=-100)
            y += 0.5

    plt.show()


if __name__ == "__main__":
    main()
