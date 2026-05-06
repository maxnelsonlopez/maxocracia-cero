import os
import subprocess
import sys

def build_frontend():
    """Ejecuta el build de Next.js y verifica la exportación."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_dir = os.path.join(base_dir, "frontend")
    static_dist_dir = os.path.join(base_dir, "app", "static", "dist")

    print(f"INFO: Iniciando build en {frontend_dir}...")
    
    try:
        # Ejecutar npm install por si acaso
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, shell=True)
        
        # Ejecutar el build/export (Next.js 16 exportará a /out por defecto)
        subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True, shell=True)
        
        # Mover archivos de frontend/out a app/static/dist
        if not os.path.exists(static_dist_dir):
            os.makedirs(static_dist_dir)
            
        print(f"INFO: Moviendo archivos a {static_dist_dir}...")
        # Usamos xcopy en Windows para asegurar la copia recursiva correcta
        subprocess.run(["xcopy", "/E", "/I", "/Y", "frontend\\out\\*", "app\\static\\dist\\"], cwd=base_dir, check=True, shell=True)
        
        if os.path.exists(os.path.join(static_dist_dir, "index.html")):
            print(f"OK: Build completado exitosamente en {static_dist_dir}")
        else:
            print(f"AVISO: El build terminó pero no se encontró index.html en {static_dist_dir}")
            
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Durante el build: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("ERROR: No se encontró 'npm'. Asegúrate de tener Node.js instalado.")
        sys.exit(1)

if __name__ == "__main__":
    build_frontend()
