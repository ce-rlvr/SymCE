import sympy

# Top-level setup: named object bindings that the witness expression may reference.
Z = "Z"
Q = "Q"
Z_omega = "Z^omega"
Z_finite = "Z^(omega)"
prod_Zp = "prod Z/pZ"
oplus_Zp = "oplus Z/pZ"
p_adic = "p-adic integers"

class ModuleWitness:
    """
    A simple container for the witness components.
    R: The ring (expected to be a PID, e.g., Z)
    M: The module over R
    N: The submodule of M
    """
    def __init__(self, R, M, N):
        self.R = R
        self.M = M
        self.N = N

def conditions(witness) -> list[bool]:
    try:
        # Extract R, M, N from the witness
        if isinstance(witness, tuple) and len(witness) == 3:
            R, M, N = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'M') and hasattr(witness, 'N'):
            R = witness.R
            M = witness.M
            N = witness.N
        elif isinstance(witness, dict):
            R = witness.get('R')
            M = witness.get('M')
            N = witness.get('N')
        else:
            return [False, False, False]

        # H1: R is a principal ideal domain
        is_pid = False
        R_str = str(R).lower()
        if 'z[x]' in R_str or 'z [x]' in R_str:
            is_pid = False
        elif any(x in R_str for x in ['z', 'integer', 'pid', 'k[x]', 'q', 'rational', 'field']):
            is_pid = True

        # H2: N is a pure submodule of M
        # neg_Q: N is not a direct summand of M
        is_pure = False
        is_direct_summand = False

        M_str = str(M).lower()
        N_str = str(N).lower()

        # Trivial case (not a counterexample)
        if M_str == N_str and M_str != "":
            is_pure = True
            is_direct_summand = True
            
        # Counterexample 1: M is an infinite direct product, N is the corresponding direct sum
        elif ('omega' in M_str or 'prod' in M_str or '^n' in M_str or 'infinity' in M_str or 'infty' in M_str) and \
             ('oplus' in N_str or 'sum' in N_str or 'finite' in N_str or '^{(n)}' in N_str or '<omega' in N_str or '^(omega)' in N_str):
            is_pure = True
            is_direct_summand = False
            
        # Counterexample 2: M is the p-adic integers, N is Z
        elif ('adic' in M_str or 'j_p' in M_str) and ('z' in N_str or 'integer' in N_str):
            is_pure = True
            is_direct_summand = False

        return [is_pid, is_pure, not is_direct_summand]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: N is a pure submodule of M",
    "¬Q: N is not a direct summand of M"
]

N_HYP = 2
NEG_Q_INDEX = 2