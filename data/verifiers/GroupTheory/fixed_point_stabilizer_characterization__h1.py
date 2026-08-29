import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    """
    Checks whether the given witness is a counterexample to the false conjecture.
    The witness can be a tuple (G, X, x) for the natural action, 
    or (G, X, action, x) for a custom action.
    """
    try:
        if len(witness) == 3:
            G, X, x = witness
            action = None
        elif len(witness) == 4:
            G, X, action, x = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: x is an element of X
    try:
        h1_ok = x in X
    except Exception:
        h1_ok = False

    # Conclusion: The element x is a fixed point of the action of G if and only if 
    # the stabilizer of x in G is equal to G.
    try:
        elements = G.elements if hasattr(G, 'elements') else G
        
        if action is None:
            # Natural action evaluation
            is_fixed = all(g(x) == x for g in elements)
            
            if hasattr(G, 'stabilizer'):
                stab_eq_G = (G.stabilizer(x) == G)
            else:
                stab_elements = [g for g in elements if g(x) == x]
                if not stab_elements:
                    stab_eq_G = False
                else:
                    stab_group = PermutationGroup(*stab_elements)
                    stab_eq_G = (stab_group == G)
                    
            q_ok = (is_fixed == stab_eq_G)
        else:
            # Custom action evaluation
            if callable(action):
                is_fixed = all(action(g, x) == x for g in elements)
                stab_elements = [g for g in elements if action(g, x) == x]
            else:
                is_fixed = all(action[(g, x)] == x for g in elements)
                stab_elements = [g for g in elements if action[(g, x)] == x]
            
            if not stab_elements:
                stab_eq_G = False
            else:
                stab_group = PermutationGroup(*stab_elements)
                stab_eq_G = (stab_group == G)
            
            q_ok = (is_fixed == stab_eq_G)
            
    except Exception:
        # If the action is undefined or stabilizer cannot be computed (e.g. out of bounds),
        # the conclusion is considered to fail.
        q_ok = False

    neg_q_ok = not q_ok

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: x is an element of X",
    "¬Q: The equivalence between x being a fixed point and its stabilizer being G fails"
]

N_HYP = 1
NEG_Q_INDEX = 1