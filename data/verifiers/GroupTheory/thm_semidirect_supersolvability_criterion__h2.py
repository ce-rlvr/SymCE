import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import itertools

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

def get_all_normal_subgroups(G):
    elements = list(G.generate())
    n = len(elements)
    
    conjugacy_classes = []
    unseen = set(elements)
    while unseen:
        x = unseen.pop()
        cclass = set()
        for g in elements:
            cclass.add(g * x * ~g)
        conjugacy_classes.append(cclass)
        unseen -= cclass
        
    identity = elements[0] * ~elements[0]
    id_class = {identity}
            
    other_classes = [c for c in conjugacy_classes if c != id_class]
    
    normal_subgroups = []
    for r in range(len(other_classes) + 1):
        for combo in itertools.combinations(other_classes, r):
            subset = set(id_class)
            for c in combo:
                subset.update(c)
            
            if n % len(subset) != 0:
                continue
                
            is_subgroup = True
            for a in subset:
                for b in subset:
                    if a * b not in subset:
                        is_subgroup = False
                        break
                if not is_subgroup:
                    break
            if is_subgroup:
                normal_subgroups.append(subset)
                
    return normal_subgroups

def has_invariant_prime_series(G, N_elements):
    n_order = len(N_elements)
    if n_order == 1:
        return True
        
    normal_subgroups = get_all_normal_subgroups(G)
    
    valid_subgroups = [ns for ns in normal_subgroups if ns.issubset(N_elements)]
    valid_subgroups.sort(key=len)
    
    if not valid_subgroups or len(valid_subgroups[-1]) != n_order:
        return False
        
    def dfs(idx):
        if len(valid_subgroups[idx]) == n_order:
            return True
        for next_idx in range(idx + 1, len(valid_subgroups)):
            A = valid_subgroups[idx]
            B = valid_subgroups[next_idx]
            if len(B) % len(A) == 0 and sympy.isprime(len(B) // len(A)):
                if A.issubset(B):
                    if dfs(next_idx):
                        return True
        return False

    return dfs(0)

def is_supersolvable(G):
    n = G.order()
    if n == 1:
        return True
    
    normal_subgroups = get_all_normal_subgroups(G)
    normal_subgroups.sort(key=len)
    
    def dfs(idx):
        if len(normal_subgroups[idx]) == n:
            return True
        for next_idx in range(idx + 1, len(normal_subgroups)):
            A = normal_subgroups[idx]
            B = normal_subgroups[next_idx]
            if len(B) % len(A) == 0 and sympy.isprime(len(B) // len(A)):
                if A.issubset(B):
                    if dfs(next_idx):
                        return True
        return False

    return dfs(0)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False, False]
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a finite group, N and H are subgroups of G
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
        if h1:
            G_elements = set(G.generate())
            for g in N.generators:
                if g not in G_elements:
                    h1 = False
            for g in H.generators:
                if g not in G_elements:
                    h1 = False
    except Exception:
        h1 = False

    # H2: G = N ⋊ H
    try:
        if h1:
            G_elements = set(G.generate())
            N_elements = set(N.generate())
            H_elements = set(H.generate())
            
            h2 = True
            # N is normal in G
            for g in G.generators:
                for n in N.generators:
                    if g * n * ~g not in N_elements:
                        h2 = False
                        break
                if not h2:
                    break
            
            if h2:
                # N intersect H is trivial
                if len(N_elements.intersection(H_elements)) != 1:
                    h2 = False
                
                # G = NH
                if G.order() != N.order() * H.order():
                    h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: N has a series of H-invariant normal subgroups with prime cyclic quotient factors
    try:
        if h1 and h2:
            N_elements = set(N.generate())
            h3 = has_invariant_prime_series(G, N_elements)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: G is not a supersolvable group
    try:
        if h1:
            neg_q = not is_supersolvable(G)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group, N and H are subgroups of G",
    "H_2: G is a semidirect product of N and H (G = N ⋊ H)",
    "H_3: N has a series of H-invariant normal subgroups with prime cyclic quotient factors",
    "¬Q: G is not a supersolvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3