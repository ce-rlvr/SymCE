import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "The action of G on X is regular if and only if the action is transitive 
    and the stabilizer of every point in X is the trivial subgroup."
    
    The dropped hypothesis from the true theorem is that the action must actually 
    be a valid group action. Without it, a binary operation can be transitive 
    and free, but fail to be a regular action (since it fails to be a group action).
    """
    try:
        G, X, action = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        if isinstance(G, PermutationGroup):
            h1 = True
        else:
            elements = list(G)
            identity = None
            for g in elements:
                if all(g * h == h and h * g == h for h in elements):
                    identity = g
                    break
            if identity is None:
                h1 = False
            else:
                h1 = True
                for g in elements:
                    if not any(g * h == identity and h * g == identity for h in elements):
                        h1 = False
                        break
    except Exception:
        h1 = False
        
    # H2: X is a nonempty set
    try:
        h2 = isinstance(X, (set, list, tuple)) and len(X) > 0
    except Exception:
        h2 = False
        
    # ¬Q: The equivalence fails
    try:
        if callable(action):
            act = action
        elif isinstance(action, dict):
            act = lambda g, x: action[(g, x)]
        else:
            raise ValueError("Action must be callable or a dictionary")
            
        if isinstance(G, PermutationGroup):
            elements_q = list(G.elements)
            identity_q = G.identity
        else:
            elements_q = list(G)
            identity_q = None
            for g in elements_q:
                if all(g * h == h and h * g == h for h in elements_q):
                    identity_q = g
                    break
            if identity_q is None:
                raise ValueError("Group identity not found")
                
        # Check if Q holds: action is transitive and free
        is_transitive = True
        for x in X:
            for y in X:
                if not any(act(g, x) == y for g in elements_q):
                    is_transitive = False
                    break
            if not is_transitive:
                break
                
        is_free = True
        for x in X:
            for g in elements_q:
                if act(g, x) == x and g != identity_q:
                    is_free = False
                    break
            if not is_free:
                break
                
        Q = is_transitive and is_free
        
        # Check if P holds: action is regular
        # A regular action MUST be a valid group action that is transitive and free.
        is_group_action = True
        for x in X:
            if act(identity_q, x) != x:
                is_group_action = False
                break
            for g in elements_q:
                for h in elements_q:
                    if act(g, act(h, x)) != act(g * h, x):
                        is_group_action = False
                        break
                if not is_group_action:
                    break
            if not is_group_action:
                break
                
        P = is_group_action and is_transitive and is_free
        
        # The conjecture claims P <==> Q. We want this to fail.
        neg_q = not (P == Q)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a nonempty set",
    "¬Q: The equivalence between regular action and (transitive + free) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2