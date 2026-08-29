import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: Let Q be the additive group of rational numbers.
    # This is a context statement establishing the domain, vacuous for the witness G itself.
    h1_ok = True
    
    # H_2: Let G be finitely generated.
    try:
        # In SymPy, PermutationGroups and FpGroups are finitely generated.
        # We verify it's a group-like object by checking for generators or elements.
        h2_ok = hasattr(witness, 'generators') or hasattr(witness, 'elements')
        h2_ok = bool(h2_ok)
    except Exception:
        h2_ok = False
        
    # ¬Q: G is not a cyclic group.
    try:
        is_cyc = None
        # Check if the object has a built-in is_cyclic property/method
        if hasattr(witness, 'is_cyclic'):
            res = witness.is_cyclic
            if callable(res):
                res = res()
            if res is not None:
                is_cyc = bool(res)
                
        # Fallback for finite groups if is_cyclic is not directly available
        if is_cyc is None:
            n = witness.order() if callable(witness.order) else witness.order
            is_cyc = False
            for g in witness.elements:
                order_g = g.order() if callable(g.order) else g.order
                if order_g == n:
                    is_cyc = True
                    break
                    
        neg_q_ok = not is_cyc
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Q is the additive group of rational numbers",
    "H_2: G is finitely generated",
    "¬Q: G is not cyclic"
]

N_HYP = 2
NEG_Q_INDEX = 2