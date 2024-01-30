#From MQTT Building

E_grid=-25

#From MQTT Charging Station

E_plug_1=1
E_plug_2=1
E_plug_3=4
E_plug_4=1


"Algorithm"

E_plugs=E_plug_1 + E_plug_2 + E_plug_3 + E_plug_4

if E_grid > 0:
    E_build = E_grid - E_plugs
else:
    E_build=0

if E_grid<0:
    E_ex=-E_grid
    E_imp=0
else:
    E_ex=0
    E_imp=E_grid 
    
def distribuisci_energia(E_plug_1, E_plug_2, E_plug_3, E_plug_4, E_ex):
    E_plug = [E_plug_1, E_plug_2, E_plug_3, E_plug_4]
    limite = 11
    soglia = 0.01  # Soglia per evitare il ciclo infinito

    # Distribuisci E_ex in parti uguali inizialmente
    quota_iniziale = E_ex / 4
    for i in range(4):
        E_plug[i] += min(quota_iniziale, limite - E_plug[i])
        E_ex -= min(quota_iniziale, limite - E_plug[i])

    # Se rimane ancora energia in E_ex, distribuiscila tra le E_plug che non hanno raggiunto il limite
    while E_ex > soglia and j<100:
        for i in range(4):
            if E_plug[i] < limite:
                energia_da_aggiungere = min(E_ex, limite - E_plug[i])
                E_plug[i] += energia_da_aggiungere
                E_ex -= energia_da_aggiungere

                if E_ex <= soglia:
                    break

    # Arrotonda i valori finali per evitare numeri con troppe cifre decimali
    E_plug = [round(e, 2) for e in E_plug]

    return E_plug

# Esempio di utilizzo

Plug_capacity=44-E_plugs

E_ex=min(E_ex,Plug_capacity)

E_plug_1_new, E_plug_2_new, E_plug_3_new, E_plug_4_new = distribuisci_energia(E_plug_1, E_plug_2, E_plug_3, E_plug_4, E_ex)

print(E_plug_1_new, E_plug_2_new, E_plug_3_new, E_plug_4_new)
