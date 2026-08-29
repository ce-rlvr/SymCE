import sympy
import sympy.ntheory
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

# Top-level setup: named object bindings
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

def is_subgroup(sub, G):
    try:
        for g in sub.generators:
            if g not in G:
                return False
        return True
    except Exception:
        return False

def is_normal(G, N):
    try:
        if not is_subgroup(N, G):
            return False
        for g in G.generators:
            for n in N.generators:
                if g * n * g**-1 not in N:
                    return False
        return True
    except Exception:
        return False

def is_semidirect_product(G, N, H):
    try:
        if not (is_subgroup(N, G) and is_subgroup(H, G)):
            return False
        intersection = set(N.elements).intersection(set(H.elements))
        if len(intersection) != 1:
            return False
        if G.order() != N.order() * H.order():
            return False
        return True
    except Exception:
        return False

def is_supersolvable(G):
    try:
        order = G.order()
        if order == 1:
            return True
        
        elements = list(G.elements)
        
        # A finite group is supersolvable iff it has a normal subgroup of prime order
        # and the quotient group is supersolvable.
        prime_normal_subgroups = []
        for p in sympy.ntheory.primefactors(order):
            for g in elements:
                if g.order() == p:
                    subg = frozenset(g**k for k in range(p))
                    if subg in prime_normal_subgroups:
                        continue
                    
                    is_normal_subg = True
                    for h in G.generators:
                        if h * g * h**-1 not in subg:
                            is_normal_subg = False
                            break
                    if is_normal_subg:
                        prime_normal_subgroups.append(subg)
                        
        if not prime_normal_subgroups:
            return False
            
        for N in prime_normal_subgroups:
            cosets = []
            unseen = set(elements)
            while unseen:
                x = unseen.pop()
                coset = frozenset(x * n for n in N)
                cosets.append(coset)
                unseen -= coset
                
            cosets = list(cosets)
            
            quotient_gens = []
            for g in G.generators:
                perm = []
                for c in cosets:
                    rep = next(iter(c))
                    target = g * rep
                    for i, c2 in enumerate(cosets):
                        if target in c2:
                            perm.append(i)
                            break
                quotient_gens.append(Permutation(perm))
            
            Q = PermutationGroup(quotient_gens)
            if is_supersolvable(Q):
                return True
                
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False] * 7
        G, N, H = witness
    except Exception:
        return [False] * 7

    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = is_normal(G, N)
    except Exception:
        h2 = False

    try:
        h3 = is_subgroup(H, G)
    except Exception:
        h3 = False

    try:
        h4 = is_semidirect_product(G, N, H)
    except Exception:
        h4 = False

    try:
        h5 = is_supersolvable(N)
    except Exception:
        h5 = False

    try:
        h6 = is_supersolvable(H)
    except Exception:
        h6 = False

    try:
        neg_q = not is_supersolvable(G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: G, N, H are permutation groups",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: G is the semidirect product of N and H",
    "H_5: N is supersolvable",
    "H_6: H is supersolvable",
    "¬Q: G is not supersolvable"
]

N_HYP = 6
NEG_Q_INDEX = 6