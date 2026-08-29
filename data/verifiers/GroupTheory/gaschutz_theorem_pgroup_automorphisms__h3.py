import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
from itertools import product

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
    "H_1: G is a finite group",
    "H_2: G is a p-group for some prime p",
    "¬Q: G does not have an automorphism of order p that is not an inner automorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # H1: G is a finite group
    try:
        if not isinstance(witness, PermutationGroup):
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # H2: G is a p-group for some prime p
    p = None
    try:
        if h1:
            order_G = witness.order()
            factors = factorint(order_G)
            if len(factors) == 1:
                p = list(factors.keys())[0]
                h2 = True
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: G does not have an automorphism of order p that is not an inner automorphism
    neg_q = False
    try:
        if h1 and h2:
            elements = list(witness.generate())
            n = len(elements)
            gens = witness.generators
            id_elem = next(e for e in elements if e.order() == 1)
            
            elem_to_idx = {e: i for i, e in enumerate(elements)}
            
            inner_automorphisms = set()
            for g in elements:
                g_inv = g**-1
                img_tuple = tuple(g * x * g_inv for x in elements)
                inner_automorphisms.add(img_tuple)
                
            has_outer_order_p = False
            
            gen_orders = [g.order() for g in gens]
            valid_targets = [[e for e in elements if e.order() == go] for go in gen_orders]
            
            for target_gens in product(*valid_targets):
                mapping = {id_elem: id_elem}
                valid = True
                for g, tg in zip(gens, target_gens):
                    if g in mapping:
                        if mapping[g] != tg:
                            valid = False
                            break
                    else:
                        mapping[g] = tg
                if not valid:
                    continue
                    
                closure = list(mapping.keys())
                idx = 0
                while idx < len(closure):
                    x = closure[idx]
                    idx += 1
                    for g in gens:
                        y = x * g
                        ty = mapping[x] * mapping[g]
                        if y not in mapping:
                            mapping[y] = ty
                            closure.append(y)
                        else:
                            if mapping[y] != ty:
                                valid = False
                                break
                    if not valid:
                        break
                        
                if valid and len(mapping) == n:
                    if len(set(mapping.values())) == n:
                        aut_tuple = tuple(mapping[e] for e in elements)
                        perm = [elem_to_idx[img] for img in aut_tuple]
                        order = Permutation(perm).order()
                        if order == p:
                            if aut_tuple not in inner_automorphisms:
                                has_outer_order_p = True
                                break
            
            neg_q = not has_outer_order_p
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]