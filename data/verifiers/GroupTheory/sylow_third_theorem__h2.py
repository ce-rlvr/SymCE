import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def highest_power_dividing(n, p):
    p = int(p)
    n = int(n)
    if p <= 1:
        return 1
    power = 1
    while n % (power * p) == 0:
        power *= p
    return power

def close_subgroup(gens, identity):
    sg = {identity}
    queue = [identity]
    while queue:
        x = queue.pop(0)
        for gen in gens:
            y = x * gen
            if y not in sg:
                sg.add(y)
                queue.append(y)
    return frozenset(sg)

def get_all_subgroups(G):
    elements = list(G.generate())
    # The identity is the unique element e such that e * e == e
    identity = next(e for e in elements if e * e == e)
    subgroups = {frozenset([identity]): []}
    
    queue = [frozenset([identity])]
    while queue:
        sg = queue.pop(0)
        gens_of_sg = subgroups[sg]
        for g in elements:
            if g not in sg:
                new_gens = gens_of_sg + [g]
                new_sg = close_subgroup(new_gens, identity)
                if new_sg not in subgroups:
                    subgroups[new_sg] = new_gens
                    queue.append(new_sg)
    return subgroups.keys()

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, p, n_p = witness
            elif len(witness) == 2:
                G, p = witness
                n_p = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        order_G = int(G.order())
        h1_ok = order_G > 0
    except Exception:
        h1_ok = False

    # H2: p divides the order of G
    try:
        p_int = int(p)
        h2_ok = h1_ok and (order_G % p_int == 0)
    except Exception:
        h2_ok = False

    # H3: n_p is the number of Sylow p-subgroups of G
    try:
        if h1_ok and h2_ok:
            pk = highest_power_dividing(order_G, p_int)
            all_subgroups = get_all_subgroups(G)
            expected_n_p = sum(1 for sg in all_subgroups if len(sg) == pk)
            if n_p is None:
                n_p = expected_n_p
                h3_ok = True
            else:
                h3_ok = (int(n_p) == expected_n_p)
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # neg_Q: n_p does NOT divide the order of G OR n_p != 1 mod p
    try:
        if n_p is not None:
            n_p_int = int(n_p)
            if n_p_int == 0:
                divides = False
            else:
                divides = (order_G % n_p_int == 0)
            mod_1 = (n_p_int % p_int == 1)
            q_ok = divides and mod_1
            neg_q = not q_ok
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p divides the order of G",
    "H_3: n_p is the number of Sylow p-subgroups of G",
    "¬Q: n_p does not divide the order of G or n_p ≢ 1 (mod p)"
]

N_HYP = 3
NEG_Q_INDEX = 3