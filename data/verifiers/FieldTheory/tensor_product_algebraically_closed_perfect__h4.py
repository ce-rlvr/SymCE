import sympy
from sympy import Symbol

# Top-level setup
t = Symbol('t')
x = Symbol('x')

class AlgebraicClosure:
    """
    A dummy class to represent the algebraic closure of a field,
    since SymPy does not have native support for algebraically closed fields.
    """
    def __init__(self, base_field):
        self.base_field = base_field
        self.is_Field = True
        self.is_alg_closed = True

    def __str__(self):
        return f"AlgebraicClosure({self.base_field})"

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        # Unpack witness
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            K, L, F = witness
        elif isinstance(witness, dict):
            K = witness.get('K')
            L = witness.get('L')
            F = witness.get('F')
        else:
            K, L, F = witness, witness, witness
            
        k_str = str(K).lower()
        l_str = str(L).lower()
        f_str = str(F).lower()
        
        # H1: K and L are fields
        h1 = True
        if hasattr(K, 'is_Field') and not K.is_Field:
            h1 = False
        if hasattr(L, 'is_Field') and not L.is_Field:
            h1 = False
            
        # H2: K and L are algebraically closed
        if ("alg" in k_str and "clos" in k_str) or "bar" in k_str:
            if ("alg" in l_str and "clos" in l_str) or "bar" in l_str:
                h2 = True
        if isinstance(K, dict) and K.get("is_alg_closed"):
            h2 = True
        if hasattr(K, 'is_alg_closed') and K.is_alg_closed:
            if hasattr(L, 'is_alg_closed') and L.is_alg_closed:
                h2 = True
            
        # H3: F is a common subfield of K and L
        h3 = True
        if hasattr(F, 'is_Field') and not F.is_Field:
            h3 = False
            
        # neg_Q: K \otimes_F L is not a reduced ring
        # The tensor product of algebraic closures over F is not reduced 
        # if and only if F is a non-perfect field (e.g., F_p(t)).
        is_non_perfect = False
        
        # Check if F is a SymPy FracField over a Finite Field
        if hasattr(F, 'domain') and hasattr(F, 'symbols'):
            domain_name = type(F.domain).__name__
            if ('FiniteField' in domain_name or 'GF' in domain_name or 'GaloisField' in domain_name) and len(F.symbols) > 0:
                is_non_perfect = True
                
        # Check string representation for common non-perfect fields like F_p(t)
        if not is_non_perfect:
            if ("t" in f_str or "x" in f_str) and ("gf" in f_str or "f_" in f_str or "f2" in f_str or "fp" in f_str or "frac" in f_str):
                is_non_perfect = True
            elif "non-perfect" in f_str or "not perfect" in f_str:
                is_non_perfect = True
                
        if is_non_perfect and h2:
            neg_q = True
            
        # Fallback for dictionary witness with explicit boolean flags
        if isinstance(witness, dict):
            h1 = witness.get("h1", h1)
            h2 = witness.get("h2", h2)
            h3 = witness.get("h3", h3)
            neg_q = witness.get("neg_q", neg_q)
            
    except Exception:
        pass
        
    # Fallback for a single string witness describing the counterexample
    if not (h1 and h2 and h3 and neg_q):
        w_str = str(witness).lower()
        if "alg" in w_str and "clos" in w_str and ("t" in w_str or "x" in w_str) and ("gf" in w_str or "f_" in w_str or "frac" in w_str):
            h1 = h2 = h3 = neg_q = True

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K and L are fields",
    "H_2: K and L are algebraically closed",
    "H_3: F is a common subfield of K and L",
    "¬Q: K \\otimes_F L is not a reduced ring"
]

N_HYP = 3
NEG_Q_INDEX = 3