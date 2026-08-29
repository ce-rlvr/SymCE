import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness objects
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
    # Extract properties from the witness
    if isinstance(witness, dict):
        N = witness.get('N')
        H = witness.get('H')
        phi = witness.get('phi')
        G = witness.get('G')
        n = witness.get('n')
        h = witness.get('h')
        m = witness.get('m')
    else:
        N = getattr(witness, 'N', None)
        H = getattr(witness, 'H', None)
        phi = getattr(witness, 'phi', None)
        G = getattr(witness, 'G', None)
        n = getattr(witness, 'n', None)
        h = getattr(witness, 'h', None)
        m = getattr(witness, 'm', None)

    def op(group, a, b):
        if hasattr(group, 'op'):
            return group.op(a, b)
        return a * b

    def apply_phi(phi_obj, h_val, n_val):
        if isinstance(phi_obj, dict):
            f = phi_obj[h_val]
        else:
            f = phi_obj(h_val)
        if isinstance(f, dict):
            return f[n_val]
        return f(n_val)

    # H1: N and H are groups
    try:
        def is_group(grp):
            if grp is None: return False
            if hasattr(grp, 'is_group'): return grp.is_group
            if hasattr(grp, 'elements'): return True
            if hasattr(grp, 'op'): return True
            if hasattr(grp, 'is_abelian'): return True
            return False
        h1 = is_group(N) and is_group(H)
    except Exception:
        h1 = False

    # H2: phi: H -> Aut(N) is a group homomorphism
    try:
        h2 = True
        # Check homomorphism property for the provided h
        h2_val = op(H, h, h)
        left = apply_phi(phi, h2_val, n)
        right = apply_phi(phi, h, apply_phi(phi, h, n))
        if left != right:
            h2 = False
        
        # Check automorphism property for the provided n
        n2_val = op(N, n, n)
        left_aut = apply_phi(phi, h, n2_val)
        right_aut = op(N, apply_phi(phi, h, n), apply_phi(phi, h, n))
        if left_aut != right_aut:
            h2 = False
    except Exception:
        h2 = False

    # H3: (n, h) is an element of G
    try:
        if hasattr(G, 'contains'):
            h3 = G.contains((n, h))
        else:
            # Duck-typing check: try to operate (n, h) with itself in G
            _ = op(G, (n, h), (n, h))
            h3 = True
    except Exception:
        h3 = False

    # H4: m is a positive integer
    try:
        h4 = isinstance(m, int) and m > 0
    except Exception:
        h4 = False

    # ¬Q: The m-th power (n, h)^m in G is NOT equal to the semidirect product formula
    try:
        # Compute (n, h)^m in G
        res_G = (n, h)
        for _ in range(m - 1):
            res_G = op(G, res_G, (n, h))
        
        # Compute the formula: (n * phi_h(n) * phi_{h^2}(n) * ... * phi_{h^{m-1}}(n), h^m)
        prod_n = n
        current_h = h
        for i in range(1, m):
            term = apply_phi(phi, current_h, n)
            prod_n = op(N, prod_n, term)
            current_h = op(H, current_h, h)
        
        formula_res = (prod_n, current_h)
        
        # The conclusion FAILS if the power in G does not match the formula
        neg_q = (res_G != formula_res)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi: H -> Aut(N) is a group homomorphism",
    "H_3: (n, h) is an element of G",
    "H_4: m is a positive integer",
    "¬Q: The m-th power (n, h)^m in G is NOT equal to (n phi_h(n) ... phi_{h^{m-1}}(n), h^m)"
]

N_HYP = 4
NEG_Q_INDEX = 4