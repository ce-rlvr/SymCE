import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_order(obj):
    o = obj.order
    if callable(o):
        return o()
    return o

def is_abelian(G):
    ab = G.is_abelian
    if callable(ab):
        return ab()
    return ab

def is_identity(x):
    id_val = x.is_Identity
    if callable(id_val):
        return id_val()
    return id_val

def is_minimal_normal(G, N):
    try:
        if get_order(N) == 1:
            return False
        
        # Check if N is a subgroup of G
        for gen in N.generators:
            if gen not in G:
                return False
                
        # Check if N is normal in G
        for g in G.generators:
            for n in N.generators:
                if (g * n * (g**-1)) not in N:
                    return False
                if ((g**-1) * n * g) not in N:
                    return False
        
        n_order = get_order(N)
        # Check minimality: the normal closure of any non-trivial element in N must be N itself.
        for x in N.generate():
            if is_identity(x):
                continue
            conjugates = set()
            queue = [x]
            conjugates.add(x)
            for elem in queue:
                for g in G.generators:
                    conj1 = g * elem * (g**-1)
                    if conj1 not in conjugates:
                        conjugates.add(conj1)
                        queue.append(conj1)
                    conj2 = (g**-1) * elem * g
                    if conj2 not in conjugates:
                        conjugates.add(conj2)
                        queue.append(conj2)
            H = PermutationGroup(list(conjugates))
            if get_order(H) < n_order:
                return False
        return True
    except Exception:
        return False

def is_elementary_abelian_p_group(N):
    try:
        if not is_abelian(N):
            return False
        
        orders = set()
        for x in N.generate():
            if not is_identity(x):
                orders.add(get_order(x))
        
        if len(orders) == 0:
            return False
            
        if len(orders) != 1:
            return False
        
        p = orders.pop()
        if not isprime(p):
            return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness should be a tuple (G, N) where G is a group and N is a subgroup.
    """
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = is_minimal_normal(G, N)
    except Exception:
        h1 = False
        
    try:
        neg_q = not is_elementary_abelian_p_group(N)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a minimal normal subgroup of G",
    "¬Q: N is not an elementary abelian p-group for any prime p"
]

N_HYP = 1
NEG_Q_INDEX = 1