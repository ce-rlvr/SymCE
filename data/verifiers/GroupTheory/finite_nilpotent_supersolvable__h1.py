import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_nilpotent(G):
    """Helper to check if a group is nilpotent."""
    if hasattr(G, 'is_nilpotent'):
        val = G.is_nilpotent
        if callable(val):
            return val()
        return val
    if hasattr(G, 'lower_central_series'):
        try:
            lcs = G.lower_central_series()
            return lcs[-1].order() == 1
        except Exception:
            pass
    return False

def is_supersolvable(G):
    """Helper to check if a finite group is supersolvable."""
    # Every nilpotent group is supersolvable
    if check_nilpotent(G):
        return True

    # If G is supersolvable, its derived subgroup must be nilpotent
    try:
        if hasattr(G, 'derived_series'):
            ds = G.derived_series()
            G_prime = ds[1] if len(ds) > 1 else ds[0]
            if not check_nilpotent(G_prime):
                return False
    except Exception:
        pass

    try:
        elements = list(G.elements)
    except Exception:
        return False

    # Compute conjugacy classes
    classes = []
    seen = set()
    for e in elements:
        if e not in seen:
            c = set()
            for g in elements:
                c.add(g * e * (g**-1))
            classes.append(list(c))
            seen.update(c)

    # DFS to find a normal series with prime index steps
    def dfs(current_group):
        if current_group.order() == G.order():
            return True
            
        current_elements = set(current_group.elements)
        
        for C in classes:
            if C[0] not in current_elements:
                gens = list(current_group.generators) + C
                N_new = PermutationGroup(gens)
                
                # Check if the new normal subgroup has prime index over the current one
                if N_new.order() % current_group.order() == 0:
                    index = N_new.order() // current_group.order()
                    if isprime(index):
                        if dfs(N_new):
                            return True
        return False

    try:
        trivial_group = PermutationGroup([G.identity])
        return dfs(trivial_group)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group
    try:
        h1 = False
        if hasattr(witness, 'order') and hasattr(witness, 'elements'):
            o = witness.order()
            if o > 0 and o != float('inf'):
                h1 = True
    except Exception:
        h1 = False

    # H_2: G is nilpotent
    try:
        h2 = bool(check_nilpotent(witness))
    except Exception:
        h2 = False

    # ¬Q: G is not supersolvable
    try:
        neg_q = not is_supersolvable(witness)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is nilpotent",
    "¬Q: G is not supersolvable"
]

N_HYP = 2
NEG_Q_INDEX = 2