import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy import isprime

# Top-level setup for potential witness expressions
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

def is_in_H(H, conj):
    """Safely check if a permutation is in a PermutationGroup, handling degree mismatches."""
    try:
        if H.contains(conj):
            return True
    except Exception:
        pass

    if conj.size > H.degree:
        for i in range(H.degree, conj.size):
            if conj(i) != i:
                return False
        conj_trunc = Permutation(conj.array_form[:H.degree])
        try:
            return H.contains(conj_trunc)
        except Exception:
            return False
    elif conj.size < H.degree:
        conj_pad = Permutation(conj.array_form + list(range(conj.size, H.degree)))
        try:
            return H.contains(conj_pad)
        except Exception:
            return False
    return False

def normalizer_order(G, H):
    """Compute the order of the normalizer of H in G."""
    count = 0
    gens = H.generators
    if not gens:
        return G.order()
    
    for g in G.generate():
        is_in_norm = True
        for h in gens:
            conj = g * h * (~g)
            if not is_in_H(H, conj):
                is_in_norm = False
                break
        if is_in_norm:
            count += 1
    return count

def conditions(witness):
    """
    Check the hypotheses and the negated conclusion for the given witness.
    The witness can be either (G, p, P) or (G, p, P, n_p).
    """
    try:
        if len(witness) == 3:
            G, p, P = witness
            n_p_wit = None
        elif len(witness) == 4:
            G, p, P, n_p_wit = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: p is a prime number dividing the order of G
    try:
        h2 = isprime(p) and G.order() % p == 0
    except Exception:
        h2 = False

    # H3: n_p is the number of Sylow p-subgroups of G (and P is a subgroup of G)
    try:
        p_is_subgroup = True
        for g in P.generators:
            if not is_in_H(G, g):
                p_is_subgroup = False
                break
        
        S = G.sylow_subgroup(p)
        actual_n_p = G.order() // normalizer_order(G, S)
        
        if n_p_wit is not None:
            h3 = p_is_subgroup and (n_p_wit == actual_n_p)
        else:
            h3 = p_is_subgroup
            n_p_wit = actual_n_p
    except Exception:
        h3 = False

    # neg_Q: The index of N_G(P) in G is not equal to n_p
    try:
        if n_p_wit is None:
            S = G.sylow_subgroup(p)
            n_p_wit = G.order() // normalizer_order(G, S)
        
        idx_N_G_P = G.order() // normalizer_order(G, P)
        neg_q = (idx_N_G_P != n_p_wit)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number dividing the order of G",
    "H_3: n_p is the number of Sylow p-subgroups of G",
    "¬Q: The index of N_G(P) in G is not equal to n_p"
]

N_HYP = 3
NEG_Q_INDEX = 3