import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if len(witness) == 2:
            G, p = witness
            q = p
        elif len(witness) == 3:
            G, p, q = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False

    # neg_Q: The number of p-regular conjugacy classes in G is NOT equal to the number of isomorphism classes of simple kG-modules.
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            classes = G.conjugacy_classes()
            class_sets = [set(c) for c in classes]
            reps = [list(c)[0] for c in classes]
            
            p_reg_count = 0
            for rep in reps:
                if math.gcd(int(rep.order()), int(p)) == 1:
                    p_reg_count += 1
            
            if q == 0:
                visited = set()
                simple_mod_count = 0
                for i, rep in enumerate(reps):
                    if i in visited:
                        continue
                    simple_mod_count += 1
                    ord_r = int(rep.order())
                    for j in range(1, ord_r):
                        if math.gcd(j, ord_r) == 1:
                            rep_j = rep**j
                            for k, c_set in enumerate(class_sets):
                                if rep_j in c_set:
                                    visited.add(k)
                                    break
                neg_q = (p_reg_count != simple_mod_count)
            else:
                factors = sympy.factorint(q)
                if len(factors) != 1:
                    neg_q = False
                else:
                    e = list(factors.keys())[0]
                    
                    e_reg_indices = []
                    for i, rep in enumerate(reps):
                        if math.gcd(int(rep.order()), int(e)) == 1:
                            e_reg_indices.append(i)
                            
                    visited = set()
                    simple_mod_count = 0
                    q_int = int(q)
                    for i in e_reg_indices:
                        if i in visited:
                            continue
                        simple_mod_count += 1
                        curr = reps[i]
                        visited.add(i)
                        max_iter = int(curr.order()) + 1
                        for _ in range(max_iter):
                            curr = curr**q_int
                            found_idx = -1
                            for k in e_reg_indices:
                                if curr in class_sets[k]:
                                    found_idx = k
                                    break
                            if found_idx != -1:
                                visited.add(found_idx)
                            else:
                                break
                    
                    neg_q = (p_reg_count != simple_mod_count)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "¬Q: The number of p-regular conjugacy classes in G is not equal to the number of isomorphism classes of simple kG-modules"
]

N_HYP = 2
NEG_Q_INDEX = 2