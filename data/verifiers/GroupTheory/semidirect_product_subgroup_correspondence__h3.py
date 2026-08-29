import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup
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

def get_attr(obj, name):
    if isinstance(obj, dict):
        return obj[name]
    return getattr(obj, name)

def is_group(elements, op):
    if not elements: return False
    elements_set = set(elements)
    # closure
    for a in elements:
        for b in elements:
            if op(a, b) not in elements_set:
                return False
    # associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if op(op(a, b), c) != op(a, op(b, c)):
                    return False
    # identity
    id_elem = None
    for e in elements:
        if all(op(e, a) == a and op(a, e) == a for a in elements):
            id_elem = e
            break
    if id_elem is None: return False
    # inverses
    for a in elements:
        has_inv = False
        for b in elements:
            if op(a, b) == id_elem and op(b, a) == id_elem:
                has_inv = True
                break
        if not has_inv: return False
    return True

def get_identity(elements, op):
    for e in elements:
        if all(op(e, a) == a and op(a, e) == a for a in elements):
            return e
    return None

def conditions(witness):
    try:
        N = get_attr(witness, 'N')
        H = get_attr(witness, 'H')
        G = get_attr(witness, 'G')
        op_N = get_attr(witness, 'op_N')
        op_H = get_attr(witness, 'op_H')
        op_G = get_attr(witness, 'op_G')
        phi = get_attr(witness, 'phi')
        embed = get_attr(witness, 'embed')
    except Exception:
        return [False, False, False, False]

    # H1: N and H are groups
    try:
        h1 = is_group(N, op_N) and is_group(H, op_H)
    except Exception:
        h1 = False

    # H2: phi: H -> Aut(N) is a group homomorphism
    try:
        def check_h2():
            if not h1: return False
            id_N = get_identity(N, op_N)
            id_H = get_identity(H, op_H)
            if id_N is None or id_H is None: return False
            for h in H:
                mapped = [phi(h, n) for n in N]
                if len(set(mapped)) != len(N): return False
                if any(m not in N for m in mapped): return False
                for n1 in N:
                    for n2 in N:
                        if phi(h, op_N(n1, n2)) != op_N(phi(h, n1), phi(h, n2)):
                            return False
            for h1_elem in H:
                for h2_elem in H:
                    for n in N:
                        if phi(op_H(h1_elem, h2_elem), n) != phi(h1_elem, phi(h2_elem, n)):
                            return False
            return True
        h2 = check_h2()
    except Exception:
        h2 = False

    # H3: N_tilde = N x {1_H} is the base subgroup in G
    try:
        def check_h3():
            if not h1: return False
            if not is_group(G, op_G): return False
            id_H = get_identity(H, op_H)
            if id_H is None: return False
            
            # Check embed is a valid injective homomorphism from N rtimes H to G
            for n1 in N:
                for h1_elem in H:
                    for n2 in N:
                        for h2_elem in H:
                            n3 = op_N(n1, phi(h1_elem, n2))
                            h3_elem = op_H(h1_elem, h2_elem)
                            if op_G(embed(n1, h1_elem), embed(n2, h2_elem)) != embed(n3, h3_elem):
                                return False
            images = [embed(n, h) for n in N for h in H]
            if len(set(images)) != len(N) * len(H): return False
            if any(x not in G for x in images): return False
            return True
        h3 = check_h3()
    except Exception:
        h3 = False

    # neg_Q: The map K |-> N rtimes K is NOT a lattice isomorphism to subgroups of G containing N_tilde
    try:
        def check_neg_Q():
            if not (h1 and h2 and h3): return False
            
            def closure(subset, elements, op):
                s = set(subset)
                added = True
                while added:
                    added = False
                    new_elements = set()
                    for a in s:
                        for b in s:
                            c = op(a, b)
                            if c not in s and c not in new_elements:
                                new_elements.add(c)
                    if new_elements:
                        s.update(new_elements)
                        added = True
                return frozenset(s)

            def get_all_subgroups(elements, op):
                id_elem = get_identity(elements, op)
                base = closure({id_elem}, elements, op)
                all_subgroups = {base}
                changed = True
                while changed:
                    changed = False
                    new_subs = set()
                    for sg in all_subgroups:
                        for g in elements:
                            if g not in sg:
                                new_sg = closure(sg.union({g}), elements, op)
                                if new_sg not in all_subgroups and new_sg not in new_subs:
                                    new_subs.add(new_sg)
                    if new_subs:
                        all_subgroups.update(new_subs)
                        changed = True
                return list(all_subgroups)

            def get_subgroups_containing_fast(G_elements, op_G, N_tilde):
                N_tilde_closure = closure(N_tilde, G_elements, op_G)
                all_subgroups = {N_tilde_closure}
                changed = True
                while changed:
                    changed = False
                    new_subs = set()
                    for sg in all_subgroups:
                        for g in G_elements:
                            if g not in sg:
                                new_sg = closure(sg.union({g}), G_elements, op_G)
                                if new_sg not in all_subgroups and new_sg not in new_subs:
                                    new_subs.add(new_sg)
                    if new_subs:
                        all_subgroups.update(new_subs)
                        changed = True
                return list(all_subgroups)

            subs_H = get_all_subgroups(H, op_H)
            id_H = get_identity(H, op_H)
            N_tilde = [embed(n, id_H) for n in N]
            subs_G = get_subgroups_containing_fast(G, op_G, N_tilde)
            
            mapped_subs = {}
            for K in subs_H:
                S_K = frozenset(embed(n, k) for n in N for k in K)
                if S_K not in subs_G:
                    return True 
                mapped_subs[K] = S_K
                
            if len(set(mapped_subs.values())) != len(subs_G):
                return True
            if len(subs_H) != len(subs_G):
                return True
                
            for K1 in subs_H:
                for K2 in subs_H:
                    is_sub_H = K1.issubset(K2)
                    is_sub_G = mapped_subs[K1].issubset(mapped_subs[K2])
                    if is_sub_H != is_sub_G:
                        return True
                        
            return False
            
        neg_Q = check_neg_Q()
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi: H -> Aut(N) is a group homomorphism",
    "H_3: N_tilde = N x {1_H} is the base subgroup in G",
    "¬Q: The map K |-> N rtimes K is NOT a lattice isomorphism to subgroups of G containing N_tilde"
]

N_HYP = 3
NEG_Q_INDEX = 3