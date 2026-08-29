import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

CONDITION_LABELS = [
    "H_1: X and Y are topological spaces",
    "H_2: A is a connected subset of the product space X \\times Y",
    "¬Q: The projections \\pi_X(A) and \\pi_Y(A) are not both connected subsets of X and Y"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_topology(pts, topo):
    pts_set = frozenset(pts)
    topo_sets = set(frozenset(t) for t in topo)
    
    if frozenset() not in topo_sets: return False
    if pts_set not in topo_sets: return False
    
    for u in topo_sets:
        for v in topo_sets:
            if u.intersection(v) not in topo_sets:
                return False
                
    for u in topo_sets:
        for v in topo_sets:
            if u.union(v) not in topo_sets:
                return False
                
    return True

def product_topology(X_pts, X_topo, Y_pts, Y_topo):
    basis = set()
    for u in X_topo:
        for v in Y_topo:
            basis.add(frozenset((x, y) for x in u for y in v))
            
    topo = set(basis)
    topo.add(frozenset())
    while True:
        new_topo = set(topo)
        for t1 in topo:
            for t2 in basis:
                new_topo.add(t1.union(t2))
        if len(new_topo) == len(topo):
            break
        topo = new_topo
    return topo

def is_connected(A_set, topo):
    if not A_set:
        return True
    
    for u in topo:
        for v in topo:
            u_A = A_set.intersection(u)
            v_A = A_set.intersection(v)
            if u_A.union(v_A) == A_set and not u_A.intersection(v_A):
                if u_A and v_A:
                    return False
    return True

def conditions(witness):
    # 1. Try finite topological space dictionary
    try:
        if isinstance(witness, dict) and 'X_topo' in witness and 'Y_topo' in witness and 'A' in witness:
            X_topo = [frozenset(t) for t in witness['X_topo']]
            Y_topo = [frozenset(t) for t in witness['Y_topo']]
            A_set = frozenset(witness['A'])
            
            if 'X_pts' in witness:
                X_pts = frozenset(witness['X_pts'])
            else:
                X_pts = frozenset().union(*X_topo) if X_topo else frozenset()
                
            if 'Y_pts' in witness:
                Y_pts = frozenset(witness['Y_pts'])
            else:
                Y_pts = frozenset().union(*Y_topo) if Y_topo else frozenset()
                
            h1 = is_topology(X_pts, X_topo) and is_topology(Y_pts, Y_topo)
            
            if not h1:
                return [False, False, False]
                
            prod_topo = product_topology(X_pts, X_topo, Y_pts, Y_topo)
            
            valid_A = all(isinstance(p, tuple) and len(p) == 2 and p[0] in X_pts and p[1] in Y_pts for p in A_set)
            if not valid_A and A_set:
                return [True, False, False]
                
            h2 = is_connected(A_set, prod_topo)
            
            pi_X = frozenset(x for (x, y) in A_set)
            pi_Y = frozenset(y for (x, y) in A_set)
            
            q_X = is_connected(pi_X, X_topo)
            q_Y = is_connected(pi_Y, Y_topo)
            
            neg_q = not (q_X and q_Y)
            
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try list of points in R^2
    try:
        if isinstance(witness, list) and all(isinstance(p, tuple) and len(p) == 2 for p in witness):
            h1 = True
            h2 = len(witness) <= 1
            
            pi_X = set(x for x, y in witness)
            pi_Y = set(y for x, y in witness)
            
            q_X = len(pi_X) <= 1
            q_Y = len(pi_Y) <= 1
            
            neg_q = not (q_X and q_Y)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try sympy Set
    try:
        from sympy import Set
        if isinstance(witness, Set):
            h1 = True
            if witness.is_FiniteSet:
                h2 = len(witness) <= 1
                pi_X = set(p[0] for p in witness)
                pi_Y = set(p[1] for p in witness)
                q_X = len(pi_X) <= 1
                q_Y = len(pi_Y) <= 1
                neg_q = not (q_X and q_Y)
                return [h1, h2, neg_q]
            else:
                return [True, False, False]
    except Exception:
        pass

    return [False, False, False]