import os
import subprocess
import sys
import shutil

def build_frontend():
    """Ejecuta el build de Next.js y verifica la exportación."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_dir = os.path.join(base_dir, "frontend")
    static_dist_dir = os.path.join(base_dir, "app", "static", "dist")

    print(f"INFO: Iniciando build en {frontend_dir}...")
    
    try:
        # 1. Limpiar directorio previo para evitar archivos fantasma
        if os.path.exists(static_dist_dir):
            print(f"INFO: Limpiando {static_dist_dir}...")
            shutil.rmtree(static_dist_dir)
        os.makedirs(static_dist_dir)

        # 2. Ejecutar npm install por si acaso
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, shell=True)
        
        # 3. Ejecutar el build/export
        subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True, shell=True)
        
        # 4. Mover archivos de frontend/out a app/static/dist
        print(f"INFO: Moviendo archivos a {static_dist_dir}...")
        # Usamos xcopy en Windows para asegurar la copia recursiva correcta
        subprocess.run(["xcopy", "/E", "/I", "/Y", "frontend\\out\\*", "app\\static\\dist\\"], cwd=base_dir, check=True, shell=True)
        
        # 5. Validación de integridad
        critical_files = ["index.html", "404.html", "favicon.ico"]
        missing = [f for f in critical_files if not os.path.exists(os.path.join(static_dist_dir, f))]
        
        if not missing:
            print(f"OK: Build completado y verificado exitosamente en {static_dist_dir}")
        else:
            print(f"AVISO: El build terminó pero faltan archivos críticos: {', '.join(missing)}")
            
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Durante el build: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_frontend()
