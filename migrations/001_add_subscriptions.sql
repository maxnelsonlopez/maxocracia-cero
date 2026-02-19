-- Migración: Sistema de Suscripciones Premium
-- Fecha: Febrero 2026
-- Autor: Kimi (Moonshot AI)
-- Descripción: Agrega tablas para manejo de suscripciones "Contribuidor Consciente"

-- ============================================================================
-- TABLA: subscriptions
-- ============================================================================
-- Almacena las suscripciones activas e históricas de usuarios

CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    tier TEXT NOT NULL CHECK(tier IN ('free', 'contributor', 'enterprise')),
    status TEXT NOT NULL CHECK(status IN ('active', 'cancelled', 'expired')),
    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TEXT,
    payment_method TEXT,  -- 'stripe', 'manual', 'crypto', 'transfer'
    external_customer_id TEXT,  -- ID de Stripe/PayPal/etc
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, started_at)  -- Un usuario puede tener múltiples suscripciones históricas
);

-- Índices para búsquedas frecuentes
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_subscriptions_tier ON subscriptions(tier);
CREATE INDEX IF NOT EXISTS idx_subscriptions_expires ON subscriptions(expires_at);

-- ============================================================================
-- TABLA: premium_benefits_log
-- ============================================================================
-- Registra el uso de beneficios premium (para análisis y transparencia)

CREATE TABLE IF NOT EXISTS premium_benefits_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    benefit_type TEXT NOT NULL,  -- 'support_ticket', 'early_access', 'api_call', etc.
    metadata_json TEXT,  -- Datos adicionales en JSON
    claimed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_benefits_user ON premium_benefits_log(user_id);
CREATE INDEX IF NOT EXISTS idx_benefits_type ON premium_benefits_log(benefit_type);
CREATE INDEX IF NOT EXISTS idx_benefits_date ON premium_benefits_log(claimed_at);

-- ============================================================================
-- COMENTARIOS DOCUMENTACIÓN
-- ============================================================================

/*
Principios implementados:

1. TRANSPARENCIA RADICAL (T13)
   - Todos los datos de suscripción son auditables
   - Reportes públicos de ingresos y costos
   - Sin datos ocultos

2. IGUALDAD TEMPORAL (T2)
   - Precios ajustados por PPP (Paridad de Poder Adquisitivo)
   - El tiempo de cada persona vale igual
   - Sistema de honor para ajustes por ingreso

3. MINIMIZAR DAÑO (T7)
   - Sin dark patterns
   - Cancelación en cualquier momento
   - Sin venta de datos

4. RECIPROCIDAD JUSTA (T9)
   - Beneficios claros por cada nivel de contribución
   - Precio proporcional al valor recibido
*/
