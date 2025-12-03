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


-- Insert default VHV parameters (only if table is empty)
INSERT OR IGNORE INTO vhv_parameters (id, alpha, beta, gamma, delta, notes)
VALUES (1, 100.0, 2000.0, 1.0, 100.0, 'Initial parameters based on paper_formalizacion_matematica_maxo.txt');
