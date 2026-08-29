import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    # Extract n, F, G from the witness
    n, F, G = None, None, None
    if isinstance(witness, dict):
        n = witness.get('n')
        F = witness.get('F')
        G = witness.get('G')
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 3:
            n, F, G = witness
        elif len(witness) == 2:
            n, F = witness

    # Fallback if G is provided as a list of generators
    try:
        if isinstance(G, list):
            G = PermutationGroup(G)
    except Exception:
        pass

    # H_1: n >= 3
    try:
        h1 = bool(n >= 3)
    except Exception:
        h1 = False

    # H_2: F is a field
    try:
        if isinstance(F, (int, sympy.Integer)):
            factors = factorint(int(F))
            h2 = bool(len(factors) == 1)
        elif hasattr(F, 'is_Field'):
            h2 = bool(F.is_Field)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: G is the special linear group SL(n, F)
    try:
        if isinstance(F, (int, sympy.Integer)):
            q = int(F)
        elif hasattr(F, 'order'):
            q = F.order() if callable(F.order) else F.order
        elif hasattr(F, 'mod'):
            q = F.mod
        else:
            q = None
            
        if q is not None and G is not None:
            order = 1
            n_int = int(n)
            for i in range(n_int):
                order *= (q**n_int - q**i)
            order = order // (q - 1)
            h3 = bool(G.order() == order)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The commutator subgroup of G is not equal to G
    try:
        if G is not None:
            if hasattr(G, 'is_perfect'):
                val = G.is_perfect
                if callable(val):
                    val = val()
                neg_q = not bool(val)
            elif hasattr(G, 'derived_subgroup'):
                neg_q = bool(G.derived_subgroup().order() != G.order())
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3",
    "H_2: F is a field",
    "H_3: G is the special linear group SL(n, F)",
    "¬Q: The commutator subgroup of G is not equal to G"
]

N_HYP = 3
NEG_Q_INDEX = 3