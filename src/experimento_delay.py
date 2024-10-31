import sounddevice as sd
import numpy as np
import time
import matplotlib.pyplot as plt

# Configuración de parámetros
fs = 44100  # Frecuencia de muestreo

def medir_retraso(duracion_tono=0.05):
    # Generar un sonido breve para reproducir (por ejemplo, un tono de 1 kHz)
    frecuencia_tono = 1000  # Frecuencia en Hz
    t = np.linspace(0, duracion_tono, int(fs * duracion_tono), endpoint=False)
    tono = 0.5 * np.sin(2 * np.pi * frecuencia_tono * t)

    # Configuración de dispositivos
    dispositivo_entrada = 1  # Índice del dispositivo de entrada (micrófono)
    dispositivo_salida = 3   # Índice del dispositivo de salida (altavoz)

    # Ejecutar el experimento 10 veces
    retrasos = []  # Lista para almacenar los retrasos medidos
    for i in range(10):
        # Reproducir el sonido breve y grabar simultáneamente
        print(f"Ejecutando prueba {i+1}/10: Reproduciendo tono y grabando...")
        inicio = time.time()
        grabacion = sd.playrec(
            tono,
            samplerate=fs,
            channels=1,
            dtype='float64',
            device=[dispositivo_entrada, dispositivo_salida]
        )
        sd.wait()  # Esperar a que termine la reproducción/grabación

        # Fin de la grabación
        fin = time.time()
        duracion_total = fin - inicio
        time.sleep(1)

        # Procesar la grabación para encontrar el retraso
        grabacion = grabacion.flatten()  # Convertir a 1D
        max_indice = np.argmax(np.abs(grabacion))  # Encontrar la posición del pico máximo
        tiempo_retraso = round(max_indice / fs, 4)   # Calcular el tiempo del retraso en segundos, redondeando a 4 decimales

        # Almacenar el retraso en la lista
        if tiempo_retraso > 0.0000:
            retrasos.append(tiempo_retraso)
            print(f"Duración total de la prueba: {duracion_total:.4f} segundos")
            print(f"Retraso medido en la prueba {i+1}: {tiempo_retraso:.4f} segundos")
            print("------------------------------------------------------------")

            # Graficar el tono original y la grabación
            tiempo_original = np.linspace(0, duracion_tono, len(tono), endpoint=False)
            tiempo_grabacion = np.linspace(0, len(grabacion) / fs, len(grabacion), endpoint=False)

            plt.figure(figsize=(10, 6))
            plt.plot(tiempo_original, tono, label='Tono original', alpha=0.7)
            plt.plot(tiempo_grabacion, grabacion, label='Grabación', alpha=0.7)
            plt.axvline(x=tiempo_retraso, color='r', linestyle='--', label='Retraso detectado')
            plt.title(f'Prueba {i+1}: Retraso medido = {tiempo_retraso:.4f} segundos')
            plt.xlabel('Tiempo (s)')
            plt.ylabel('Amplitud')
            plt.legend()
            plt.grid()
            plt.show()

    # Calcular la media de los retrasos
    media_retraso = np.mean(retrasos)
    print(f"--------------------------------------------------\n\033[1mMedia del retraso después de 10 pruebas: {media_retraso:.4f} segundos\033[0m")

if __name__ == "__main__":

    tiempos = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]

    for tiempo in tiempos:
        medir_retraso(tiempo)
