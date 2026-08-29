import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            x = witness['x']
            N = witness['N']
        elif len(witness) == 3:
            G = witness[0]
            if isinstance(witness[1], Permutation):
                x = witness[1]
                N = witness[2]
            elif isinstance(witness[2], Permutation):
                x = witness[2]
                N = witness[1]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: x is an element of G
    try:
        h2 = x in G
    except Exception:
        h2 = False

    # neg_Q: The size of the conjugacy class of xN in G/N does NOT divide the size of the conjugacy class of x in G
    try:
        # Compute the orbit of x under conjugation in G (conjugacy class of x in G)
        orbit_x = set()
        queue = [x]
        orbit_x.add(x)
        gens = G.generators
        while queue:
            curr = queue.pop(0)
            for g in gens:
                conj = g * curr * ~g
                if conj not in orbit_x:
                    orbit_x.add(conj)
                    queue.append(conj)
        size_C = len(orbit_x)

        # Compute the number of distinct left cosets of N intersecting the conjugacy class of x.
        # This corresponds to the size of the conjugacy class of xN in G/N.
        # Two elements y1, y2 are in the same left coset iff y1^-1 * y2 in N.
        cosets = []
        for y in orbit_x:
            found = False
            for rep in cosets:
                if (~rep * y) in N:
                    found = True
                    break
            if not found:
                cosets.append(y)
        size_C_prime = len(cosets)

        # The conclusion fails if the size in the quotient does not divide the size in the group
        neg_q = (size_C % size_C_prime != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is an element of G",
    "¬Q: The size of the conjugacy class of xN in G/N does not divide the size of the conjugacy class of x in G"
]

N_HYP = 2
NEG_Q_INDEX = 2