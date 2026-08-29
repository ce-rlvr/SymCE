import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def create_FpGroup(gens, rels):
    if not gens:
        F, d = free_group("dummy")
        return FpGroup(F, [d])
    F, F_gens = free_group(", ".join(gens))
    if len(gens) == 1:
        F_gens = (F_gens,)
    gen_dict = {g: sym for g, sym in zip(gens, F_gens)}
    
    F_rels = []
    for word in rels:
        elem = F.identity
        for g, p in word:
            elem = elem * (gen_dict[g] ** p)
        F_rels.append(elem)
    return FpGroup(F, F_rels)

def eval_word(word, mapping, identity):
    res = identity
    for gen, power in word:
        val = mapping[gen]
        res = res * (val ** power)
    return res

def conditions(witness):
    try:
        N = witness['N']
        H = witness['H']
        X = witness['X']
        R = witness['R']
        Y = witness['Y']
        S = witness['S']
        pi_X = witness['pi_X']
        pi_Y = witness['pi_Y']
        phi = witness['phi']
        w = witness['w']
    except KeyError:
        return [False, False, False, False]

    # H_1: H is a group with presentation <Y | S>
    try:
        if not all(y in pi_Y and pi_Y[y] in H.elements for y in Y):
            h1 = False
        else:
            H_gens = [pi_Y[y] for y in Y]
            if H_gens:
                H_sub = PermutationGroup(H_gens)
            else:
                H_sub = PermutationGroup([H.identity])
            
            if H_sub.order() != H.order():
                h1 = False
            else:
                rels_ok = True
                for rel in S:
                    if eval_word(rel, pi_Y, H.identity) != H.identity:
                        rels_ok = False
                        break
                if not rels_ok:
                    h1 = False
                else:
                    Fp_H = create_FpGroup(Y, S)
                    h1 = (Fp_H.order() == H.order())
    except Exception:
        h1 = False

    # H_2: phi: H -> Aut(N) is a group homomorphism
    try:
        h2 = True
        N_elements = list(N.elements)
        H_elements = list(H.elements)
        
        if not all(h in phi for h in H_elements):
            h2 = False
        else:
            for h in H_elements:
                mapping = phi[h]
                if set(mapping.keys()) != set(N_elements) or set(mapping.values()) != set(N_elements):
                    h2 = False
                    break
                for n1 in N_elements:
                    for n2 in N_elements:
                        if mapping[n1 * n2] != mapping[n1] * mapping[n2]:
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
            
            if h2:
                for h1_el in H_elements:
                    for h2_el in H_elements:
                        h12 = h1_el * h2_el
                        for n in N_elements:
                            if phi[h12][n] != phi[h1_el][phi[h2_el][n]]:
                                h2 = False
                                break
                        if not h2: break
                    if not h2: break
    except Exception:
        h2 = False

    # H_3: w_{y,x} represents phi(y)(x)
    try:
        h3 = True
        for y in Y:
            for x in X:
                if (y, x) not in w:
                    h3 = False
                    break
                word = w[(y, x)]
                if not all(gen in X for gen, power in word):
                    h3 = False
                    break
                val = eval_word(word, pi_X, N.identity)
                expected = phi[pi_Y[y]][pi_X[x]]
                if val != expected:
                    h3 = False
                    break
            if not h3: break
    except Exception:
        h3 = False

    # neg_Q: N rtimes H is NOT isomorphic to the presentation
    try:
        sd_order = N.order() * H.order()
        
        gens = list(X) + list(Y)
        rels = list(R) + list(S)
        for y in Y:
            for x in X:
                word = w[(y, x)]
                inv_word = [(g, -p) for g, p in reversed(word)]
                rel = [(y, 1), (x, 1), (y, -1)] + inv_word
                rels.append(rel)
        
        Fp_G = create_FpGroup(gens, rels)
        
        # If the orders differ, they are definitely not isomorphic.
        if Fp_G.order() != sd_order:
            neg_Q = True
        else:
            neg_Q = False
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = [
    "H_1: H is a group with presentation <Y | S>",
    "H_2: phi is a group homomorphism from H to Aut(N)",
    "H_3: w_{y,x} represents the element phi(y)(x) in N",
    "¬Q: The semidirect product N rtimes H is not isomorphic to the given presentation"
]

N_HYP = 3
NEG_Q_INDEX = 3