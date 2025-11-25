import streamlit as st
import matplotlib.pyplot as plt
import random
import time
import math
import pandas as pd

# -------------------------------
#  Funciones principales
# -------------------------------

def inicializar_vector(n):
    return [0] * n

def distancia_origen(v):
    return math.sqrt(sum(coord**2 for coord in v))

def caminata_aleatoria(n_pasos=10, prob=0.5, size_paso=1, n_caminatas=100, n_dimensiones=2):
    caminatas = []
    tiempos = []
    distancias_finales = []

    for _ in range(n_caminatas):
        start = time.time()
        vector = inicializar_vector(n_dimensiones)
        trayectoria = [vector.copy()]

        for _ in range(n_pasos):
            for i in range(n_dimensiones):
                if random.random() < prob:
                    vector[i] -= size_paso
                else:
                    vector[i] += size_paso

            trayectoria.append(vector.copy())

        end = time.time()

        caminatas.append(trayectoria)
        tiempos.append(end - start)
        distancias_finales.append(distancia_origen(vector))

    return caminatas, tiempos, distancias_finales

def guardar_en_excel(caminatas, distancias, tiempos, nombre_archivo="resultados.xlsx"):
    df_distancias = pd.DataFrame({
        "Caminata": range(1, len(distancias) + 1),
        "Distancia_Final": distancias
    })

    df_tiempos = pd.DataFrame({
        "Caminata": range(1, len(tiempos) + 1),
        "Tiempo (s)": tiempos
    })

    with pd.ExcelWriter(nombre_archivo, engine="openpyxl") as writer:
        df_distancias.to_excel(writer, sheet_name="Distancias", index=False)
        df_tiempos.to_excel(writer, sheet_name="Tiempos", index=False)

    return nombre_archivo


# -------------------------------
#        STREAMLIT UI
# -------------------------------

st.title("Simulador de Caminatas Aleatorias 🐾")

st.sidebar.header("Parámetros")
n_pasos = st.sidebar.number_input("Número de pasos", min_value=1, value=100)
prob = st.sidebar.slider("Probabilidad de disminuir", 0.0, 1.0, 0.5)
size_paso = st.sidebar.number_input("Tamaño del paso", value=1.0)
n_caminatas = st.sidebar.number_input("Número de caminatas", min_value=1, value=50)
n_dimensiones = st.sidebar.number_input("Dimensiones", min_value=1, value=2)

if st.button("Ejecutar simulación"):
    caminatas, tiempos, distancias = caminata_aleatoria(
        n_pasos, prob, size_paso, n_caminatas, n_dimensiones
    )

    st.success("Simulación completada 🎉")

    # --- Distancias ---
    st.subheader("Distancias finales por caminata")
    st.line_chart(distancias)

    # --- Tiempos ---
    st.subheader("Tiempo por caminata")
    st.line_chart(tiempos)

    # --- Promedio ---
    st.write(f"**Promedio de distancias finales:** {sum(distancias)/len(distancias):.4f}")

    # --- Descarga Excel ---
    archivo = guardar_en_excel(caminatas, distancias, tiempos)

    with open(archivo, "rb") as f:
        st.download_button(
            label="Descargar resultados en Excel",
            data=f,
            file_name=archivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )