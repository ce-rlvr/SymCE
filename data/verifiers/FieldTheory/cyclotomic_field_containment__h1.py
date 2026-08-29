import sympy

# Top-level setup
# No specific named bindings needed for this number theory/field theory problem;
# witnesses are expected to be tuples or dicts of integers.

def conditions(witness) -> list[bool]:
    try:
        # Parse witness: accept either a dict with 'm' and 'n' or a sequence (m, n, ...)
        if isinstance(witness, dict):
            m = witness.get('m')
            n = witness.get('n')
        else:
            m = witness[0]
            n = witness[1]
            
        if m is None or n is None:
            return [False, False, False]
            
        # Ensure m and n are integers
        if not (isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer))):
            return [False, False, False]
            
        m = int(m)
        n = int(n)
        
        # H_1: m divides n
        h1 = (m != 0) and (n % m == 0)
        
        # H_2: zeta_m and zeta_n are primitive m-th and n-th roots of unity in C
        # This implies m and n are valid indices for roots of unity (positive integers)
        h2 = (m >= 1) and (n >= 1)
        
        # Conclusion: The cyclotomic field Q(zeta_m) is a subfield of Q(zeta_n)
        # Mathematically, Q(zeta_m) is a subfield of Q(zeta_n) if and only if:
        # m divides n OR (m == 2 mod 4 and (m/2) divides n)
        q = (n % m == 0) or (m % 4 == 2 and n % (m // 2) == 0)
        
        # We need the negation of the conclusion (True if the conclusion FAILS)
        neg_q = not q
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: m divides n",
    "H_2: zeta_m and zeta_n are primitive m-th and n-th roots of unity in C",
    "¬Q: The cyclotomic field Q(zeta_m) is not a subfield of Q(zeta_n)"
]

N_HYP = 2
NEG_Q_INDEX = 2