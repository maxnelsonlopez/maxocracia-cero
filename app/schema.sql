PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  alias TEXT,
  password_hash TEXT,
  phone TEXT,
  city TEXT,
  neighborhood TEXT,
  values_json TEXT,
  is_admin INTEGER DEFAULT 0,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS profiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL UNIQUE,
  bio TEXT,
  skills TEXT,
  availability TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS interchange (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  interchange_id TEXT UNIQUE,
  date TEXT,
  giver_id INTEGER,
  receiver_id INTEGER,
  type TEXT,
  description TEXT,
  urgency TEXT,
  uth_hours REAL,
  uvc_score REAL,
  urf_units REAL,
  urf_description TEXT,
  economic_value_approx TEXT,
  vhv_time_seconds REAL,
  vhv_lives REAL,
  vhv_resources_json TEXT,
  impact_resolution_score INTEGER,
  reciprocity_status TEXT,
  human_dimension_attended TEXT,
  coordination_method TEXT CHECK(coordination_method IN ('max_direct', 'participants_alone', 'intermediary', 'other') OR coordination_method IS NULL),
  requires_followup INTEGER DEFAULT 0,
  followup_scheduled_date TEXT,
  facilitator_notes TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (giver_id) REFERENCES users(id),
  FOREIGN KEY (receiver_id) REFERENCES users(id)
);

-- Refresh tokens table for rotating refresh token support
CREATE TABLE IF NOT EXISTS refresh_tokens (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  jti TEXT NOT NULL UNIQUE,
  token_hash TEXT NOT NULL,
  issued_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires_at TEXT,
  revoked INTEGER DEFAULT 0,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE(token_hash)
);

CREATE TABLE IF NOT EXISTS resources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  title TEXT,
  description TEXT,
  category TEXT,
  available BOOLEAN DEFAULT 1,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS reputation (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  score REAL DEFAULT 0,
  reviews_count INTEGER DEFAULT 0,
  updated_at TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS maxo_ledger (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  change_amount REAL,
  reason TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- VHV Calculator Tables

-- Stores the global parameters for VHV valuation function
-- Precio_Maxos = α·T + β·V^γ + δ·R·(FRG × CS)
CREATE TABLE IF NOT EXISTS vhv_parameters (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  alpha REAL NOT NULL DEFAULT 100.0,  -- Weight of time component
  beta REAL NOT NULL DEFAULT 2000.0,  -- Weight of life component
  gamma REAL NOT NULL DEFAULT 1.0,    -- Suffering aversion exponent (axiom: γ ≥ 1)
  delta REAL NOT NULL DEFAULT 100.0,  -- Weight of resources component
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_by INTEGER,  -- user_id who updated
  notes TEXT,  -- Documentation of why parameters were changed
  FOREIGN KEY (updated_by) REFERENCES users(id),
  CHECK (alpha > 0),   -- Axiom: cannot ignore time
  CHECK (beta > 0),    -- Axiom: cannot ignore life
  CHECK (gamma >= 1),  -- Axiom: cannot reward suffering
  CHECK (delta >= 0)   -- Axiom: cannot ignore finite resources
);

-- Catalog of products with their VHV breakdown
CREATE TABLE IF NOT EXISTS vhv_products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  category TEXT,  -- e.g., 'food', 'electronics', 'housing', 'transport'
  description TEXT,
  
  -- Componente T (Tiempo Vital Indexado)
  t_direct_hours REAL DEFAULT 0,    -- Direct labor hours
  t_inherited_hours REAL DEFAULT 0, -- Amortized tool/infrastructure time
  t_future_hours REAL DEFAULT 0,    -- Projected maintenance/recycling time
  
  -- Componente V (Unidades de Vida Consumidas)
  v_organisms_affected REAL DEFAULT 0,  -- Number of organisms (UVC_base)
  v_consciousness_factor REAL DEFAULT 0,  -- F_consciencia (0-1)
  v_suffering_factor REAL DEFAULT 1,     -- F_sufrimiento (≥1)
  v_abundance_factor REAL DEFAULT 1,     -- F_abundancia
  v_rarity_factor REAL DEFAULT 1,        -- F_rareza_genética
  
  -- Componente R (Recursos Finitos)
  r_minerals_kg REAL DEFAULT 0,
  r_water_m3 REAL DEFAULT 0,
  r_petroleum_l REAL DEFAULT 0,
  r_land_hectares REAL DEFAULT 0,
  r_frg_factor REAL DEFAULT 1,  -- Factor de Rareza Geológica
  r_cs_factor REAL DEFAULT 1,   -- Criticidad Sistémica
  
  -- Calculated results
  vhv_json TEXT,  -- Complete VHV vector as JSON: {"T": x, "V": y, "R": z}
  maxo_price REAL,  -- Final price in Maxos
  
  -- Metadata
  created_by INTEGER,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Audit trail of all VHV calculations
CREATE TABLE IF NOT EXISTS vhv_calculations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER,
  user_id INTEGER,
  
  -- Snapshot of parameters used for this calculation
  parameters_snapshot TEXT,  -- JSON: {"alpha": x, "beta": y, "gamma": z, "delta": w}
  
  -- Snapshot of VHV at time of calculation
  vhv_snapshot TEXT,  -- JSON: complete VHV breakdown
  
  -- Result
  maxo_price REAL,
  
  calculation_date TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES vhv_products(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- TVI (Tiempo Vital Indexado) Tables

-- Stores unique time blocks for users
CREATE TABLE IF NOT EXISTS tvi_entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  start_time TEXT NOT NULL, -- ISO8601
  end_time TEXT NOT NULL,   -- ISO8601
  duration_seconds INTEGER NOT NULL,
  category TEXT NOT NULL CHECK(category IN ('MAINTENANCE', 'INVESTMENT', 'WASTE', 'WORK', 'LEISURE')),
  description TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  CHECK (end_time > start_time)
);

-- Index to enforce uniqueness and optimize overlap checks
-- Note: SQLite doesn't support partial indexes or complex constraints easily for overlaps in CREATE TABLE,
-- so application logic must enforce no-overlap. However, a unique index on start_time per user helps.
CREATE UNIQUE INDEX IF NOT EXISTS idx_tvi_user_start ON tvi_entries(user_id, start_time);

-- Additional indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_tvi_user_category ON tvi_entries(user_id, category);
CREATE INDEX IF NOT EXISTS idx_tvi_user_date_range ON tvi_entries(user_id, start_time, end_time);
CREATE INDEX IF NOT EXISTS idx_vhv_products_category ON vhv_products(category);
CREATE INDEX IF NOT EXISTS idx_vhv_products_created_by ON vhv_products(created_by);
CREATE INDEX IF NOT EXISTS idx_vhv_parameters_updated_at ON vhv_parameters(updated_at DESC);


-- Forms System Tables

-- Participants table (Formulario CERO - Inscripción)
CREATE TABLE IF NOT EXISTS participants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  
  -- Personal Information
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  referred_by TEXT,
  phone_call TEXT,
  phone_whatsapp TEXT,
  telegram_handle TEXT,
  city TEXT NOT NULL,
  neighborhood TEXT NOT NULL,
  personal_values TEXT,  -- Long text field
  
  -- Offers (What they can provide)
  offer_categories TEXT,  -- JSON array of selected categories
  offer_description TEXT NOT NULL,
  offer_human_dimensions TEXT,  -- JSON array of dimensions their offer addresses
  
  -- Needs (What they require)
  need_categories TEXT,  -- JSON array of selected categories
  need_description TEXT NOT NULL,
  need_urgency TEXT CHECK(need_urgency IN ('Alta', 'Media', 'Baja')),
  need_human_dimensions TEXT,  -- JSON array of dimensions their need addresses
  
  -- Consent and metadata
  consent_given INTEGER DEFAULT 1,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  status TEXT DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'paused'))
);

-- Tabla para ofertas adicionales de los participantes
CREATE TABLE IF NOT EXISTS participant_offers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  participant_id INTEGER NOT NULL,
  description TEXT NOT NULL,
  categories TEXT NOT NULL,          -- Array JSON de categorías (ej: ["habilidad", "tiempo"])
  human_dimensions TEXT,            -- Array JSON de dimensiones humanas del SDV
  status TEXT DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'paused')),
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
);

-- Tabla para necesidades adicionales de los participantes
CREATE TABLE IF NOT EXISTS participant_needs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  participant_id INTEGER NOT NULL,
  description TEXT NOT NULL,
  categories TEXT NOT NULL,          -- Array JSON de categorías
  urgency TEXT CHECK(urgency IN ('Alta', 'Media', 'Baja')),
  human_dimensions TEXT,            -- Array JSON de dimensiones humanas
  status TEXT DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'paused')),
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE
);

-- Índices de rendimiento
CREATE INDEX IF NOT EXISTS idx_participant_offers_pid ON participant_offers(participant_id);
CREATE INDEX IF NOT EXISTS idx_participant_needs_pid ON participant_needs(participant_id);

-- Follow-ups table (Formulario B - Reporte de Seguimiento)
CREATE TABLE IF NOT EXISTS follow_ups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  
  -- Identification
  follow_up_date TEXT NOT NULL,
  participant_id INTEGER NOT NULL,
  related_interchange_id INTEGER,  -- Optional reference to interchange
  
  -- Type of follow-up
  follow_up_type TEXT NOT NULL CHECK(follow_up_type IN (
    'verification_completed',
    'update_in_progress', 
    'situation_evolution',
    'new_urgent_need',
    'need_resolved',
    'spontaneous_feedback',
    'routine_check'
  )),
  
  -- Current Status
  current_situation TEXT NOT NULL,  -- Long text description
  need_level INTEGER CHECK(need_level BETWEEN 1 AND 5),  -- 1=resolved, 5=critical
  situation_change TEXT CHECK(situation_change IN (
    'improved_significantly',
    'improved_slightly',
    'same',
    'worsened_slightly',
    'worsened_significantly',
    'first_evaluation'
  )),
  
  -- Active Interchanges
  active_interchanges_status TEXT CHECK(active_interchanges_status IN (
    'receiving_help',
    'giving_help',
    'both',
    'none',
    'paused'
  )),
  interchanges_working_well TEXT CHECK(interchanges_working_well IN (
    'very_well',
    'minor_difficulties',
    'significant_problems',
    'needs_adjustment',
    NULL
  )),
  
  -- New Opportunities
  new_needs_detected TEXT,  -- JSON array of categories
  new_offers_detected TEXT,  -- JSON array of categories
  
  -- Emotional Health
  emotional_state TEXT CHECK(emotional_state IN (
    'very_good',
    'good',
    'neutral',
    'worried',
    'bad',
    'alert_signs',
    'could_not_evaluate',
    NULL
  )),
  community_connection INTEGER CHECK(community_connection BETWEEN 1 AND 5 OR community_connection IS NULL),
  
  -- Required Actions
  actions_required TEXT,  -- JSON array of actions
  follow_up_priority TEXT NOT NULL CHECK(follow_up_priority IN (
    'high',      -- 🔴 24-48 hours
    'medium',    -- 🟡 next week
    'low',       -- 🟢 monthly
    'closed'     -- ✅ no more follow-up needed
  )),
  next_follow_up_date TEXT,
  
  -- Facilitator Notes
  facilitator_notes TEXT,
  learnings TEXT,
  
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE,
  FOREIGN KEY (related_interchange_id) REFERENCES interchange(id) ON DELETE SET NULL
);

-- Extend interchange table with additional fields for Formulario A
-- Note: We cannot use ALTER TABLE to add CHECK constraints in SQLite easily,
-- so we document the expected values here for application-level validation

-- Expected new columns to be added via migration:
-- coordination_method TEXT CHECK(coordination_method IN ('max_direct', 'participants_alone', 'intermediary', 'other'))
-- requires_followup INTEGER DEFAULT 0
-- followup_scheduled_date TEXT

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_participants_email ON participants(email);
CREATE INDEX IF NOT EXISTS idx_participants_city ON participants(city);
CREATE INDEX IF NOT EXISTS idx_participants_status ON participants(status);
CREATE INDEX IF NOT EXISTS idx_follow_ups_participant ON follow_ups(participant_id);
CREATE INDEX IF NOT EXISTS idx_follow_ups_priority ON follow_ups(follow_up_priority);
CREATE INDEX IF NOT EXISTS idx_follow_ups_date ON follow_ups(follow_up_date);

-- MaxoContracts Tables (Capa 4 - Legal)

CREATE TABLE IF NOT EXISTS maxo_contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id TEXT UNIQUE NOT NULL,
    civil_description TEXT,
    state TEXT NOT NULL CHECK(state IN ('draft', 'pending', 'active', 'executed', 'retracted', 'expired')),
    total_vhv_t REAL DEFAULT 0,
    total_vhv_v REAL DEFAULT 0,
    total_vhv_h REAL DEFAULT 0,
    parent_contract_id TEXT, -- Contratos interescala anidados (ROADMAP Bloque B, Fase 5)
    creator_user_id INTEGER, -- Inmutabilidad (Ola 3A.2): quién creó el contrato
    signature_deadline TEXT, -- Ventana de firma (Ola 3A.7)
    min_reflection_hours REAL DEFAULT 0, -- Enfriamiento server-side (Ola 3A.7)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Registro de Partes de cualquier escala (ROADMAP Bloque B, Fase 1):
-- persona (user-), micro-sociedad (society-), cooperativa (coop-),
-- institución (org-), sintética (synthetic-) y ecosistema del Reino Natural (eco-).
CREATE TABLE IF NOT EXISTS maxo_parties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    party_id TEXT UNIQUE NOT NULL,
    party_type TEXT NOT NULL CHECK(party_type IN ('human','society','cooperative','institution','synthetic','ecosystem')),
    display_name TEXT NOT NULL,
    parent_party_id TEXT, -- anidación: una cooperativa contiene personas
    members_json TEXT DEFAULT '{}', -- resolución de miembros/consentimiento (quórum)
    wellness_value REAL DEFAULT 1.0,
    owner_user_id INTEGER, -- Autoridad (Ola 3A.3): quién gobierna la parte
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Votos de cambio de gobernanza (Ola 3A.3): los delegados aprueban por
-- quórum una propuesta de cambio de membresía cuando el owner no actúa.
CREATE TABLE IF NOT EXISTS maxo_party_governance_votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    party_id TEXT NOT NULL,
    proposal_hash TEXT NOT NULL,
    delegate_id TEXT NOT NULL,
    approved INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(party_id, proposal_hash, delegate_id)
);

-- Firmas delegadas de partes colectivas (ROADMAP Bloque B, Fase 2):
-- cada delegado firma un término; el quórum decide el consentimiento agregado.
CREATE TABLE IF NOT EXISTS maxo_contract_delegate_approvals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id TEXT NOT NULL,
    term_id TEXT NOT NULL,
    party_id TEXT NOT NULL,   -- parte colectiva (ej. 'coop-7')
    delegate_id TEXT NOT NULL, -- delegado humano (ej. 'user-2')
    paraphrase TEXT, -- Derecho a la comprensión (Ola 3B): palabras del delegado
    approved_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE,
    UNIQUE(contract_id, term_id, party_id, delegate_id)
);

-- Perfil de protección de usuarios (Ola 3B, escalera de equidad):
-- standard | assisted | shielded con acompañante humano opcional.
CREATE TABLE IF NOT EXISTS maxo_user_protection (
    user_id INTEGER PRIMARY KEY,
    level TEXT NOT NULL DEFAULT 'standard' CHECK(level IN ('standard','assisted','shielded')),
    companion_user_id INTEGER,
    declared_age INTEGER,
    declared_education TEXT,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS maxo_contract_terms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id TEXT NOT NULL,
    term_id TEXT NOT NULL,
    civil_text TEXT,
    vhv_t REAL DEFAULT 0,
    vhv_v REAL DEFAULT 0,
    vhv_h REAL DEFAULT 0,
    assigned_participant TEXT, -- Parte obligada del término (user-N o synthetic-X)
    penalty_gamma REAL DEFAULT 0, -- Penalización γ por incumplimiento (Ola 3C)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE,
    UNIQUE(contract_id, term_id)
);

CREATE TABLE IF NOT EXISTS maxo_contract_participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id TEXT NOT NULL,
    participant_id TEXT NOT NULL, -- Format: user-ID
    wellness_value REAL DEFAULT 1.0,
    sdv_status TEXT DEFAULT 'ok',
    reported_by TEXT, -- Actor que reportó el γ (Ola 3A.5, T13)
    reported_at TEXT, -- Timestamp del reporte (Ola 3A.5)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE,
    UNIQUE(contract_id, participant_id)
);

CREATE TABLE IF NOT EXISTS maxo_contract_term_approvals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id TEXT NOT NULL,
    term_id TEXT NOT NULL,
    participant_id TEXT NOT NULL,
    paraphrase TEXT, -- Derecho a la comprensión (Ola 3B): palabras propias del firmante
    approved_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE,
    UNIQUE(contract_id, term_id, participant_id)
);

-- Bitácora de cumplimiento (Ola 3C, dientes): cada término reportado
-- como cumplido/parcial/violado con evidencia, actor y penalización γ.
CREATE TABLE IF NOT EXISTS maxo_contract_term_fulfillments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id TEXT NOT NULL,
    term_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('fulfilled','partial','violated','appealed')),
    evidence TEXT,
    reported_by TEXT NOT NULL,
    wellness_delta REAL DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS maxo_contract_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    description TEXT,
    metadata_json TEXT, -- JSON snapshot of the event data
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE
);

-- Check-ins de bienestar real (Ola 4, Puente A: γ que escucha la vida).
-- Serie temporal de γ reportada por las partes: el contrato escucha, no crea.
CREATE TABLE IF NOT EXISTS maxo_contract_checkins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id TEXT NOT NULL,
    participant_id TEXT NOT NULL,
    wellness REAL NOT NULL,
    source TEXT NOT NULL DEFAULT 'checkin',
    reported_by TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE
);

-- Métricas de MaxoContracts (dashboard de Cohorte Cero: γ, SDV, NPS)
CREATE TABLE IF NOT EXISTS maxo_contract_nps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id TEXT NOT NULL,
    participant_id TEXT NOT NULL, -- user-ID o synthetic-*
    score INTEGER NOT NULL CHECK(score >= 0 AND score <= 10),
    comment TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE,
    UNIQUE(contract_id, participant_id)
);

CREATE TABLE IF NOT EXISTS maxo_contract_meta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id TEXT NOT NULL,
    meta_key TEXT NOT NULL, -- ej: 'category' (aseo | prestamo | comida | otros)
    meta_value TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE,
    UNIQUE(contract_id, meta_key)
);

CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    api_key TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_used_at TEXT,
    revoked INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS maxo_webhooks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    events TEXT NOT NULL,
    secret TEXT NOT NULL,
    party_filter TEXT, -- JSON list de party_id (null = todos). Webhooks por parte (Ext. 4)
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert default VHV parameters (only if table is empty)
INSERT OR IGNORE INTO vhv_parameters (id, alpha, beta, gamma, delta, notes)
VALUES (1, 100.0, 2000.0, 1.0, 100.0, 'Initial parameters based on paper_formalizacion_matematica_maxo.txt');

-- MicroMaxocracia Tables (Capa 3 - Equidad Doméstica y Salud Relacional)

CREATE TABLE IF NOT EXISTS micromax_households (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    invite_code TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS micromax_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL,
    user_id INTEGER UNIQUE,
    name TEXT NOT NULL,
    monthly_income REAL DEFAULT 0,
    work_hours REAL DEFAULT 0,
    travel_hours REAL DEFAULT 0,
    sleep_hours REAL DEFAULT 56,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (household_id) REFERENCES micromax_households(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS micromax_cdd_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    task_name TEXT NOT NULL,
    duration_hours REAL NOT NULL,
    effort_factor REAL NOT NULL,
    mental_factor REAL NOT NULL,
    scope_factor REAL NOT NULL,
    attention_factor REAL DEFAULT 1.0,
    fragmentation_factor REAL DEFAULT 1.0,
    loneliness_factor REAL DEFAULT 1.0,
    calculated_vhv REAL NOT NULL,
    logged_date TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES micromax_members(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS micromax_safety_surveys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL UNIQUE,
    score INTEGER NOT NULL,
    answers_json TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES micromax_members(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS micromax_audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    household_id INTEGER NOT NULL,
    audit_date TEXT NOT NULL,
    conflicts_count INTEGER NOT NULL,
    weapon_count INTEGER NOT NULL,
    accusations_count INTEGER NOT NULL,
    threats_count INTEGER NOT NULL,
    s1_hours REAL DEFAULT 0,
    s2_score REAL DEFAULT 0,
    s3_score REAL DEFAULT 0,
    s4_score REAL DEFAULT 0,
    s5_score REAL DEFAULT 0,
    duration_weeks INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (household_id) REFERENCES micromax_households(id) ON DELETE CASCADE
);

-- Indices for MicroMaxocracia tables
CREATE INDEX IF NOT EXISTS idx_micromax_members_household ON micromax_members(household_id);
CREATE INDEX IF NOT EXISTS idx_micromax_cdd_member ON micromax_cdd_logs(member_id);
CREATE INDEX IF NOT EXISTS idx_micromax_cdd_date ON micromax_cdd_logs(logged_date);
CREATE INDEX IF NOT EXISTS idx_micromax_audits_household ON micromax_audits(household_id);


-- ============================================================================
-- Votación Comunitaria (Gobernanza Operativa - Cap 14 Consenso Diverso)
-- ============================================================================
CREATE TABLE IF NOT EXISTS maxo_community_proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'operational',
    options_json TEXT NOT NULL,
    quorum_ratio REAL NOT NULL DEFAULT 0.5,
    majority_ratio REAL NOT NULL DEFAULT 0.5,
    status TEXT NOT NULL DEFAULT 'open',
    result TEXT,
    result_detail TEXT,
    created_by INTEGER NOT NULL,
    reason TEXT DEFAULT '',
    deadline TEXT,
    closed_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS maxo_community_votes (
    proposal_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    option TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (proposal_id, user_id)
);
CREATE INDEX IF NOT EXISTS idx_community_votes_proposal ON maxo_community_votes(proposal_id);
CREATE TABLE IF NOT EXISTS maxo_community_analysis (
    proposal_id INTEGER PRIMARY KEY,
    analysis_json TEXT NOT NULL,
    model TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
