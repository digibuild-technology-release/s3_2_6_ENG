# DigiBUILD Serivce 3.2.6 - EMOTION Pilot 5a
## Introduction
## Local Install

The software is stored in the projects GitHub repository, available here [LINK], or it can be directly pulled from DockerHub, at this [LINK]
To locally run it, simply clone the repository and run the following command

```
docker run -p 8090:8090 -d andnatalini/digibuild:emot-s326 
```

## API Endpoints 

The software has been deployed on the Azure DigiBUILD's Infrastructure and it's callable from this endpoint.

```
http://127.0.0.2:8090/decision_support_system/
```

To make it work, the following input body is requested

- "AUTOPILOT": = 0 or 1,
- "E_GRID": RT Value of the energy taken/given to the grid,
- "E_PLUG": RT power erogated byt the available plugs,
- "SOC": RT SoC of the Selected Vehicles


an example is reported here:

```json
{
    "AUTOPILOT": 0,
    "E_GRID": -50,
    "E_PLUG": [1, 1, 4, 1],
    "SOC": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
```


















