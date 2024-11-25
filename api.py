from pydantic import BaseModel
from functions import *
from fastapi import FastAPI

"""
    E_PLUG = [1, 1, 4, 1] # List of the available plugs
    E_GRID = sum(E_PLUG) # List of all the SoC from 1 to 10


    E_PLUGS = sum(E_PLUG)
    E_BUILD = max(0, E_GRID - E_PLUGS)

    E_EX, E_IMP = max(0, -E_GRID), max(0, E_GRID)
"""

MAX_CAPACITY = 44
app = FastAPI()


class Variables(BaseModel):
    gridPower: int
    plugPowers: list
    vehicleSoCs: list
    autopilot: int


@app.post("/check_input/")
async def check_input(user_data: Variables):
    autopilot = user_data.autopilot
    grid_power = user_data.gridPower
    cs_plug_powers = user_data.plugPowers
    vehicle_socs = user_data.vehicleSoCs

    return {
        "autopilot": autopilot,
        "grid_power": grid_power,
        "cs_plug_powers": cs_plug_powers,
        "vehicle_socs": vehicle_socs
    }


@app.post("/decision_support_system/")
def dss(user_data: Variables):
    e_plugs = sum(user_data.plugPowers)
    plugs_capacity = MAX_CAPACITY - e_plugs
    e_ex, e_imp = max(0, - user_data.gridPower), max(0, user_data.gridPower)

    e_plugs_ex = distribute_energy_function(e_plug=user_data.plugPowers, e_ex=min(e_ex, plugs_capacity))
    e_plugs_imp = reduce_energy_function(user_data.plugPowers, min(e_imp, e_plugs), e_imp)

    message = decision_support_system(autopilot=user_data.autopilot, e_grid=user_data.gridPower,
                                      plug_capacity=plugs_capacity, e_plugs=e_plugs)

    if e_plugs_ex != user_data.plugPowers:
        advice = f"To Reduce Export {tuple(e_plugs_ex)}"
    elif e_plugs_imp != user_data.plugPowers:
        advice = f'To Reduce Import {tuple(e_plugs_imp)}'
    else:
        advice = f"No Advice"

    solution = {
        'plugs': e_plugs,
        'grid': user_data.gridPower,
        'NewPlugs_ex': sum(e_plugs_ex),
        'Reduction_ex': e_plugs - sum(e_plugs_ex),
        'NewPlugs_imp': sum(e_plugs_imp),
        'reduction_imp': e_plugs - sum(e_plugs_imp),
        'advice': advice,
        'setpoint_adjustment': message
    }

    return solution


@app.get("/test_connection")
def test_connection():
    return {"API": "Connected"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
