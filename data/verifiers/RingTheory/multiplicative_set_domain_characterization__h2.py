import sympy
from sympy import isprime

# Top-level setup
Z = 0
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            n_obj = witness.get('R', witness.get('n'))
            S_obj = witness.get('S')
        else:
            n_obj, S_obj = witness
            
        if isinstance(n_obj, str):
            if n_obj.startswith("Z"):
                n_str = n_obj.replace("Z", "").replace("_", "")
                n = 0 if n_str == "" else int(n_str)
            else:
                n = int(n_obj)
        else:
            n = int(n_obj)
            
        S = set()
        for x in S_obj:
            S.add(int(x))
            
        # H1: R is a commutative ring with a non-zero identity element
        # We represent R as Z_n (integers modulo n) for n >= 2, or Z for n = 0.
        # Both are commutative rings with 1 != 0.
        if n == 0:
            h1 = True
        else:
            h1 = (n >= 2) and all(0 <= x < n for x in S)
    except Exception:
        h1 = False

    try:
        if h1:
            # R is an integral domain iff n is prime (or n == 0 for Z)
            is_domain = True if n == 0 else isprime(n)
            
            # S is closed under multiplication
            is_closed = True
            for a in S:
                for b in S:
                    prod = (a * b) if n == 0 else (a * b) % n
                    if prod not in S:
                        is_closed = False
                        break
                if not is_closed:
                    break
                    
            # ¬Q: The conclusion fails if the equivalence does not hold
            neg_q = (is_domain != is_closed)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with a non-zero identity element",
    "¬Q: It is NOT the case that (R is an integral domain iff S is closed under multiplication)"
]

N_HYP = 1
NEG_Q_INDEX = 1