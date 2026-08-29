import sympy
from sympy.matrices import eye, zeros, Matrix
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Expected witness format: (G, H, a, b)
    """
    try:
        G, H, a, b = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: H is a subgroup of G
    def is_subgroup(H, G):
        if hasattr(H, 'is_subgroup') and hasattr(G, 'is_group'):
            try:
                return H.is_subgroup(G)
            except Exception:
                pass
        
        try:
            H_list = list(H)
            
            if hasattr(G, 'contains'):
                try:
                    for h in H_list:
                        if not G.contains(h):
                            return False
                except Exception:
                    G_list = list(G)
                    for h in H_list:
                        if not any(h == g for g in G_list):
                            return False
            else:
                G_list = list(G)
                for h in H_list:
                    if not any(h == g for g in G_list):
                        return False
                        
            if len(H_list) == 0:
                return False
            
            # Find identity in H
            identities = []
            for e in H_list:
                is_id = True
                for h in H_list:
                    if not (e * h == h and h * e == h):
                        is_id = False
                        break
                if is_id:
                    identities.append(e)
            if not identities:
                return False
            e = identities[0]
            
            # Check closure and inverses
            for h1 in H_list:
                has_inverse = False
                for h2 in H_list:
                    if h1 * h2 == e and h2 * h1 == e:
                        has_inverse = True
                    
                    prod = h1 * h2
                    if not any(prod == h for h in H_list):
                        return False
                if not has_inverse:
                    return False
            return True
        except Exception:
            return False

    try:
        h1_ok = is_subgroup(H, G)
    except Exception:
        h1_ok = False

    # H_2: a is an element of G
    try:
        if hasattr(G, 'contains'):
            try:
                h2_ok = bool(G.contains(a))
            except Exception:
                h2_ok = any(a == g for g in list(G))
        else:
            h2_ok = any(a == g for g in list(G))
    except Exception:
        h2_ok = False

    # H_3: b is an element of G
    try:
        if hasattr(G, 'contains'):
            try:
                h3_ok = bool(G.contains(b))
            except Exception:
                h3_ok = any(b == g for g in list(G))
        else:
            h3_ok = any(b == g for g in list(G))
    except Exception:
        h3_ok = False

    # Conclusion: aH == bH iff a^{-1}b in H
    try:
        H_elems = list(H)
        
        aH_list = [a * h for h in H_elems]
        bH_list = [b * h for h in H_elems]
        
        cosets_equal = True
        for x in aH_list:
            if not any(x == y for y in bH_list):
                cosets_equal = False
                break
        if cosets_equal:
            for y in bH_list:
                if not any(x == y for x in aH_list):
                    cosets_equal = False
                    break
    except Exception:
        cosets_equal = False

    try:
        a_inv = None
        try:
            a_inv = a**-1
        except Exception:
            try:
                a_inv = ~a
            except Exception:
                try:
                    a_inv = a.inv()
                except Exception:
                    pass
        
        if a_inv is None:
            in_H = False
        else:
            a_inv_b = a_inv * b
            if hasattr(H, 'contains'):
                try:
                    in_H = bool(H.contains(a_inv_b))
                except Exception:
                    in_H = any(a_inv_b == h for h in H_elems)
            else:
                in_H = any(a_inv_b == h for h in H_elems)
    except Exception:
        in_H = False

    try:
        Q = (cosets_equal == in_H)
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [h1_ok, h2_ok, h3_ok, neg_Q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: a is an element of G",
    "H_3: b is an element of G",
    "¬Q: aH == bH is not equivalent to a^{-1}b in H"
]

N_HYP = 3
NEG_Q_INDEX = 3