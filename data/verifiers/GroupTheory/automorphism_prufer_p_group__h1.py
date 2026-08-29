import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The true theorem requires p to be a prime. The false conjecture drops this hypothesis.
    Thus, a valid counterexample is a composite integer p >= 2.
    """
    p = witness
    # Handle cases where the witness might be passed as a tuple (G, p) or a dict
    if isinstance(witness, (tuple, list)) and len(witness) == 2:
        p = witness[1]
    elif isinstance(witness, dict) and 'p' in witness:
        p = witness['p']
        
    try:
        # H_1: G is the Prüfer p-group, denoted as Z(p^\infty)
        # This implies p is the parameter for the group. We check if p is a valid integer >= 2.
        if not isinstance(p, (int, sympy.Integer)):
            H_1 = False
        else:
            H_1 = p >= 2
    except Exception:
        H_1 = False

    try:
        # neg_Q: The conclusion fails.
        # The conclusion is that Aut(G) is isomorphic to the p-adic units.
        # This is true if p is prime. If p is composite, p-adic units are undefined 
        # (the p-adic integers do not form an integral domain, so "p-adic units" is a category error).
        # Thus, the conclusion fails if p is not prime.
        if not isinstance(p, (int, sympy.Integer)):
            neg_Q = False
        else:
            neg_Q = not sympy.isprime(p)
    except Exception:
        neg_Q = False

    return [H_1, neg_Q]

CONDITION_LABELS = [
    "H_1: G is the Prüfer p-group, denoted as Z(p^\\infty)",
    "¬Q: The automorphism group Aut(G) is not isomorphic to the multiplicative group of p-adic units Z_p^\\times"
]

N_HYP = 1
NEG_Q_INDEX = 1