import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup

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
        X = witness.get('X', [])
        R = witness.get('R', [])
        A = witness.get('A', [])
        B = witness.get('B', [])
        A_mul = witness.get('A_mul', {})
        B_mul = witness.get('B_mul', {})
        alpha = witness.get('alpha', {})
        t = witness.get('t', '')
    except Exception:
        return [False, False, False, False]

    # H1: G is a group with presentation <X | R>
    try:
        h1 = isinstance(X, list) and all(isinstance(x, str) for x in X) and \
             isinstance(R, list) and all(isinstance(r, str) for r in R)
    except Exception:
        h1 = False

    # H2: alpha: A -> B is a group isomorphism
    try:
        def is_group(G, mul):
            if not G: return False
            for g1 in G:
                for g2 in G:
                    if (g1, g2) not in mul or mul[(g1, g2)] not in G: return False
            for g1 in G:
                for g2 in G:
                    for g3 in G:
                        if mul[(mul[(g1, g2)], g3)] != mul[(g1, mul[(g2, g3)])]: return False
            has_id = False
            for e in G:
                if all(mul[(e, g)] == g and mul[(g, e)] == g for g in G):
                    has_id = True
                    inv_ok = True
                    for g in G:
                        if not any(mul[(g, inv)] == e and mul[(inv, g)] == e for inv in G):
                            inv_ok = False
                            break
                    if inv_ok: return True
            return False

        h2_A = is_group(A, A_mul)
        h2_B = is_group(B, B_mul)
        h2_iso = True
        if h2_A and h2_B:
            if set(alpha.keys()) != set(A) or set(alpha.values()) != set(B):
                h2_iso = False
            else:
                for g1 in A:
                    for g2 in A:
                        if alpha[A_mul[(g1, g2)]] != B_mul[(alpha[g1], alpha[g2])]:
                            h2_iso = False
                            break
        else:
            h2_iso = False
        h2 = h2_A and h2_B and h2_iso
    except Exception:
        h2 = False

    # H3: t is a new generator symbol not contained in X
    try:
        h3 = isinstance(t, str) and t not in X and len(t) > 0
    except Exception:
        h3 = False

    # neg_Q: The conclusion fails.
    # The conclusion assumes A and B are subgroups of G. If they are not, the HNN extension
    # is undefined and the presentation is either syntactically invalid or incorrect.
    try:
        if X:
            F = free_group(','.join(X))[0]
        else:
            F = None

        def is_valid_word(w):
            if w == 'e' or w == '': return True
            if F is None: return False
            if hasattr(w, 'is_identity') and hasattr(w, 'group') and w.group == F:
                return True
            try:
                if isinstance(w, str):
                    w = w.replace('^', '**')
                F(w)
                return True
            except Exception:
                return False

        valid_syntax = all(is_valid_word(a) for a in A) and all(is_valid_word(b) for b in B)
        
        if not valid_syntax:
            neg_q = True
        else:
            if not X:
                if len(A) == 1 and len(B) == 1:
                    neg_q = False
                else:
                    neg_q = True
            else:
                def to_F(w):
                    if w == 'e' or w == '': return F.identity
                    if hasattr(w, 'is_identity'): return w
                    if isinstance(w, str):
                        w = w.replace('^', '**')
                    return F(w)
                
                is_subgroup_of_F = True
                for a1 in A:
                    for a2 in A:
                        if to_F(a1) * to_F(a2) != to_F(A_mul[(a1, a2)]):
                            is_subgroup_of_F = False
                            break
                for b1 in B:
                    for b2 in B:
                        if to_F(b1) * to_F(b2) != to_F(B_mul[(b1, b2)]):
                            is_subgroup_of_F = False
                            break
                
                if not R:
                    neg_q = not is_subgroup_of_F
                else:
                    try:
                        G_fp = FpGroup(F, [to_F(r) for r in R])
                        is_subgroup_of_G = True
                        for a1 in A:
                            for a2 in A:
                                w1 = to_F(a1)
                                w2 = to_F(a2)
                                w3 = to_F(A_mul[(a1, a2)])
                                if G_fp(w1 * w2) != G_fp(w3):
                                    is_subgroup_of_G = False
                                    break
                        for b1 in B:
                            for b2 in B:
                                w1 = to_F(b1)
                                w2 = to_F(b2)
                                w3 = to_F(B_mul[(b1, b2)])
                                if G_fp(w1 * w2) != G_fp(w3):
                                    is_subgroup_of_G = False
                                    break
                        neg_q = not is_subgroup_of_G
                    except Exception:
                        neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group with presentation <X | R>",
    "H_2: alpha: A -> B is a group isomorphism",
    "H_3: t is a new generator symbol not contained in X",
    "¬Q: The presentation is invalid or does not define the HNN extension (A and B are not subgroups of G)"
]

N_HYP = 3
NEG_Q_INDEX = 3