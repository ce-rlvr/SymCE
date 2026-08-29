import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    # H_1: G is a finite cyclic group of order n
    try:
        if not hasattr(witness, 'elements'):
            h1 = False
        else:
            elements = list(witness.elements)
            n = len(elements)
            if n < 1:
                h1 = False
            else:
                h1 = any(g.order() == n for g in elements)
    except Exception:
        h1 = False

    # H_2: rad(n) is the radical of n, defined as the product of all distinct prime factors of n
    # This is a definitional hypothesis that holds as long as n is a valid positive integer.
    try:
        if hasattr(witness, 'elements'):
            n = len(list(witness.elements))
            h2 = (n >= 1)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: \Phi(G) is not the unique subgroup of G of order n/rad(n)
    try:
        if not hasattr(witness, 'elements'):
            neg_q = False
        else:
            elements = list(witness.elements)
            n = len(elements)
            if n < 1:
                neg_q = False
            else:
                factors = factorint(n)
                rad_n = 1
                for p in factors:
                    rad_n *= p
                target_order = n // rad_n
                
                # Compute all subgroups
                subgroups = set()
                for g in elements:
                    sg = set()
                    curr = g
                    while curr not in sg:
                        sg.add(curr)
                        curr = curr * g
                    subgroups.add(frozenset(sg))
                    
                queue = list(subgroups)
                while queue:
                    H1 = queue.pop(0)
                    for H2_sg in list(subgroups):
                        if not H1.issubset(H2_sg) and not H2_sg.issubset(H1):
                            cl = set(H1 | H2_sg)
                            added = True
                            while added:
                                added = False
                                new_els = set()
                                for x in cl:
                                    for y in cl:
                                        xy = x * y
                                        if xy not in cl and xy not in new_els:
                                            new_els.add(xy)
                                if new_els:
                                    cl.update(new_els)
                                    added = True
                            cl_frozen = frozenset(cl)
                            if cl_frozen not in subgroups:
                                subgroups.add(cl_frozen)
                                queue.append(cl_frozen)
                                
                G_set = frozenset(elements)
                proper_subgroups = [H for H in subgroups if H != G_set]
                
                # Find maximal subgroups
                if not proper_subgroups:
                    frattini = G_set
                else:
                    maximal_subgroups = []
                    for H in proper_subgroups:
                        is_maximal = True
                        for K in proper_subgroups:
                            if H != K and H.issubset(K):
                                is_maximal = False
                                break
                        if is_maximal:
                            maximal_subgroups.append(H)
                    
                    if not maximal_subgroups:
                        frattini = G_set
                    else:
                        frattini_set = set(maximal_subgroups[0])
                        for M in maximal_subgroups[1:]:
                            frattini_set = frattini_set.intersection(M)
                        frattini = frozenset(frattini_set)
                        
                subgroups_of_target_order = [H for H in subgroups if len(H) == target_order]
                
                if len(subgroups_of_target_order) != 1:
                    neg_q = True
                else:
                    if subgroups_of_target_order[0] != frattini:
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group of order n",
    "H_2: rad(n) is the radical of n, defined as the product of all distinct prime factors of n",
    "¬Q: \Phi(G) is not the unique subgroup of G of order n/rad(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2