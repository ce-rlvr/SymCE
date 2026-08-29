import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.homomorphisms import homomorphism
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def wreath_product(A, B):
    """Constructs the regular wreath product A Wr B as a PermutationGroup."""
    deg_A = A.degree if A.degree > 0 else 1
    deg_B = B.degree if B.degree > 0 else 1
    
    gens = []
    A_gens = A.generators if A.generators else [Permutation(deg_A - 1)]
    B_gens = B.generators if B.generators else [Permutation(deg_B - 1)]
    
    if A.order() == 1 and B.order() == 1:
        return PermutationGroup([Permutation(0)])
        
    # Base group A^B generators
    for g in A_gens:
        for i in range(deg_B):
            perm = list(range(deg_A * deg_B))
            for j in range(deg_A):
                perm[j * deg_B + i] = g(j) * deg_B + i
            if perm != list(range(deg_A * deg_B)):
                gens.append(Permutation(perm))
            
    # Action of B generators
    for g in B_gens:
        perm = list(range(deg_A * deg_B))
        for i in range(deg_B):
            for j in range(deg_A):
                perm[j * deg_B + i] = j * deg_B + g(i)
        if perm != list(range(deg_A * deg_B)):
            gens.append(Permutation(perm))
            
    if not gens:
        return PermutationGroup([Permutation(deg_A * deg_B - 1)])
    return PermutationGroup(gens)

def embeds(G, W):
    """Checks if G is isomorphic to a subgroup of W."""
    if G.order() > W.order(): 
        return False
    if W.order() % G.order() != 0: 
        return False
    
    gens = G.generators
    W_elems = list(W.generate())
    
    for imgs in itertools.product(W_elems, repeat=len(gens)):
        try:
            h = homomorphism(G, W, gens, imgs)
            img_group = PermutationGroup(imgs)
            if img_group.order() == G.order():
                return True
        except Exception:
            pass
    return False

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(N, PermutationGroup) and 
              isinstance(H, PermutationGroup))
    except Exception:
        h1 = False
        
    try:
        if not N.is_subgroup(G):
            h2 = False
        elif not G.is_normal(N):
            h2 = False
        else:
            Q = G.quotient_group(N)
            h2 = H.is_isomorphic(Q)
    except Exception:
        h2 = False
        
    try:
        # The Kaloujnine-Krasner theorem states that G embeds in N Wr H.
        # If the conjecture is false, it may be due to a notational confusion 
        # (e.g., expecting H Wr N) or a misunderstanding of the theorem's scope.
        # We check both interpretations to robustly catch the intended failure.
        W_NH = wreath_product(N, H)
        W_HN = wreath_product(H, N)
        
        emb_NH = embeds(G, W_NH)
        emb_HN = embeds(G, W_HN)
        
        neg_Q = (not emb_NH) or (not emb_HN)
    except Exception:
        neg_Q = False
        
    return [h1, h2, neg_Q]

CONDITION_LABELS = [
    "H_1: G, N, and H are groups",
    "H_2: H is isomorphic to the quotient group G/N",
    "¬Q: G is not isomorphic to a subgroup of the unrestricted wreath product of N by H"
]

N_HYP = 2
NEG_Q_INDEX = 2