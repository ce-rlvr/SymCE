import math
from sympy.ntheory import factorint
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.polys.domains import QQ, ZZ, RR, CC, GF

# Standard group bindings for the witness namespace
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n is a positive integer",
    "H_3: The characteristic of K does not divide n",
    "¬Q: The Galois group Gal(L/K) is NOT isomorphic to a subgroup of (Z/nZ)^x"
]
N_HYP = 3
NEG_Q_INDEX = 3

def znz_star_structure(n):
    """Returns a list of cyclic group orders whose direct product is isomorphic to (Z/nZ)^x."""
    if n <= 0: return []
    if n == 1: return [1]
    factors = factorint(n)
    structure = []
    for p, k in factors.items():
        if p == 2:
            if k == 1:
                pass
            elif k == 2:
                structure.append(2)
            else:
                structure.append(2)
                structure.append(2**(k-2))
        else:
            structure.append((p**(k-1)) * (p - 1))
    return structure

def p_group_decomposition(cyclic_orders):
    """Decomposes a list of cyclic group orders into their p-group partitions."""
    decomp = {}
    for order in cyclic_orders:
        for p, k in factorint(order).items():
            if p not in decomp:
                decomp[p] = []
            decomp[p].append(k)
    for p in decomp:
        decomp[p].sort(reverse=True)
    return decomp

def get_p_structure_from_orders(orders):
    """Deduces the p-group partitions of a finite abelian group given the orders of all its elements."""
    total_elements = len(orders)
    if total_elements <= 1:
        return {}
    
    group_order_factors = factorint(total_elements)
    structure = {}
    
    for p in group_order_factors:
        p_parts = []
        for o in orders:
            k = 0
            while o % p == 0:
                k += 1
                o //= p
            p_parts.append(k)
            
        p_prime_order = total_elements // (p ** group_order_factors[p])
        
        C = {}
        max_k = max(p_parts)
        for k in range(max_k + 1):
            count = sum(1 for x in p_parts if x <= k)
            C[k] = count // p_prime_order
            
        S = {}
        for k in range(max_k + 1):
            S[k] = round(math.log(C[k], p))
            
        b = []
        for k in range(1, max_k + 1):
            num_parts_ge_k = S[k] - S.get(k-1, 0)
            num_parts_ge_k_plus_1 = S.get(k+1, S[max_k]) - S[k]
            num_parts_eq_k = num_parts_ge_k - num_parts_ge_k_plus_1
            for _ in range(num_parts_eq_k):
                b.append(k)
        
        b.sort(reverse=True)
        structure[p] = b
        
    return structure

def conditions(witness):
    try:
        if isinstance(witness, dict):
            K = witness.get('K')
            n = witness.get('n')
            G = witness.get('G')
        elif isinstance(witness, (list, tuple)) and len(witness) >= 3:
            K = witness[0]
            n = witness[1]
            G = witness[2]
        else:
            K = getattr(witness, 'K', None)
            n = getattr(witness, 'n', None)
            G = getattr(witness, 'G', None)
    except Exception:
        return [False, False, False, False]

    # H_1: K is a field
    try:
        if K in [QQ, RR, CC]:
            h1 = True
        elif hasattr(K, 'is_Field'):
            h1 = bool(K.is_Field)
        elif hasattr(K, 'is_field'):
            h1 = bool(K.is_field)
        elif isinstance(K, str):
            h1 = K in ['Q', 'R', 'C', 'QQ', 'RR', 'CC'] or K.startswith('GF') or (K.startswith('F') and len(K)>1 and K[1].isdigit())
        elif K.__class__.__name__ == 'FiniteField':
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        n_val = int(n)
        h2 = (n_val == n) and (n_val > 0)
    except Exception:
        h2 = False
        n_val = 1

    # H_3: The characteristic of K does not divide n
    try:
        if hasattr(K, 'characteristic'):
            char_K = int(K.characteristic() if callable(K.characteristic) else K.characteristic)
        elif hasattr(K, 'char'):
            char_K = int(K.char() if callable(K.char) else K.char)
        elif isinstance(K, str):
            if K in ['Q', 'R', 'C', 'QQ', 'RR', 'CC']:
                char_K = 0
            elif K.startswith('GF') or (K.startswith('F') and len(K)>1 and K[1].isdigit()):
                import re
                m = re.search(r'\d+', K)
                char_K = int(m.group()) if m else 0
            else:
                char_K = 0
        else:
            char_K = 0
            
        if char_K == 0:
            h3 = True
        else:
            h3 = (n_val % char_K != 0)
    except Exception:
        h3 = False

    # neg_Q: G is NOT isomorphic to a subgroup of (Z/nZ)^x
    try:
        if G is None:
            neg_Q = False
        else:
            if isinstance(G, list) and all(isinstance(x, int) for x in G):
                G_p_decomp = p_group_decomposition(G)
                is_abelian = True
            elif hasattr(G, 'is_abelian'):
                is_abelian = G.is_abelian
                if is_abelian:
                    order = G.order() if callable(G.order) else G.order
                    if order > 10000:
                        raise ValueError("Group too large")
                    orders = [g.order() if callable(g.order) else g.order for g in G.elements]
                    G_p_decomp = get_p_structure_from_orders(orders)
            else:
                raise ValueError("Unknown group format")

            if not is_abelian:
                neg_Q = True
            else:
                znz_structure = znz_star_structure(n_val)
                znz_p_decomp = p_group_decomposition(znz_structure)
                
                is_subgroup = True
                for p, G_parts in G_p_decomp.items():
                    if not G_parts:
                        continue
                    H_parts = znz_p_decomp.get(p, [])
                    if len(G_parts) > len(H_parts):
                        is_subgroup = False
                        break
                    for g_val, h_val in zip(G_parts, H_parts):
                        if g_val > h_val:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                        
                neg_Q = not is_subgroup
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]