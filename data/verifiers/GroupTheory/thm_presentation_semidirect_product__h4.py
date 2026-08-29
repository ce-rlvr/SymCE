import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard groups
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

CONDITION_LABELS = [
    "H_1: N is a group with presentation <X | R>",
    "H_2: H is a group with presentation <Y | S>",
    "H_3: phi is a group homomorphism from H to Aut(N)",
    "¬Q: The semidirect product N rtimes H is not isomorphic to the given presentation"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys:
      - 'X': list of strings (generators of N)
      - 'R': list of words in X (relations of N), where a word is a list of (generator_name, power) tuples
      - 'Y': list of strings (generators of H)
      - 'S': list of words in Y (relations of H)
      - 'phi': dict mapping y in Y to a dict mapping x in X to a word in X
    """
    try:
        X = witness['X']
        R = witness['R']
        Y = witness['Y']
        S = witness['S']
        phi = witness['phi']
    except (KeyError, TypeError):
        return [False, False, False, False]

    def to_word(F, gen_dict, word_repr):
        w = F.identity
        for gen_name, power in word_repr:
            w = w * (gen_dict[gen_name] ** power)
        return w

    def apply_phi(phi_dict, y_name, w_N_repr):
        res = []
        for x_name, power in w_N_repr:
            sub_word = phi_dict[y_name][x_name]
            if power > 0:
                for _ in range(power):
                    res.extend(sub_word)
            elif power < 0:
                inv_sub = [(n, -p) for n, p in reversed(sub_word)]
                for _ in range(-power):
                    res.extend(inv_sub)
        return res

    def apply_phi_word(phi_dict, w_H_repr, w_N_repr):
        current_w = w_N_repr
        for y_name, power in reversed(w_H_repr):
            if power < 0:
                raise ValueError("Negative powers in H words not supported in this verifier")
            for _ in range(power):
                current_w = apply_phi(phi_dict, y_name, current_w)
        return current_w

    # H1: N is a group with presentation <X | R>
    h1 = False
    try:
        if not X:
            raise ValueError
        F_N, X_gens = free_group(",".join(X))
        X_dict = {x: g for x, g in zip(X, X_gens)}
        R_words = [to_word(F_N, X_dict, r) for r in R]
        N = FpGroup(F_N, R_words)
        try:
            N.make_confluent()
        except Exception:
            pass
        N_order = N.order()
        h1 = True
    except Exception:
        h1 = False

    # H2: H is a group with presentation <Y | S>
    h2 = False
    try:
        if not Y:
            raise ValueError
        F_H, Y_gens = free_group(",".join(Y))
        Y_dict = {y: g for y, g in zip(Y, Y_gens)}
        S_words = [to_word(F_H, Y_dict, s) for s in S]
        H = FpGroup(F_H, S_words)
        try:
            H.make_confluent()
        except Exception:
            pass
        H_order = H.order()
        h2 = True
    except Exception:
        h2 = False

    # H3: phi is a homomorphism H -> Aut(N)
    h3 = False
    try:
        if h1 and h2:
            h3_ok = True
            for y in Y:
                for r in R:
                    w_out = apply_phi(phi, y, r)
                    w_out_word = to_word(F_N, X_dict, w_out)
                    if N.reduce(w_out_word) != F_N.identity:
                        h3_ok = False
            for s in S:
                for x in X:
                    w_out = apply_phi_word(phi, s, [(x, 1)])
                    w_out_word = to_word(F_N, X_dict, w_out)
                    if N.reduce(w_out_word) != X_dict[x]:
                        h3_ok = False
            h3 = h3_ok
    except Exception:
        h3 = False

    # neg_Q: The semidirect product is NOT isomorphic to G
    neg_q = False
    try:
        if h1 and h2 and h3:
            X_Y = list(set(X + Y))
            X_Y.sort()
            F_G, G_gens = free_group(",".join(X_Y))
            G_dict = {g_name: g for g_name, g in zip(X_Y, G_gens)}

            G_relations = []
            for r in R:
                G_relations.append(to_word(F_G, G_dict, r))
            for s in S:
                G_relations.append(to_word(F_G, G_dict, s))

            for x in X:
                for y in Y:
                    w_yx = phi[y][x]
                    inv_w_yx = [(n, -p) for n, p in reversed(w_yx)]
                    rel_repr = [(y, 1), (x, 1), (y, -1)] + inv_w_yx
                    G_relations.append(to_word(F_G, G_dict, rel_repr))

            G = FpGroup(F_G, G_relations)
            try:
                G.make_confluent()
            except Exception:
                pass
            G_order = G.order()

            # If the orders differ, they are definitely not isomorphic.
            if G_order != N_order * H_order:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]