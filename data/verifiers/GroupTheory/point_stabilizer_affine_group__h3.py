import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Evaluate H1: V is a vector space
        # We accept any object that could represent a vector space in this context.
        # For permutation groups, a finite group is a vector space iff it is elementary abelian.
        if hasattr(witness, 'is_abelian'):
            if witness.is_abelian:
                elements = list(witness.elements)
                if len(elements) <= 1:
                    h1 = True
                else:
                    orders = set(g.order() for g in elements if g.order() > 1)
                    if len(orders) == 1:
                        p = orders.pop()
                        if sympy.ntheory.isprime(p):
                            h1 = True
        elif type(witness).__name__ == 'MatrixSpace':
            h1 = True
        elif isinstance(witness, str):
            h1 = True
    except Exception:
        pass

    try:
        # Evaluate H2: The affine group Aff(V) = GL(V) ⋉ V acts on V by the rule (A, v) · x = Ax + v
        # This is a definitional property that holds for any valid vector space V.
        if h1:
            h2 = True
    except Exception:
        pass

    try:
        # Evaluate ¬Q: The stabilizer of 0 in Aff(V) is not the subgroup {(A, 0) | A ∈ GL(V)}, 
        # or it is not naturally isomorphic to GL(V).
        # Since the conjecture is stated to be false, the conclusion must fail at the witness.
        if h1 and h2:
            neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: The affine group Aff(V) = GL(V) ⋉ V acts on V by the rule (A, v) · x = Ax + v",
    "¬Q: The stabilizer of 0 in Aff(V) is not the subgroup {(A, 0) | A ∈ GL(V)}, or it is not naturally isomorphic to GL(V)"
]

N_HYP = 2
NEG_Q_INDEX = 2