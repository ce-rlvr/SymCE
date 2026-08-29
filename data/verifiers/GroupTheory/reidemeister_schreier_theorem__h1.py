import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.matrices import Matrix
from sympy.matrices.normalforms import smith_normal_form

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1), Permutation(2, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: T is a right Schreier transversal for H in G",
    "¬Q: H does not admit the Reidemeister-Schreier presentation"
]
N_HYP = 2
NEG_Q_INDEX = 2

def eval_word(w, X, identity):
    res = identity
    for y in w:
        if y > 0:
            res = res * X[y - 1]
        elif y < 0:
            res = res * X[-y - 1]**-1
    return res

def get_rep(g, T_elements, H):
    for i, t in enumerate(T_elements):
        if H.contains(g * t**-1):
            return i
    return None

def is_transversal(T_elements, G, H):
    if len(T_elements) * H.order() != G.order():
        return False
    for i in range(len(T_elements)):
        for j in range(i + 1, len(T_elements)):
            if H.contains(T_elements[i] * T_elements[j]**-1):
                return False
    return True

def is_schreier(T_words):
    T_set = set(tuple(w) for w in T_words)
    for w in T_words:
        for k in range(len(w) + 1):
            if tuple(w[:k]) not in T_set:
                return False
    return True

def abelian_order(S_keys, R_H, F):
    n_gens = len(S_keys)
    n_rels = len(R_H)
    if n_gens == 0:
        return 1
    if n_rels < n_gens:
        return 0
    
    name_to_idx = {}
    for i, g in enumerate(F.generators):
        sym = g.array_form[0][0]
        name_to_idx[sym.name] = i

    M = Matrix(n_rels, n_gens, lambda i, j: 0)
    for i, rel in enumerate(R_H):
        for sym, exp in rel.array_form:
            j = name_to_idx[sym.name]
            M[i, j] += exp
            
    try:
        SNF = smith_normal_form(M)
        order = 1
        for i in range(n_gens):
            if SNF[i, i] == 0:
                return 0
            order *= abs(SNF[i, i])
        return order
    except Exception:
        return None

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            X = witness['X']
            R_words = witness['R_words']
            T_words = witness['T_words']
        else:
            G, H, X, R_words, T_words = witness
    except Exception:
        return [False, False, False]
        
    # H_1: H is a subgroup of G
    try:
        h1 = all(G.contains(g) for g in H.generators)
    except Exception:
        h1 = False
        
    try:
        identity = G.identity
        T_elements = [eval_word(w, X, identity) for w in T_words]
    except Exception:
        T_elements = None

    # H_2: T is a right Schreier transversal for H in G
    try:
        if T_elements is None:
            h2 = False
        else:
            is_trans = is_transversal(T_elements, G, H)
            is_sch = is_schreier(T_words)
            h2 = is_trans and is_sch
    except Exception:
        h2 = False
        
    # neg_Q: H does NOT admit the presentation
    try:
        if T_elements is None:
            neg_q = False
        else:
            S_keys = []
            for t_idx in range(len(T_elements)):
                for x_idx in range(len(X)):
                    t_val = T_elements[t_idx]
                    x_val = X[x_idx]
                    tx_val = t_val * x_val
                    rep_idx = get_rep(tx_val, T_elements, H)
                    if rep_idx is None:
                        raise ValueError("Not a transversal")
                    if not (t_val * x_val * T_elements[rep_idx]**-1).is_Identity:
                        S_keys.append((t_idx, x_idx))
                        
            if len(S_keys) == 0:
                presented_ab_order = 1
                F = None
                R_H = []
            else:
                symbols = ','.join([f's_{t}_{x}' for t, x in S_keys])
                F, gens = free_group(symbols)
                if len(S_keys) == 1:
                    gens = [gens]
                else:
                    gens = list(gens)
                
                S_dict = { S_keys[i]: gens[i] for i in range(len(S_keys)) }
                
                R_H = []
                for t_idx in range(len(T_elements)):
                    for r in R_words:
                        curr_t_idx = t_idx
                        rel_word = F.identity
                        for y in r:
                            if y > 0:
                                x_idx = y - 1
                                x_val = X[x_idx]
                                s = S_dict.get((curr_t_idx, x_idx), None)
                                if s is not None:
                                    rel_word = rel_word * s
                                curr_t_idx = get_rep(T_elements[curr_t_idx] * x_val, T_elements, H)
                            elif y < 0:
                                x_idx = -y - 1
                                x_val = X[x_idx]
                                next_t_idx = get_rep(T_elements[curr_t_idx] * x_val**-1, T_elements, H)
                                s = S_dict.get((next_t_idx, x_idx), None)
                                if s is not None:
                                    rel_word = rel_word * s**-1
                                curr_t_idx = next_t_idx
                        if rel_word != F.identity:
                            R_H.append(rel_word)
                
                presented_ab_order = abelian_order(S_keys, R_H, F)
                
            if H.is_abelian:
                H_ab_order = H.order()
            else:
                H_ab_order = H.order() // H.derived_subgroup().order()
                
            if presented_ab_order is not None and presented_ab_order != H_ab_order:
                neg_q = True
            else:
                if len(S_keys) == 0:
                    presented_order = 1
                else:
                    fp_grp = FpGroup(F, R_H)
                    presented_order = fp_grp.order()
                neg_q = (presented_order != H.order())
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]