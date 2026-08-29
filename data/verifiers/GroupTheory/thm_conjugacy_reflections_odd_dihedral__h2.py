import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n is an odd positive integer",
    "H_2: R is the set of all reflections (elements of order 2 that are not rotations) in G",
    "¬Q: R does not constitute exactly one conjugacy class in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness, checks whether it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (G, n, R) or a dictionary with these keys.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            n = witness.get('n')
            R = witness.get('R')
        else:
            G, n, R = witness
    except Exception:
        return [False, False, False]

    # H_1: n is an odd positive integer
    try:
        h1 = bool(isinstance(n, (int, sympy.Integer)) and n > 0 and n % 2 == 1)
    except Exception:
        h1 = False

    # H_2: R is the set of all reflections (elements of order 2 that are not rotations) in G
    try:
        order = G.order()
        if order % 2 != 0:
            h2 = False
        else:
            m = order // 2
            rotations = set()
            
            # Find the cyclic subgroup of index 2 (the rotations)
            for g in G.elements:
                if g.order() == m:
                    curr = G.identity
                    for _ in range(m):
                        rotations.add(curr)
                        curr = curr * g
                    break
            
            # Reflections are elements of order 2 that are not in the rotation subgroup
            expected_R = {g for g in G.elements if g.order() == 2 and g not in rotations}
            h2 = bool(set(R) == expected_R)
    except Exception:
        h2 = False

    # ¬Q: R does not constitute exactly one conjugacy class in G
    try:
        if not R:
            # An empty set does not constitute exactly one conjugacy class
            neg_q = True
        else:
            R_set = set(R)
            r = next(iter(R_set))
            
            # Compute the conjugacy class of r in G
            C = {g * r * g**-1 for g in G.elements}
            
            # If R is exactly one conjugacy class, it must be exactly equal to C.
            # If it differs, then R does not constitute exactly one conjugacy class.
            neg_q = bool(R_set != C)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]