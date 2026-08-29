import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def eval_phi(phi, h, n):
    if callable(phi):
        return phi(h, n)
    elif isinstance(phi, dict):
        return phi[h][n]
    else:
        raise ValueError("phi must be callable or dict")

def is_valid_action(N, H, phi):
    try:
        for h in H.elements:
            for n1 in N.elements:
                for n2 in N.elements:
                    if eval_phi(phi, h, n1 * n2) != eval_phi(phi, h, n1) * eval_phi(phi, h, n2):
                        return False
        for h1 in H.elements:
            for h2 in H.elements:
                for n in N.elements:
                    if eval_phi(phi, h1 * h2, n) != eval_phi(phi, h1, eval_phi(phi, h2, n)):
                        return False
        for n in N.elements:
            if eval_phi(phi, H.identity, n) != n:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        N, H, phi = witness
    except Exception:
        return [False, False, False]
    
    # H1: N is an abelian group
    try:
        h1_ok = isinstance(N, PermutationGroup) and N.is_abelian
    except Exception:
        h1_ok = False
        
    # H2: H is a group
    try:
        h2_ok = isinstance(H, PermutationGroup)
    except Exception:
        h2_ok = False
        
    # neg_Q: The center of N \rtimes H is NOT equal to S
    try:
        if not is_valid_action(N, H, phi):
            neg_q_ok = False
        else:
            G_elements = [(n, h) for n in N.elements for h in H.elements]
            Z_G = []
            for g in G_elements:
                is_center = True
                for x in G_elements:
                    gx_0 = g[0] * eval_phi(phi, g[1], x[0])
                    gx_1 = g[1] * x[1]
                    
                    xg_0 = x[0] * eval_phi(phi, x[1], g[0])
                    xg_1 = x[1] * g[1]
                    
                    if gx_0 != xg_0 or gx_1 != xg_1:
                        is_center = False
                        break
                if is_center:
                    Z_G.append(g)
            
            S = []
            for n in N.elements:
                fixed_by_all = True
                for h in H.elements:
                    if eval_phi(phi, h, n) != n:
                        fixed_by_all = False
                        break
                if fixed_by_all:
                    S.append((n, H.identity))
            
            neg_q_ok = set(Z_G) != set(S)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: N is an abelian group",
    "H_2: H is a group",
    "¬Q: The center of N \\rtimes_\\phi H is not equal to the subgroup of elements (n, 1_H) such that n is fixed by all \\phi_h"
]

N_HYP = 2
NEG_Q_INDEX = 2