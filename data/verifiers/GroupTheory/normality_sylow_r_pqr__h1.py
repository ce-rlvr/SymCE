import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime, factorint
import math
import itertools
import functools

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_normal_subgroup(G, H):
    """Check if H is a normal subgroup of G."""
    for g in G.generators:
        g_inv = ~g
        for h in H.generators:
            conj = g * h * g_inv
            if conj not in H:
                return False
    return True

def get_pqr(witness):
    """
    Extracts (G, p, q, r) from the witness.
    If the witness is just a group, attempts to infer p, q, r such that
    the Sylow r-subgroup is not normal (to act as a valid counterexample).
    """
    if isinstance(witness, tuple) and len(witness) == 4:
        return witness
    elif hasattr(witness, 'order'):
        G = witness
        try:
            order = G.order()
            factors = factorint(order)
            primes = []
            for prime, mult in factors.items():
                primes.extend([prime] * mult)
            
            if len(primes) == 3:
                # Try to find a prime r such that the Sylow r-subgroup is NOT normal
                for r in set(primes):
                    try:
                        S = G.sylow_subgroup(r)
                        if not is_normal_subgroup(G, S):
                            p_q = primes[:]
                            p_q.remove(r)
                            return G, p_q[0], p_q[1], r
                    except Exception:
                        pass
                # If all are normal or check fails, just return any assignment
                return G, primes[0], primes[1], primes[2]
        except Exception:
            pass
    return None, None, None, None

def conditions(witness) -> list[bool]:
    H1 = False
    neg_Q = False
    
    G, p, q, r = None, None, None, None
    try:
        G, p, q, r = get_pqr(witness)
    except Exception:
        pass

    # Check H1: G is a finite group of order pqr
    try:
        if G is not None and hasattr(G, 'order') and hasattr(G, 'generators'):
            if isprime(p) and isprime(q) and isprime(r):
                if G.order() == p * q * r:
                    H1 = True
    except Exception:
        pass

    # Check neg_Q: The Sylow r-subgroup of G is NOT normal in G
    try:
        if H1 and G is not None:
            S = G.sylow_subgroup(r)
            if not is_normal_subgroup(G, S):
                neg_Q = True
    except Exception:
        pass

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a finite group of order pqr",
    "¬Q: The Sylow r-subgroup of G is not normal in G"
]

N_HYP = 1
NEG_Q_INDEX = 1