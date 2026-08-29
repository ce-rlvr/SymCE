import sympy

# Top-level setup
# No named bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            m = witness.get('m')
            n = witness.get('n')
            k = witness.get('k', witness.get('K'))
        else:
            try:
                m, n, k = witness
            except (TypeError, ValueError):
                return [False, False, False]
            
        h1 = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and m > 0 and n > 0
        h2 = isinstance(k, (int, sympy.Integer))
        
        if not (h1 and h2):
            return [bool(h1), bool(h2), False]
            
        neg_q = sympy.lcm(m, k) != sympy.lcm(m, n)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "H_2: K is a subgroup of Z (represented by integer k)",
    "¬Q: H \\cap K is not the subgroup lcm(m, n)Z"
]

N_HYP = 2
NEG_Q_INDEX = 2