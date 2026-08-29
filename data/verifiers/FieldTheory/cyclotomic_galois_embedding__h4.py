import math
import sympy
from sympy.ntheory import factorint
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup, AbelianGroup

# Top-level setup
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

QQ = sympy.QQ

def exact_log_p(n, p):
    if n <= 0: return 0
    ans = 0
    while n % p == 0 and n > 1:
        ans += 1
        n //= p
    return ans

def znz_star_structure(n):
    if n <= 0: return []
    if n == 1: return []
    factors = factorint(n)
    groups = []
    for p, k in factors.items():
        if p == 2:
            if k == 1:
                pass
            elif k == 2:
                groups.append(2)
            else:
                groups.append(2)
                groups.append(2**(k-2))
        else:
            groups.append((p**(k-1)) * (p - 1))
    return groups

def p_primary_decomposition(cyclic_orders):
    decomp = {}
    for order in cyclic_orders:
        for p, k in factorint(order).items():
            if p not in decomp:
                decomp[p] = []
            decomp[p].append(k)
    for p in decomp:
        decomp[p].sort(reverse=True)
    return decomp

def embeds(G_orders, H_orders):
    G_decomp = p_primary_decomposition(G_orders)
    H_decomp = p_primary_decomposition(H_orders)
    for p, G_powers in G_decomp.items():
        H_powers = H_decomp.get(p, [])
        if len(G_powers) > len(H_powers):
            return False
        for g_pow, h_pow in zip(G_powers, H_powers):
            if g_pow > h_pow:
                return False
    return True

def get_group_structure(G):
    if isinstance(G, int):
        if G <= 0: raise ValueError("Invalid group order")
        if G == 1: return []
        structure = []
        for p, k in factorint(G).items():
            structure.append(p**k)
        return structure
    
    if not hasattr(G, 'is_abelian'):
        raise ValueError("G must be an int or a PermutationGroup")
        
    if not G.is_abelian:
        return None
    
    try:
        if hasattr(G, 'order') and G.order() > 1000:
            raise ValueError("Group too large")
        orders = [g.order() for g in G.elements]
    except Exception:
        raise ValueError("Cannot compute elements")
        
    group_order = len(orders)
    if group_order == 1:
        return []
    
    primes = factorint(group_order).keys()
    structure = []
    for p in primes:
        max_k = factorint(group_order)[p]
        N = [0] * (max_k + 1)
        for o in orders:
            facts = factorint(o)
            if not facts:
                for k in range(max_k + 1): N[k] += 1
            elif len(facts) == 1 and p in facts:
                pow_p = facts[p]
                for k in range(pow_p, max_k + 1):
                    N[k] += 1
        
        D = []
        for k in range(1, max_k + 1):
            log_Nk = exact_log_p(N[k], p)
            log_Nk_1 = exact_log_p(N[k-1], p)
            D.append(log_Nk - log_Nk_1)
        
        D.append(0)
        for k in range(1, max_k + 1):
            count = D[k-1] - D[k]
            for _ in range(count):
                structure.append(p**k)
                
    return structure

def parse_witness(witness):
    K = None
    n = None
    G = None
    if isinstance(witness, dict):
        if 'q' in witness and 'n' in witness and 'd' in witness:
            K = witness['q']
            n = witness['n']
            G = witness['d']
        else:
            K = witness.get('K', witness.get('char', -1))
            n = witness.get('n', -1)
            G = witness.get('G', None)
    elif isinstance(witness, (list, tuple)) and len(witness) == 3:
        K, n, G = witness
    else:
        return None, None, None

    K_char = None
    if K == 0 or str(K) in ('QQ', 'Q', 'RationalField()', 'Rationals', 'QQ()'):
        K_char = 0
    elif isinstance(K, int) and K > 0:
        facts = factorint(K)
        if len(facts) == 1:
            K_char = list(facts.keys())[0]
        else:
            K_char = -1
    elif str(K).startswith('GF('):
        import re
        m = re.search(r'\d+', str(K))
        if m:
            q = int(m.group(0))
            facts = factorint(q)
            if len(facts) == 1:
                K_char = list(facts.keys())[0]
            else:
                K_char = -1
    else:
        K_char = -1

    if isinstance(G, str):
        mapping = {
            'S3': S3, 'S4': S4, 'A4': A4, 'D4': D4, 'C4': C4, 'V4': V4,
            'Z2': Z2, 'Z3': Z3, 'Z4': Z4, 'Z6': Z6, 'trivial': trivial
        }
        G = mapping.get(G, G)

    return K_char, n, G

def conditions(witness):
    try:
        K_char, n, G = parse_witness(witness)
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = (K_char is not None and K_char >= 0)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False
        
    try:
        if not h1 or not h2:
            h3 = False
        else:
            h3 = (K_char == 0) or (n % K_char != 0)
    except Exception:
        h3 = False
        
    try:
        if not h2 or G is None:
            neg_q = False
        else:
            znz_star = znz_star_structure(n)
            G_struct = get_group_structure(G)
            
            if G_struct is None:
                neg_q = True
            else:
                neg_q = not embeds(G_struct, znz_star)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n is a positive integer",
    "H_3: The characteristic of K does not divide n",
    "¬Q: Gal(L/K) does not embed injectively into (Z/nZ)^x"
]

N_HYP = 3
NEG_Q_INDEX = 3