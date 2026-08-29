import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import totient
from sympy import oo, Integer

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

def conditions(witness):
    h1_ok = False
    neg_q_ok = False
    
    # The witness can be interpreted as either the group G itself or its order n.
    is_group = hasattr(witness, 'is_cyclic')
    
    # Check Hypothesis 1: G is a cyclic group of order n
    try:
        if is_group:
            is_cyc = witness.is_cyclic() if callable(witness.is_cyclic) else witness.is_cyclic
            if is_cyc:
                h1_ok = True
        else:
            # If witness is an order, it must be a valid order for a cyclic group
            # (a positive integer, or infinity/0 for the infinite cyclic group Z)
            if witness == oo or witness == 0 or witness == "Z":
                h1_ok = True
            elif isinstance(witness, (int, Integer)) and witness >= 1:
                h1_ok = True
    except Exception:
        h1_ok = False

    # Check Negated Conclusion: The order of the automorphism group of G is NOT \phi(n)
    try:
        if is_group:
            order = witness.order() if callable(witness.order) else witness.order
            if order == oo or order == 0:
                # The infinite cyclic group has exactly 2 automorphisms (identity and inversion).
                try:
                    phi = totient(order)
                    neg_q_ok = bool(phi != 2)
                except Exception:
                    # totient(oo) is undefined / raises an error
                    neg_q_ok = True
            else:
                # For finite cyclic groups, the automorphism group order is exactly \phi(n).
                neg_q_ok = False
        else:
            if witness == oo or witness == 0 or witness == "Z":
                try:
                    phi = totient(witness)
                    neg_q_ok = bool(phi != 2)
                except Exception:
                    neg_q_ok = True
            elif isinstance(witness, (int, Integer)) and witness >= 1:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a cyclic group of order n",
    r"¬Q: The order of the automorphism group of G is not \phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1