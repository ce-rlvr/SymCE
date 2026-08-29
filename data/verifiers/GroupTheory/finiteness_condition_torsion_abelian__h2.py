import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, CyclicGroup, DihedralGroup, AlternatingGroup, AbelianGroup
)
from sympy import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    h1 = False
    h2 = False
    neg_q = False
    
    # 1. String witness heuristic for known infinite torsion abelian groups
    try:
        if isinstance(witness, str):
            w = witness.lower()
            is_inf_torsion_ab = False
            if "q/z" in w or "q / z" in w:
                is_inf_torsion_ab = True
            elif "prufer" in w or "prüfer" in w:
                is_inf_torsion_ab = True
            elif ("infinite" in w or "infty" in w or "infinity" in w) and ("direct sum" in w or "oplus" in w):
                is_inf_torsion_ab = True
            elif "torsion" in w and "abelian" in w and "infinite" in w:
                is_inf_torsion_ab = True
                
            if is_inf_torsion_ab:
                return [True, True, True]
    except Exception:
        pass

    # 2. Instantiate if witness is a class
    try:
        if isinstance(witness, type):
            witness = witness()
    except Exception:
        pass

    # 3. Evaluate H1: G is an abelian group
    try:
        if hasattr(witness, 'is_abelian'):
            val = getattr(witness, 'is_abelian')
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_commutative'):
            val = getattr(witness, 'is_commutative')
            h1 = bool(val() if callable(val) else val)
    except Exception:
        pass

    # 4. Evaluate H2: Every element of G has finite order
    try:
        if hasattr(witness, 'is_torsion'):
            val = getattr(witness, 'is_torsion')
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'elements_have_finite_order'):
            val = getattr(witness, 'elements_have_finite_order')
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_finite'):
            val = getattr(witness, 'is_finite')
            if bool(val() if callable(val) else val):
                h2 = True
    except Exception:
        pass

    # 5. Evaluate ¬Q: G is not a finite group
    try:
        if hasattr(witness, 'is_finite'):
            val = getattr(witness, 'is_finite')
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_infinite'):
            val = getattr(witness, 'is_infinite')
            neg_q = bool(val() if callable(val) else val)
        elif hasattr(witness, 'order'):
            val = getattr(witness, 'order')
            order_val = val() if callable(val) else val
            neg_q = (order_val == sympy.oo or order_val == float('inf'))
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: Every element of G has finite order",
    "¬Q: G is not a finite group"
]

N_HYP = 2
NEG_Q_INDEX = 2