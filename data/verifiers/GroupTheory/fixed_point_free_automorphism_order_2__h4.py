import sympy
from sympy.combinatorics import (
    PermutationGroup, SymmetricGroup, AlternatingGroup,
    CyclicGroup, DihedralGroup, AbelianGroup
)
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, phi = witness
        else:
            G = witness.G
            phi = witness.phi
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        if isinstance(G, PermutationGroup):
            order = G.order
            if callable(order):
                order = order()
            h1 = order <= 2000
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: \phi is an automorphism of G
    try:
        if not h1:
            h2 = False
        else:
            elems = G.elements
            if callable(elems):
                elems = elems()
            elements_set = set(elems)
            elements = list(elements_set)
            h2 = True
            mapped = set()
            
            for g in elements:
                pg = phi(g) if callable(phi) else phi[g]
                if pg not in elements_set:
                    h2 = False
                    break
                mapped.add(pg)
                
            if h2 and len(mapped) != len(elements):
                h2 = False
                
            if h2:
                for g in elements:
                    for h in elements:
                        pg = phi(g) if callable(phi) else phi[g]
                        ph = phi(h) if callable(phi) else phi[h]
                        pgh = phi(g * h) if callable(phi) else phi[g * h]
                        if pgh != pg * ph:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H_3: The order of \phi is 2
    try:
        if not h1:
            h3 = False
        else:
            elems = G.elements
            if callable(elems):
                elems = elems()
            elements = list(elems)
            is_identity = True
            h3 = True
            
            for g in elements:
                pg = phi(g) if callable(phi) else phi[g]
                ppg = phi(pg) if callable(phi) else phi[pg]
                if ppg != g:
                    h3 = False
                    break
                if pg != g:
                    is_identity = False
                    
            if is_identity:
                h3 = False
    except Exception:
        h3 = False

    # neg_Q: G is not solvable
    try:
        if not h1:
            neg_q = False
        else:
            solvable = G.is_solvable
            if callable(solvable):
                solvable = solvable()
            neg_q = not bool(solvable)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: \\phi is an automorphism of G",
    "H_3: The order of \\phi is 2",
    "¬Q: G is not solvable"
]

N_HYP = 3
NEG_Q_INDEX = 3