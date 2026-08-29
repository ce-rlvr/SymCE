import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools
import z3

# Top-level setup for potential witness expressions
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def _get_order(g):
    if hasattr(g, 'order'):
        return g.order() if callable(g.order) else g.order
    raise ValueError("Object has no order attribute")

def conditions(witness) -> list[bool]:
    # H_1: Every maximal subgroup of G has an index in G that is a prime number
    h1_ok = False
    try:
        if hasattr(witness, 'maximal_subgroups'):
            max_subs = witness.maximal_subgroups
            if callable(max_subs):
                max_subs = max_subs()
            
            all_prime = True
            for H in max_subs:
                idx = None
                if hasattr(witness, 'index'):
                    idx_attr = witness.index
                    if callable(idx_attr):
                        try:
                            idx = idx_attr(H)
                        except Exception:
                            pass
                if idx is None:
                    w_order = _get_order(witness)
                    h_order = _get_order(H)
                    idx = w_order // h_order
                
                if not isprime(idx):
                    all_prime = False
                    break
            h1_ok = all_prime
            
        elif hasattr(witness, 'subgroups'):
            subs = witness.subgroups
            if callable(subs):
                subs = subs()
            
            w_order = _get_order(witness)
            proper = [H for H in subs if _get_order(H) < w_order]
            max_subs = []
            for H in proper:
                is_max = True
                h_order = _get_order(H)
                for K in proper:
                    k_order = _get_order(K)
                    if h_order < k_order:
                        is_sub = False
                        if hasattr(H, 'is_subgroup'):
                            is_sub = H.is_subgroup(K)
                        elif hasattr(K, 'has_subgroup'):
                            is_sub = K.has_subgroup(H)
                        if is_sub:
                            is_max = False
                            break
                if is_max:
                    max_subs.append(H)
            
            all_prime = True
            for H in max_subs:
                idx = w_order // _get_order(H)
                if not isprime(idx):
                    all_prime = False
                    break
            h1_ok = all_prime
    except Exception:
        h1_ok = False

    # neg_Q: G is NOT a solvable group
    neg_q_ok = False
    try:
        if hasattr(witness, 'is_solvable'):
            is_solv = witness.is_solvable
            if callable(is_solv):
                is_solv = is_solv()
            neg_q_ok = not bool(is_solv)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Every maximal subgroup of G has an index in G that is a prime number",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1