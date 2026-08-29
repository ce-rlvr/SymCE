import itertools
import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: W_1 and W_2 are subspaces of V",
    "H_2: Stab_G(W_1) and Stab_G(W_2) denote their respective setwise stabilizers in G",
    "¬Q: The intersection Stab_G(W_1) ∩ Stab_G(W_2) is not a subgroup of Stab_G(W_1 + W_2)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        V = witness['V']
        add = witness['add']
        zero = witness['zero']
        W1 = witness['W1']
        W2 = witness['W2']
        G = witness['G']
        
        def do_add(a, b):
            if isinstance(add, dict):
                return add.get((a, b))
            return add(a, b)
    except Exception:
        return [False, False, False]

    # H_1: W_1 and W_2 are subspaces of V
    try:
        h1_ok = True
        if zero not in V:
            h1_ok = False
            
        if h1_ok:
            # Check V is an abelian group
            for x in V:
                if do_add(x, zero) != x: h1_ok = False
                if do_add(zero, x) != x: h1_ok = False
                for y in V:
                    xy = do_add(x, y)
                    if xy not in V: h1_ok = False
                    if xy != do_add(y, x): h1_ok = False
                    for z in V:
                        if do_add(xy, z) != do_add(x, do_add(y, z)): h1_ok = False

        if h1_ok:
            # Find the characteristic of V to ensure it's an elementary abelian p-group (vector space over F_p)
            char_p = None
            for p in [2, 3, 5, 7, 11]:
                all_zero = True
                for x in V:
                    curr = zero
                    for _ in range(p):
                        curr = do_add(curr, x)
                    if curr != zero:
                        all_zero = False
                        break
                if all_zero:
                    char_p = p
                    break
            if char_p is None:
                h1_ok = False

        if h1_ok:
            # Check W1 and W2 are subspaces (subgroups of V)
            for W in [W1, W2]:
                if zero not in W: h1_ok = False
                for w in W:
                    if w not in V: h1_ok = False
                for w1 in W:
                    for w2 in W:
                        if do_add(w1, w2) not in W: h1_ok = False
                # check inverses
                for w in W:
                    inv_found = False
                    for v in W:
                        if do_add(w, v) == zero:
                            inv_found = True
                            break
                    if not inv_found: h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: Stab_G(W_1) and Stab_G(W_2) denote their respective setwise stabilizers in G
    try:
        h2_ok = True
        if not G:
            h2_ok = False
        else:
            for g in G:
                if not isinstance(g, dict):
                    h2_ok = False
                    break
                if set(g.keys()) != set(V): h2_ok = False
                if set(g.values()) != set(V): h2_ok = False
            
            if h2_ok:
                has_id = False
                for g in G:
                    if all(g[x] == x for x in V):
                        has_id = True
                        break
                if not has_id: h2_ok = False
                
                for g1 in G:
                    for g2 in G:
                        comp = {x: g1[g2[x]] for x in V}
                        if comp not in G: h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The intersection Stab_G(W_1) ∩ Stab_G(W_2) is not a subgroup of Stab_G(W_1 + W_2)
    try:
        W1_plus_W2 = set()
        for w1 in W1:
            for w2 in W2:
                W1_plus_W2.add(do_add(w1, w2))
                
        neg_q = False
        for g in G:
            stab_w1 = set(g[w] for w in W1) == set(W1)
            stab_w2 = set(g[w] for w in W2) == set(W2)
            stab_sum = set(g[w] for w in W1_plus_W2) == set(W1_plus_W2)
            
            if stab_w1 and stab_w2 and not stab_sum:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]