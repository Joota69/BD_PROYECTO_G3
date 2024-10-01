import subprocess

# Ejecuta `juego.py` y `teclas.py` en paralelo
def main():
    juego_process = subprocess.Popen(["python", "juego.py"])
    teclas_process = subprocess.Popen(["python", "teclas.py"])

    juego_process.wait()
    teclas_process.wait()

if __name__ == "__main__":
    main()
