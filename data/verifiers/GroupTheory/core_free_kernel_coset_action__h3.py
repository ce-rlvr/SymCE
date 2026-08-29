import math
import itertools
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
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

def get_K_elements(G, H):
    G_elements = list(G.generate())
    H_elements = set(H.generate())
    
    K_elements = set(G_elements)
    for g in G_elements:
        g_inv = ~g
        conj_H = set(g * h * g_inv for h in H_elements)
        K_elements = K_elements.intersection(conj_H)
    return K_elements

def check_embeddable(G, K_elements, n):
    G_elements = list(G.generate())
    order_quotient = len(G_elements) // len(K_elements)
    
    if n >= order_quotient:
        return True
        
    if n < 1:
        return False
        
    if math.factorial(n) < order_quotient:
        return False
        
    if n > 7:
        raise ValueError("n is too large for fast verification")
        
    Sn = SymmetricGroup(n)
    Sn_elements = list(Sn.generate())
    
    def get_order(perm):
        return perm.order()
        
    Sn_orders = {s: get_order(s) for s in Sn_elements}
    
    G_gens = G.generators
    if not G_gens:
        return True
        
    valid_targets = []
    for g in G_gens:
        g_ord = get_order(g)
        targets = [s for s in Sn_elements if g_ord % Sn_orders[s] == 0]
        valid_targets.append(targets)
        
    G_id = G_gens[0] ** get_order(G_gens[0])
    Sn_id = Sn.generators[0] ** get_order(Sn.generators[0]) if Sn.generators else list(Sn.generate())[0]
    
    for target_gens in itertools.product(*valid_targets):
        gen_mapping = dict(zip(G_gens, target_gens))
        
        mapping = {G_id: Sn_id}
        queue = [G_id]
        valid = True
        
        while queue and valid:
            curr = queue.pop(0)
            for g in G_gens:
                nxt = curr * g
                nxt_val = mapping[curr] * gen_mapping[g]
                if nxt in mapping:
                    if mapping[nxt] != nxt_val:
                        valid = False
                        break
                else:
                    mapping[nxt] = nxt_val
                    queue.append(nxt)
                    
        if valid:
            kernel = {g for g, val in mapping.items() if val == Sn_id}
            if kernel == set(K_elements):
                return True
                
    return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, H, n = witness
        if float(n) != int(n):
            return [False, False, False, False]
        n = int(n)
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H3: G acts on the set of left cosets G/H by left multiplication
    try:
        h3 = h1 and h2
    except Exception:
        h3 = False

    # neg_Q: The conclusion fails
    try:
        if not (h1 and h2):
            neg_Q = False
        else:
            K_elements = get_K_elements(G, H)
            embeddable = check_embeddable(G, K_elements, n)
            neg_Q = not embeddable
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: G acts on the set of left cosets G/H by left multiplication",
    "¬Q: G/K is not isomorphic to a subgroup of S_n"
]

N_HYP = 3
NEG_Q_INDEX = 3