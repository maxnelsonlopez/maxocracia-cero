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
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
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
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE,
    UNIQUE(contract_id, participant_id)
);

CREATE TABLE IF NOT EXISTS maxo_contract_term_approvals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_id TEXT NOT NULL,
    term_id TEXT NOT NULL,
    participant_id TEXT NOT NULL,
    approved_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES maxo_contracts(contract_id) ON DELETE CASCADE,
    UNIQUE(contract_id, term_id, participant_id)
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

-- Insert default VHV parameters (only if table is empty)
INSERT OR IGNORE INTO vhv_parameters (id, alpha, beta, gamma, delta, notes)
VALUES (1, 100.0, 2000.0, 1.0, 100.0, 'Initial parameters based on paper_formalizacion_matematica_maxo.txt');
