import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
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

def conditions(witness):
    try:
        # Extract G, X, and the action from the witness
        if isinstance(witness, PermutationGroup):
            G_obj = witness
            G_elements = list(witness.generate())
            X_elements = list(range(witness.degree))
            def action(g, x):
                return g(x)
        else:
            G_obj = witness[0]
            X_elements = list(witness[1])
            action = witness[2]
            if hasattr(G_obj, 'generate'):
                G_elements = list(G_obj.generate())
            else:
                G_elements = list(G_obj)
                
        # H1: G is a group
        if isinstance(G_obj, PermutationGroup):
            h1 = True
        else:
            h1 = len(G_elements) > 0
            
        # H2: X is a set
        if isinstance(witness, PermutationGroup):
            h2 = True
        else:
            h2 = isinstance(witness[1], (list, set, tuple, frozenset))
            
        # Evaluate "The action of G on X is regular" (Sharply transitive)
        # For all x, y in X, there exists exactly one g in G such that g.x = y.
        is_regular = True
        for x in X_elements:
            for y in X_elements:
                count = sum(1 for g in G_elements if action(g, x) == y)
                if count != 1:
                    is_regular = False
                    break
            if not is_regular:
                break
                
        # Evaluate "The action is transitive"
        # X is non-empty and for all x, y in X, there exists at least one g in G such that g.x = y.
        if len(X_elements) == 0:
            is_transitive = False
        else:
            is_transitive = True
            for x in X_elements:
                for y in X_elements:
                    if not any(action(g, x) == y for g in G_elements):
                        is_transitive = False
                        break
                if not is_transitive:
                    break
                    
        # Evaluate "The stabilizer of every element x \in X is the trivial subgroup" (Free action)
        # For all x in X, exactly one g in G (which must be the identity) fixes x.
        is_free = True
        for x in X_elements:
            count = sum(1 for g in G_elements if action(g, x) == x)
            if count != 1:
                is_free = False
                break
                
        # Conclusion: The action is regular iff it is transitive and free
        conclusion = (is_regular == (is_transitive and is_free))
        neg_q = not conclusion
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "¬Q: The action is regular if and only if it is transitive and free (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2