import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            G, alpha = witness
            alphas = [alpha]
        else:
            G = witness
            # If no alpha is provided, we will search for one that makes the equivalence fail
            alphas = list(range(int(G.degree))) if hasattr(G, 'degree') else []
            
        if not hasattr(G, 'degree') or not hasattr(G, 'stabilizer') or not hasattr(G, 'orbits'):
            return [False, False]
            
        degree = int(G.degree)
        
        valid_alphas = [a for a in alphas if 0 <= a < degree]
        if not valid_alphas:
            return [False, False]
            
        h1_ok = True
    except Exception:
        return [False, False]
        
    try:
        # P: G is doubly transitive on Omega
        # A group is doubly transitive iff it is transitive (degree >= 2) and 
        # the stabilizer of a point (e.g., 0) acts transitively on the remaining points.
        if degree < 2:
            P = False
        else:
            if len(G.orbits()) != 1:
                P = False
            else:
                H0 = G.stabilizer(0)
                S0 = set(range(degree)) - {0}
                P = False
                for orb in H0.orbits():
                    if orb == S0:
                        P = True
                        break
                        
        neg_q_ok = False
        for a in valid_alphas:
            # Q: G_alpha acts transitively on Omega \ {alpha}
            H_a = G.stabilizer(a)
            S_a = set(range(degree)) - {a}
            Q = False
            if not S_a:
                Q = False  # Action on an empty set is not considered transitive
            else:
                for orb in H_a.orbits():
                    if orb == S_a:
                        Q = True
                        break
            
            # The conjecture states P iff Q. The negation is P != Q.
            if P != Q:
                neg_q_ok = True
                break
                
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a permutation group and alpha is a point in its domain",
    "¬Q: The equivalence 'G is doubly transitive iff G_alpha acts transitively on Omega \\ {alpha}' fails"
]

N_HYP = 1
NEG_Q_INDEX = 1