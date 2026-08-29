import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_all_elements(G):
    if hasattr(G, '_all_elements_cache'):
        return G._all_elements_cache
    elements = set([G.identity])
    queue = [G.identity]
    while queue:
        curr = queue.pop(0)
        for gen in G.generators:
            nxt = curr * gen
            if nxt not in elements:
                elements.add(nxt)
                queue.append(nxt)
    res = list(elements)
    G._all_elements_cache = res
    return res

def is_abelian(G):
    for g in G.generators:
        for h in G.generators:
            if g * h != h * g:
                return False
    return True

def is_normal(G, N, G_elements):
    N_elems = frozenset(get_all_elements(N))
    for g in G_elements:
        for n in N.generators:
            if (~g * n * g) not in N_elems:
                return False
    return True

def get_centralizer(G, S, G_elements):
    c_elems = []
    for g in G_elements:
        commutes = True
        for s in S.generators:
            if g * s != s * g:
                commutes = False
                break
        if commutes:
            c_elems.append(g)
    if not c_elems:
        return PermutationGroup([G.identity])
    return PermutationGroup(c_elems)

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False]*4 + [False]
        G, S, I_S, alpha = witness
    except Exception:
        return [False]*4 + [False]

    try:
        G_elements = get_all_elements(G)
        S_elements = get_all_elements(S)
    except Exception:
        return [False]*4 + [False]

    try:
        normal_closures = []
        for g in G_elements:
            if g == G.identity: continue
            conjugates = list(set([~x * g * x for x in G_elements]))
            N = PermutationGroup(conjugates)
            N_elems = frozenset(get_all_elements(N))
            if not any(N_elems == existing[1] for existing in normal_closures):
                normal_closures.append((N, N_elems))
        
        minimal_normal = []
        for N, N_elems in normal_closures:
            is_minimal = True
            for M, M_elems in normal_closures:
                if M_elems != N_elems and M_elems.issubset(N_elems):
                    is_minimal = False
                    break
            if is_minimal:
                minimal_normal.append(N)
    except Exception:
        minimal_normal = []

    # H1: G is a semisimple group
    try:
        h1 = True
        if not minimal_normal:
            h1 = True
        else:
            for N in minimal_normal:
                if is_abelian(N):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: S is a non-abelian simple group that is a direct factor of G
    try:
        h2 = False
        if not is_abelian(S):
            S_normal_closures = []
            for s in S_elements:
                if s == S.identity: continue
                conjs = list(set([~x * s * x for x in S_elements]))
                N_s = PermutationGroup(conjs)
                N_s_elems = frozenset(get_all_elements(N_s))
                if not any(N_s_elems == existing[1] for existing in S_normal_closures):
                    S_normal_closures.append((N_s, N_s_elems))
            
            is_S_simple = len(S_normal_closures) == 1 and S_normal_closures[0][1] == frozenset(S_elements)
            
            if is_S_simple:
                if is_normal(G, S, G_elements):
                    H = get_centralizer(G, S, G_elements)
                    H_elems = frozenset(get_all_elements(H))
                    if len(S_elements) * len(H_elems) == len(G_elements):
                        if len(frozenset(S_elements).intersection(H_elems)) == 1:
                            h2 = True
    except Exception:
        h2 = False

    # H3: I_S is the isotypic component of G corresponding to S
    try:
        h3 = False
        isomorphic_minimal_normal = []
        for N in minimal_normal:
            iso = False
            if hasattr(N, 'is_isomorphic'):
                try:
                    iso = N.is_isomorphic(S)
                except Exception:
                    iso = (len(get_all_elements(N)) == len(S_elements))
            else:
                iso = (len(get_all_elements(N)) == len(S_elements))
            if iso:
                isomorphic_minimal_normal.append(N)
        
        if not isomorphic_minimal_normal:
            expected_I_S = PermutationGroup([G.identity])
        else:
            gens = []
            for N in isomorphic_minimal_normal:
                gens.extend(N.generators)
            expected_I_S = PermutationGroup(gens)
            
        expected_elems = frozenset(get_all_elements(expected_I_S))
        I_S_elems = frozenset(get_all_elements(I_S))
        h3 = (expected_elems == I_S_elems)
    except Exception:
        h3 = False

    # H4: \alpha is an automorphism of G
    try:
        h4 = False
        mapping = None
        if callable(alpha):
            alpha_dict = {g: alpha(g) for g in G.generators}
        elif isinstance(alpha, dict):
            alpha_dict = alpha
        elif isinstance(alpha, (list, tuple)) and len(alpha) == len(G.generators):
            alpha_dict = {G.generators[i]: alpha[i] for i in range(len(G.generators))}
        else:
            alpha_dict = None
            
        if alpha_dict is not None:
            if set(G.generators).issubset(set(alpha_dict.keys())):
                valid_images = True
                for gen in G.generators:
                    if alpha_dict[gen] not in G_elements:
                        valid_images = False
                        break
                if valid_images:
                    mapping = {G.identity: G.identity}
                    queue = [G.identity]
                    is_homo = True
                    while queue:
                        curr = queue.pop(0)
                        for gen in G.generators:
                            nxt = curr * gen
                            if nxt not in mapping:
                                mapping[nxt] = mapping[curr] * alpha_dict[gen]
                                queue.append(nxt)
                            else:
                                if mapping[nxt] != mapping[curr] * alpha_dict[gen]:
                                    is_homo = False
                                    break
                        if not is_homo:
                            break
                    
                    if is_homo and len(mapping) == len(G_elements):
                        if len(set(mapping.values())) == len(G_elements):
                            h4 = True
    except Exception:
        h4 = False

    # neg_Q: \alpha(I_S) != I_S
    try:
        neg_q = False
        if h4 and mapping is not None:
            alpha_I_S_gens = []
            for g in I_S.generators:
                if g in mapping:
                    alpha_I_S_gens.append(mapping[g])
                else:
                    alpha_I_S_gens.append(G.identity)
            if not alpha_I_S_gens:
                alpha_I_S_gens = [G.identity]
            alpha_I_S = PermutationGroup(alpha_I_S_gens)
            alpha_I_S_elems = frozenset(get_all_elements(alpha_I_S))
            I_S_elems = frozenset(get_all_elements(I_S))
            neg_q = (alpha_I_S_elems != I_S_elems)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "H_2: S is a non-abelian simple group that is a direct factor of G",
    "H_3: I_S is the isotypic component of G corresponding to S",
    "H_4: alpha is an automorphism of G",
    "¬Q: alpha(I_S) != I_S (I_S is not characteristic)"
]

N_HYP = 4
NEG_Q_INDEX = 4