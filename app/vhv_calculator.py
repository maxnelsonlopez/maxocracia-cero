"""
VHV Calculator Module

Implements the complete Vector de Huella Vital (VHV) calculation
based on the mathematical formalization in paper_formalizacion_matematica_maxo.txt

VHV = [T, V, R]
Precio_Maxos = α·T + β·V^γ + δ·R·(FRG × CS)

Where:
- T = Temporal component (Tiempo Vital Indexado)
- V = Vital component (Unidades de Vida Consumidas ponderadas)
- R = Resources component (Recursos Finitos)
- α, β, γ, δ = Governance parameters with axiomatic constraints
"""

from typing import Dict


class VHVCalculator:
    """Calculator for Vector de Huella Vital (VHV) and Maxo pricing."""

    def calculate_t_component(
        self, direct_hours: float, inherited_hours: float, future_hours: float
    ) -> float:
        """
        Calculate T component: Tiempo Total Vital Indexado (TTVI)

        TTVI = Σ(TVI_Directos) + Σ(TVI_Heredados) + Σ(TVI_Futuros)

        Args:
            direct_hours: Direct labor hours invested
            inherited_hours: Amortized time from tools/infrastructure
            future_hours: Projected maintenance and recycling time

        Returns:
            Total time in hours
        """
        return direct_hours + inherited_hours + future_hours

    def calculate_v_component(
        self,
        organisms_affected: float,
        f_consciousness: float,
        f_suffering: float,
        f_abundance: float,
        f_rarity: float,
    ) -> float:
        """
        Calculate V component: Unidades de Vida Consumidas (UVC) ponderadas

        V_total = Σ[UVC_base × F_consciencia × F_sufrimiento × F_abundancia × F_rareza_genética]

        Args:
            organisms_affected: Number of organisms (UVC_base)
            f_consciousness: Consciousness factor (0-1)
            f_suffering: Suffering factor (≥1, exponential penalty for excess)
            f_abundance: Abundance factor (population scarcity multiplier)
            f_rarity: Genetic rarity factor

        Returns:
            Weighted life units consumed
        """
        return (
            organisms_affected * f_consciousness * f_suffering * f_abundance * f_rarity
        )

    def calculate_r_component(
        self,
        minerals_kg: float,
        water_m3: float,
        petroleum_l: float,
        land_hectares: float,
        frg_factor: float,
        cs_factor: float,
    ) -> float:
        """
        Calculate R component: Recursos Finitos consumidos

        R = Σ(recursos) × (FRG × CS)

        Args:
            minerals_kg: Minerals consumed in kg
            water_m3: Fresh water in cubic meters
            petroleum_l: Petroleum in liters
            land_hectares: Land use in hectares
            frg_factor: Factor de Rareza Geológica (geological scarcity)
            cs_factor: Criticidad Sistémica (systemic criticality)

        Returns:
            Weighted resource consumption
        """
        # Aggregate resources with basic weights
        # These weights could be refined based on actual resource criticality
        total_resources = (
            minerals_kg * 1.0
            + water_m3 * 0.1
            + petroleum_l * 2.0
            + land_hectares * 100.0
        )

        return total_resources * frg_factor * cs_factor

    def calculate_maxo_price(
        self,
        t_component: float,
        v_component: float,
        r_component: float,
        alpha: float,
        beta: float,
        gamma: float,
        delta: float,
    ) -> float:
        """
        Calculate final price in Maxos using the valuation function.

        Precio_Maxos = α·T + β·V^γ + δ·R·(FRG × CS)

        Note: R component already includes FRG × CS from calculate_r_component

        Args:
            t_component: Time component (hours)
            v_component: Weighted life component
            r_component: Weighted resources component
            alpha: Weight of time (must be > 0)
            beta: Weight of life (must be > 0)
            gamma: Suffering aversion exponent (must be ≥ 1)
            delta: Weight of resources (must be ≥ 0)

        Returns:
            Price in Maxos

        Raises:
            ValueError: If axiomatic constraints are violated
        """
        # Validate axiomatic constraints
        if alpha <= 0:
            raise ValueError("Axiom violation: α must be > 0 (cannot ignore time)")
        if beta <= 0:
            raise ValueError("Axiom violation: β must be > 0 (cannot ignore life)")
        if gamma < 1:
            raise ValueError("Axiom violation: γ must be ≥ 1 (cannot reward suffering)")
        if delta < 0:
            raise ValueError(
                "Axiom violation: δ must be ≥ 0 (cannot ignore finite resources)"
            )

        # Calculate price components
        time_price = alpha * t_component
        life_price = beta * (v_component**gamma)
        resource_price = delta * r_component

        total_price = time_price + life_price + resource_price

        return float(round(total_price, 2))

    def calculate_vhv(
        self,
        # T component
        t_direct_hours: float,
        t_inherited_hours: float,
        t_future_hours: float,
        # V component
        v_organisms_affected: float,
        v_consciousness_factor: float,
        v_suffering_factor: float,
        v_abundance_factor: float,
        v_rarity_factor: float,
        # R component
        r_minerals_kg: float,
        r_water_m3: float,
        r_petroleum_l: float,
        r_land_hectares: float,
        r_frg_factor: float,
        r_cs_factor: float,
        # Parameters
        alpha: float,
        beta: float,
        gamma: float,
        delta: float,
    ) -> Dict:
        """
        Calculate complete VHV and Maxo price.

        Returns:
            Dictionary with:
                - vhv: {"T": float, "V": float, "R": float}
                - maxo_price: float
                - breakdown: detailed calculation breakdown
        """
        # Calculate components
        t = self.calculate_t_component(
            t_direct_hours, t_inherited_hours, t_future_hours
        )
        v = self.calculate_v_component(
            v_organisms_affected,
            v_consciousness_factor,
            v_suffering_factor,
            v_abundance_factor,
            v_rarity_factor,
        )
        r = self.calculate_r_component(
            r_minerals_kg,
            r_water_m3,
            r_petroleum_l,
            r_land_hectares,
            r_frg_factor,
            r_cs_factor,
        )

        # Calculate price
        maxo_price = self.calculate_maxo_price(t, v, r, alpha, beta, gamma, delta)

        # Calculate breakdown
        time_contribution = alpha * t
        life_contribution = beta * (v**gamma) if v > 0 else 0
        resource_contribution = delta * r

        return {
            "vhv": {"T": round(t, 4), "V": round(v, 6), "R": round(r, 4)},
            "maxo_price": maxo_price,
            "breakdown": {
                "time_contribution": round(time_contribution, 2),
                "life_contribution": round(life_contribution, 2),
                "resource_contribution": round(resource_contribution, 2),
            },
            "parameters_used": {
                "alpha": alpha,
                "beta": beta,
                "gamma": gamma,
                "delta": delta,
            },
        }


# Case studies from paper_formalizacion_matematica_maxo.txt

# Example 1: Huevo de granja ética (líneas 318-329)
CASE_STUDY_HUEVO_ETICO = {
    "name": "Huevo de Granja Ética",
    "category": "food",
    "description": "Huevo de gallina con 10m² espacio, alimentación óptima, sacrificio humanitario",
    "t_direct_hours": 0.15,
    "t_inherited_hours": 0.0,
    "t_future_hours": 0.0,
    "v_organisms_affected": 0.001,  # Fractional chicken
    "v_consciousness_factor": 0.9,  # Bird consciousness
    "v_suffering_factor": 1.1,  # Minimal suffering
    "v_abundance_factor": 0.0006,  # 25 billion chickens globally
    "v_rarity_factor": 1.0,  # Common genetics
    "r_minerals_kg": 0.08,  # Organic feed
    "r_water_m3": 0.0,
    "r_petroleum_l": 0.0,
    "r_land_hectares": 0.0,
    "r_frg_factor": 1.0,
    "r_cs_factor": 1.0,
}

# Example 2: Huevo de granja industrial (líneas 306-317)
CASE_STUDY_HUEVO_INDUSTRIAL = {
    "name": "Huevo de Granja Industrial",
    "category": "food",
    "description": "Huevo de gallina en jaula 0.05m², hacinamiento extremo, antibióticos masivos",
    "t_direct_hours": 0.1,
    "t_inherited_hours": 0.0,
    "t_future_hours": 0.0,
    "v_organisms_affected": 0.001,  # Fractional chicken
    "v_consciousness_factor": 0.9,  # Bird consciousness
    "v_suffering_factor": 25.0,  # Massive suffering penalty
    "v_abundance_factor": 0.0006,  # 25 billion chickens globally
    "v_rarity_factor": 1.0,  # Common genetics
    "r_minerals_kg": 0.05,  # Minimal survival feed
    "r_water_m3": 0.0,
    "r_petroleum_l": 0.0,
    "r_land_hectares": 0.0,
    "r_frg_factor": 1.0,
    "r_cs_factor": 1.0,
}
