import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: G = N \\rtimes_\\phi H is the external semidirect product",
    "H_3: \\tilde{N} = N \\times \\{1_H\\} is the base subgroup in G",
    "¬Q: The map K \\mapsto N \\rtimes_{\\phi|_K} K does not define a lattice isomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            N = witness['N']
            H = witness['H']
            N_mul = witness['N_mul']
            H_mul = witness['H_mul']
            N_id = witness['N_id']
            H_id = witness['H_id']
            phi = witness['phi']
        else:
            N = witness.N
            H = witness.H
            N_mul = witness.N_mul
            H_mul = witness.H_mul
            N_id = witness.N_id
            H_id = witness.H_id
            phi = witness.phi
    except Exception:
        return [False, False, False, False]

    def is_group_general(elements, mul, identity):
        if identity not in elements:
            return False
        for a in elements:
            for b in elements:
                try:
                    if mul(a, b) not in elements:
                        return False
                except Exception:
                    return False
        for a in elements:
            try:
                if mul(identity, a) != a or mul(a, identity) != a:
                    return False
            except Exception:
                return False
        for a in elements:
            has_inv = False
            for b in elements:
                try:
                    if mul(a, b) == identity and mul(b, a) == identity:
                        has_inv = True
                        break
                except Exception:
                    pass
            if not has_inv:
                return False
        for a in elements:
            for b in elements:
                try:
                    ab = mul(a, b)
                    for c in elements:
                        if mul(ab, c) != mul(a, mul(b, c)):
                            return False
                except Exception:
                    return False
        return True

    try:
        h1 = is_group_general(N, N_mul, N_id) and is_group_general(H, H_mul, H_id)
    except Exception:
        h1 = False

    try:
        G = list(itertools.product(N, H))
        def G_mul(x, y):
            n1, h1 = x
            n2, h2 = y
            return (N_mul(n1, phi(h1, n2)), H_mul(h1, h2))
        
        phi_well_defined = True
        for h in H:
            for n in N:
                if phi(h, n) not in N:
                    phi_well_defined = False
                    break
        h2 = phi_well_defined
    except Exception:
        h2 = False

    try:
        N_tilde = [(n, H_id) for n in N]
        h3 = is_group_general(N_tilde, G_mul, (N_id, H_id))
    except Exception:
        h3 = False

    try:
        # The conclusion holds if and only if G is a valid group.
        # If G is not a group, the map sends H to G, which is not a subgroup of G,
        # so the map is not well-defined and cannot be a lattice isomorphism.
        neg_Q = not is_group_general(G, G_mul, (N_id, H_id))
    except Exception:
        neg_Q = False

    return [h1, h2, h3, neg_Q]