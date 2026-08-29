import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import itertools

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

def conditions(witness):
    try:
        G1 = witness['G1']
        N1 = witness['N1']
        H1 = witness['H1']
        phi1 = witness['phi1']
        G2 = witness['G2']
        N2 = witness['N2']
        H2 = witness['H2']
        phi2 = witness['phi2']
    except (KeyError, TypeError):
        return [False, False]

    def apply_phi(phi, h, n):
        if callable(phi):
            return phi(h, n)
        else:
            return phi[h][n]

    def get_perm_group(elements, mult):
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        perms = []
        for g in elements:
            p = []
            for x in elements:
                try:
                    gx = mult(g, x)
                    idx = elem_to_idx[gx]
                except Exception:
                    return None
                p.append(idx)
            try:
                perms.append(Permutation(p))
            except ValueError:
                return None
        try:
            G = PermutationGroup(perms)
            if G.order() != len(elements):
                return None
            return G
        except Exception:
            return None

    def build_sdp(N, H, phi):
        try:
            N_elems = list(N.elements)
            H_elems = list(H.elements)
            elements = list(itertools.product(N_elems, H_elems))
            def sdp_mult(x, y):
                n1, h1 = x
                n2, h2 = y
                n2_prime = apply_phi(phi, h1, n2)
                return (n1 * n2_prime, h1 * h2)
            return get_perm_group(elements, sdp_mult)
        except Exception:
            return None

    # H_1: G2 = N2 \rtimes_{\phi_2} H2 is a semidirect product
    try:
        sdp2 = build_sdp(N2, H2, phi2)
        if sdp2 is None:
            h1_ok = False
        else:
            h1_ok = G2.is_isomorphic(sdp2)
    except Exception:
        h1_ok = False

    # neg_Q: G1 x G2 is NOT isomorphic to (N1 x N2) \rtimes (H1 x H2)
    try:
        def build_dp(A, B):
            A_elems = list(A.elements)
            B_elems = list(B.elements)
            elements = list(itertools.product(A_elems, B_elems))
            def dp_mult(x, y):
                return (x[0] * y[0], x[1] * y[1])
            return get_perm_group(elements, dp_mult)

        def build_rhs(N1, H1, phi1, N2, H2, phi2):
            N1_elems = list(N1.elements)
            H1_elems = list(H1.elements)
            N2_elems = list(N2.elements)
            H2_elems = list(H2.elements)
            
            elements = []
            for n1 in N1_elems:
                for n2 in N2_elems:
                    for h1 in H1_elems:
                        for h2 in H2_elems:
                            elements.append(((n1, n2), (h1, h2)))
                            
            def rhs_mult(x, y):
                n1, n2 = x[0]
                h1, h2 = x[1]
                n1_prime, n2_prime = y[0]
                h1_prime, h2_prime = y[1]
                
                n1_act = apply_phi(phi1, h1, n1_prime)
                n2_act = apply_phi(phi2, h2, n2_prime)
                
                res_n = (n1 * n1_act, n2 * n2_act)
                res_h = (h1 * h1_prime, h2 * h2_prime)
                return (res_n, res_h)
                
            return get_perm_group(elements, rhs_mult)

        lhs = build_dp(G1, G2)
        rhs = build_rhs(N1, H1, phi1, N2, H2, phi2)
        
        if lhs is None:
            neg_q = False
        elif rhs is None:
            neg_q = True
        else:
            neg_q = not lhs.is_isomorphic(rhs)
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G2 is a semidirect product of N2 and H2",
    "¬Q: G1 x G2 is not isomorphic to (N1 x N2) rtimes (H1 x H2)"
]

N_HYP = 1
NEG_Q_INDEX = 1