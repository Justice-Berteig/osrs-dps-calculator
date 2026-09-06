"""Functions for calculating damage
"""

import random

import numpy as np

import constants
from matrix import Matrix


def get_ideal_avg_damage_per_attack(
    hit_chance,
    max_hit
):
    """Get the average damage per attack roll under ideal circumstances

    Ideal circumstances being no damage loss due to overkill and no regeneration
    for enemies.

    Calculated with the formula at
    https://oldschool.runescape.wiki/w/Damage_per_second/Ranged
    using a given hit chance and maximum hit.
    """

    avg_damage_per_roll = (
        hit_chance * (
            (max_hit / 2)
            + (1 / (max_hit + 1))
        )
    )

    return avg_damage_per_roll


def get_damage_chances(
    hit_chance,
    max_hit
):
    """Get array of probabilities for the damage of an attack

    The value of each element of the array represents the probability (0 - 1) of
    dealing that element's index damage.
    """

    chance_per_damage = hit_chance / (max_hit + 1)
    damage_chances = []
    for i in range(0, max_hit + 1):
        if i == 0:
            damage_chances.append(1 - hit_chance)
        elif i == 1:
            damage_chances.append(chance_per_damage * 2)
        else:
            damage_chances.append(chance_per_damage)
    return damage_chances


def get_brute_force_avg_damage_per_attack(
    hit_chance,
    max_hit,
    simulated_kills,
    enemy_max_health
):
    """Get the average damage per attack roll by brute force simulation

    Takes into account overkill damage, but is slow.

    Calculated by simulating a given number of kills for a given enemy max
    health using a given hit chance and maximum hit. Simulation accounts for
    overkill damage by capping any damage done to the enemy's remaining health.
    """

    damage_chances = get_damage_chances(hit_chance, max_hit)

    # Function to roll damage for an attack
    def roll_damage(damage_chances):
        roll = random.random()
        sum = 0
        for i in range(0, len(damage_chances)):
            sum += damage_chances[i]
            if roll <= sum:
                return i
        return len(damage_chances - 1)

    # Simulate a bunch of kills and average the damage
    sum_damage = 0
    num_attacks = 0
    for _ in range(0, simulated_kills):
        enemy_health = enemy_max_health
        while enemy_health > 0:
            num_attacks += 1
            damage = roll_damage(damage_chances)

            # Cap damage to remaining enemy health
            if damage > enemy_health:
                damage = enemy_health

            enemy_health -= damage
            sum_damage += damage

    return sum_damage / num_attacks


def get_brute_force_avg_damage_per_attack_regen(
    hit_chance,
    max_hit,
    seconds_between_attacks,
    simulated_kills,
    enemy_max_health
):
    """Get the average damage per attack roll by brute force simulation

    Takes into account overkill damage and health regen, but is slow.

    Calculated by simulating a given number of kills for a given enemy max
    health using a given hit chance and maximum hit. Simulation accounts for
    overkill damage by capping any damage done to the enemy's remaining health.
    """

    damage_chances = get_damage_chances(hit_chance, max_hit)

    # Function to roll damage for an attack
    def roll_damage(damage_chances):
        roll = random.random()
        sum = 0
        for i in range(0, len(damage_chances)):
            sum += damage_chances[i]
            if roll <= sum:
                return i
        return len(damage_chances - 1)

    # Simulate a bunch of kills and average the damage
    sum_damage = 0
    num_attacks = 0
    for _ in range(0, simulated_kills):
        enemy_health = enemy_max_health
        regen_cooldown = None
        while enemy_health > 0:
            if regen_cooldown != None:
                regen_cooldown -= seconds_between_attacks
                if regen_cooldown <= 0:
                    enemy_health += 1
                    regen_cooldown = 60

            num_attacks += 1
            damage = roll_damage(damage_chances)

            # Cap damage to remaining enemy health
            if damage > enemy_health:
                damage = enemy_health

            enemy_health -= damage
            sum_damage += damage

            if enemy_health < enemy_max_health and regen_cooldown == None:
                regen_cooldown = 60

    return sum_damage / num_attacks


def get_markov_avg_damage_per_attack(
    hit_chance,
    max_hit,
    step_count,
    enemy_max_health
):
    """Get the average damage per attack roll using a Markov chain

    Takes into account overkill damage, and is faster thanks to numpy

    Calculated by creating a transition matrix for an enemy with a given max
    health, and calculating the transition matrix after a given number of steps
    through a Markov chain using the initial transition matrix.
    """

    matrix_side_length = enemy_max_health + max_hit

    damage_chances = get_damage_chances(hit_chance, max_hit)
    # Make sure hit chance array is as long as matrix side length
    while len(damage_chances) < (matrix_side_length):
        damage_chances.append(0)

    # Create initial values for transition matrix
    transition_matrix = np.empty(
        (matrix_side_length, matrix_side_length),
        dtype="float"
    )
    for i in range(0, matrix_side_length):
        for j in range(0, matrix_side_length):
            if i >= enemy_max_health:
                transition_matrix[i][j] = damage_chances[j]
            else:
                if 0 <= j < i:
                    transition_matrix[i][j] = 0
                if i <= j < min(i + len(damage_chances), matrix_side_length):
                    transition_matrix[i][j] = damage_chances[j-i]


    result_matrix = transition_matrix
    for _ in range(0, step_count):
        result_matrix = np.matmul(result_matrix, transition_matrix)

    damage_chances_after = result_matrix[0]
    for i in range(1, len(result_matrix)):
        for j in range(0, len(result_matrix[i])):
            damage_chances_after[j] += result_matrix[i][j]

    for i in range(0, len(damage_chances_after)):
        damage_chances_after[i] /= len(result_matrix)

    avg_lost_damage = 0
    for i in range(
        len(damage_chances_after) - (max_hit),
        len(damage_chances_after)
    ):
        avg_lost_damage += (i - enemy_max_health) * damage_chances_after[i]

    return get_ideal_avg_damage_per_attack(hit_chance, max_hit) - avg_lost_damage


def get_markov_avg_damage_per_attack_regen(
    hit_chance,
    max_hit,
    seconds_between_attacks,
    step_count,
    enemy_max_health
):
    """Get the average damage per attack roll using a Markov chain

    Takes into account overkill damage and health regen, and is faster thanks to
    numpy.

    Calculated by creating a transition matrix for an enemy with a given max
    health, and calculating the transition matrix after a given number of steps
    through a Markov chain using the initial transition matrix.
    """

    matrix_side_length = enemy_max_health + max_hit

    # Calculate chances for all damage values from 0 to max_hit
    damage_chances = get_damage_chances(hit_chance, max_hit)
    # Make sure hit chance array is as long as matrix side length
    while len(damage_chances) < (matrix_side_length):
        damage_chances.append(0)

    # Calculate regen chance per hit
    regen_chance_per_hit = seconds_between_attacks / 60
    # Calculate damage chances when accounting for regen
    damage_chances_with_regen = []
    prev_diff = None
    for i in range(0, len(damage_chances) + 1):
        damage_chances_with_regen.append(0)
        if prev_diff != None:
            damage_chances_with_regen[i] = prev_diff

        if i < len(damage_chances):
            damage_chances_with_regen[i] += damage_chances[i] * regen_chance_per_hit
            prev_diff = damage_chances[i] - damage_chances[i] * regen_chance_per_hit

    # Create initial values for transition matrix
    transition_matrix = np.empty(
        (matrix_side_length, matrix_side_length),
        dtype="float"
    )
    for i in range(0, matrix_side_length):
        for j in range(0, matrix_side_length):
            if i == 0 or i >= enemy_max_health:
                transition_matrix[i][j] = damage_chances[j]
            else:
                if 0 <= j < (i - 1):
                    transition_matrix[i][j] = 0
                if (i - 1) <= j < min(i + len(damage_chances), matrix_side_length):
                    transition_matrix[i][j] = damage_chances_with_regen[j-i+1]

    # Calculate transition matrix after step_count steps
    result_matrix = transition_matrix
    for _ in range(0, step_count):
        result_matrix = np.matmul(result_matrix, transition_matrix)

    # Calculate overall damage chances by averaging each column
    # First sum each column
    damage_chances_after = result_matrix[0]
    for i in range(1, len(result_matrix)):
        for j in range(0, len(result_matrix[i])):
            damage_chances_after[j] += result_matrix[i][j]
    # Divide each column by column length
    for i in range(0, len(damage_chances_after)):
        damage_chances_after[i] /= len(result_matrix)

    # Calculate average damage lost
    avg_lost_damage = 0
    for i in range(
        len(damage_chances_after) - (max_hit),
        len(damage_chances_after)
    ):
        avg_lost_damage += (i - enemy_max_health) * damage_chances_after[i]

    return get_ideal_avg_damage_per_attack(hit_chance, max_hit) - avg_lost_damage


def get_avg_dps(
    avg_damage_per_hit,
    active_attack_style
):
    """Get the average damage per second

    Calculated using a given hit chance and maximum hit by simply dividing
    average damage per hit by the number of seconds between each attack.
    """

    seconds_between_attacks = (
        constants.ATTACK_STYLES[active_attack_style]["attack_period_seconds"]
    )

    avg_dps = avg_damage_per_hit / seconds_between_attacks

    return avg_dps


def get_avg_time_to_kill(
    avg_dps,
    target_enemy
):
    """Get the average time to kill

    Calculated using a given average damage per second and a target enemy by
    simply dividing the target enemy's max health by the average damage per
    second.
    """

    time_to_kill = constants.ENEMIES[target_enemy]["max_health"] / avg_dps

    return time_to_kill
