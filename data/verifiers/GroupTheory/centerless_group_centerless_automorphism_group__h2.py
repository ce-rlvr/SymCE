import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from itertools import permutations, product

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # Generate all elements and sort deterministically
            elements = sorted(list(witness.generate()), key=lambda p: p.array_form)
            n = len(elements)
            
            # Restrict to small groups to ensure fast execution
            if n > 10:
                neg_q = False
            else:
                id_idx = -1
                for i, el in enumerate(elements):
                    if el.order() == 1:
                        id_idx = i
                        break
                
                # Precompute multiplication table and orders
                mult = [[0] * n for _ in range(n)]
                orders = [0] * n
                for i in range(n):
                    orders[i] = elements[i].order()
                    for j in range(n):
                        prod = elements[i] * elements[j]
                        mult[i][j] = elements.index(prod)
                        
                # Group non-identity elements by their order
                by_order = {}
                for i in range(n):
                    if i != id_idx:
                        o = orders[i]
                        if o not in by_order:
                            by_order[o] = []
                        by_order[o].append(i)
                        
                # Generate all possible permutations that preserve element orders
                order_perms = []
                for o, indices in by_order.items():
                    order_perms.append([list(zip(indices, p)) for p in permutations(indices)])
                    
                # Find all automorphisms
                auts = []
                for perm_combo in product(*order_perms):
                    p = [0] * n
                    p[id_idx] = id_idx
                    for mapping in perm_combo:
                        for orig, new in mapping:
                            p[orig] = new
                            
                    is_aut = True
                    for i in range(n):
                        for j in range(n):
                            if p[mult[i][j]] != mult[p[i]][p[j]]:
                                is_aut = False
                                break
                        if not is_aut:
                            break
                    if is_aut:
                        auts.append(p)
                        
                # Find the center of the automorphism group
                center = []
                for p in auts:
                    is_central = True
                    for q in auts:
                        # Check if p and q commute: p(q(x)) == q(p(x)) for all x
                        for i in range(n):
                            if p[q[i]] != q[p[i]]:
                                is_central = False
                                break
                        if not is_central:
                            break
                    if is_central:
                        center.append(p)
                        
                # The negated conclusion is True if the center is not trivial (size > 1)
                neg_q = len(center) > 1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The center of the automorphism group of G is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1