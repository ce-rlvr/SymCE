import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools
import z3

# Top-level setup for standard algebra objects
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

def check_is_hall(G, S, pi):
    if hasattr(G, 'is_hall_subgroup'):
        res = G.is_hall_subgroup(S, pi)
        if res is not None: return res
    if hasattr(S, 'is_hall_subgroup'):
        res = S.is_hall_subgroup(G, pi)
        if res is not None: return res
    if hasattr(S, 'is_hall'):
        res = S.is_hall(pi)
        if res is not None: return res
        
    if not S.is_subgroup(G):
        return False
    s_ord = S.order()
    g_ord = G.order()
    if s_ord == sympy.oo or g_ord == sympy.oo:
        raise ValueError("Cannot compute Hall property for infinite groups without custom methods")
        
    for p in sympy.ntheory.primefactors(s_ord):
        if p not in pi:
            return False
    idx = g_ord // s_ord
    for p in sympy.ntheory.primefactors(idx):
        if p in pi:
            return False
    return True

def check_conjugate(G, H, K):
    if hasattr(G, 'are_conjugate_subgroups'):
        res = G.are_conjugate_subgroups(H, K)
        if res is not None: return res
    if hasattr(H, 'is_conjugate'):
        res = H.is_conjugate(K)
        if res is not None: return res
    
    g_ord = G.order()
    if g_ord == sympy.oo or g_ord > 5000:
        raise ValueError("Group too large to check conjugacy manually")
        
    for g in G.generate():
        conj_gens = [g**-1 * h * g for h in H.generators]
        H_g = sympy.combinatorics.PermutationGroup(conj_gens)
        if H_g == K:
            return True
    return False

def conditions(witness):
    # If witness is a custom object that provides a 'conditions' method, use it directly
    if hasattr(witness, 'conditions') and callable(witness.conditions):
        try:
            return witness.conditions()
        except Exception:
            pass

    try:
        if hasattr(witness, 'G'):
            G = witness.G
            pi = witness.pi
            H = witness.H
            K = witness.K
        else:
            G, pi, H, K = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a solvable group
    try:
        if hasattr(G, 'is_solvable'):
            h1 = G.is_solvable() if callable(G.is_solvable) else G.is_solvable
        elif hasattr(witness, 'is_solvable'):
            h1 = witness.is_solvable() if callable(witness.is_solvable) else witness.is_solvable
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: pi is a set of prime numbers
    try:
        if hasattr(witness, 'is_pi_set'):
            h2 = witness.is_pi_set() if callable(witness.is_pi_set) else witness.is_pi_set
        else:
            h2 = isinstance(pi, (set, frozenset, list, tuple)) and all(sympy.isprime(p) for p in pi)
    except Exception:
        h2 = False

    # H_3: H and K are Hall pi-subgroups of G
    try:
        if hasattr(witness, 'are_hall_subgroups'):
            h3 = witness.are_hall_subgroups() if callable(witness.are_hall_subgroups) else witness.are_hall_subgroups
        else:
            h3 = check_is_hall(G, H, pi) and check_is_hall(G, K, pi)
    except Exception:
        h3 = False

    # ¬Q: H and K are not conjugate in G
    try:
        if hasattr(witness, 'are_conjugate'):
            are_conj = witness.are_conjugate() if callable(witness.are_conjugate) else witness.are_conjugate
            neg_q = not are_conj
        else:
            are_conj = check_conjugate(G, H, K)
            neg_q = not are_conj
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a solvable group",
    "H_2: pi is a set of prime numbers",
    "H_3: H and K are Hall pi-subgroups of G",
    "¬Q: H and K are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3