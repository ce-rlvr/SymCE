import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.ntheory import factorint

# Top-level setup: named object bindings
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

def is_p_group(G, p):
    order = G.order()
    if order == 1:
        return True
    while order % p == 0:
        order //= p
    return order == 1

def normal_closure_is_p_group(G, x, p):
    closure_gens = [x]
    H = PermutationGroup(closure_gens)
    if not is_p_group(H, p):
        return False
    
    i = 0
    while i < len(closure_gens):
        h = closure_gens[i]
        for g in G.generators:
            conj = ~g * h * g
            if not H.contains(conj):
                closure_gens.append(conj)
                H = PermutationGroup(closure_gens)
                if not is_p_group(H, p):
                    return False
        i += 1
    return True

def O_p(G, p):
    S = G.sylow_subgroup(p)
    op_gens = []
    current_op = PermutationGroup([G.identity])
    for x in S.generate():
        if current_op.contains(x):
            continue
        if normal_closure_is_p_group(G, x, p):
            op_gens.append(x)
            current_op = PermutationGroup(op_gens)
    return current_op

def fitting_subgroup(G):
    order = G.order()
    if order == 1:
        return G
    primes = list(factorint(order).keys())
    fitting_gens = []
    for p in primes:
        op = O_p(G, p)
        for g in op.generators:
            if not g.is_Identity:
                fitting_gens.append(g)
    if not fitting_gens:
        return PermutationGroup([G.identity])
    return PermutationGroup(fitting_gens)

def groups_equal(G1, G2):
    if G1.order() != G2.order():
        return False
    for g in G1.generators:
        if not G2.contains(g):
            return False
    for g in G2.generators:
        if not G1.contains(g):
            return False
    return True

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False]
        G, H = witness
    except Exception:
        return [False]
    
    try:
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            GxH = G * H
            F_GxH = fitting_subgroup(GxH)
            F_G = fitting_subgroup(G)
            F_H = fitting_subgroup(H)
            F_G_x_F_H = F_G * F_H
            
            neg_Q = not groups_equal(F_GxH, F_G_x_F_H)
            return [neg_Q]
        else:
            # Fallback for custom group objects
            GxH = G * H
            F_GxH = GxH.fitting_subgroup()
            F_G = G.fitting_subgroup()
            F_H = H.fitting_subgroup()
            F_G_x_F_H = F_G * F_H
            neg_Q = not (F_GxH == F_G_x_F_H)
            return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: F(G × H) != F(G) × F(H)"
]
N_HYP = 0
NEG_Q_INDEX = 0