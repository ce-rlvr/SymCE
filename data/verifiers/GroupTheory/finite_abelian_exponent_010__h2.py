import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.matrices import eye, zeros

# Top-level setup
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
        if isinstance(witness, dict):
            G = witness.get('G')
            m = witness.get('m')
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, m = witness
        elif hasattr(witness, 'G') and hasattr(witness, 'm'):
            G = witness.G
            m = witness.m
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H1: G is a finite abelian group
    try:
        h1_ok = isinstance(G, PermutationGroup) and bool(G.is_abelian)
    except Exception:
        h1_ok = False

    # neg_Q: The order of every element in G divides m (negated)
    # True if there exists an element in G whose order does NOT divide m
    try:
        neg_q_ok = False
        m_int = int(m)
        
        elements = None
        if hasattr(G, 'elements'):
            elements = G.elements
        elif hasattr(G, 'generate'):
            elements = G.generate()
            
        if elements is not None:
            for g in elements:
                if m_int % g.order() != 0:
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite abelian group",
    "¬Q: There exists an element in G whose order does not divide m"
]

N_HYP = 1
NEG_Q_INDEX = 1