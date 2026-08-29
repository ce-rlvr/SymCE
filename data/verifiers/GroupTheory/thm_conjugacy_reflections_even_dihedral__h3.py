import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n is an even positive integer",
    "H_2: G is the dihedral group of order 2n",
    "¬Q: R is not the disjoint union of exactly two conjugacy classes in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            G = witness.get('G')
            R = witness.get('R', None)
        else:
            if len(witness) == 3:
                n, G, R = witness
            elif len(witness) == 2:
                n, G = witness
                R = None
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: n is an even positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0 and n % 2 == 0
    except Exception:
        h1 = False

    # H_2: G is the dihedral group of order 2n
    try:
        h2 = False
        if hasattr(G, 'order') and hasattr(G, 'elements'):
            if G.order() == 2 * n:
                elements = list(G.elements)
                for r in elements:
                    if r.order() == n:
                        for s in elements:
                            if s.order() == 2:
                                if s * r * s == r**-1:
                                    if PermutationGroup(r, s).order() == G.order():
                                        h2 = True
                                        break
                        if h2:
                            break
    except Exception:
        h2 = False

    # ¬Q: R is not the disjoint union of exactly two conjugacy classes in G
    try:
        def check_neg_Q(G, R):
            elements = list(G.elements)
            classes = []
            seen = set()
            for g in elements:
                if g in seen:
                    continue
                c = set()
                for x in elements:
                    c.add(x * g * x**-1)
                classes.append(c)
                seen.update(c)
            
            R_set = set(R)
            count = 0
            for c in classes:
                if c.issubset(R_set):
                    count += 1
                    R_set -= c
                elif not c.isdisjoint(R_set):
                    return True
            
            if len(R_set) > 0:
                return True
                
            return count != 2

        if R is None:
            elements = list(G.elements)
            rotations = None
            unique = True
            for g in elements:
                if g.order() == n:
                    rot = {g**i for i in range(n)}
                    if len(rot) == n:
                        if rotations is None:
                            rotations = rot
                        elif rotations != rot:
                            unique = False
                            break
            if not unique or rotations is None:
                neg_q = True
            else:
                R = [g for g in elements if g not in rotations]
                neg_q = check_neg_Q(G, R)
        else:
            neg_q = check_neg_Q(G, R)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]