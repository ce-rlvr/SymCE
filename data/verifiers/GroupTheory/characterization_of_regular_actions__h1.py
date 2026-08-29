import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, CyclicGroup
from sympy.combinatorics.named_groups import AlternatingGroup, DihedralGroup
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
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

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts on X",
    "¬Q: The action is regular iff it is transitive and the stabilizer of every element is trivial (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_witness_components(witness):
    """
    Helper to parse various witness formats into a standard representation:
    (G_elements, X, act, identity, op)
    """
    op = None
    
    # Case 1: witness is a SymPy PermutationGroup
    if hasattr(witness, 'generators') and hasattr(witness, 'degree'):
        G_elements = list(witness.generate())
        X = list(range(witness.degree))
        identity = witness.identity
        def act(g, x): return g(x)
        op = lambda g1, g2: g1 * g2
        return G_elements, X, act, identity, op
    
    # Case 2: witness is a tuple
    if isinstance(witness, tuple):
        if len(witness) == 2:
            G, X = witness
            if hasattr(G, 'generators'):
                G_elements = list(G.generate())
                identity = G.identity
                def act(g, x): return g(x)
                op = lambda g1, g2: g1 * g2
                return G_elements, list(X), act, identity, op
            else:
                G_elements = list(G)
                identity = G_elements[0]
                def act(g, x): return g(x)
                op = None
                return G_elements, list(X), act, identity, op
                
        elif len(witness) == 3:
            G, X, act = witness
            if hasattr(G, 'generators'):
                G_elements = list(G.generate())
                identity = G.identity
                op = lambda g1, g2: g1 * g2
            else:
                G_elements = list(G)
                identity = G_elements[0]
                op = None
            return G_elements, list(X), act, identity, op
            
        elif len(witness) == 4:
            G, X, act, identity = witness
            if hasattr(G, 'generators'):
                G_elements = list(G.generate())
                op = lambda g1, g2: g1 * g2
            else:
                G_elements = list(G)
                op = None
            return G_elements, list(X), act, identity, op
            
    # Case 3: witness is just a list (interpreted as set X, with trivial group)
    if isinstance(witness, list):
        X = witness
        G_elements = ['e']
        identity = 'e'
        def act(g, x): return x
        op = lambda g1, g2: 'e'
        return G_elements, X, act, identity, op

    # Case 4: witness is an integer (interpreted as size of set X, with trivial group)
    if isinstance(witness, int):
        X = list(range(witness))
        G_elements = ['e']
        identity = 'e'
        def act(g, x): return x
        op = lambda g1, g2: 'e'
        return G_elements, X, act, identity, op

    raise ValueError("Cannot parse witness format")

def conditions(witness) -> list[bool]:
    try:
        G_elements, X, act, identity, op = get_witness_components(witness)
    except Exception:
        return [False, False, False]
        
    # H_1: X is a set
    try:
        h1 = isinstance(X, (list, set, tuple))
    except Exception:
        h1 = False
        
    # H_2: G acts on X
    try:
        h2 = True
        for x in X:
            if act(identity, x) != x:
                h2 = False
                break
            for g in G_elements:
                if act(g, x) not in X:
                    h2 = False
                    break
        if h2 and op is not None:
            for x in X:
                for g1 in G_elements:
                    for g2 in G_elements:
                        if act(g1, act(g2, x)) != act(op(g1, g2), x):
                            h2 = False
                            break
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion fails
    # Conclusion: The action is regular iff it is transitive and the stabilizer of every element is trivial.
    try:
        # is_regular: for all x, y in X, there exists a UNIQUE g in G such that act(g, x) == y
        is_regular = True
        for x in X:
            for y in X:
                count = sum(1 for g in G_elements if act(g, x) == y)
                if count != 1:
                    is_regular = False
                    break
            if not is_regular:
                break
                
        # is_transitive: X is non-empty AND for all x, y in X, there exists g in G such that act(g, x) == y
        if not X:
            is_transitive = False
        else:
            is_transitive = True
            for x in X:
                for y in X:
                    if not any(act(g, x) == y for g in G_elements):
                        is_transitive = False
                        break
                if not is_transitive:
                    break
                    
        # is_free (stabilizer of every element is trivial): for all x in X, for all g in G, if act(g, x) == x then g == identity
        is_free = True
        for x in X:
            for g in G_elements:
                if act(g, x) == x and g != identity:
                    is_free = False
                    break
            if not is_free:
                break
                
        # The conclusion is the equivalence of regular and (transitive AND free)
        conclusion = (is_regular == (is_transitive and is_free))
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]