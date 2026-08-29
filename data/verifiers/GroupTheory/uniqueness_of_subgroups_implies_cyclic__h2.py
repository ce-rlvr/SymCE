import math
import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup
from sympy import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: For every positive integer d dividing n, G contains at most one subgroup of order d",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_comb(n, k):
    try:
        return math.comb(n, k)
    except AttributeError:
        f = math.factorial
        return f(n) // (f(k) * f(n - k))

def conditions(witness):
    try:
        # The dropped hypothesis was "|G| = n", making n a free variable.
        # Thus, a valid counterexample must provide both G and n.
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            n = G.order()
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = getattr(G, 'is_group', False)
        if not h1:
            h1 = isinstance(G, PermutationGroup)
        if h1:
            order = G.order()
            h1 = order < float('inf')
    except Exception:
        h1 = False

    # H2: For every positive integer d dividing n, G contains at most one subgroup of order d
    try:
        h2 = True
        try:
            n_val = int(n)
            if n_val != n or n_val < 1:
                h2 = False
        except Exception:
            h2 = False

        if h2 and h1:
            is_cyclic = getattr(G, 'is_cyclic', None)
            if is_cyclic is None:
                order = G.order()
                is_cyclic = any(g.order() == order for g in G.elements)
            
            if is_cyclic:
                # A cyclic group has exactly one subgroup for every divisor of its order,
                # and zero for non-divisors. In all cases, it's <= 1.
                h2 = True
            else:
                elements = list(G.elements)
                id_elem = G.identity
                elements.remove(id_elem)
                
                # We only need to check divisors of n that also divide |G|
                # because if d does not divide |G|, G has 0 subgroups of order d (which is <= 1).
                gcd_val = math.gcd(n_val, int(G.order()))
                for d in range(1, gcd_val + 1):
                    if gcd_val % d == 0:
                        if d == 1:
                            count = 1
                        else:
                            # Prevent timeout on maliciously large non-cyclic groups
                            if get_comb(len(elements), d - 1) > 200000:
                                h2 = False
                                break
                            
                            count = 0
                            for subset in itertools.combinations(elements, d - 1):
                                subgroup = set(subset)
                                subgroup.add(id_elem)
                                closed = True
                                # Check closure under multiplication
                                for a in subset:
                                    for b in subset:
                                        if a * b not in subgroup:
                                            closed = False
                                            break
                                    if not closed:
                                        break
                                if closed:
                                    count += 1
                                    if count > 1:
                                        break
                        if count > 1:
                            h2 = False
                            break
    except Exception:
        h2 = False

    # neg_Q: G is not a cyclic group
    try:
        if h1:
            is_cyclic = getattr(G, 'is_cyclic', None)
            if is_cyclic is None:
                order = G.order()
                is_cyclic = any(g.order() == order for g in G.elements)
            neg_q = not is_cyclic
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]