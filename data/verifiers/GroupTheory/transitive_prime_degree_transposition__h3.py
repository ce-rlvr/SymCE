import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should ideally be a tuple (p, G) where p is a prime and G is a PermutationGroup.
    If only G is provided, p is inferred from the size of the orbit of 0.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p, G = witness
        else:
            G = witness
            p = len(G.orbit(0))
    except Exception:
        return [False] * 5

    # H_1: Let p be a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H_2: Let S_p be the symmetric group on p letters
    # This is a definitional hypothesis; we just verify p is a valid positive integer.
    try:
        h2 = int(p) > 0
    except Exception:
        h2 = False

    # H_3: Assume G acts transitively on the set {1, 2, ..., p}
    # In 0-indexed SymPy, this means {0, 1, ..., p-1} is an orbit of G.
    try:
        p_int = int(p)
        orbit = G.orbit(0)
        h3 = set(orbit) == set(range(p_int))
    except Exception:
        h3 = False

    # H_4: Assume G contains at least one transposition
    try:
        h4 = False
        # Check generators first for speed
        for g in G.generators:
            if len(g.cyclic_form) == 1 and len(g.cyclic_form[0]) == 2:
                h4 = True
                break
        # If not found in generators, search through elements (up to a limit)
        if not h4:
            for i, g in enumerate(G.generate()):
                if i > 1000:
                    break
                if len(g.cyclic_form) == 1 and len(g.cyclic_form[0]) == 2:
                    h4 = True
                    break
    except Exception:
        h4 = False

    # ¬Q: The subgroup G is not equal to the symmetric group S_p
    try:
        Sp = SymmetricGroup(int(p))
        # In SymPy, PermutationGroup equality requires the same degree and same generated elements.
        neg_q = not (G == Sp)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: S_p is the symmetric group on p letters",
    "H_3: G acts transitively on the set {1, 2, ..., p}",
    "H_4: G contains at least one transposition",
    "¬Q: G is not equal to the symmetric group S_p"
]

N_HYP = 4
NEG_Q_INDEX = 4