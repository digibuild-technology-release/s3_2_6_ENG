# DigiBUILD Serivce 3.2.6 - EMOTION Pilot 5a
## Introduction
## Local Install

The software is stored in the projects GitHub repository, available here [LINK], or it can be directly pulled from DockerHub, at this [LINK]
To locally run it, simply clone the repository and run the following command

```
docker run -p 8000:8000 -d digibuild.azurecr.io/emot/dss-api:latest
```

## API Endpoints 

The software has been deployed on the Azure DigiBUILD's Infrastructure and it's callable from this endpoint.

```
http://127.0.0.1:8000/decision_support_system/
```

To make it work, the following input body is requested

- "autopilot": = 0 or 1,
- "gridPower": RT Value of the energy taken/given to the grid, main_active_power_total
- "plugPowers": RT power erogated byt the available plugs, 55_1_ac_instant_power, 39_1_ac_instant_power, 39_2_ac_instant_power
- "vehicleSoCs": RT SoC of the Selected Vehicles


an example is reported here:

```json
{
    "autopilot": 1,
    "gridPower": -50,
    "plugPowers": [1, 1, 4],
    "vehicleSoCs": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
```


















