"""
Ejemplo: Préstamo Simple de Maxos

Demuestra la creación y ejecución de un MaxoContract básico.

Uso:
    python -m maxocontracts.examples.simple_loan
"""

import os
import sys
from decimal import Decimal

# Añadir path del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from maxocontracts.blocks.gamma_protector import WellnessProtectorBlock
from maxocontracts.core.contract import MaxoContract
from maxocontracts.core.types import VHV, ContractTerm, Participant, Wellness
from maxocontracts.oracles.synthetic import SyntheticOracle


def create_simple_loan():
    """
    Crea un contrato de préstamo simple entre dos participantes.

    Escenario:
    - Alice presta 10 Maxos a Bob
    - Bob devuelve en 7 días
    - Costo VHV del contrato: 0.5h tiempo gestión
    """
    print("=" * 60)
    print("MAXOCONTRACTS - Ejemplo: Préstamo Simple")
    print("=" * 60)
    print()

    # 1. Crear participantes
    print("1. Creando participantes...")
    alice = Participant(
        id="alice-001",
        name="Alice",
        wellness_current=Wellness(value=Decimal("1.2")),  # Floreciendo
    )

    bob = Participant(
        id="bob-001",
        name="Bob",
        wellness_current=Wellness(value=Decimal("1.1")),  # Neutral-positivo
    )

    print(f"   - {alice.name}: γ = {alice.wellness_current.value}")
    print(f"   - {bob.name}: γ = {bob.wellness_current.value}")
    print()

    # 2. Crear contrato
    print("2. Creando contrato...")
    contract = MaxoContract(
        contract_id="loan-simple-001",
        description="Préstamo de 10 Maxos por 7 días",
        participants=[alice, bob],
        civil_summary="Alice presta 10 Maxos a Bob. Bob devuelve en 7 días sin interés.",
    )

    print(f"   ID: {contract.contract_id}")
    print(f"   Estado: {contract.state.value}")
    print()

    # 3. Añadir términos
    print("3. Añadiendo términos...")

    term1 = ContractTerm(
        id="term-1",
        description="Alice transfiere 10 Maxos a Bob",
        vhv_cost=VHV(T=Decimal("0.2"), V=Decimal("0"), R=Decimal("0")),
    )

    term2 = ContractTerm(
        id="term-2",
        description="Bob devuelve 10 Maxos en máximo 7 días",
        vhv_cost=VHV(T=Decimal("0.3"), V=Decimal("0"), R=Decimal("0")),
    )

    contract.add_term(term1)
    contract.add_term(term2)

    print(f"   Término 1: {term1.description}")
    print(f"   Término 2: {term2.description}")
    print(f"   VHV Total: T={contract.total_vhv.T}h")
    print()

    # 4. Validar axiomas
    print("4. Validando axiomas...")
    is_valid, results = contract.validate()

    for result in results:
        status = "✓" if result.is_valid else "✗"
        print(f"   {status} {result.axiom_code}: {result.message}")

    print(f"\n   Resultado: {'VÁLIDO' if is_valid else 'INVÁLIDO'}")
    print()

    # 5. Procesar hacia activación
    print("5. Proceso de aceptación...")

    # Enviar a aceptación
    contract.submit_for_acceptance()
    print(f"   Estado: {contract.state.value}")

    # Ambas partes aceptan
    contract.accept_term("term-1", "alice-001")
    contract.accept_term("term-1", "bob-001")
    contract.accept_term("term-2", "alice-001")
    contract.accept_term("term-2", "bob-001")

    print("   Alice aceptó: term-1, term-2")
    print("   Bob aceptó: term-1, term-2")
    print()

    # 6. Activar contrato
    print("6. Activando contrato...")
    success = contract.activate()

    print(f"   Activación: {'EXITOSA' if success else 'FALLIDA'}")
    print(f"   Estado: {contract.state.value}")
    print()

    # 7. Verificar con oráculo sintético
    print("7. Validación por Oráculo Sintético...")
    oracle = SyntheticOracle(mode="simulation")
    response = oracle.validate_contract(contract.to_dict())

    print(f"   Aprobado: {response.approved}")
    print(f"   Confianza: {response.verdict.confidence}")
    print(f"   Razonamiento: {response.verdict.reasoning}")
    print()

    # 8. Mostrar resumen en lenguaje civil
    print("8. Resumen en Lenguaje Civil:")
    print("-" * 40)
    print(contract.to_civil_language())
    print("-" * 40)
    print()

    # 9. Simular γ bajo y retractación
    print("9. Simulando escenario de retractación...")

    # Bob tiene crisis - γ cae
    bob.update_wellness(Decimal("0.7"))
    print(f"   Bob γ actualizado: {bob.wellness_current.value} (crítico)")

    # Verificar con protector de bienestar
    protector = WellnessProtectorBlock()
    check = protector.check([alice, bob])

    if check.should_trigger_retraction:
        print("   ⚠️ Protector de Bienestar recomienda retractación")

        # Evaluar retractación con oráculo
        retraction_response = oracle.evaluate_retraction(
            contract_id=contract.contract_id,
            reason="gamma_below_threshold",
            evidence={"current_gamma": str(bob.wellness_current.value)},
        )

        print(f"   Oráculo: {retraction_response.reasoning}")

        if retraction_response.approved:
            contract.retract(
                reason="γ < 1 detectado - sufrimiento del participante Bob",
                actor_id="bob-001",
            )
            print(f"   ✓ Contrato retractado - Estado: {contract.state.value}")

    print()
    print("=" * 60)
    print("Ejemplo completado exitosamente")
    print("=" * 60)

    return contract


def main():
    """Punto de entrada del ejemplo."""
    contract = create_simple_loan()

    # Mostrar log de eventos
    print("\n📋 Log de Eventos:")
    for i, event in enumerate(contract.get_event_log(), 1):
        print(f"   {i}. [{event.event_type}] {event.timestamp.strftime('%H:%M:%S')}")


if __name__ == "__main__":
    main()
