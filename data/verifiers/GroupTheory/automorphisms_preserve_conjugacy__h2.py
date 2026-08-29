import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def eval_phi(phi, val):
    if isinstance(phi, dict):
        return phi[val]
    return phi(val)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, x, y, g, phi) or (G, x, y, phi).
    """
    try:
        if len(witness) == 5:
            G, x, y, g, phi = witness
        elif len(witness) == 4:
            G, x, y, phi = witness
            g = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = hasattr(G, 'elements') and hasattr(G, 'identity')
    except Exception:
        h1 = False

    # H_2: There exists an element g \in G such that y = gxg^{-1}
    try:
        g_works = False
        if g is not None:
            try:
                if g in G.elements and y == g * x * g**-1:
                    g_works = True
            except Exception:
                pass
        
        if not g_works:
            for elem in G.elements:
                try:
                    if y == elem * x * elem**-1:
                        g = elem
                        g_works = True
                        break
                except Exception:
                    continue
        h2 = g_works
    except Exception:
        h2 = False

    # H_3: \phi is an automorphism of G
    try:
        elements = list(G.elements)
        mapped_elements = [eval_phi(phi, elem) for elem in elements]
        
        is_bijection = True
        for m in mapped_elements:
            if m not in elements:
                is_bijection = False
                break
        if is_bijection:
            for i in range(len(elements)):
                for j in range(i + 1, len(elements)):
                    if mapped_elements[i] == mapped_elements[j]:
                        is_bijection = False
                        break
                if not is_bijection:
                    break
        
        is_homo = True
        if is_bijection:
            for a in elements:
                for b in elements:
                    if eval_phi(phi, a * b) != eval_phi(phi, a) * eval_phi(phi, b):
                        is_homo = False
                        break
                if not is_homo:
                    break
                
        h3 = is_bijection and is_homo
    except Exception:
        h3 = False

    # ¬Q: \phi(y) != \phi(g)\phi(x)\phi(g)^{-1}
    try:
        lhs = eval_phi(phi, y)
        rhs = eval_phi(phi, g) * eval_phi(phi, x) * eval_phi(phi, g)**-1
        neg_q = bool(lhs != rhs)
    except Exception:
        # If evaluating \phi on x or y raises an exception (e.g. they are outside G),
        # the conclusion equation is undefined, hence the conclusion fails.
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: There exists an element g in G such that y = gxg^{-1}",
    "H_3: phi is an automorphism of G",
    "¬Q: phi(y) != phi(g)phi(x)phi(g)^{-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3