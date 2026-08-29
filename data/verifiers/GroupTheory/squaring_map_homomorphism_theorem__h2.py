import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, f = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        is_abelian = bool(G.is_abelian)
        is_hom = True
        
        # Evaluate homomorphism property over all pairs of elements
        elements = list(G.elements)
        for x in elements:
            for y in elements:
                if callable(f):
                    fx = f(x)
                    fy = f(y)
                    fxy = f(x * y)
                elif isinstance(f, dict):
                    fx = f[x]
                    fy = f[y]
                    fxy = f[x * y]
                else:
                    raise ValueError("f must be callable or a dictionary")
                
                if fxy != fx * fy:
                    is_hom = False
                    break
            if not is_hom:
                break
        
        # The conclusion is: f is a homomorphism iff G is abelian.
        # We want the negation of the conclusion.
        neg_q_ok = (is_hom != is_abelian)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: It is not the case that f is a group homomorphism iff G is an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1