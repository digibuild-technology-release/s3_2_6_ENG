import numpy as np
import datetime

# Inputs
E_grid = -10
E_plug = [1, 1, 4, 1]  # Plugs 1 through 4
SoC = [0] * 10         # SoC 1 through 10

# Algorithm
E_plugs = sum(E_plug)
E_build = max(0, E_grid - E_plugs)
E_ex, E_imp = max(0, -E_grid), max(0, E_grid)

# Algorithm for export
def distribute_energy(E_plug, E_ex):
    limit, threshold = 11, 0.01
    total_plugs = len(E_plug)

    while E_ex > threshold:
        equal_share = E_ex / total_plugs
        for i in range(total_plugs):
            if E_plug[i] < limit:
                energy_to_add = min(equal_share, limit - E_plug[i])
                E_plug[i] += energy_to_add
                E_ex -= energy_to_add

        if E_ex <= threshold or all(e >= limit for e in E_plug):
            break

    return [round(e, 2) for e in E_plug]


# Example usage
Plug_capacity = 44 - E_plugs
E_plugs_ex = distribute_energy(E_plug, min(E_ex, Plug_capacity))

if E_plugs_ex != E_plug:
    print(f'To Reduce Export {tuple(E_plugs_ex)}')

# Verify maximum vehicle capacities
Caps = [22] * 10
Caps_np = np.array(Caps)
SoCs_in_np = np.array(SoC)
Caps_ev = Caps_np * (100 - SoCs_in_np) / 100

# Algorithm for import
def reduce_energy(E_plug, E_ex):
    if E_imp == 0:
        return E_plug  # Return the original values if there is no energy to import.

    threshold = 0.01
    possible_reduction = sum(E_plug)
    E_ex = min(E_ex, possible_reduction)

    while E_ex > threshold:
        total_reduction = sum(e for e in E_plug if e > threshold)
        if total_reduction == 0:
            break

        for i, e in enumerate(E_plug):
            if e > threshold:
                proportional_reduction = (e / total_reduction) * E_ex
                actual_reduction = min(proportional_reduction, e)
                E_plug[i] -= actual_reduction
                E_ex -= actual_reduction
                if E_ex <= threshold:
                    break

    return [round(e, 2) for e in E_plug]

E_plugs_imp = reduce_energy(E_plug, min(E_imp, E_plugs))

if E_plugs_imp != E_plug:
    print(f'To Reduce Import {tuple(E_plugs_imp)}')

# Output
print('Plugs', E_plugs)
print('Grid', E_grid)
print('NewPlugs_ex', sum(E_plugs_ex))
print('Reduction_ex', E_plugs - sum(E_plugs_ex))
print('NewPlugs_imp', sum(E_plugs_imp))
print('Reduction_imp', E_plugs - sum(E_plugs_imp))

# Algorithm for setpoint
current_date = datetime.datetime.now()
current_month = current_date.month

if -E_grid - Plug_capacity > 0:
    setpoint_adjustment = "Reduce" if 3 <= current_month <= 10 else "Increase"
    print(f"{setpoint_adjustment} the HP Setpoint by 1°C")

if E_grid - E_plugs > 0:
    setpoint_adjustment = "Increase" if 3 <= current_month <= 10 else "Reduce"
    print(f"{setpoint_adjustment} the HP Setpoint by 1°C")