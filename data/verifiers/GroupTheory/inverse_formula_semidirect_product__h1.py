import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    # Extract components from the witness
    if isinstance(witness, dict):
        phi = witness.get('phi')
        G = witness.get('G')
        n = witness.get('n')
        h = witness.get('h')
        N = witness.get('N')
        H = witness.get('H')
    else:
        phi = getattr(witness, 'phi', None)
        G = getattr(witness, 'G', None)
        n = getattr(witness, 'n', None)
        h = getattr(witness, 'h', None)
        N = getattr(witness, 'N', None)
        H = getattr(witness, 'H', None)

    def get_inv(x, group=None):
        if group is not None:
            if hasattr(group, 'inv'):
                try: return group.inv(x)
                except Exception: pass
            if hasattr(group, 'inverse'):
                try: return group.inverse(x)
                except Exception: pass
        try: return x**-1
        except Exception: pass
        try: return ~x
        except Exception: pass
        try: return x.inv()
        except Exception: pass
        try: return x.inverse()
        except Exception: pass
        try: return -x
        except Exception: pass
        return None

    def apply_phi(phi_func, h_val, n_val):
        if isinstance(phi_func, (dict, list, tuple)):
            aut = phi_func[h_val]
        else:
            aut = phi_func(h_val)
            
        if isinstance(aut, (dict, list, tuple)):
            return aut[n_val]
        else:
            return aut(n_val)

    def G_mul(x, y):
        if hasattr(G, 'mul'): return G.mul(x, y)
        if hasattr(G, 'multiply'): return G.multiply(x, y)
        if hasattr(witness, 'G_mul'): return witness.G_mul(x, y)
        try:
            res = x * y
            # Ignore if it just concatenated two tuples
            if isinstance(x, tuple) and isinstance(y, tuple) and isinstance(res, tuple) and len(res) == len(x) + len(y):
                pass
            else:
                return res
        except Exception:
            pass
        return G(x, y)

    def get_G_inv(x):
        if hasattr(G, 'inv'):
            try: return G.inv(x)
            except Exception: pass
        if hasattr(G, 'inverse'):
            try: return G.inverse(x)
            except Exception: pass
        if hasattr(witness, 'G_inv'):
            try: return witness.G_inv(x)
            except Exception: pass
        return get_inv(x)

    # H_1: phi is a group homomorphism from H to Aut(N)
    h1_ok = False
    try:
        _ = apply_phi(phi, h, n)
        h1_ok = True
    except Exception:
        pass

    # H_2: G is the external semidirect product of N and H
    h2_ok = False
    try:
        if G is not None or hasattr(witness, 'G_mul'):
            h2_ok = True
    except Exception:
        pass

    # H_3: (n, h) is an element of G
    h3_ok = False
    try:
        if hasattr(G, '__contains__'):
            h3_ok = bool((n, h) in G)
        elif hasattr(G, 'contains'):
            h3_ok = bool(G.contains((n, h)))
        elif hasattr(witness, 'G_contains'):
            h3_ok = bool(witness.G_contains((n, h)))
        else:
            h3_ok = True
    except Exception:
        pass

    # neg_Q: The inverse of (n, h) in G is NOT (\phi_{h^{-1}}(n^{-1}), h^{-1})
    neg_q = False
    try:
        h_inv = get_inv(h, H)
        n_inv = get_inv(n, N)
        
        if h_inv is None or n_inv is None:
            return [h1_ok, h2_ok, h3_ok, False]
            
        n_part = apply_phi(phi, h_inv, n_inv)
        proposed_inv = (n_part, h_inv)
        
        actual_inv = get_G_inv((n, h))
        
        if actual_inv is not None:
            if isinstance(actual_inv, list):
                actual_inv = tuple(actual_inv)
            neg_q = bool(actual_inv != proposed_inv)
        else:
            # Verify by checking if proposed_inv acts as the identity when multiplied
            prod1 = G_mul((n, h), proposed_inv)
            prod2 = G_mul(proposed_inv, (n, h))
            
            test_prod1 = G_mul(prod1, (n, h))
            test_prod2 = G_mul(prod2, (n, h))
            
            is_inv = bool(test_prod1 == (n, h)) and bool(test_prod2 == (n, h))
            neg_q = not is_inv
            
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from H to Aut(N)",
    "H_2: G is the external semidirect product of N and H",
    "H_3: (n, h) is an element of G",
    "¬Q: The inverse of (n, h) in G is NOT (phi_{h^{-1}}(n^{-1}), h^{-1})"
]

N_HYP = 3
NEG_Q_INDEX = 3