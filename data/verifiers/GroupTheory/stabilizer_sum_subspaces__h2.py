import sympy
from sympy import eye, zeros, Matrix
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks whether it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (G, W1, W2) where:
      - G is a list of sympy Matrices representing the group elements.
      - W1, W2 are either lists/tuples of vectors (representing finite subsets)
        OR sympy Matrices (representing subspaces via their column spaces).
    """
    try:
        G, W1, W2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group acting linearly on a vector space V
    try:
        if not isinstance(G, list) or not G:
            h1 = False
        else:
            # Find the identity element
            e = None
            for g in G:
                if all(g*h == h for h in G) and all(h*g == h for h in G):
                    e = g
                    break
            if e is None:
                h1 = False
            else:
                h1 = True
                for g in G:
                    # Check for inverse
                    has_inv = False
                    for h in G:
                        if g*h == e and h*g == e:
                            has_inv = True
                            break
                    if not has_inv:
                        h1 = False
                        break
                    
                    # Check for closure
                    for h in G:
                        if not any(g*h == k for k in G):
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # H_2: Stab_G(W_1) and Stab_G(W_2) denote their respective setwise stabilizers in G
    try:
        is_list_rep = isinstance(W1, (list, tuple)) and isinstance(W2, (list, tuple))
        is_mat_rep = hasattr(W1, 'row_join') and hasattr(W2, 'row_join') and hasattr(W1, 'rank')
        
        h2 = is_list_rep or is_mat_rep
        if not h2:
            pass
        elif is_list_rep:
            if G and W1: _ = G[0] * W1[0]
            if G and W2: _ = G[0] * W2[0]
        elif is_mat_rep:
            if G: 
                _ = G[0] * W1
                _ = G[0] * W2
    except Exception:
        h2 = False

    # ¬Q: The intersection Stab_G(W_1) \cap Stab_G(W_2) is NOT a subgroup of the setwise stabilizer Stab_G(W_1 + W_2)
    try:
        if is_list_rep:
            def get_unique(W):
                unique_W = []
                for w in W:
                    if not any(w == uw for uw in unique_W):
                        unique_W.append(w)
                return unique_W

            uW1 = get_unique(W1)
            uW2 = get_unique(W2)
            
            def get_stab_list(uW):
                stab = []
                for g in G:
                    is_stab = True
                    for w in uW:
                        gw = g * w
                        if not any(gw == uw for uw in uW):
                            is_stab = False
                            break
                    if is_stab:
                        stab.append(g)
                return stab

            stab1 = get_stab_list(uW1)
            stab2 = get_stab_list(uW2)
            stab_int = [g for g in stab1 if any(g == h for h in stab2)]

            W_sum = []
            for w1 in uW1:
                for w2 in uW2:
                    W_sum.append(w1 + w2)
            
            uW_sum = get_unique(W_sum)
            stab_sum = get_stab_list(uW_sum)

            # Check if stab_int is a subgroup of stab_sum
            is_subgroup = True
            for g in stab_int:
                if not any(g == h for h in stab_sum):
                    is_subgroup = False
                    break
            
            neg_q = not is_subgroup

        elif is_mat_rep:
            def get_stab_mat(W):
                stab = []
                try:
                    rW = W.rank()
                except Exception:
                    rW = len(W.rref()[1])
                for g in G:
                    gW = g * W
                    concat = W.row_join(gW)
                    try:
                        rC = concat.rank()
                    except Exception:
                        rC = len(concat.rref()[1])
                    if rC == rW:
                        stab.append(g)
                return stab

            stab1 = get_stab_mat(W1)
            stab2 = get_stab_mat(W2)
            stab_int = [g for g in stab1 if any(g == h for h in stab2)]

            W_sum = W1.row_join(W2)
            stab_sum = get_stab_mat(W_sum)

            # Check if stab_int is a subgroup of stab_sum
            is_subgroup = True
            for g in stab_int:
                if not any(g == h for h in stab_sum):
                    is_subgroup = False
                    break
            
            neg_q = not is_subgroup
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting linearly on a vector space V",
    "H_2: Stab_G(W_1) and Stab_G(W_2) denote their respective setwise stabilizers in G",
    "¬Q: The intersection Stab_G(W_1) ∩ Stab_G(W_2) is not a subgroup of the setwise stabilizer Stab_G(W_1 + W_2)"
]

N_HYP = 2
NEG_Q_INDEX = 2