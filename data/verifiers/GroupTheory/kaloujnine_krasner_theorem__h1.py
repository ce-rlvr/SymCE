import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_normal_subgroup(G, N):
    N_elems = set(N.generate())
    G_elems = set(G.generate())
    if not N_elems.issubset(G_elems):
        return False
    for n in N.generators:
        for g in G.generators:
            if g * n * (~g) not in N_elems:
                return False
    return True

def get_quotient_group(G, N):
    N_elems = set(N.generate())
    reps = []
    seen = set()
    for g in G.generate():
        if g not in seen:
            reps.append(g)
            for n in N_elems:
                seen.add(g * n)
                
    perms = []
    for gen in G.generators:
        p = []
        for rep in reps:
            target = gen * rep
            for i, r in enumerate(reps):
                if (~r * target) in N_elems:
                    p.append(i)
                    break
        perms.append(Permutation(p))
    if not perms:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(perms)

def embeds_in(G, W):
    len_G = len(G)
    len_W = len(W)
    if len_G > len_W:
        return False
    if len_W % len_G != 0:
        return False
    if len_G == 1:
        return True
        
    gens = G.generators
    gen_orders = [g.order() for g in gens]
    
    W_elems = list(W.generate())
    
    candidates = []
    for o in gen_orders:
        cands = [w for w in W_elems if w.order() == o]
        candidates.append(cands)
        
    elements_G = list(G.generate())
    word_of = {G.identity: []}
    q = [G.identity]
    head = 0
    while head < len(q):
        curr = q[head]
        head += 1
        for i, gen in enumerate(gens):
            nxt = curr * gen
            if nxt not in word_of:
                word_of[nxt] = word_of[curr] + [i]
                q.append(nxt)
                
    def check_homomorphism(images):
        mapping = {G.identity: W.identity}
        for g in elements_G:
            if g == G.identity:
                continue
            w_elem = W.identity
            for idx in word_of[g]:
                w_elem = w_elem * images[idx]
            mapping[g] = w_elem
            
        visited = set()
        for v in mapping.values():
            if v in visited:
                return False
            visited.add(v)
            
        for g in elements_G:
            mg = mapping[g]
            for i, gen in enumerate(gens):
                if mapping[g * gen] != mg * images[i]:
                    return False
        return True

    for images in itertools.product(*candidates):
        if check_homomorphism(images):
            return True
            
    return False

def is_isomorphic(H, Q):
    if len(H) != len(Q):
        return False
    if len(H) == 1:
        return True
    return embeds_in(H, Q)

def wreath_product(N, H):
    d_N = N.degree if N.degree > 0 else 1
    d_H = H.degree if H.degree > 0 else 1
    
    wreath_gens = []
    for i in range(d_H):
        for g in N.generators:
            p = list(range(d_N * d_H))
            for x in range(d_N):
                p[i * d_N + x] = i * d_N + g(x)
            wreath_gens.append(Permutation(p))
            
    for h in H.generators:
        p = list(range(d_N * d_H))
        for i in range(d_H):
            hi = h(i)
            for x in range(d_N):
                p[i * d_N + x] = hi * d_N + x
        wreath_gens.append(Permutation(p))
        
    if not wreath_gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(wreath_gens)

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_normal_subgroup(G, N)
    except Exception:
        h1 = False
        
    try:
        Q = get_quotient_group(G, N)
        h2 = is_isomorphic(H, Q)
    except Exception:
        h2 = False
        
    try:
        W = wreath_product(N, H)
        neg_q = not embeds_in(G, W)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is isomorphic to the quotient group G/N",
    "¬Q: G is not isomorphic to a subgroup of the unrestricted wreath product of N by H"
]

N_HYP = 2
NEG_Q_INDEX = 2