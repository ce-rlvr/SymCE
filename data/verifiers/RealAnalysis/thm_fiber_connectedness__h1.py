import sympy
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices as matrices
import math
import itertools
import functools

# Top-level setup
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
V4 = named_groups.AlternatingGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)
I2 = matrices.eye(2)
I3 = matrices.eye(3)
O2 = matrices.zeros(2, 2)
O3 = matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the Fiber Connectedness Theorem conjecture.
    The witness is expected to be a dictionary representing finite topological spaces and a map:
    {
        'X': list of elements in X,
        'Y': list of elements in Y,
        'O_X': list of open sets in X (each open set is a list/set of elements),
        'O_Y': list of open sets in Y,
        'f': dictionary mapping elements of X to elements of Y
    }
    """
    try:
        X = frozenset(witness['X'])
        Y = frozenset(witness['Y'])
        O_X = set(frozenset(s) for s in witness['O_X'])
        O_Y = set(frozenset(s) for s in witness['O_Y'])
        f = witness['f']
        
        # Ensure f is a well-defined function from X to Y
        if not all(x in f and f[x] in Y for x in X):
            return [False] * 6
            
        def is_topology(space, topology):
            if frozenset() not in topology or space not in topology:
                return False
            for a in topology:
                for b in topology:
                    if a.intersection(b) not in topology:
                        return False
                    if a.union(b) not in topology:
                        return False
            return True
            
        if not is_topology(X, O_X) or not is_topology(Y, O_Y):
            return [False] * 6
            
        def get_closed(space, topology):
            return set(space - o for o in topology)
            
        C_X = get_closed(X, O_X)
        C_Y = get_closed(Y, O_Y)
        
        # H_1: f: X \to Y is a continuous map
        h1 = True
        for V in O_Y:
            preimage = frozenset(x for x in X if f[x] in V)
            if preimage not in O_X:
                h1 = False
                break
                
        # H_2: f is a surjective map
        image = set(f[x] for x in X)
        h2 = (image == Y)
        
        # H_3: f is a closed map
        h3 = True
        for C in C_X:
            img = frozenset(f[x] for x in C)
            if img not in C_Y:
                h3 = False
                break
                
        # Helper for connectedness
        def is_connected(space, topology):
            if not space:
                return False
            closed_sets = get_closed(space, topology)
            clopen = topology.intersection(closed_sets)
            return clopen == {frozenset(), space}
            
        # H_4: Y is a connected space
        h4 = is_connected(Y, O_Y)
        
        # H_5: f^{-1}(y) is a connected subset of X for all y \in Y
        h5 = True
        for y in Y:
            fiber = frozenset(x for x in X if f[x] == y)
            if not fiber:
                h5 = False
                break
            sub_open = set(o.intersection(fiber) for o in O_X)
            if not is_connected(fiber, sub_open):
                h5 = False
                break
                
        # ¬Q: X is not a connected space
        neg_q = not is_connected(X, O_X)
        
        return [h1, h2, h3, h4, h5, neg_q]
    except Exception:
        return [False, False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: f: X \\to Y is a continuous map",
    "H_2: f is a surjective map",
    "H_3: f is a closed map",
    "H_4: Y is a connected space",
    "H_5: f^{-1}(y) is a connected subset of X for all y \\in Y",
    "¬Q: X is not a connected space"
]

N_HYP = 5
NEG_Q_INDEX = 5