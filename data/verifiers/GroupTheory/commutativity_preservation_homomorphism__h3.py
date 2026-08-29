import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
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
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, H, f_input = witness
    except Exception:
        return [False, False, False]
    
    # H1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: f is a homomorphism from G to H
    try:
        if callable(f_input):
            f = f_input
        elif isinstance(f_input, dict):
            def f(x):
                return f_input[x]
        else:
            f = None
            
        if f is None:
            h2 = False
        else:
            if G.order() > 2000:
                h2 = False
            else:
                h2 = True
                elements = list(G.elements)
                for x in elements:
                    if f(x) not in H:
                        h2 = False
                        break
                if h2:
                    for x in elements:
                        for y in elements:
                            if f(x * y) != f(x) * f(y):
                                h2 = False
                                break
                        if not h2:
                            break
    except Exception:
        h2 = False

    # neg_Q: f(x)f(y) != f(y)f(x) in H for some x, y in G
    try:
        if callable(f_input):
            f = f_input
        elif isinstance(f_input, dict):
            def f(x):
                return f_input[x]
        else:
            f = None

        neg_q = False
        if f is not None:
            elements_to_check = list(G.elements) if G.order() <= 2000 else G.generators
            for x in elements_to_check:
                for y in elements_to_check:
                    if f(x) * f(y) != f(y) * f(x):
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f: G -> H is a group homomorphism",
    "¬Q: f(x)f(y) != f(y)f(x) in H for some x, y in G"
]

N_HYP = 2
NEG_Q_INDEX = 2