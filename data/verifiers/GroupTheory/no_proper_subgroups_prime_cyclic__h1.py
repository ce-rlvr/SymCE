import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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
    # H_1: G is not the trivial group
    try:
        if hasattr(witness, 'order'):
            order_val = witness.order() if callable(witness.order) else witness.order
            h1 = (order_val > 1)
        else:
            # If it's not a group, it is not the trivial group
            h1 = True
    except Exception:
        h1 = True

    # H_2: G has no subgroups other than the trivial subgroup and G itself
    try:
        if hasattr(witness, 'subgroups'):
            subs = witness.subgroups()
            h2 = (len(subs) <= 2)
        else:
            if hasattr(witness, 'generators') and hasattr(witness, 'order'):
                # It looks like a group but lacks a subgroups method; fail safely
                h2 = False
            else:
                # If it's not a group, it vacuously has no subgroups
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: G is not a finite cyclic group of prime order
    try:
        if hasattr(witness, 'is_cyclic') and hasattr(witness, 'order'):
            c = witness.is_cyclic
            is_cyc = c() if callable(c) else c
            order_val = witness.order() if callable(witness.order) else witness.order
            q = bool(is_cyc) and isprime(order_val)
        else:
            q = False
        neg_q = not q
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is not the trivial group",
    "H_2: G has no subgroups other than the trivial subgroup and G itself",
    "¬Q: G is not a finite cyclic group of prime order"
]

N_HYP = 2
NEG_Q_INDEX = 2