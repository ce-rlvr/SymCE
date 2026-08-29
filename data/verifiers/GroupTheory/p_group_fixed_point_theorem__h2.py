import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                p, n, G = witness
            elif len(witness) == 2:
                p, G = witness
                try:
                    n = G.degree
                except Exception:
                    n = -1
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: p is a prime number
    try:
        h1 = bool(sympy.ntheory.isprime(p))
    except Exception:
        h1 = False

    # H2: X is a finite set
    try:
        h2 = int(n) == n and n >= 0
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        h3 = isinstance(G, sympy.combinatorics.PermutationGroup) and G.degree <= int(n)
    except Exception:
        h3 = False

    # neg_Q: |X| \not\equiv |X^G| \pmod p
    try:
        if not (h2 and h3):
            neg_q = False
        else:
            n_int = int(n)
            fixed_points = 0
            for i in range(n_int):
                if i >= G.degree:
                    fixed_points += 1
                elif all(g(i) == i for g in G.generators):
                    fixed_points += 1
            neg_q = bool((n_int % p) != (fixed_points % p))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: X is a finite set",
    "H_3: G acts on X",
    "¬Q: |X| is not congruent to |X^G| mod p"
]

N_HYP = 3
NEG_Q_INDEX = 3