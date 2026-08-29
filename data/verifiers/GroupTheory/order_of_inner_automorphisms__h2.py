import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    # Extract witness components
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            g = witness.get('g')
            n_given = witness.get('n')
            e_given = witness.get('e')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                G, g = witness
                n_given = None
                e_given = None
            elif len(witness) == 3:
                G, g, n_given = witness
                e_given = None
            elif len(witness) == 4:
                G, g, n_given, e_given = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
            h1 = True
        elif isinstance(G, (list, set, tuple)):
            elements = list(G)
            h1 = True
        else:
            elements = []
            h1 = False
    except Exception:
        h1 = False
        elements = []

    # H_2: There exists a positive integer n such that g^n = e, and n is the smallest such integer
    try:
        if e_given is not None:
            e = e_given
        else:
            if elements and isinstance(elements[0], Permutation):
                e = Permutation()
            elif hasattr(g, 'shape'):
                e = eye(g.shape[0])
            else:
                e = elements[0]**0

        n = 1
        curr = g
        while curr != e and n < 10000:
            curr = curr * g
            n += 1
        
        if n_given is not None:
            h2 = (curr == e) and (n == n_given)
        else:
            h2 = (curr == e)
    except Exception:
        h2 = False

    # H_3: \phi_g: G \to G is the inner automorphism defined by \phi_g(x) = gxg^{-1}
    try:
        maps_to_G = True
        for x in elements:
            conj = g * x * g**-1
            if conj not in elements:
                maps_to_G = False
                break
        
        is_inner = False
        if maps_to_G:
            for h in elements:
                match = True
                for x in elements:
                    if g * x * g**-1 != h * x * h**-1:
                        match = False
                        break
                if match:
                    is_inner = True
                    break
        h3 = maps_to_G and is_inner
    except Exception:
        h3 = False

    # neg_Q: The order of \phi_g in the automorphism group Aut(G) does not divide n
    try:
        m = 1
        while m < 10000:
            is_id = True
            for x in elements:
                if g**m * x * g**-m != x:
                    is_id = False
                    break
            if is_id:
                break
            m += 1
        
        q = (n % m == 0)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: There exists a positive integer n such that g^n = e, and n is the smallest such integer",
    "H_3: \\phi_g: G \\to G is the inner automorphism defined by \\phi_g(x) = gxg^{-1}",
    "¬Q: The order of \\phi_g in the automorphism group Aut(G) does not divide n"
]

N_HYP = 3
NEG_Q_INDEX = 3