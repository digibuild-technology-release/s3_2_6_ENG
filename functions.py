import datetime


def decision_support_system(autopilot, e_grid, plug_capacity, e_plugs):
    message = ""
    current_date = datetime.datetime.now()
    current_month = current_date.month

    if -e_grid - plug_capacity > 0 and autopilot == 1:
        setpoint_adjustment = "Reduce" if 3 <= current_month <= 10 else "Increase"
        message = f"{setpoint_adjustment} the HP Setpoint by 1°C"

    elif e_grid - e_plugs > 0 and autopilot == 1:
        setpoint_adjustment = "Increase" if 3 <= current_month <= 10 else "Reduce"
        message = f"{setpoint_adjustment} the HP Setpoint by 1°C "

    elif -e_grid - plug_capacity > 0 and autopilot == 0:
        setpoint_adjustment = "Reduce" if 3 <= current_month <= 10 else "Increase"
        message = f"{setpoint_adjustment} the HP Setpoint by 1°C or Enable Autopilot"

    elif e_grid - e_plugs > 0 and autopilot == 0:
        setpoint_adjustment = "Increase" if 3 <= current_month <= 10 else "Reduce"
        message = f"{setpoint_adjustment} the HP Setpoint by 1°C or Enable Autopilot"

    else:
        setpoint_adjustment = "No Setpoint Adjustment"
        message = f"{setpoint_adjustment}"

    return message


def reduce_energy_function(e_plugs, e_ex, e_imp):
    if e_imp == 0:
        return e_plugs  # Return the original values if there is no energy to import.

    threshold = 0.01
    possible_reduction = sum(e_plugs)
    e_ex = min(e_ex, possible_reduction)

    while e_ex > threshold:
        total_reduction = sum(e for e in e_plugs if e > threshold)
        if total_reduction == 0:
            break

        for i, e in enumerate(e_plugs):
            if e > threshold:
                proportional_reduction = (e / total_reduction) * e_ex
                actual_reduction = min(proportional_reduction, e)
                e_plugs[i] -= actual_reduction
                e_ex -= actual_reduction
                if e_ex <= threshold:
                    break

    return [round(e, 2) for e in e_plugs]


def distribute_energy_function(e_plug, e_ex):
    limit, threshold = 11, 0.01
    total_plugs = len(e_plug)

    while e_ex > threshold:
        equal_share = e_ex / total_plugs
        for i in range(total_plugs):
            if e_plug[i] < limit:
                energy_to_add = min(equal_share, limit - e_plug[i])
                e_plug[i] += energy_to_add
                e_ex -= energy_to_add

        if e_ex <= threshold or all(e >= limit for e in e_plug):
            break

    return [round(e, 2) for e in e_plug]

