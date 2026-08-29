import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros, MatrixBase

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

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False, False, False]

    # Safely extract elements of G into a list (up to a limit to prevent hanging on infinite sets)
    try:
        G_list = []
        for i, x in enumerate(G):
            if i > 2000:
                G_list = None
                break
            if not any(x == y for y in G_list):
                G_list.append(x)
    except Exception:
        G_list = None

    # Safely extract elements of H into a list
    try:
        H_list = []
        for i, x in enumerate(H):
            if i > 2000:
                H_list = None
                break
            if not any(x == y for y in H_list):
                H_list.append(x)
    except Exception:
        H_list = None

    # H_1: H is a non-empty subset of G
    try:
        if H_list is None:
            h1 = False
        else:
            h1 = len(H_list) > 0
            if h1:
                try:
                    is_subset = all(h in G for h in H_list)
                except Exception:
                    if G_list is not None:
                        is_subset = all(any(h == g for g in G_list) for h in H_list)
                    else:
                        is_subset = False
                h1 = h1 and is_subset
    except Exception:
        h1 = False

    # H_2: H is finite
    try:
        h2 = H_list is not None
    except Exception:
        h2 = False

    # H_3: For all a, b \in H, the product ab is in H
    try:
        if H_list is None:
            h3 = False
        else:
            h3 = True
            for a in H_list:
                for b in H_list:
                    try:
                        ab = a * b
                    except Exception:
                        h3 = False
                        break
                    if not any(ab == x for x in H_list):
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # ¬Q: H is not a subgroup of G
    try:
        if H_list is None:
            neg_q = False
        else:
            def is_group(S_list):
                if not S_list: 
                    return False
                # Closure
                for a in S_list:
                    for b in S_list:
                        try:
                            ab = a * b
                        except Exception:
                            return False
                        if not any(ab == x for x in S_list):
                            return False
                # Associativity (skip O(N^3) check for known associative types to ensure speed)
                is_known_associative = all(isinstance(x, (MatrixBase, Permutation, int, float, complex, sympy.Expr)) for x in S_list)
                if not is_known_associative:
                    for a in S_list:
                        for b in S_list:
                            try:
                                ab = a * b
                            except Exception:
                                return False
                            for c in S_list:
                                try:
                                    if not ((ab * c) == (a * (b * c))):
                                        return False
                                except Exception:
                                    return False
                # Identity
                identities = []
                for e in S_list:
                    is_id = True
                    for a in S_list:
                        try:
                            if not (e * a == a) or not (a * e == a):
                                is_id = False
                                break
                        except Exception:
                            is_id = False
                            break
                    if is_id:
                        identities.append(e)
                if not identities:
                    return False
                e = identities[0]
                # Inverses
                for a in S_list:
                    has_inv = False
                    for b in S_list:
                        try:
                            if (a * b == e) and (b * a == e):
                                has_inv = True
                                break
                        except Exception:
                            pass
                    if not has_inv:
                        return False
                return True

            h_is_group = is_group(H_list)
            if not h_is_group:
                # If H is not a group, it cannot be a subgroup
                neg_q = True
            else:
                if G_list is None:
                    # If G is infinite or un-iterable, we can't easily verify if it's a group.
                    # We conservatively return False to avoid falsely accepting an invalid witness.
                    neg_q = False
                else:
                    g_is_group = is_group(G_list)
                    is_subgroup = g_is_group
                    if is_subgroup:
                        # Check subset property explicitly
                        is_subset = all(any(h == g for g in G_list) for h in H_list)
                        if not is_subset:
                            is_subgroup = False
                        else:
                            # Check if they share the same identity
                            e_G = None
                            for e in G_list:
                                try:
                                    if all((e * a == a) and (a * e == a) for a in G_list):
                                        e_G = e
                                        break
                                except Exception:
                                    pass
                            e_H = None
                            for e in H_list:
                                try:
                                    if all((e * a == a) and (a * e == a) for a in H_list):
                                        e_H = e
                                        break
                                except Exception:
                                    pass
                            if not (e_G == e_H):
                                is_subgroup = False
                    neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a non-empty subset of G",
    "H_2: H is finite",
    "H_3: For all a, b in H, the product ab is in H",
    "¬Q: H is not a subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3