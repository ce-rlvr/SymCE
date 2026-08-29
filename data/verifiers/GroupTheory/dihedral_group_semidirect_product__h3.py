import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_dihedral(G, n):
    try:
        if not isinstance(G, PermutationGroup):
            return False
        if G.order() != 2 * n:
            return False
        elements = list(G.elements)
        order_n_elements = [g for g in elements if g.order() == n]
        if not order_n_elements:
            return False
        r = order_n_elements[0]
        C = set()
        curr = r**0
        for _ in range(n):
            C.add(curr)
            curr = curr * r
        for g in elements:
            if g not in C:
                if g.order() != 2:
                    return False
        return True
    except Exception:
        return False

def get_k(phi, n):
    try:
        if isinstance(phi, int) or (hasattr(phi, 'is_Integer') and phi.is_Integer):
            return int(phi) % n
    except Exception:
        pass
    
    if isinstance(phi, (dict, list, tuple)):
        try:
            aut = phi[1]
            if isinstance(aut, int) or (hasattr(aut, 'is_Integer') and aut.is_Integer):
                return int(aut) % n
            if isinstance(aut, (dict, list, tuple)):
                return int(aut[1]) % n
            if hasattr(aut, '__call__'):
                return int(aut(1)) % n
        except Exception:
            pass
        try:
            return int(phi[1]) % n
        except Exception:
            pass

    if hasattr(phi, '__call__'):
        try:
            aut = phi(1)
            if isinstance(aut, int) or (hasattr(aut, 'is_Integer') and aut.is_Integer):
                return int(aut) % n
            if isinstance(aut, (dict, list, tuple)):
                return int(aut[1]) % n
            if hasattr(aut, '__call__'):
                return int(aut(1)) % n
        except Exception:
            pass
        try:
            return int(phi(1)) % n
        except Exception:
            pass

    return None

def conditions(witness) -> list[bool]:
    n, D2n, phi = None, None, None
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            D2n = witness.get('D2n')
            phi = witness.get('phi')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                n, D2n, phi = witness
            elif len(witness) == 2:
                n = witness[0]
                if hasattr(witness[1], 'is_group') or hasattr(witness[1], 'elements') or isinstance(witness[1], PermutationGroup):
                    D2n = witness[1]
                else:
                    phi = witness[1]
            elif len(witness) == 1:
                n = witness[0]
        else:
            n = witness
    except Exception:
        pass

    try:
        h1_ok = (isinstance(n, int) or (hasattr(n, 'is_Integer') and n.is_Integer)) and int(n) >= 3
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            h2_ok = False
        else:
            if D2n is None:
                h2_ok = True
            else:
                h2_ok = is_dihedral(D2n, int(n))
    except Exception:
        h2_ok = False

    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            n_int = int(n)
            k = get_k(phi, n_int)
            if k is None:
                # If phi is not provided, we assume the trivial homomorphism
                # which makes the semidirect product a direct product (abelian),
                # thus not isomorphic to D_{2n} (non-abelian for n >= 3).
                k = 1
            
            if (k * k) % n_int != 1:
                # Not a valid homomorphism, so not isomorphic to D2n
                neg_q_ok = True
            else:
                # Valid semidirect product. Is it isomorphic to D2n?
                # It is isomorphic iff k == n - 1 (or k == -1 mod n)
                if k % n_int == (n_int - 1) % n_int:
                    neg_q_ok = False
                else:
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "H_2: D_{2n} is the dihedral group of order 2n",
    "¬Q: D_{2n} is NOT isomorphic to the external semidirect product Z_n \\rtimes_\\phi Z_2"
]

N_HYP = 2
NEG_Q_INDEX = 2