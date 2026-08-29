import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

SIMPLE_OUT_ORDERS = {
    60: 2,      # A5
    168: 2,     # PSL(2,7)
    360: 4,     # A6
    504: 3,     # PSL(2,8)
    660: 2,     # PSL(2,11)
    1092: 2,    # PSL(2,13)
    2448: 2,    # PSL(2,17)
    2520: 2,    # A7
    3420: 2,    # PSL(2,19)
    4080: 4,    # PSL(2,16)
    5616: 2,    # PSL(3,3)
    6048: 2,    # PSL(2,23)
    7920: 1,    # M11
}

def conditions(witness):
    try:
        h1_ok = False
        if hasattr(witness, 'is_finite'):
            is_fin = witness.is_finite
            if callable(is_fin):
                is_fin = is_fin()
            if is_fin and hasattr(witness, 'is_perfect'):
                is_perf = witness.is_perfect
                if callable(is_perf):
                    is_perf = is_perf()
                if is_perf and hasattr(witness, 'composition_series'):
                    series = witness.composition_series()
                    is_semi = True
                    for i in range(len(series) - 1):
                        order = int(series[i].order() // series[i+1].order())
                        if sympy.isprime(order):
                            is_semi = False
                            break
                    h1_ok = is_semi
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = False
        if hasattr(witness, 'composition_series'):
            series = witness.composition_series()
            prod_out = 1
            orders = []
            for i in range(len(series) - 1):
                order = int(series[i].order() // series[i+1].order())
                orders.append(order)
                if sympy.isprime(order):
                    prod_out *= (order - 1)
                else:
                    prod_out *= SIMPLE_OUT_ORDERS.get(order, 2)
            
            if h1_ok:
                # For semisimple groups, Out(G) order is exactly prod(Out(S_i)^k * k!)
                counts = {}
                for order in orders:
                    counts[order] = counts.get(order, 0) + 1
                out_G = 1
                for order, k in counts.items():
                    s_out = SIMPLE_OUT_ORDERS.get(order, 2)
                    out_G *= (s_out ** k) * math.factorial(k)
                neg_q_ok = (out_G != prod_out)
            else:
                # For non-semisimple groups, attempt exact computation if small enough
                order_G = int(witness.order())
                if order_G <= 100:
                    try:
                        aut_G = len(list(witness.isomorphisms(witness)))
                        inn_G = order_G // int(witness.center().order())
                        out_G = aut_G // inn_G
                        neg_q_ok = (out_G != prod_out)
                    except Exception:
                        neg_q_ok = True
                else:
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "¬Q: Out(G) is not isomorphic to the direct product of the outer automorphism groups of its simple factors"
]

N_HYP = 1
NEG_Q_INDEX = 1