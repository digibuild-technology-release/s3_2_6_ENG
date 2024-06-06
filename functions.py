import datetime
import numpy as np

class Balancer:
    
    def __init__():
        pass
    
    def reduce_energy_function(E_PLUG, E_EX, E_IMP):
        
        """
        Descrizione TT
        """
        
        current_date = datetime.datetime.now()
        current_month = current_date.month
        
        if E_IMP == 0:
            return E_PLUG  # Return the original values if there is no energy to import.

        threshold = 0.01
        possible_reduction = sum(E_PLUG)
        E_EX = min(E_EX, possible_reduction)

        while E_EX > threshold:
            total_reduction = sum(e for e in E_PLUG if e > threshold)
            if total_reduction == 0:
                break

            for i, e in enumerate(E_PLUG):
                if e > threshold:
                    proportional_reduction = (e / total_reduction) * E_EX
                    actual_reduction = min(proportional_reduction, e)
                    E_PLUG[i] -= actual_reduction
                    E_EX -= actual_reduction
                    if E_EX <= threshold:
                        break

        return [round(e, 2) for e in E_PLUG]


    def distribute_energy_function(E_PLUG, E_EX):
        
        """
        Descrizione TT
        """
        
        current_date = datetime.datetime.now()
        current_month = current_date.month
                
        limit, threshold = 11, 0.01
        total_plugs = len(E_PLUG)

        while E_EX > threshold:
            equal_share = E_EX / total_plugs
            for i in range(total_plugs):
                if E_PLUG[i] < limit:
                    energy_to_add = min(equal_share, limit - E_PLUG[i])
                    E_PLUG[i] += energy_to_add
                    E_EX -= energy_to_add

            if E_EX <= threshold or all(e >= limit for e in E_PLUG):
                break

        return [round(e, 2) for e in E_PLUG]

    def decision_support_system(AUTOPILOT, E_GRID, PLUG_CAPACITY, E_PLUGS):
        
        current_date = datetime.datetime.now()
        current_month = current_date.month
        
        if -E_GRID - PLUG_CAPACITY > 0 and AUTOPILOT == 1:
            setpoint_adjustment = "Reduce" if 3 <= current_month <= 10 else "Increase"
            print(f"{setpoint_adjustment} the HP Setpoint by 1°C")

        elif E_GRID - E_PLUGS > 0 and AUTOPILOT == 1:
            setpoint_adjustment = "Increase" if 3 <= current_month <= 10 else "Reduce"
            print(f"{setpoint_adjustment} the HP Setpoint by 1°C ")
            
        elif -E_GRID - PLUG_CAPACITY > 0 and AUTOPILOT == 0:
            setpoint_adjustment = "Reduce" if 3 <= current_month <= 10 else "Increase"
            print(f"{setpoint_adjustment} the HP Setpoint by 1°C or Enable Autopilot")
            
        elif E_GRID - E_PLUGS > 0 and AUTOPILOT == 0:
            setpoint_adjustment = "Increase" if 3 <= current_month <= 10 else "Reduce"
            print(f"{setpoint_adjustment} the HP Setpoint by 1°C or Enable Autopilot")