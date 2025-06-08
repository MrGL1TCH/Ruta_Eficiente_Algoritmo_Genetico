import numpy as np
import random
import math
import matplotlib.pyplot as plt

# Coordenadas de los lugares
coordenadas = {
    'Alcaldia Azcaptzalco': (19.4837, -99.1844),
    'Museo del Cuartel Zapatista': (19.1845, -99.0728),
    'ITESM SF': (19.3597, -99.2587),
    'Museo Frida Kahlo': (19.3551, -99.1622),
    'WTC': (19.3936, -99.1746),
    'Aeropuerto Benito Juárez': (19.4361, -99.0719),
    'Antigua Hacienda de Tlalpan': (19.288919, -99.1629),
    'Museo del Templo Mayor': (19.4350, -99.1312)
}
lugares = list(coordenadas.keys())

# Función para calcular distancia entre dos coordenadas (Haversine)
def calcular_distancia_haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# Crear matriz de distancias
num_lugares = len(lugares)
distancias = np.zeros((num_lugares, num_lugares))
for i in range(num_lugares):
    for j in range(num_lugares):
        if i != j:
            distancias[i, j] = calcular_distancia_haversine(coordenadas[lugares[i]], coordenadas[lugares[j]])

# Función para calcular la distancia total de una ruta
def calcular_distancia(ruta):
    return sum(distancias[ruta[i], ruta[i + 1]] for i in range(len(ruta) - 1)) + distancias[ruta[-1], ruta[0]]

# Generar una población inicial de rutas
def generar_poblacion_inicial(tamano_poblacion):
    return [random.sample(range(num_lugares), num_lugares) for _ in range(tamano_poblacion)]

# Función de selección (torneo)
def seleccionar_padres(poblacion, fitness, k=3):
    seleccionados = random.sample(range(len(poblacion)), k)
    return min(seleccionados, key=lambda i: fitness[i])

# Cruce (Order Crossover - OX)
def cruzar(padre1, padre2):
    n = len(padre1)
    inicio, fin = sorted(random.sample(range(n), 2))
    hijo = [-1] * n
    hijo[inicio:fin + 1] = padre1[inicio:fin + 1]
    elementos_restantes = [gen for gen in padre2 if gen not in hijo]
    for i in range(n):
        if hijo[i] == -1:
            hijo[i] = elementos_restantes.pop(0)
    return hijo

# Mutación (intercambio)
def mutar(ruta, prob_mutacion=0.1):
    if random.random() < prob_mutacion:
        i, j = random.sample(range(len(ruta)), 2)
        ruta[i], ruta[j] = ruta[j], ruta[i]

# Función para dibujar la ruta en el mapa
def dibujar_ruta(ruta, generacion, distancia_total):
    plt.figure(figsize=(8, 8))
    for i in range(len(ruta)):
        x1, y1 = coordenadas[lugares[ruta[i]]]
        x2, y2 = coordenadas[lugares[ruta[(i + 1) % len(ruta)]]]  # Volver al inicio al final
        plt.plot([x1, x2], [y1, y2], 'ro-')  # Línea roja con puntos
        plt.text(x1, y1, lugares[ruta[i]], fontsize=12)

    plt.title(f"Generación: {generacion} - Distancia Total: {distancia_total:.2f} km")
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.grid(True)
    plt.show()

# Algoritmo genético con visualización
def algoritmo_genetico_visualizado(tamano_poblacion, generaciones, prob_mutacion):
    poblacion = generar_poblacion_inicial(tamano_poblacion)
    fitness = [calcular_distancia(ruta) for ruta in poblacion]
    mejor_ruta = poblacion[np.argmin(fitness)]
    mejor_distancia = min(fitness)

    for gen in range(generaciones):
        nueva_poblacion = []
        for _ in range(tamano_poblacion // 2):
            padre1 = poblacion[seleccionar_padres(poblacion, fitness)]
            padre2 = poblacion[seleccionar_padres(poblacion, fitness)]
            hijo1, hijo2 = cruzar(padre1, padre2), cruzar(padre2, padre1)
            mutar(hijo1, prob_mutacion)
            mutar(hijo2, prob_mutacion)
            nueva_poblacion.extend([hijo1, hijo2])
        
        poblacion = nueva_poblacion
        fitness = [calcular_distancia(ruta) for ruta in poblacion]
        mejor_ruta_generacion = poblacion[np.argmin(fitness)]
        mejor_distancia_generacion = min(fitness)
        
        if mejor_distancia_generacion < mejor_distancia:
            mejor_ruta, mejor_distancia = mejor_ruta_generacion, mejor_distancia_generacion

        # Visualizar la ruta en las primeras 10 generaciones o cada 10 generaciones después
        if gen < 10 or (gen + 1) % 10 == 0:
            print(f"Generación {gen + 1}: Mejor distancia = {mejor_distancia:.2f} km")
            dibujar_ruta(mejor_ruta, gen + 1, mejor_distancia)

    return mejor_ruta, mejor_distancia

# Ejecutar el algoritmo genético con visualización
tamano_poblacion = 50
generaciones = 100
prob_mutacion = 0.3

mejor_ruta, mejor_distancia = algoritmo_genetico_visualizado(
    tamano_poblacion, generaciones, prob_mutacion
)

# Mostrar la mejor ruta encontrada
print("Mejor ruta encontrada:")
for i in mejor_ruta:
    print(lugares[i], end=" -> ")
print(f"\nDistancia total: {mejor_distancia:.2f} km")
