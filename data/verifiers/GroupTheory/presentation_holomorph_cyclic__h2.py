import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

def holomorph(n):
    """
    Constructs the holomorph of Z_n as a PermutationGroup.
    The holomorph is the semidirect product of Z_n and Aut(Z_n).
    """
    if n < 2:
        return None
    
    # Generator for the normal subgroup Z_n
    x_list = [(k + 1) % n for k in range(n)]
    x = Permutation(x_list)
    gens = [x]
    
    # Generators for Aut(Z_n)
    for a in range(1, n):
        if math.gcd(a, n) == 1:
            y_list = [(a * k) % n for k in range(n)]
            y = Permutation(y_list)
            gens.append(y)
            
    return PermutationGroup(gens)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness is expected to provide an integer n and a group G.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            G = witness.get('G')
        elif isinstance(witness, tuple) and len(witness) == 2:
            # Try to identify which element is the group and which is the integer
            if hasattr(witness[0], 'is_isomorphic'):
                G, n = witness[0], witness[1]
            elif hasattr(witness[1], 'is_isomorphic'):
                n, G = witness[0], witness[1]
            else:
                n, G = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: n >= 2 is an integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n >= 2
        n_val = int(n)
    except Exception:
        h1 = False

    # ¬Q: G does NOT admit the presentation
    # The presentation given defines exactly the holomorph of Z_n.
    # Therefore, the conclusion holds iff G is isomorphic to Hol(Z_n).
    try:
        if not h1:
            neg_q = False
        else:
            H = holomorph(n_val)
            if H is None:
                q = False
            else:
                q = G.is_isomorphic(H)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "¬Q: G does not admit the presentation (i.e., G is not isomorphic to the holomorph of Z_n)"
]

N_HYP = 1
NEG_Q_INDEX = 1