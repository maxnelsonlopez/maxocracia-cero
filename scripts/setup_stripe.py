#!/usr/bin/env python3
"""
Script de Setup para Stripe - Maxocracia
=========================================

Guía interactiva para configurar Stripe paso a paso.
No requiere conocimientos técnicos previos.

Uso:
    python scripts/setup_stripe.py

Autor: Kimi (Moonshot AI)
Fecha: Febrero 2026
"""

import os
import sys
from pathlib import Path


def print_header(text: str):
    """Imprime header decorado."""
    print()
    print("=" * 60)
    print(f"  {text}")
    print("=" * 60)
    print()


def print_step(number: int, text: str):
    """Imprime paso numerado."""
    print(f"\n📌 PASO {number}: {text}")
    print("-" * 60)


def get_input(prompt: str, required: bool = True) -> str:
    """Obtiene input del usuario."""
    while True:
        value = input(f"{prompt}: ").strip()
        if value or not required:
            return value
        print("⚠️  Este campo es requerido")


def confirm(text: str) -> bool:
    """Pide confirmación al usuario."""
    response = input(f"{text} [s/N]: ").strip().lower()
    return response in ('s', 'si', 'yes', 'y')


def check_env_exists() -> Path:
    """Verifica/crea archivo .env"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("No se encontró archivo .env")
        if Path("config.example.env").exists():
            if confirm("¿Crear .env desde config.example.env?"):
                import shutil
                shutil.copy("config.example.env", ".env")
                print("✓ Archivo .env creado")
            else:
                print("❌ No se puede continuar sin .env")
                sys.exit(1)
        else:
            print("❌ No se encontró config.example.env")
            sys.exit(1)
    
    return env_path


def read_env() -> dict:
    """Lee variables de entorno actuales."""
    env_vars = {}
    if Path(".env").exists():
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key] = value
    return env_vars


def write_env(env_vars: dict):
    """Escribe variables a .env preservando comentarios."""
    env_path = Path(".env")
    
    # Leer contenido existente para preservar comentarios
    lines = []
    if env_path.exists():
        with open(env_path, "r") as f:
            lines = f.readlines()
    
    # Actualizar variables
    updated_vars = set()
    new_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=", 1)[0]
            if key in env_vars:
                new_lines.append(f"{key}={env_vars[key]}\n")
                updated_vars.add(key)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    # Agregar variables nuevas al final
    for key, value in env_vars.items():
        if key not in updated_vars:
            new_lines.append(f"{key}={value}\n")
    
    with open(env_path, "w") as f:
        f.writelines(new_lines)
    
    print("✓ Archivo .env actualizado")


def setup_stripe_keys():
    """Configura claves de Stripe."""
    print_step(1, "Configuración de Claves Stripe")
    
    print("""
Para obtener tus claves de Stripe:
1. Ve a https://dashboard.stripe.com
2. Inicia sesión
3. Ve a Desarrolladores → API keys
4. Copia las claves (empiezan con pk_... y sk_...)
""")
    
    env_vars = read_env()
    
    # Publishable Key
    current_pk = env_vars.get("STRIPE_PUBLISHABLE_KEY", "")
    if current_pk and not current_pk.startswith("..."):
        print(f"Publishable Key actual: {current_pk[:15]}...")
        if not confirm("¿Actualizar?"):
            pk = current_pk
        else:
            pk = get_input("STRIPE_PUBLISHABLE_KEY (pk_test_... o pk_live_...)")
    else:
        pk = get_input("STRIPE_PUBLISHABLE_KEY (pk_test_... o pk_live_...)")
    
    # Secret Key
    current_sk = env_vars.get("STRIPE_SECRET_KEY", "")
    if current_sk and not current_sk.startswith("..."):
        print(f"Secret Key configurada: {current_sk[:15]}...")
        if not confirm("¿Actualizar?"):
            sk = current_sk
        else:
            sk = get_input("STRIPE_SECRET_KEY (sk_test_... o sk_live_...)")
    else:
        sk = get_input("STRIPE_SECRET_KEY (sk_test_... o sk_live_...)")
    
    # Verificar modo
    if "sk_live" in sk:
        print("\n⚠️  ATENCIÓN: Estás configurando MODO LIVE (pagos reales)")
        if not confirm("¿Estás seguro?"):
            print("Cancelado. Usa sk_test_... para modo prueba.")
            return
    
    env_vars["STRIPE_PUBLISHABLE_KEY"] = pk
    env_vars["STRIPE_SECRET_KEY"] = sk
    
    write_env(env_vars)


def setup_stripe_prices():
    """Configura IDs de precios."""
    print_step(2, "Configuración de Precios (Price IDs)")
    
    print("""
Para obtener los Price IDs:
1. Ve a Stripe Dashboard → Productos
2. Crea o selecciona tu producto "Contributor"
3. En la sección de precios, copia el ID (price_...)
4. Repite para "Enterprise"

Nota: Si aún no has creado los productos, deja en blanco
y configura más tarde.
""")
    
    env_vars = read_env()
    
    current_contributor = env_vars.get("STRIPE_PRICE_CONTRIBUTOR", "")
    if current_contributor and not current_contributor.startswith("..."):
        print(f"Price Contributor actual: {current_contributor}")
        if confirm("¿Actualizar?"):
            env_vars["STRIPE_PRICE_CONTRIBUTOR"] = get_input(
                "STRIPE_PRICE_CONTRIBUTOR", 
                required=False
            ) or current_contributor
    else:
        price = get_input("STRIPE_PRICE_CONTRIBUTOR (price_...)", required=False)
        if price:
            env_vars["STRIPE_PRICE_CONTRIBUTOR"] = price
    
    current_enterprise = env_vars.get("STRIPE_PRICE_ENTERPRISE", "")
    if current_enterprise and not current_enterprise.startswith("..."):
        print(f"Price Enterprise actual: {current_enterprise}")
        if confirm("¿Actualizar?"):
            env_vars["STRIPE_PRICE_ENTERPRISE"] = get_input(
                "STRIPE_PRICE_ENTERPRISE",
                required=False
            ) or current_enterprise
    else:
        price = get_input("STRIPE_PRICE_ENTERPRISE (price_...)", required=False)
        if price:
            env_vars["STRIPE_PRICE_ENTERPRISE"] = price
    
    write_env(env_vars)


def setup_webhook():
    """Instrucciones para webhook."""
    print_step(3, "Configuración de Webhook")
    
    print("""
Para desarrollo local, necesitas el Stripe CLI:

1. Instala Stripe CLI:
   - Windows: Descarga de https://github.com/stripe/stripe-cli/releases
   - Mac: brew install stripe/stripe-cli/stripe
   - Linux: Descarga el binario

2. Autentica:
   stripe login

3. En otra terminal, ejecuta:
   stripe listen --forward-to localhost:5001/stripe/webhook

4. Copia el webhook signing secret (whsec_...) que se muestra
   y pégalo abajo:
""")
    
    env_vars = read_env()
    
    current_wh = env_vars.get("STRIPE_WEBHOOK_SECRET", "")
    if current_wh and not current_wh.startswith("..."):
        print(f"Webhook secret actual configurado")
        if confirm("¿Actualizar?"):
            wh = get_input("STRIPE_WEBHOOK_SECRET (whsec_...)", required=False)
            if wh:
                env_vars["STRIPE_WEBHOOK_SECRET"] = wh
    else:
        wh = get_input("STRIPE_WEBHOOK_SECRET (whsec_...)", required=False)
        if wh:
            env_vars["STRIPE_WEBHOOK_SECRET"] = wh
    
    write_env(env_vars)


def test_connection():
    """Prueba la conexión con Stripe."""
    print_step(4, "Prueba de Conexión")
    
    try:
        # Cargar variables
        from dotenv import load_dotenv
        load_dotenv()
        
        import stripe
        stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
        
        if not stripe.api_key:
            print("❌ No se encontró STRIPE_SECRET_KEY")
            return False
        
        # Probar conexión
        account = stripe.Account.retrieve()
        print(f"✓ Conexión exitosa")
        print(f"  Cuenta: {account.settings.dashboard.display_name or account.id}")
        print(f"  Modo: {'LIVE' if 'sk_live' in stripe.api_key else 'TEST'}")
        
        # Verificar productos
        try:
            prices = stripe.Price.list(limit=3)
            print(f"  Precios configurados: {len(prices.data)}")
            for price in prices.data:
                amount = price.unit_amount / 100 if price.unit_amount else 0
                print(f"    - {price.id}: ${amount} {price.currency.upper()}")
        except Exception as e:
            print(f"  ⚠️  No se pudieron listar precios: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False


def show_next_steps():
    """Muestra siguientes pasos."""
    print_header("CONFIGURACIÓN COMPLETADA")
    
    print("""
🎉 ¡Excelente! Has configurado Stripe.

PRÓXIMOS PASOS:

1. Iniciar servidor backend:
   python run.py

2. En otra terminal, iniciar webhook:
   stripe listen --forward-to localhost:5001/stripe/webhook

3. En otra terminal, iniciar frontend:
   cd frontend && npm run dev

4. Abrir en navegador:
   http://localhost:3000/upgrade

5. Probar checkout con tarjeta de prueba:
   Número: 4242 4242 4242 4242
   Fecha: Cualquier fecha futura
   CVC: Cualquier 3 dígitos

PARA PRODUCCIÓN:
- Cambia a claves LIVE (sk_live_...)
- Configura webhook en dashboard de Stripe
- Usa HTTPS obligatoriamente
- Revisa docs/GUIA_CONFIGURACION_STRIPE.md

¿PREGUNTAS?
- Revisa docs/GUIA_CONFIGURACION_STRIPE.md
- Stripe Docs: https://stripe.com/docs
""")


def main():
    """Función principal."""
    print_header("Setup de Stripe - Maxocracia")
    
    print("""
Este script te guiará paso a paso para configurar Stripe
y activar el sistema de pagos "Contribuidor Consciente".

Tiempo estimado: 10-15 minutos
Requisitos: Cuenta de Stripe (gratis)
""")
    
    if not confirm("¿Continuar?"):
        print("Cancelado.")
        return
    
    # Verificar .env
    check_env_exists()
    
    # Setup paso a paso
    setup_stripe_keys()
    setup_stripe_prices()
    setup_webhook()
    
    # Probar conexión
    if confirm("¿Probar conexión con Stripe ahora?"):
        test_connection()
    
    # Mostrar siguientes pasos
    show_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelado por usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
