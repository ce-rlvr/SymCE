import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard named objects for potential witness expressions
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

def get_order(grp):
    try:
        return grp.order()
    except TypeError:
        return grp.order

def conditions(witness):
    """
    Expects witness to be a tuple: (G, alpha, A)
    where:
      - G is a sympy PermutationGroup
      - alpha is an integer representing an element x in the domain X of G
      - A is a sympy PermutationGroup representing the abelian normal subgroup of G_x
    """
    try:
        G, alpha, A = witness
    except Exception:
        return [False] * 5

    # H1: G is a perfect group
    try:
        ds = G.derived_subgroup
        if callable(ds):
            ds = ds()
        h1 = (get_order(ds) == get_order(G)) and (get_order(G) > 1)
    except Exception:
        h1 = False

    # H2: X is a non-empty set
    try:
        h2 = G.degree > 0
    except Exception:
        h2 = False

    # H3: G_x contains A, and A is an abelian normal subgroup of G_x
    try:
        if not (0 <= alpha < G.degree):
            h3 = False
        else:
            G_x = G.stabilizer(alpha)
            
            # Check if A is a subgroup of G_x
            is_sub = True
            for gen in A.generators:
                if not G_x.contains(gen):
                    is_sub = False
                    break
            
            if not is_sub:
                h3 = False
            else:
                # Check if A is abelian
                is_ab = A.is_abelian
                if callable(is_ab):
                    is_ab = is_ab()
                
                # Check if A is normal in G_x
                is_norm = True
                for g in G_x.generators:
                    for a in A.generators:
                        if not A.contains(~g * a * g):
                            is_norm = False
                            break
                    if not is_norm:
                        break
                
                h3 = bool(is_ab and is_norm)
    except Exception:
        h3 = False

    # H4: The conjugates of A in G generate the group G
    try:
        gens_A = list(A.generators)
        if not gens_A:
            h4 = (get_order(G) == 1)
        else:
            closure = PermutationGroup(gens_A)
            while True:
                order = get_order(closure)
                new_gens = list(closure.generators)
                for g in G.generators:
                    for a in closure.generators:
                        new_gens.append(~g * a * g)
                closure = PermutationGroup(new_gens)
                if get_order(closure) == order:
                    break
            h4 = (get_order(closure) == get_order(G))
    except Exception:
        h4 = False

    # neg_Q: G is not a simple group
    try:
        ns = G.normal_subgroups
        if callable(ns):
            ns = ns()
        # A simple group has exactly 2 normal subgroups (trivial and itself).
        # If it has more than 2, it is not simple.
        neg_q = len(ns) > 2
    except Exception:
        try:
            res = G.is_simple
            if callable(res):
                res = res()
            neg_q = not res
        except Exception:
            neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a perfect group",
    "H_2: X is a non-empty set",
    "H_3: There exists an element x in X such that the stabilizer G_x contains an abelian normal subgroup A of G_x",
    "H_4: The conjugates of A in G generate the group G",
    "¬Q: G is not a simple group"
]

N_HYP = 4
NEG_Q_INDEX = 4