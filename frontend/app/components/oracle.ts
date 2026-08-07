// Helpers compartidos del Oráculo Sintético en Vivo (ROADMAP Bloque A)
// Usados por OracleNegotiationPanel y la página /contracts/negotiate.

export interface DraftTerm {
  term_id: string;
  civil_text: string;
  vhv: { t: number; v: number; h: number };
  assigned_participant?: string;
}

export interface DraftResult {
  session_id: string;
  version: number;
  instruction: string;
  draft_terms: DraftTerm[];
  proposed_parties: string[];
  axiom_check: {
    valid: boolean;
    violations: { axiom: string; message: string }[];
    warnings: { axiom: string; message: string }[];
    reciprocity_balance: Record<string, number>;
  };
  reasoning: string;
  suggested_contract_id: string;
  oracle_id: string;
}

export interface CritiqueResult {
  contract_id: string;
  valid: boolean;
  issues: { axiom: string; severity: string; message: string }[];
  recommendations: string[];
  reasoning: string;
  oracle_id: string;
}

// Mapea un pid (user-1 | synthetic-qwen-1 | coop-7 | eco-1) al formato que acepta POST /contracts/
export const mapParty = (pid: string) => {
  if (pid.startsWith('synthetic-')) {
    return { participant_id: pid.slice('synthetic-'.length), synthetic: {} };
  }
  if (pid.startsWith('user-')) {
    const id = parseInt(pid.slice(5), 10);
    return Number.isFinite(id) ? { user_id: id } : { participant_id: pid, synthetic: {} };
  }
  // Escalas colectivas (ROADMAP Bloque B): society- | coop- | org- | eco-
  return { party_id: pid };
};

// Instrucciones sugeridas para empezar la conversación
export const SUGGESTED_INSTRUCTIONS = [
  'Max ofrece 10 horas de trabajo y quiere que Ana dé a cambio un objeto, un servicio o sus propias horas',
  'Luis presta 20 Maxos a Caro y quiere saber cómo devolvérselos sin explotación',
  'Una micro-sociedad de 3 personas quiere un acuerdo de cuidado compartido',
];

export const materializeContract = (
  draft: DraftResult,
  contractName: string,
  instruction: string,
) => ({
  contract_id: contractName,
  civil_description: instruction || draft.instruction,
  participants: draft.proposed_parties.map(mapParty),
  terms: draft.draft_terms.map((t) => ({
    term_id: t.term_id,
    civil_text: t.civil_text,
    vhv: t.vhv,
    assigned_participant_id: t.assigned_participant,
  })),
});
