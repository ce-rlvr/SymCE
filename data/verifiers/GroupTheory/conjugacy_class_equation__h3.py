import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
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
    "H_2: Z(G) is the center of G",
    "¬Q: |G| != |Z(G)| + sum of index of C_G(a) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, A = witness
                Z = None
            elif len(witness) == 3:
                G, Z, A = witness
            else:
                return [False, False, False]
            A = list(A)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = hasattr(G, 'order') and hasattr(G, 'generate') and G.order() > 0
    except Exception:
        h1_ok = False

    # H_2: Z(G) is the center of G
    try:
        if not h1_ok:
            h2_ok = False
        else:
            elements = list(G.generate())
            actual_center = [g for g in elements if all(g * x == x * g for x in elements)]
            if Z is not None:
                if hasattr(Z, 'generate'):
                    Z_elements = list(Z.generate())
                else:
                    Z_elements = list(Z)
                
                def is_in(elem, lst):
                    for e in lst:
                        if e == elem:
                            return True
                        if hasattr(e, 'size') and hasattr(elem, 'size'):
                            max_deg = max(e.size, elem.size)
                            if all(e(i) == elem(i) for i in range(max_deg)):
                                return True
                    return False
                
                h2_ok = all(is_in(z, actual_center) for z in Z_elements) and \
                        all(is_in(c, Z_elements) for c in actual_center)
            else:
                h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: |G| != |Z(G)| + sum of index of C_G(a) in G
    try:
        if not h1_ok:
            neg_Q_ok = False
        else:
            G_order = G.order()
            elements = list(G.generate())
            Z_order = sum(1 for g in elements if all(g * x == x * g for x in elements))
            
            sum_indices = 0
            neg_Q_ok = False
            for a in A:
                matched_a = None
                for g in elements:
                    if g == a:
                        matched_a = g
                        break
                    if hasattr(a, 'size') and hasattr(g, 'size'):
                        max_deg = max(a.size, g.size)
                        if all(a(i) == g(i) for i in range(max_deg)):
                            matched_a = g
                            break
                if matched_a is None:
                    neg_Q_ok = False
                    break
                
                a = matched_a
                c_order = sum(1 for g in elements if g * a == a * g)
                sum_indices += G_order // c_order
            else:
                neg_Q_ok = (G_order != Z_order + sum_indices)
    except Exception:
        neg_Q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_Q_ok)]