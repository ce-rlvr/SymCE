import sympy as sp
import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is the semidirect product of a normal subgroup N and a subgroup H",
    "H_2: N has finite exponent e_N",
    "¬Q: The exponent of G is not finite or does not divide e_N * e_H"
]

N_HYP = 2
NEG_Q_INDEX = 2

def compute_lcm(orders):
    if not orders:
        return 1
    res = orders[0]
    for o in orders[1:]:
        res = (res * o) // math.gcd(res, o)
    return res

def matrix_order(M, max_order=1000):
    M = sp.ImmutableMatrix(M)
    I = sp.ImmutableMatrix(sp.eye(M.shape[0]))
    if M == I:
        return 1
    curr = M
    for i in range(2, max_order + 1):
        curr = curr * M
        if curr == I:
            return i
    return float('inf')

def generate_group(gens, max_size=1000):
    if not gens:
        return set(), True
    gens = [sp.ImmutableMatrix(g) for g in gens]
    I = sp.ImmutableMatrix(sp.eye(gens[0].shape[0]))
    elements = {I}
    queue = [I]
    while queue:
        curr = queue.pop(0)
        for g in gens:
            nxt = curr * g
            if nxt not in elements:
                if len(elements) >= max_size:
                    return elements, False
                elements.add(nxt)
                queue.append(nxt)
    return elements, True

def conditions(witness):
    # 1. Try SymPy PermutationGroup tuple: (G, N, H)
    try:
        if isinstance(witness, tuple) and len(witness) == 3 and hasattr(witness[0], 'is_subgroup'):
            G, N, H = witness
            h1 = False
            if N.is_subgroup(G) and H.is_subgroup(G) and N.is_normal(G):
                intersect = set(N.elements).intersection(set(H.elements))
                if len(intersect) == 1 and N.order() * H.order() == G.order():
                    h1 = True
            e_N = compute_lcm([g.order() for g in N.elements])
            h2 = (e_N > 0)
            e_G = compute_lcm([g.order() for g in G.elements])
            e_H = compute_lcm([g.order() for g in H.elements])
            neg_q = ((e_N * e_H) % e_G != 0)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try Matrix generators tuple: (N_gens, H_gens)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            N_gens, H_gens = witness
            if isinstance(N_gens, list) and isinstance(H_gens, list):
                if len(N_gens) > 0 and hasattr(sp.ImmutableMatrix(N_gens[0]), 'inv'):
                    N_gens = [sp.ImmutableMatrix(g) for g in N_gens]
                    H_gens = [sp.ImmutableMatrix(g) for g in H_gens]
                    I = sp.ImmutableMatrix(sp.eye(N_gens[0].shape[0]))
                    
                    N_elements, N_finite = generate_group(N_gens, max_size=200)
                    if not N_finite:
                        h2 = False
                        e_N = float('inf')
                    else:
                        orders = [matrix_order(n) for n in N_elements]
                        if float('inf') in orders:
                            h2 = False
                            e_N = float('inf')
                        else:
                            e_N = compute_lcm(orders)
                            h2 = True
                            
                    h1_normal = True
                    if N_finite:
                        for h in H_gens:
                            try:
                                h_inv = h.inv()
                            except Exception:
                                h1_normal = False
                                break
                            for n in N_elements:
                                if h * n * h_inv not in N_elements:
                                    h1_normal = False
                                    break
                                if h_inv * n * h not in N_elements:
                                    h1_normal = False
                                    break
                            if not h1_normal:
                                break
                    else:
                        h1_normal = False
                        
                    h1_intersect = True
                    if N_finite:
                        H_elements, _ = generate_group(H_gens, max_size=100)
                        intersect = N_elements.intersection(H_elements)
                        if len(intersect) > 1:
                            h1_intersect = False
                            
                    h1 = h1_normal and h1_intersect
                    
                    e_H = 1
                    for h in H_gens:
                        o = matrix_order(h)
                        if o == float('inf'):
                            e_H = float('inf')
                            break
                        else:
                            e_H = compute_lcm([e_H, o])
                            
                    if e_H == float('inf'):
                        neg_q = True
                    else:
                        G_gens = N_gens + H_gens
                        G_elements, G_finite = generate_group(G_gens, max_size=1000)
                        if not G_finite or e_N == float('inf'):
                            neg_q = True
                        else:
                            e_G = compute_lcm([matrix_order(g) for g in G_elements])
                            neg_q = ((e_N * e_H) % e_G != 0)
                            
                    return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try custom object with properties
    try:
        h1 = bool(witness.is_semidirect_product)
    except Exception:
        h1 = False

    try:
        e_N = witness.e_N
        h2 = isinstance(e_N, int) and e_N > 0
    except Exception:
        h2 = False

    try:
        e_G = witness.e_G
        e_H = witness.e_H
        e_N = witness.e_N
        
        if e_G == float('inf') or e_G == 0 or e_G is None:
            neg_q = True
        elif e_H == float('inf') or e_H == 0 or e_H is None:
            neg_q = True
        else:
            neg_q = ((e_N * e_H) % e_G != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]