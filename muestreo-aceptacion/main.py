import math

def calcular_poisson_probabilidad(landa, k):
    """
    Calcula la probabilidad de que ocurran exactamente 'k' eventos
    en un intervalo dado, según la distribución de Poisson.
    """
    if k < 0:
        return 0.0
    return (math.exp(-landa) * (landa ** k)) / math.factorial(k)

def calcular_probabilidad_aceptacion(N, n, c, p):
    """
    Calcula la probabilidad de aceptación (Pa) de un lote
    utilizando la aproximación de Poisson.
    """
    if n <= 0 or c < 0 or p < 0 or p > 1:
        print("Error: Los valores de n, c y p deben ser válidos.")
        return 0.0

    # Calcular lambda (media esperada de defectos en la muestra)
    # lambda = n * p
    landa = n * p

    print(f"Parámetros del lote y muestreo:")
    print(f"  Tamaño del lote (N): {N} unidades")
    print(f"  Tamaño de la muestra (n): {n} unidades")
    print(f"  Número de aceptación (c): {c} defectos")
    print(f"  Proporción de defectuosos en el lote (p): {p*100:.2f}%")
    print(f"  Media de defectos esperados en la muestra (lambda): {landa:.4f}")

    probabilidad_acumulada = 0.0
    for x in range(c + 1):
        prob = calcular_poisson_probabilidad(landa, x)
        print(f"  P(X={x} defectos) = {prob:.6f}")
        probabilidad_acumulada += prob

    return probabilidad_acumulada

if __name__ == "__main__":
    print("Bienvenido al calculador de Probabilidad de aceptación (Pa) para control de calidad.")
    print("Este programa usa la aproximación de Poisson, adecuada para lotes grandes y baja tasa de defectos.")

    try:
        N_lote = int(input("\nIntroduce el tamaño total del lote (N): "))
        n_muestra = int(input("Introduce el tamaño de la muestra a inspeccionar (n): "))
        c_aceptacion = int(input("Introduce el número máximo de defectos aceptables en la muestra (c): "))

        p_def = float(input("Introduce el porcentaje de unidades no conformes en el lote (p, ej. 1 para 1%): ")) / 100.0

        if p_def < 0 or p_def > 1:
            print("El porcentaje de unidades no conformes (p) debe estar entre 0 y 100.")
        elif n_muestra > N_lote:
            print("El tamaño de la muestra (n) no puede ser mayor que el tamaño del lote (N).")
        else:
            prob_aceptacion = calcular_probabilidad_aceptacion(N_lote, n_muestra, c_aceptacion, p_def)

            print(f"\n----------------------------------------------------")
            print(f"La probabilidad de aceptación (Pa) del lote es: {prob_aceptacion:.4f} ({prob_aceptacion*100:.2f}%)")
            print(f"----------------------------------------------------")
            print(f"\nEsto significa que hay un {prob_aceptacion*100:.2f}% de posibilidades de que un lote con {p_def*100:.2f}% de defectos sea aceptado por tu plan de muestreo.")

    except ValueError:
        print("\nError: Por favor, introduce valores numéricos válidos.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")