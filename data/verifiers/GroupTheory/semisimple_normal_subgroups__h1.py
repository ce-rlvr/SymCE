import sympy
import sympy.combinatorics as combinatorics
import sympy.combinatorics.named_groups as named_groups
import sympy.combinatorics.permutations as permutations
import sympy.matrices as matrices
import sympy.ntheory as ntheory
import sympy.abc as abc
import sympy.polys as polys
import z3
import math
import itertools
import functools

S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
V4 = named_groups.AlternatingGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)

I2 = matrices.eye(2)
I3 = matrices.eye(3)
O2 = matrices.zeros(2, 2)
O3 = matrices.zeros(3, 3)

def get_order(grp):
    try:
        o = getattr(grp, 'order', 1)
        return o() if callable(o) else o
    except Exception:
        return 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, N, factors = witness
            else:
                G, N = witness[0], witness[1]
                factors = None
        else:
            G = getattr(witness, 'G', None)
            N = getattr(witness, 'N', None)
            factors = getattr(witness, 'factors', None)
    except Exception:
        return [False, False, False]

    if G is None or N is None or factors is None:
        return [False, False, False]

    # H1: G is isomorphic to a direct product of non-abelian simple groups S_1 x ... x S_k
    h1_ok = False
    try:
        is_non_abelian_simple = True
        for f in factors:
            is_abelian_attr = getattr(f, 'is_abelian', True)
            is_abelian_val = is_abelian_attr() if callable(is_abelian_attr) else is_abelian_attr
            if is_abelian_val:
                is_non_abelian_simple = False
                break
            
            is_simple_attr = getattr(f, 'is_simple', False)
            is_simple_val = is_simple_attr() if callable(is_simple_attr) else is_simple_attr
            if not is_simple_val:
                is_non_abelian_simple = False
                break
        
        if is_non_abelian_simple:
            expected_order = 1
            for f in factors:
                expected_order *= get_order(f)
            if get_order(G) == expected_order:
                if get_order(G.derived_subgroup()) == get_order(G) and get_order(G.center()) == 1:
                    h1_ok = True
    except Exception:
        h1_ok = False

    # H2: N is a normal subgroup of G
    h2_ok = False
    try:
        is_sub = True
        for n in N.generators:
            if n not in G:
                is_sub = False
                break
        if is_sub:
            is_norm = True
            for g in G.generators:
                g_inv = g**-1
                for n in N.generators:
                    if (g * n * g_inv) not in N:
                        is_norm = False
                        break
                if not is_norm:
                    break
            if is_norm:
                h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: N is NOT trivial AND N is NOT isomorphic to a direct product of a subset of the SET of simple factors
    neg_q_ok = False
    try:
        if get_order(N) > 1:
            unique_factors = []
            for f in factors:
                if not any(get_order(uf) == get_order(f) for uf in unique_factors):
                    unique_factors.append(f)
            
            is_isomorphic_to_subset = False
            for r in range(len(unique_factors) + 1):
                for subset in itertools.combinations(unique_factors, r):
                    subset_order = 1
                    for f in subset:
                        subset_order *= get_order(f)
                    
                    if get_order(N) == subset_order:
                        is_isomorphic_to_subset = True
                        break
                if is_isomorphic_to_subset:
                    break
            
            if not is_isomorphic_to_subset:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is isomorphic to a direct product of non-abelian simple groups S_1 x ... x S_k",
    "H_2: N is a normal subgroup of G",
    "¬Q: N is not the trivial subgroup and not isomorphic to a direct product of a subset of the simple factors"
]

N_HYP = 2
NEG_Q_INDEX = 2