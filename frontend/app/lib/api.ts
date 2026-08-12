export const API_URL = process.env.NEXT_PUBLIC_API_URL || (process.env.NODE_ENV === "development" ? "http://localhost:5001" : "");

// Wrapper simple sobre fetch que inyecta el token y maneja 401s básicos
export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem("mc_access_token") : null;
  
  const headers = new Headers(options.headers || {});
  headers.set("Content-Type", "application/json");
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Idealmente aquí interceptaríamos el 401 para intentar refresh token,
  // pero el backend usa HttpOnly cookies para mc_refresh, así que un 401
  // probablemente significa que la sesión caducó por completo.
  
  return response;
}

export interface VHVCalculateInput {
  name?: string;
  t_direct_hours?: number;
  t_inherited_hours?: number;
  t_future_hours?: number;
  v_organisms_affected?: number;
  v_consciousness_factor?: number;
  v_suffering_factor?: number;
  v_abundance_factor?: number;
  v_rarity_factor?: number;
  r_minerals_kg?: number;
  r_water_m3?: number;
  r_petroleum_l?: number;
  r_land_hectares?: number;
  r_frg_factor?: number;
  r_cs_factor?: number;
  save?: boolean;
}

export interface VHVParametersInput {
  alpha: number;
  beta: number;
  gamma: number;
  delta: number;
}

export const api = {
  calculateVHV: async (data: VHVCalculateInput) => {
    const res = await apiFetch("/vhv/calculate", {
      method: "POST",
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Error calculating VHV");
    return res.json();
  },

  getVHVParameters: async () => {
    const res = await apiFetch("/vhv/parameters");
    if (!res.ok) throw new Error("Error loading VHV parameters");
    return res.json();
  },

  updateVHVParameters: async (data: VHVParametersInput & { notes: string }) => {
    const res = await apiFetch("/vhv/parameters", {
      method: "PUT",
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Error updating VHV parameters");
    }
    return res.json();
  },

  getVHVCaseStudies: async () => {
    const res = await apiFetch("/vhv/case-studies");
    if (!res.ok) throw new Error("Error loading case studies");
    return res.json();
  },

  getVHVProducts: async () => {
    const res = await apiFetch("/vhv/products");
    if (!res.ok) throw new Error("Error loading products");
    return res.json();
  },

  getTVIStats: async () => {
    const res = await apiFetch("/tvi/stats");
    if (!res.ok) throw new Error("Error loading TVI stats");
    return res.json();
  },

  getTVICommunityStats: async () => {
    const res = await apiFetch("/tvi/community-stats");
    if (!res.ok) throw new Error("Error loading community stats");
    return res.json();
  },

  // MicroMaxocracia APIs
  getMicroMaxHousehold: async () => {
    const res = await apiFetch("/api/micromax/household");
    if (!res.ok) throw new Error("Error loading household");
    return res.json();
  },
  createMicroMaxHousehold: async (name: string) => {
    const res = await apiFetch("/api/micromax/household", {
      method: "POST",
      body: JSON.stringify({ name }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Error creating household");
    }
    return res.json();
  },
  joinMicroMaxHousehold: async (invite_code: string) => {
    const res = await apiFetch("/api/micromax/household/join", {
      method: "POST",
      body: JSON.stringify({ invite_code }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Error joining household");
    }
    return res.json();
  },
  updateMicroMaxConfig: async (config: { monthly_income: number; work_hours: number; travel_hours: number; sleep_hours: number }) => {
    const res = await apiFetch("/api/micromax/member/config", {
      method: "POST",
      body: JSON.stringify(config),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Error updating config");
    }
    return res.json();
  },
  logMicroMaxCDD: async (task: {
    task_name: string;
    duration_hours: number;
    effort_factor: number;
    mental_factor: number;
    scope_factor: number;
    attention_factor: number;
    fragmentation_factor: number;
    loneliness_factor: number;
    logged_date?: string;
  }) => {
    const res = await apiFetch("/api/micromax/cdd", {
      method: "POST",
      body: JSON.stringify(task),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Error logging task");
    }
    return res.json();
  },
  getMicroMaxCDDLogs: async () => {
    const res = await apiFetch("/api/micromax/cdd");
    if (!res.ok) throw new Error("Error loading CDD logs");
    return res.json();
  },
  saveMicroMaxSafetySurvey: async (answers: Record<string, boolean>) => {
    const res = await apiFetch("/api/micromax/safety-survey", {
      method: "POST",
      body: JSON.stringify({ answers }),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Error saving safety survey");
    }
    return res.json();
  },
  getMicroMaxSafetySurvey: async () => {
    const res = await apiFetch("/api/micromax/safety-survey");
    if (!res.ok) throw new Error("Error loading safety survey");
    return res.json();
  },
  logMicroMaxAudit: async (audit: {
    audit_date: string;
    conflicts_count: number;
    weapon_count: number;
    accusations_count: number;
    threats_count: number;
    s1_hours: number;
    s2_score: number;
    s3_score: number;
    s4_score: number;
    s5_score: number;
    duration_weeks: number;
  }) => {
    const res = await apiFetch("/api/micromax/audit", {
      method: "POST",
      body: JSON.stringify(audit),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error || "Error saving audit");
    }
    return res.json();
  },
  getMicroMaxAudits: async () => {
    const res = await apiFetch("/api/micromax/audits");
    if (!res.ok) throw new Error("Error loading audits");
    return res.json();
  },
  getMicroMaxDashboard: async (startDate?: string, endDate?: string) => {
    let url = "/api/micromax/dashboard";
    const params = [];
    if (startDate) params.push(`start_date=${startDate}`);
    if (endDate) params.push(`end_date=${endDate}`);
    if (params.length > 0) url += `?${params.join("&")}`;
    
    const res = await apiFetch(url);
    if (!res.ok) throw new Error("Error loading dashboard");
    return res.json();
  }
};
