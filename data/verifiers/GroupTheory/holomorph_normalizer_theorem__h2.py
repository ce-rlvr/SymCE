import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup
from sympy.combinatorics.named_groups import SymmetricGroup as SymGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

S3 = SymGroup(3)
S4 = SymGroup(4)
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: lambda is the left regular representation",
    "¬Q: The normalizer of lambda(G) in S_G is NOT isomorphic to the holomorph of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, PermutationGroup):
            return [False, False, False]
        h1_ok = True
    except Exception:
        return [False, False, False]

    try:
        elements = list(witness.generate())
        n = len(elements)
        if n == 0:
            return [h1_ok, False, False]
        h2_ok = True
    except Exception:
        return [h1_ok, False, False]

    try:
        if n > 8:
            return [h1_ok, h2_ok, False]
            
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        lambda_gens = []
        for g in witness.generators:
            p_list = [elem_to_idx[g * x] for x in elements]
            lambda_gens.append(Permutation(p_list))
        lambda_G = PermutationGroup(lambda_gens)
        lambda_elements = set(lambda_G.generate())
        
        Sn = SymmetricGroup(n)
        
        norm_elements = []
        for p in Sn.generate():
            is_norm = True
            for h in lambda_gens:
                if (p * h * ~p) not in lambda_elements:
                    is_norm = False
                    break
            if is_norm:
                norm_elements.append(p)
        
        N = PermutationGroup(norm_elements)
        
        automorphisms = []
        for p in Sn.generate():
            id_idx = elem_to_idx[witness.identity]
            if p(id_idx) != id_idx:
                continue
            
            is_hom = True
            for x in elements:
                for y in elements:
                    xy_idx = elem_to_idx[x * y]
                    px_idx = p(elem_to_idx[x])
                    py_idx = p(elem_to_idx[y])
                    if p(xy_idx) != elem_to_idx[elements[px_idx] * elements[py_idx]]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            if is_hom:
                automorphisms.append(p)
        
        if N.order() == n * len(automorphisms):
            neg_q_ok = False
        else:
            neg_q_ok = True

    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]