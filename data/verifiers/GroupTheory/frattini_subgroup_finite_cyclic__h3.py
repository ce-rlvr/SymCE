import sympy
from sympy.combinatorics import PermutationGroup, CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol
import math
from sympy.ntheory import primefactors

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # Handle both integer (implicit CyclicGroup) and PermutationGroup witnesses
    if isinstance(witness, int):
        if witness < 1:
            return [False, False, False]
        G = CyclicGroup(witness)
    elif isinstance(witness, PermutationGroup):
        G = witness
    else:
        return [False, False, False]
        
    # H_1: G is a finite cyclic group of order n
    try:
        h1 = G.is_finite and G.is_cyclic
    except Exception:
        h1 = False
        
    # H_2: \Phi(G) is the Frattini subgroup of G, defined as the intersection of all maximal subgroups of G
    # This is a definitional hypothesis, so it holds by definition.
    h2 = True
    
    # neg_Q: \Phi(G) is NOT the unique subgroup of G of order n/rad(n)
    try:
        n = G.order()
        factors = primefactors(n)
        rad_n = math.prod(factors) if factors else 1
        target_order = n / rad_n
        
        # Generate all subgroups of G
        elements = list(G.elements)
        subgroups = set()
        for g in elements:
            sub = set()
            curr = g
            while curr not in sub:
                sub.add(curr)
                curr = curr * g
            subgroups.add(frozenset(sub))
        
        subgroups_list = list(subgroups)
        changed = True
        while changed:
            changed = False
            n_sub = len(subgroups_list)
            for i in range(n_sub):
                for j in range(i + 1, n_sub):
                    s1 = subgroups_list[i]
                    s2 = subgroups_list[j]
                    closure = set(s1 | s2)
                    queue = list(closure)
                    while queue:
                        x = queue.pop()
                        for y in list(closure):
                            xy = x * y
                            if xy not in closure:
                                closure.add(xy)
                                queue.append(xy)
                            yx = y * x
                            if yx not in closure:
                                closure.add(yx)
                                queue.append(yx)
                    fs = frozenset(closure)
                    if fs not in subgroups:
                        subgroups.add(fs)
                        subgroups_list.append(fs)
                        changed = True
                        
        # Find maximal subgroups
        proper_subs = [s for s in subgroups_list if len(s) < n]
        if not proper_subs:
            phi_order = n
        else:
            maximal = []
            for s in proper_subs:
                is_max = True
                for other in proper_subs:
                    if s != other and s.issubset(other):
                        is_max = False
                        break
                if is_max:
                    maximal.append(s)
            intersection = set.intersection(*maximal)
            phi_order = len(intersection)
            
        # Evaluate conclusion
        if phi_order != target_order:
            neg_q = True
        else:
            subs_of_target_order = [s for s in subgroups_list if len(s) == target_order]
            if len(subs_of_target_order) == 1:
                neg_q = False
            else:
                neg_q = True
                
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group of order n",
    "H_2: \\Phi(G) is the Frattini subgroup of G, defined as the intersection of all maximal subgroups of G",
    "¬Q: \\Phi(G) is not the unique subgroup of G of order n/rad(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2