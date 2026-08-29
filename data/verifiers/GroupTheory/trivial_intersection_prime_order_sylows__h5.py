import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime
from sympy.matrices import eye, zeros

# Top-level setup for witness expressions
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
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: p divides the order of G",
    "H_4: p^2 does not divide the order of G",
    "¬Q: The intersection P \\cap Q is not the trivial subgroup {e}"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            P = witness.get('P')
            Q = witness.get('Q')
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                G, p, P, Q = witness
            elif len(witness) == 2:
                G, p = witness
                P = None
                Q = None
            else:
                return [False] * 5
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: p divides the order of G
    try:
        h3 = bool(G.order() % p == 0)
    except Exception:
        h3 = False

    # H_4: p^2 does not divide the order of G
    try:
        h4 = bool(G.order() % (p**2) != 0)
    except Exception:
        h4 = False

    # ¬Q: The intersection P \cap Q is not the trivial subgroup {e}
    try:
        # If P and Q are not explicitly provided, the counterexample to the false conjecture
        # (which dropped the hypothesis that P and Q are distinct) is to use the same Sylow p-subgroup.
        if P is None and Q is None:
            P = G.sylow_subgroup(p)
            Q = P
            
        if hasattr(P, 'generate'):
            elements_P = set(P.generate())
        elif hasattr(P, 'elements'):
            elements_P = set(P.elements)
        else:
            elements_P = set(P)
            
        if hasattr(Q, 'generate'):
            elements_Q = set(Q.generate())
        elif hasattr(Q, 'elements'):
            elements_Q = set(Q.elements)
        else:
            elements_Q = set(Q)
            
        intersection = elements_P.intersection(elements_Q)
        # The trivial subgroup has exactly 1 element (the identity).
        # If the intersection has more than 1 element, it is not trivial.
        neg_q = len(intersection) > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]