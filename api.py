import logging
import json
import time
import datetime

import numpy as np

from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from functions import Balancer

from fastapi import FastAPI, Request

logging.basicConfig(
    level=logging.INFO,  # Livello minimo di registrazione
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Formato del messaggio di log
    datefmt='%Y-%m-%d %H:%M:%S'  # Formato della data e dell'ora
)

"""
    E_PLUG = [1, 1, 4, 1] # List of the available plugs
    E_GRID = sum(E_PLUG) # List of all the SoC from 1 to 10


    E_PLUGS = sum(E_PLUG)
    E_BUILD = max(0, E_GRID - E_PLUGS)

    E_EX, E_IMP = max(0, -E_GRID), max(0, E_GRID)
"""

SoC = [0] * 10
MAX_CAPACITY = 44

class Variables(BaseModel):
    
    E_GRID: int  # ETL
    E_PLUG: list # ETL
    SOC: list # ETL
    AUTOPILOT: int # UI
           
app = FastAPI()

@app.post("/check_input/")

async def check_input(user_data: Variables):
    
    AUTOPILOT = user_data.AUTOPILOT
    E_GRID = user_data.E_GRID
    E_PLUG = user_data.E_PLUG
    SOC = user_data.SOC
    
    return {
        "AUTOPILOT": AUTOPILOT,
        "E_GRID": E_GRID,
        "E_PLUG": E_PLUG,
        "SOC": SOC  
    }
    
@app.post("/decision_support_system/")
def dss(user_data: Variables):
    
    current_date = datetime.datetime.now()
    current_month = current_date.month
    
    E_PLUGS = sum(user_data.E_PLUG)
    PLUGS_CAPACITY = 44 - E_PLUGS
    E_EX, E_IMP = max(0, - user_data.E_GRID), max(0, user_data.E_GRID)
    
    E_PLUGS_EX = Balancer.distribute_energy_function(E_PLUG = user_data.E_PLUG, E_EX = min(E_EX, PLUGS_CAPACITY))
    E_PLUGS_IMP = Balancer.reduce_energy_function(user_data.E_PLUG, min(E_IMP, E_PLUGS), E_IMP)
    
    dss = Balancer.decision_support_system(AUTOPILOT=user_data.AUTOPILOT, E_GRID= user_data.E_GRID, PLUG_CAPACITY=PLUGS_CAPACITY, E_PLUGS=E_PLUGS)
    
    if E_PLUGS_EX != user_data.E_PLUG:
        advice = f"To Reduce Export {tuple(E_PLUGS_EX)}"
    elif E_PLUGS_IMP != user_data.E_PLUG:
        advice = f'To Reduce Import {tuple(E_PLUGS_IMP)}'
    else:
        advice = f"No Advice"
        
    # Suggestion on setpoints

    # AUTOPILOT 1        
    if -user_data.E_GRID - PLUGS_CAPACITY > 0 and user_data.AUTOPILOT == 1:
        SETPOINT_ADJUSTMENT = "Reduce" if 3 <= current_month <= 10 else "Increase"
        result = f"{SETPOINT_ADJUSTMENT} the HP Setpoint by 1°C"
    elif user_data.E_GRID - E_PLUGS > 0 and user_data.AUTOPILOT == 1:
        SETPOINT_ADJUSTMENT = "Increase" if 3 <= current_month <= 10 else "Reduce"
        result = f"{SETPOINT_ADJUSTMENT} the HP Setpoint by 1°C"
        
    # AUTOPILOT 0
    elif -user_data.E_GRID - PLUGS_CAPACITY > 0 and user_data.AUTOPILOT == 0:
        SETPOINT_ADJUSTMENT = "Reduce" if 3 <= current_month <= 10 else "Increase"
        result = f"{SETPOINT_ADJUSTMENT} the HP Setpoint by 1°C or Enable Autopilot"
    elif user_data.E_GRID - E_PLUGS > 0 and user_data.AUTOPILOT == 1:
        SETPOINT_ADJUSTMENT = "Increase" if 3 <= current_month <= 10 else "Reduce"
        result = f"{SETPOINT_ADJUSTMENT} the HP Setpoint by 1°C or Enable Autopilot"
        
        
    #No Conditions
    else:
        SETPOINT_ADJUSTMENT = "No Setpoint Adjustment"
        result = f"{SETPOINT_ADJUSTMENT}"
        
           
    #Output
    
    solution = {
        'Plugs': E_PLUGS,
        'Grid': user_data.E_GRID,
        'NewPlugs_ex': sum(E_PLUGS_EX),
        'Reduction_ex': E_PLUGS - sum(E_PLUGS_EX),
        'NewPlugs_imp': sum(E_PLUGS_IMP),
        'reduction_imp': E_PLUGS - sum(E_PLUGS_IMP),
        'Advice': advice,
        'SETPOINT_ADJUSTMENT': result
    }
    
    return solution
      
if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8090, reload=True)
    
    