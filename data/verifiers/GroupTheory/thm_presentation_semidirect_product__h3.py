import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        X, R, Y, S, W = witness
    except Exception:
        return [False, False, False, False]

    # H1: N is a group with presentation <X | R>
    try:
        h1 = isinstance(X, list) and isinstance(R, list)
        if h1:
            for rel in R:
                if not isinstance(rel, list):
                    h1 = False
                    break
                for term in rel:
                    if not (isinstance(term, tuple) and len(term) == 2):
                        h1 = False
                        break
                    gen, power = term
                    if gen not in X or not isinstance(power, int):
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: H is a group with presentation <Y | S>
    try:
        h2 = isinstance(Y, list) and isinstance(S, list)
        if h2:
            for rel in S:
                if not isinstance(rel, list):
                    h2 = False
                    break
                for term in rel:
                    if not (isinstance(term, tuple) and len(term) == 2):
                        h2 = False
                        break
                    gen, power = term
                    if gen not in Y or not isinstance(power, int):
                        h2 = False
                        break
    except Exception:
        h2 = False

    # H3: For each y in Y and x in X, w_{y,x} is a word in X
    try:
        h3 = isinstance(W, dict)
        if h3:
            for y in Y:
                for x in X:
                    if (y, x) not in W:
                        h3 = False
                        break
                    word = W[(y, x)]
                    if not isinstance(word, list):
                        h3 = False
                        break
                    for term in word:
                        if not (isinstance(term, tuple) and len(term) == 2):
                            h3 = False
                            break
                        gen, power = term
                        if gen not in X or not isinstance(power, int):
                            h3 = False
                            break
                    if not h3:
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # neg_Q: The presented group is not isomorphic to the semidirect product
    try:
        neg_q = None
        
        # Fallback logic for simple abelian presentations if FpGroup is unavailable
        orders = {x: 0 for x in X}
        for rel in R:
            if len(rel) == 1:
                g, p = rel[0]
                if orders.get(g, 0) == 0:
                    orders[g] = abs(p)
                    
        simple_R = all(len(rel) == 1 for rel in R)
        
        if simple_R:
            def apply_y(y, word):
                res = []
                for g, p in word:
                    img = W.get((y, g), [(g, 1)])
                    if p > 0:
                        for _ in range(p):
                            res.extend(img)
                    else:
                        inv_img = [(ig, -ip) for ig, ip in reversed(img)]
                        for _ in range(-p):
                            res.extend(inv_img)
                return res

            def is_identity(word):
                exp_sums = {x: 0 for x in X}
                for g, p in word:
                    if g in exp_sums:
                        exp_sums[g] += p
                for x in X:
                    if orders[x] > 0:
                        if exp_sums[x] % orders[x] != 0:
                            return False
                    else:
                        if exp_sums[x] != 0:
                            return False
                return True

            valid_action = True
            for y in Y:
                for rel in R:
                    img_rel = apply_y(y, rel)
                    if not is_identity(img_rel):
                        valid_action = False
                        break
                if not valid_action:
                    break
                    
            if valid_action:
                for rel in S:
                    for x in X:
                        curr = [(x, 1)]
                        for y, p in reversed(rel):
                            if p > 0:
                                for _ in range(p):
                                    curr = apply_y(y, curr)
                            elif p < 0:
                                pass
                        check_word = curr + [(x, -1)]
                        if not is_identity(check_word):
                            valid_action = False
                            break
                    if not valid_action:
                        break
                        
            if not valid_action:
                neg_q = True

        if neg_q is None:
            try:
                from sympy.combinatorics import free_group
                from sympy.combinatorics.fp_groups import FpGroup
                has_fpgroup = True
            except ImportError:
                has_fpgroup = False
                
            if has_fpgroup:
                def get_order(gens_list, rels_list):
                    if not gens_list:
                        return 1
                    F, gens = free_group(",".join(gens_list))
                    if not isinstance(gens, tuple):
                        gens = (gens,)
                    g_dict = dict(zip(gens_list, gens))
                    
                    F_rels = []
                    for rel in rels_list:
                        w = F.identity
                        for gen, power in rel:
                            w = w * (g_dict[gen] ** power)
                        F_rels.append(w)
                    
                    G = FpGroup(F, F_rels)
                    return G.order()

                N_order = get_order(X, R)
                H_order = get_order(Y, S)
                
                XY = X + Y
                if not XY:
                    G_order = 1
                else:
                    F_G, gens_G = free_group(",".join(XY))
                    if not isinstance(gens_G, tuple):
                        gens_G = (gens_G,)
                    dict_G = dict(zip(XY, gens_G))
                    
                    G_rels = []
                    for rel in R + S:
                        w = F_G.identity
                        for gen, power in rel:
                            w = w * (dict_G[gen] ** power)
                        G_rels.append(w)
                        
                    for y in Y:
                        for x in X:
                            lhs = dict_G[y] * dict_G[x] * (dict_G[y] ** -1)
                            rhs = F_G.identity
                            for gen, power in W.get((y, x), [(x, 1)]):
                                rhs = rhs * (dict_G[gen] ** power)
                            G_rels.append(lhs * (rhs ** -1))
                            
                    G = FpGroup(F_G, G_rels)
                    G_order = G.order()
                    
                neg_q = (G_order != N_order * H_order)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a group with presentation <X | R>",
    "H_2: H is a group with presentation <Y | S>",
    "H_3: For each y in Y and x in X, w_{y,x} is a word in X",
    "¬Q: The presented group is not isomorphic to the semidirect product"
]

N_HYP = 3
NEG_Q_INDEX = 3