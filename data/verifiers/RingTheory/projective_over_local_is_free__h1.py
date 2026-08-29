import sympy
from sympy import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the conjecture:
    H1: R is a local ring
    H2: M is a finitely generated R-module
    H3: M is a projective R-module
    Conclusion: M is a free R-module
    """
    
    def check_prop(obj, prop_names):
        if isinstance(obj, dict):
            for p in prop_names:
                if p in obj:
                    return bool(obj[p])
        for p in prop_names:
            if hasattr(obj, p):
                val = getattr(obj, p)
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        pass
                else:
                    return bool(val)
        return None

    # 1. Try if witness is a tuple (n, P) where n is int (modulus) and P is sympy.Matrix (idempotent)
    if isinstance(witness, (tuple, list)) and len(witness) == 2:
        n, P = witness
        if isinstance(n, int) and isinstance(P, sympy.Matrix):
            try:
                # H1: R = Z/nZ is a local ring iff n is a prime power
                factors = factorint(n)
                h1 = (len(factors) == 1)
                
                # H2: M = Im(P) is finitely generated (always true for finite matrices)
                h2 = True
                
                # H3: M is projective iff P is idempotent mod n
                P_sq = P * P
                h3 = all((P_sq[i, j] - P[i, j]) % n == 0 for i in range(P.rows) for j in range(P.cols))
                
                # neg_Q: M is free iff its rank is constant.
                # Over Z/nZ where n is a prime power, projective implies free.
                neg_q = False
                return [h1, h2, h3, neg_q]
            except Exception:
                pass

    # 2. Try to unpack if it's a tuple (R, M) of custom objects/dicts
    if isinstance(witness, (tuple, list)) and len(witness) == 2:
        R, M = witness
        h1 = check_prop(R, ['is_local_ring', 'is_local'])
        h2 = check_prop(M, ['is_finitely_generated', 'is_fg'])
        h3 = check_prop(M, ['is_projective'])
        is_free = check_prop(M, ['is_free'])
        
        if any(x is not None for x in (h1, h2, h3, is_free)):
            return [
                bool(h1), 
                bool(h2), 
                bool(h3), 
                not bool(is_free) if is_free is not None else False
            ]

    # 3. Try if witness has ring and module attributes
    if hasattr(witness, 'ring') and hasattr(witness, 'module'):
        h1 = check_prop(witness.ring, ['is_local_ring', 'is_local'])
        h2 = check_prop(witness.module, ['is_finitely_generated', 'is_fg'])
        h3 = check_prop(witness.module, ['is_projective'])
        is_free = check_prop(witness.module, ['is_free'])
        
        if any(x is not None for x in (h1, h2, h3, is_free)):
            return [
                bool(h1), 
                bool(h2), 
                bool(h3), 
                not bool(is_free) if is_free is not None else False
            ]

    # 4. Try as a single object/dict
    h1 = check_prop(witness, ['is_local_ring', 'is_local', 'R_is_local'])
    h2 = check_prop(witness, ['is_finitely_generated', 'is_fg', 'M_is_finitely_generated'])
    h3 = check_prop(witness, ['is_projective', 'M_is_projective'])
    is_free = check_prop(witness, ['is_free', 'M_is_free'])

    return [
        bool(h1),
        bool(h2),
        bool(h3),
        not bool(is_free) if is_free is not None else False
    ]

CONDITION_LABELS = [
    "H_1: R is a local ring",
    "H_2: M is a finitely generated R-module",
    "H_3: M is a projective R-module",
    "¬Q: M is not a free R-module"
]

N_HYP = 3
NEG_Q_INDEX = 3