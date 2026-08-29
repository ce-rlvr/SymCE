import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

CONDITION_LABELS = [
    "H_1: f is a surjective group homomorphism from G to H",
    "H_2: A and B are subgroups of G such that A is a subgroup of B",
    "H_3: The kernel of f is a subgroup of A",
    "not Q: The index of A in B is not equal to the index of f(A) in f(B)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            f = witness['f']
            A = witness['A']
            B = witness['B']
        else:
            G = witness.G
            H = witness.H
            f = witness.f
            A = witness.A
            B = witness.B
            
        G_elements = list(G.generate())
        h_any = list(H.generate())[0]
        id_H = h_any * ~h_any
    except Exception:
        return [False, False, False, False]

    def get_f(x):
        return f[x] if isinstance(f, dict) else f(x)

    def get_order(grp):
        return grp.order() if callable(getattr(grp, 'order', None)) else grp.order

    def get_generators(grp):
        gens = grp.generators
        return gens() if callable(gens) else gens

    # H1: f is a surjective group homomorphism from G to H
    h1 = False
    try:
        image = set()
        is_hom = True
        for g in G_elements:
            try:
                val = get_f(g)
            except Exception:
                is_hom = False
                break
            
            try:
                in_H = H.contains(val)
            except AttributeError:
                in_H = (val in H)
                
            if not in_H:
                is_hom = False
                break
            image.add(val)
            
        if is_hom and len(image) == get_order(H):
            for g1 in G_elements:
                for g2 in G_elements:
                    if get_f(g1 * g2) != get_f(g1) * get_f(g2):
                        is_hom = False
                        break
                if not is_hom:
                    break
            h1 = is_hom
    except Exception:
        h1 = False

    # H2: A and B are subgroups of G such that A is a subgroup of B
    h2 = False
    try:
        def is_subgroup(sub, parent):
            try:
                return all(parent.contains(g) for g in get_generators(sub))
            except AttributeError:
                return all((g in parent) for g in get_generators(sub))
        
        if is_subgroup(A, G) and is_subgroup(B, G) and is_subgroup(A, B):
            h2 = True
    except Exception:
        h2 = False

    # H3: The kernel of f is a subgroup of A
    h3 = False
    try:
        ker_in_A = True
        for g in G_elements:
            if get_f(g) == id_H:
                try:
                    in_A = A.contains(g)
                except AttributeError:
                    in_A = (g in A)
                if not in_A:
                    ker_in_A = False
                    break
        h3 = ker_in_A
    except Exception:
        h3 = False

    # neg_Q: The index of A in B is not equal to the index of f(A) in f(B)
    neg_q = False
    try:
        fA_gens = [get_f(g) for g in get_generators(A)]
        if not fA_gens:
            fA_gens = [id_H]
        fA = PermutationGroup(fA_gens)
        
        fB_gens = [get_f(g) for g in get_generators(B)]
        if not fB_gens:
            fB_gens = [id_H]
        fB = PermutationGroup(fB_gens)
        
        neg_q = (get_order(B) * get_order(fA) != get_order(fB) * get_order(A))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]