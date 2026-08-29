import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy import QQ
from sympy.ntheory import factorint

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def min_deg_cyclic_QQ(k):
    if k == 1: return 0
    if k == 2: return 1
    factors = factorint(k)
    deg = 0
    for p, a in factors.items():
        if p == 2 and a == 1:
            continue
        elif p == 2:
            deg += 2**(a-1)
        else:
            deg += p**(a-1) * (p - 1)
    return deg

def get_invariant_factors(group):
    order = group.order()
    if order == 1:
        return []
    
    elements = list(group.elements)
    factors = factorint(order)
    p_powers = {}
    
    for p in factors:
        p_elements = [g for g in elements if g.order() > 0 and factorint(g.order()).keys() <= {p}]
        
        k = 1
        counts = []
        while True:
            count = sum(1 for g in p_elements if (p**k) % g.order() == 0)
            counts.append(count)
            if count == len(p_elements):
                break
            k += 1
            
        S = [0]
        for c in counts:
            val = c
            pw = 0
            while val > 1:
                val //= p
                pw += 1
            S.append(pw)
            
        diff = [S[i] - S[i-1] for i in range(1, len(S))]
        diff.append(0)
        
        powers = []
        for i in range(len(diff)-1):
            num_factors = diff[i] - diff[i+1]
            for _ in range(num_factors):
                powers.append(p**(i+1))
        p_powers[p] = sorted(powers)
        
    invariants = []
    while any(p_powers.values()):
        d = 1
        for p in p_powers:
            if p_powers[p]:
                d *= p_powers[p].pop()
        invariants.append(d)
        
    invariants.reverse()
    return invariants

def min_deg_abelian_QQ(group):
    if group.order() == 1:
        return 0
    invs = get_invariant_factors(group)
    return sum(min_deg_cyclic_QQ(d) for d in invs)

def embeds_in_GL(group, n, F):
    if group.order() == 1:
        return n >= 0
        
    if F == QQ:
        if group.is_abelian:
            return min_deg_abelian_QQ(group) <= n
        else:
            try:
                if group.is_isomorphic(SymmetricGroup(3)):
                    return n >= 2
                if group.is_isomorphic(SymmetricGroup(4)):
                    return n >= 3
                if group.is_isomorphic(AlternatingGroup(4)):
                    return n >= 3
                if group.is_isomorphic(DihedralGroup(4)):
                    return n >= 2
            except Exception:
                pass
            return None
    return None

def direct_product(G, H):
    if G.order() == 1 and H.order() == 1:
        return PermutationGroup([Permutation(0)])
    if G.order() == 1:
        return H
    if H.order() == 1:
        return G
    
    degG = G.degree
    degH = H.degree
    gens = []
    for g in G.generators:
        arr = [g(i) for i in range(degG)]
        gens.append(Permutation(arr + list(range(degG, degG + degH))))
    for h in H.generators:
        arr = [h(i) for i in range(degH)]
        gens.append(Permutation(list(range(degG)) + [x + degG for x in arr]))
    return PermutationGroup(gens)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            G = witness.get('G')
            n = witness.get('n')
            H = witness.get('H')
            m = witness.get('m')
        else:
            F, G, n, H, m = witness
    except Exception:
        return [False, False, False]

    # H1: F is a field
    try:
        h1 = (F == QQ) or getattr(F, 'is_Field', False)
        if not h1:
            try:
                from sympy.polys.domains import Field
                h1 = isinstance(F, Field)
            except Exception:
                pass
    except Exception:
        h1 = False

    # H2: G is a group isomorphic to a subgroup of GL_n(F)
    try:
        if not hasattr(G, 'order') or not hasattr(H, 'order'):
            h2 = False
        else:
            ans2 = embeds_in_GL(G, n, F)
            h2 = (ans2 is True)
    except Exception:
        h2 = False

    # neg_Q: G x H is NOT isomorphic to a subgroup of GL_{n+m}(F)
    try:
        if not hasattr(G, 'order') or not hasattr(H, 'order'):
            neg_q = False
        else:
            G_x_H = direct_product(G, H)
            ans_neg_q = embeds_in_GL(G_x_H, n + m, F)
            if ans_neg_q is False:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: G is a group isomorphic to a subgroup of GL_n(F)",
    "¬Q: G x H is not isomorphic to a subgroup of GL_{n+m}(F)"
]
N_HYP = 2
NEG_Q_INDEX = 2