import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime, factorint
import itertools
import functools
import math

# Top-level setup
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

def is_subgroup(H, G):
    try:
        for gen in H.generators:
            if gen not in G:
                return False
        return True
    except Exception:
        return False

def is_normal_subgroup(G, N):
    try:
        if not is_subgroup(N, G):
            return False
        for g in G.generators:
            g_inv = ~g
            for n in N.generators:
                if (g * n * g_inv) not in N:
                    return False
        return True
    except Exception:
        return False

def is_abelian(G):
    try:
        if hasattr(G, 'is_abelian'):
            return G.is_abelian
        gens = G.generators
        for i in range(len(gens)):
            for j in range(i+1, len(gens)):
                if gens[i]*gens[j] != gens[j]*gens[i]:
                    return False
        return True
    except Exception:
        return False

def has_complement(G, N):
    try:
        m = G.order() // N.order()
        if m == 1:
            return True
        if G.order() % N.order() != 0:
            return False
            
        elements = list(G.generate_dimino())
        N_set = set(N.generate_dimino())
        
        allowed_elements = [g for g in elements if m % g.order() == 0 and (g.is_Identity or g not in N_set)]
        allowed_set = set(allowed_elements)
        
        if len(allowed_elements) < m:
            return False
            
        def get_closure(gens, max_size):
            closure = set(gens)
            q = list(gens)
            while q:
                curr = q.pop(0)
                for g in gens:
                    nxt = curr * g
                    if nxt not in allowed_set:
                        return None
                    if nxt not in closure:
                        closure.add(nxt)
                        if len(closure) > max_size:
                            return None
                        q.append(nxt)
            return closure

        subgroups = []
        for g in allowed_elements:
            if g.is_Identity: continue
            cg = get_closure([g], m)
            if cg is not None:
                if len(cg) == m:
                    return True
                subgroups.append(cg)
                
        seen = {frozenset(sg) for sg in subgroups}
        queue = list(subgroups)
        
        while queue:
            sg = queue.pop(0)
            for g in allowed_elements:
                if g in sg: continue
                new_gens = list(sg) + [g]
                new_sg = get_closure(new_gens, m)
                if new_sg is not None:
                    if len(new_sg) == m:
                        return True
                    fs = frozenset(new_sg)
                    if fs not in seen:
                        seen.add(fs)
                        queue.append(new_sg)
                        
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, p, N, P = witness
            H_P = None
        elif len(witness) == 5:
            G, p, N, P, H_P = witness
        else:
            return [False]*4 + [False]
    except Exception:
        return [False]*4 + [False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # H3: N is an abelian normal p-subgroup of G
    try:
        h3 = True
        if not isinstance(N, PermutationGroup):
            h3 = False
        elif not is_subgroup(N, G):
            h3 = False
        elif not is_abelian(N):
            h3 = False
        elif not is_normal_subgroup(G, N):
            h3 = False
        else:
            order_N = N.order()
            if order_N == 1:
                pass
            else:
                factors = factorint(order_N)
                if list(factors.keys()) != [p]:
                    h3 = False
    except Exception:
        h3 = False

    # H4: P is a subgroup of G, N is a subgroup of P, and N has a complement in P
    try:
        h4 = True
        if not isinstance(P, PermutationGroup):
            h4 = False
        elif not is_subgroup(P, G):
            h4 = False
        elif not is_subgroup(N, P):
            h4 = False
        else:
            if H_P is not None:
                if not isinstance(H_P, PermutationGroup):
                    h4 = False
                elif not is_subgroup(H_P, P):
                    h4 = False
                elif H_P.order() * N.order() != P.order():
                    h4 = False
                else:
                    N_set = set(N.generate_dimino())
                    inter_trivial = True
                    for g in H_P.generate_dimino():
                        if not g.is_Identity and g in N_set:
                            inter_trivial = False
                            break
                    if not inter_trivial:
                        h4 = False
            else:
                if not has_complement(P, N):
                    h4 = False
    except Exception:
        h4 = False

    # neg_Q: N does not have a complement in G
    try:
        neg_q = not has_complement(G, N)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: N is an abelian normal p-subgroup of G",
    "H_4: P is a subgroup of G containing N, and N has a complement in P",
    "¬Q: N does not have a complement in G"
]

N_HYP = 4
NEG_Q_INDEX = 4