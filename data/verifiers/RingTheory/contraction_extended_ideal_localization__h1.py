import sympy
import sympy.combinatorics
import sympy.matrices
import itertools
import math
import functools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False
    
    # 1. Try dictionary format
    if isinstance(witness, dict):
        try:
            if 'R' in witness and 'S' in witness and 'I' in witness:
                R = witness['R']
                S = witness['S']
                I = witness['I']
                add = witness.get('add', lambda x, y: x + y)
                mul = witness.get('mul', lambda x, y: x * y)
                
                # H1: S is a multiplicatively closed subset of R
                h1 = all(s in R for s in S) and all(mul(s1, s2) in S for s1 in S for s2 in S)
                
                # H2: I is an ideal of R
                h2 = all(i in R for i in I) and len(I) > 0
                if h2:
                    closed_add = all(add(i1, i2) in I for i1 in I for i2 in I)
                    closed_mul = all(mul(r, i) in I and mul(i, r) in I for r in R for i in I)
                    h2 = closed_add and closed_mul
                    
                # H3: \phi is the canonical localization map
                h3 = witness.get('is_canonical_localization_map', witness.get('is_canonical_map', True))
                
                # neg_Q: contraction != {x \in R | \exists s \in S, sx \in I}
                if 'contraction' in witness:
                    contraction = witness['contraction']
                    target_set = []
                    for x in R:
                        if any(mul(s, x) in I for s in S):
                            target_set.append(x)
                    
                    def is_equal(set1, set2):
                        for e1 in set1:
                            if e1 not in set2: return False
                        for e2 in set2:
                            if e2 not in set1: return False
                        return True
                        
                    neg_q = not is_equal(contraction, target_set)
                else:
                    neg_q = witness.get('neg_q', False)
                    
                return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 2. Try object methods format
    try:
        h1 = bool(witness.is_multiplicatively_closed())
    except Exception:
        h1 = False

    try:
        h2 = bool(witness.is_ideal())
    except Exception:
        h2 = False

    try:
        if hasattr(witness, 'is_canonical_localization_map'):
            if callable(witness.is_canonical_localization_map):
                h3 = bool(witness.is_canonical_localization_map())
            else:
                h3 = bool(witness.is_canonical_localization_map)
        else:
            h3 = True
    except Exception:
        h3 = False

    try:
        neg_q = not bool(witness.contraction_equals_set())
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: I is an ideal of R",
    "H_3: \\phi is the canonical localization map from R to S^{-1}R",
    "¬Q: The contraction of the extended ideal \\phi^{-1}(S^{-1}I) is not equal to \\{x \\in R \\mid \\exists s \\in S \\text{ such that } sx \\in I\\}"
]

N_HYP = 3
NEG_Q_INDEX = 3