import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy import oo
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    # Extract G and n from the witness
    if isinstance(witness, tuple) and len(witness) == 2:
        G, n = witness
    else:
        G = witness
        try:
            if hasattr(G, 'order'):
                n = G.order()
                if callable(n):
                    n = n()
            elif hasattr(G, '__len__'):
                n = len(G)
            else:
                n = None
        except Exception:
            n = None

    # Determine order of G
    try:
        if hasattr(G, 'order'):
            order_G = G.order()
            if callable(order_G):
                order_G = order_G()
        elif hasattr(G, '__len__'):
            order_G = len(G)
        else:
            order_G = None
    except Exception:
        order_G = None

    # H_1: The order of G is n
    try:
        if n is None or order_G is None:
            h1 = False
        else:
            h1 = (order_G == n)
    except Exception:
        h1 = False

    # H_2: For every positive integer d dividing n, G contains at most one subgroup of order d
    try:
        if n == oo:
            # If n is infinity, there are no positive integers dividing n.
            # The condition holds vacuously.
            h2 = True
        elif n is None:
            h2 = False
        elif order_G == oo:
            h2 = False
        else:
            if hasattr(G, 'elements'):
                elements = list(G.elements)
            elif hasattr(G, 'generate_dimino'):
                elements = list(G.generate_dimino())
            else:
                elements = list(G)
                
            if hasattr(G, 'identity'):
                identity = G.identity
            else:
                identity = None
                for e in elements:
                    if e * e == e:
                        identity = e
                        break
            
            if identity is None:
                h2 = False
            else:
                subgroups_by_order = {}
                h2 = True
                max_order = len(elements)
                for g in elements:
                    if hasattr(g, 'order'):
                        d = g.order()
                        if callable(d):
                            d = d()
                    else:
                        current = g
                        d = 1
                        while current != identity and d <= max_order:
                            current = current * g
                            d += 1
                            
                    if int(n) % int(d) == 0:
                        subgroup = set()
                        current = identity
                        for _ in range(int(d)):
                            subgroup.add(current)
                            current = current * g
                            
                        subgroup_fs = frozenset(subgroup)
                        if d not in subgroups_by_order:
                            subgroups_by_order[d] = set()
                        subgroups_by_order[d].add(subgroup_fs)
                        if len(subgroups_by_order[d]) > 1:
                            h2 = False
                            break
    except Exception:
        h2 = False

    # Conclusion: G is a cyclic group
    # Negation: G is NOT a cyclic group
    try:
        if hasattr(G, 'is_cyclic'):
            is_cyclic = G.is_cyclic
            if callable(is_cyclic):
                is_cyclic = is_cyclic()
            neg_q = not is_cyclic
        elif hasattr(G, 'is_Cyclic'):
            is_cyclic = G.is_Cyclic
            if callable(is_cyclic):
                is_cyclic = is_cyclic()
            neg_q = not is_cyclic
        elif order_G == oo:
            if hasattr(G, 'generators'):
                gens = list(G.generators)
                neg_q = len(gens) > 1
            else:
                neg_q = True
        elif order_G is not None:
            if hasattr(G, 'elements'):
                elements = list(G.elements)
            elif hasattr(G, 'generate_dimino'):
                elements = list(G.generate_dimino())
            else:
                elements = list(G)
                
            if hasattr(G, 'identity'):
                identity = G.identity
            else:
                identity = None
                for e in elements:
                    if e * e == e:
                        identity = e
                        break
            
            if identity is None:
                neg_q = False
            else:
                has_gen = False
                for g in elements:
                    if hasattr(g, 'order'):
                        o = g.order()
                        if callable(o):
                            o = o()
                    else:
                        current = g
                        o = 1
                        while current != identity and o <= order_G:
                            current = current * g
                            o += 1
                    if o == order_G:
                        has_gen = True
                        break
                neg_q = not has_gen
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is n",
    "H_2: For every positive integer d dividing n, G contains at most one subgroup of order d",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2