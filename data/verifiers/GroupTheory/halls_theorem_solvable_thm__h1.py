import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
from math import gcd

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
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
    try:
        G, m, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a solvable group
    try:
        h1 = bool(G.is_solvable)
    except Exception:
        h1 = False

    # H_2: Let m and n be positive integers such that the order of G is mn
    try:
        h2 = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0 and G.order() == m * n
    except Exception:
        h2 = False

    # H_3: The greatest common divisor of m and n is 1
    try:
        h3 = gcd(m, n) == 1
    except Exception:
        h3 = False

    # neg_Q: G does not contain a subgroup of order m
    try:
        def has_subgroup_of_order(G, m):
            if m == 1:
                return True
            order_G = G.order()
            if m == order_G:
                return True
            if order_G % m != 0:
                return False
            if order_G > 2000:
                raise ValueError("Group too large to verify safely")
                
            # A finite group always has a subgroup of order p^k if p^k divides its order
            if len(factorint(m)) <= 1:
                return True
                
            elements = list(G.generate())
            # Only elements whose order divides m can be part of a subgroup of order m
            valid_elements = [g for g in elements if m % g.order() == 0 and g.order() > 1]
            
            found_subgroups = set()
            def get_canonical(pg_elements):
                return tuple(sorted([tuple(p.array_form) for p in pg_elements]))
                
            subgroups = []
            for i, g in enumerate(valid_elements):
                pg = PermutationGroup([g])
                if pg.order() == m:
                    return True
                # By Lagrange's theorem, intermediate subgroup orders must divide m
                if m % pg.order() == 0:
                    pg_elements = set(pg.generate())
                    canon = get_canonical(pg_elements)
                    if canon not in found_subgroups:
                        found_subgroups.add(canon)
                        subgroups.append((pg, i, pg_elements))
                        
            current_sgs = subgroups
            while current_sgs:
                next_sgs = []
                for pg, last_idx, pg_elements in current_sgs:
                    # To avoid redundant paths, only add generators that come after the last added one
                    for i in range(last_idx + 1, len(valid_elements)):
                        g = valid_elements[i]
                        if g not in pg_elements:
                            new_pg = PermutationGroup(pg.generators + [g])
                            new_order = new_pg.order()
                            if new_order == m:
                                return True
                            if m % new_order == 0:
                                new_elements = set(new_pg.generate())
                                canon = get_canonical(new_elements)
                                if canon not in found_subgroups:
                                    found_subgroups.add(canon)
                                    next_sgs.append((new_pg, i, new_elements))
                current_sgs = next_sgs
                
            return False

        neg_q = not has_subgroup_of_order(G, m)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a solvable group",
    "H_2: Let m and n be positive integers such that the order of G is mn",
    "H_3: The greatest common divisor of m and n is 1",
    "¬Q: G does not contain a subgroup of order m"
]

N_HYP = 3
NEG_Q_INDEX = 3