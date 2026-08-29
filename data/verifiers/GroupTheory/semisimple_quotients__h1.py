import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def get_bool_prop(objs, prop_names, default=None, args=None):
    """Helper to extract boolean properties from mock objects or dictionaries."""
    for obj in objs:
        if obj is None:
            continue
        if isinstance(obj, dict):
            for p in prop_names:
                if p in obj:
                    val = obj[p]
                    if callable(val):
                        try:
                            return val(*args) if args else val()
                        except TypeError:
                            try:
                                return val()
                            except Exception:
                                pass
                        except Exception:
                            pass
                    else:
                        return val
        for p in prop_names:
            if hasattr(obj, p):
                val = getattr(obj, p)
                if callable(val):
                    try:
                        return val(*args) if args else val()
                    except TypeError:
                        try:
                            return val()
                        except Exception:
                            pass
                    except Exception:
                        pass
                else:
                    return val
    return default

def conditions(witness):
    if callable(witness):
        try:
            witness = witness()
        except Exception:
            pass

    G, N = None, None
    if isinstance(witness, tuple) and len(witness) == 2:
        G, N = witness
    elif hasattr(witness, 'G') and hasattr(witness, 'N'):
        G = witness.G
        N = witness.N
    else:
        G = witness
        N = None

    # H1: G is isomorphic to a direct product of non-abelian simple groups
    h1_props = [
        'is_dp_nonabelian_simple',
        'is_direct_product_of_nonabelian_simple_groups',
        'is_semisimple',
        'is_direct_product_of_simple_groups'
    ]
    h1 = get_bool_prop([witness, G], h1_props, default=None)
    if h1 is None:
        try:
            is_triv = G.is_trivial() if callable(G.is_trivial) else G.is_trivial
            if is_triv:
                h1 = True
            else:
                is_perf = G.is_perfect() if callable(G.is_perfect) else G.is_perfect
                center = G.center() if callable(G.center) else G.center
                c_is_triv = center.is_trivial() if callable(center.is_trivial) else center.is_trivial
                h1 = is_perf and c_is_triv
        except Exception:
            h1 = False

    # H2: N is a normal subgroup of G
    h2_props = [
        'is_normal_subgroup',
        'has_normal_subgroup'
    ]
    h2 = get_bool_prop([witness, G], h2_props, default=None, args=[N] if N is not None else [])
    if h2 is None:
        h2 = get_bool_prop([N], ['is_normal'], default=None, args=[G] if G is not None else [])
    if h2 is None:
        h2 = False

    # Q: G/N is either the trivial group or isomorphic to a direct product of non-abelian simple groups
    q_props = [
        'quotient_is_trivial_or_dp',
        'is_quotient_dp_nonabelian_simple',
        'quotient_is_semisimple'
    ]
    q = get_bool_prop([witness, G], q_props, default=None, args=[N] if N is not None else [])
    if q is None:
        try:
            if hasattr(G, 'quotient'):
                Q_grp = G.quotient(N)
            else:
                Q_grp = G / N
            
            is_triv = Q_grp.is_trivial() if callable(Q_grp.is_trivial) else Q_grp.is_trivial
            if is_triv:
                q = True
            else:
                is_perf = Q_grp.is_perfect() if callable(Q_grp.is_perfect) else Q_grp.is_perfect
                center = Q_grp.center() if callable(Q_grp.center) else Q_grp.center
                c_is_triv = center.is_trivial() if callable(center.is_trivial) else center.is_trivial
                q = is_perf and c_is_triv
        except Exception:
            q = True

    return [bool(h1), bool(h2), not bool(q)]

CONDITION_LABELS = [
    "H_1: G is isomorphic to a direct product of non-abelian simple groups",
    "H_2: N is a normal subgroup of G",
    "¬Q: The quotient group G/N is neither the trivial group nor isomorphic to a direct product of non-abelian simple groups"
]

N_HYP = 2
NEG_Q_INDEX = 2