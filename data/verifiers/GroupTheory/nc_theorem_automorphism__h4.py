import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import itertools

SymmetricGroup = sympy.combinatorics.named_groups.SymmetricGroup
AlternatingGroup = sympy.combinatorics.named_groups.AlternatingGroup
DihedralGroup = sympy.combinatorics.named_groups.DihedralGroup
CyclicGroup = sympy.combinatorics.named_groups.CyclicGroup
PermutationGroup = sympy.combinatorics.PermutationGroup
Permutation = sympy.combinatorics.permutations.Permutation
eye = sympy.matrices.eye
zeros = sympy.matrices.zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def normalizer(G, H):
    gens_H = list(H.generators)
    if not gens_H:
        return G
    norm_gens = []
    H_elements = set(H.elements)
    for g in G.elements:
        if all((g * h * ~g) in H_elements for h in gens_H):
            norm_gens.append(g)
    if not norm_gens:
        return PermutationGroup([G.identity])
    return PermutationGroup(norm_gens)

def centralizer(G, H):
    gens_H = list(H.generators)
    if not gens_H:
        return G
    cent_gens = []
    for g in G.elements:
        if all(g * h == h * g for h in gens_H):
            cent_gens.append(g)
    if not cent_gens:
        return PermutationGroup([G.identity])
    return PermutationGroup(cent_gens)

def get_quotient_group(N, C):
    N_elements = list(N.elements)
    C_elements = set(C.elements)
    
    cosets = []
    seen = set()
    for n in N_elements:
        if n not in seen:
            coset = frozenset(n * c for c in C_elements)
            cosets.append(coset)
            seen.update(coset)
            
    perms = []
    for c1 in cosets:
        rep1 = next(iter(c1))
        perm = []
        for c2 in cosets:
            rep2 = next(iter(c2))
            prod = rep1 * rep2
            for i, c3 in enumerate(cosets):
                if prod in c3:
                    perm.append(i)
                    break
        perms.append(Permutation(perm))
        
    if not perms:
        return PermutationGroup([Permutation([0])])
    return PermutationGroup(perms)

def get_Aut_H(H):
    elements = list(H.elements)
    gens = list(H.generators)
    if not gens:
        return PermutationGroup([Permutation([0])])
        
    automorphisms = []
    for target in itertools.product(elements, repeat=len(gens)):
        try:
            if PermutationGroup(list(target)).order() != H.order():
                continue
        except Exception:
            continue
            
        mapping = {H.identity: H.identity}
        queue = [H.identity]
        valid = True
        
        head = 0
        while head < len(queue):
            curr = queue[head]
            head += 1
            curr_mapped = mapping[curr]
            
            for g, t in zip(gens, target):
                nxt = curr * g
                nxt_mapped = curr_mapped * t
                if nxt in mapping:
                    if mapping[nxt] != nxt_mapped:
                        valid = False
                        break
                else:
                    mapping[nxt] = nxt_mapped
                    queue.append(nxt)
            if not valid:
                break
                
        if valid and len(mapping) == H.order():
            perm = []
            for e in elements:
                perm.append(elements.index(mapping[e]))
            automorphisms.append(Permutation(perm))
            
    if not automorphisms:
        return PermutationGroup([Permutation([0])])
    return PermutationGroup(automorphisms)

def is_isomorphic_to_subgroup(Q, A):
    Q_elements = list(Q.elements)
    Q_gens = list(Q.generators)
    A_elements = list(A.elements)
    
    if not Q_gens:
        return True
        
    for target in itertools.product(A_elements, repeat=len(Q_gens)):
        mapping = {Q.identity: A.identity}
        queue = [Q.identity]
        valid = True
        
        head = 0
        while head < len(queue):
            curr = queue[head]
            head += 1
            curr_mapped = mapping[curr]
            
            for g, t in zip(Q_gens, target):
                nxt = curr * g
                nxt_mapped = curr_mapped * t
                if nxt in mapping:
                    if mapping[nxt] != nxt_mapped:
                        valid = False
                        break
                else:
                    mapping[nxt] = nxt_mapped
                    queue.append(nxt)
            if not valid:
                break
                
        if valid and len(mapping) == Q.order():
            if len(set(mapping.values())) == Q.order():
                return True
                
    return False

def conditions(witness):
    if isinstance(witness, tuple):
        if len(witness) == 2:
            G, H = witness
        elif len(witness) >= 3:
            G, H = witness[0], witness[1]
        else:
            return [False, False, False, False]
    else:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H_3: N_G(H) is the normalizer of H in G
    try:
        if h1 and h2:
            N = normalizer(G, H)
            h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The quotient group N_G(H)/C_G(H) is not isomorphic to a subgroup of Aut(H)
    try:
        if h1 and h2 and h3:
            C = centralizer(G, H)
            Q_grp = get_quotient_group(N, C)
            Aut_H = get_Aut_H(H)
            q_holds = is_isomorphic_to_subgroup(Q_grp, Aut_H)
            neg_q = not q_holds
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: N_G(H) is the normalizer of H in G",
    "¬Q: The quotient group N_G(H)/C_G(H) is not isomorphic to a subgroup of Aut(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3