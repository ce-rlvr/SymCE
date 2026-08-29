import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import itertools

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "not Q: The commutator identity fails for some elements in G"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple) and len(witness) == 4:
        G, x, y, z = witness
        elements_provided = True
    else:
        G = witness
        elements_provided = False

    try:
        from sympy.combinatorics import PermutationGroup
        h1 = isinstance(G, PermutationGroup) or hasattr(G, 'elements') or hasattr(G, 'generate')
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            def comm(a, b):
                return a * b * a**-1 * b**-1

            def identity_holds(a, b, c):
                lhs = comm(a, b * c)
                rhs = comm(a, c) * c**-1 * comm(a, b) * c
                return lhs == rhs

            if elements_provided:
                neg_q = not identity_holds(x, y, z)
            else:
                fails = False
                if hasattr(G, 'elements'):
                    elems = list(G.elements)
                elif hasattr(G, 'generate'):
                    elems = list(G.generate())
                else:
                    elems = []
                
                for a, b, c in itertools.product(elems, repeat=3):
                    if not identity_holds(a, b, c):
                        fails = True
                        break
                neg_q = fails
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]