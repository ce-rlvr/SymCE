import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_trivial_subgroup(G):
    """Returns the trivial subgroup {1} of G."""
    return PermutationGroup([G.identity])

def get_gamma(G, i):
    """
    Computes the i-th term of the lower central series of G.
    \gamma_1(G) = G, \gamma_2(G) = [G, G], etc.
    """
    if i <= 0:
        return G
    lcs = G.lower_central_series()
    if i - 1 < len(lcs):
        return lcs[i - 1]
    return get_trivial_subgroup(G)

def get_Z(G, j):
    """
    Computes the j-th term of the upper central series of G.
    Z_0(G) = {1}, Z_1(G) = Z(G), etc.
    """
    if j <= 0:
        return get_trivial_subgroup(G)
    
    Z = get_trivial_subgroup(G)
    all_elements = list(G.generate())
    
    for _ in range(j):
        elements = []
        for x in all_elements:
            in_Z = True
            for g in G.generators:
                # Commutator [x, g] = x^-1 * g^-1 * x * g
                comm = (~x) * (~g) * x * g
                if comm not in Z:
                    in_Z = False
                    break
            if in_Z:
                elements.append(x)
                
        next_Z = PermutationGroup(elements) if elements else get_trivial_subgroup(G)
        if next_Z.order() == Z.order():
            break
        Z = next_Z
        
    return Z

def check_subgroup(H, G_super):
    """Checks if H is a subgroup of G_super."""
    for g in H.generators:
        if g not in G_super:
            return False
    return True

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a group G, a tuple (G, i), or a tuple (G, c, i).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, c_wit, i = witness
                check_all = False
            elif len(witness) == 2:
                G, i = witness
                c_wit = None
                check_all = False
            else:
                return [False, False, False, False]
        else:
            G = witness
            c_wit = None
            i = None
            check_all = True
    except Exception:
        return [False, False, False, False]

    # H_1: G is a nilpotent group of nilpotency class c
    try:
        is_nilp = bool(G.is_nilpotent)
        actual_c = G.nilpotency_class
        if c_wit is not None:
            h1 = is_nilp and (actual_c == c_wit)
            c = c_wit
        else:
            h1 = is_nilp
            c = actual_c
    except Exception:
        h1 = False
        c = 0

    # H_2: \gamma_i(G) denotes the i-th term of the lower central series of G
    h2 = True

    # H_3: Z_j(G) denotes the j-th term of the upper central series of G
    h3 = True

    # neg_Q: \gamma_i(G) is NOT a subgroup of Z_{c-i+1}(G)
    try:
        if not h1:
            neg_q = False
        else:
            if check_all:
                all_subgroups = True
                # Check for all valid indices i
                for idx in range(1, c + 2):
                    gamma_idx = get_gamma(G, idx)
                    Z_j = get_Z(G, c - idx + 1)
                    if not check_subgroup(gamma_idx, Z_j):
                        all_subgroups = False
                        break
                neg_q = not all_subgroups
            else:
                gamma_i = get_gamma(G, i)
                Z_j = get_Z(G, c - i + 1)
                neg_q = not check_subgroup(gamma_i, Z_j)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group of nilpotency class c",
    "H_2: \\gamma_i(G) denotes the i-th term of the lower central series of G",
    "H_3: Z_j(G) denotes the j-th term of the upper central series of G",
    "¬Q: \\gamma_i(G) is not a subgroup of Z_{c-i+1}(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3