import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
    "H_1: G is a group",
    "H_2: G acts on X",
    "H_3: x is an element of X",
    "¬Q: The cardinality of the orbit G \\cdot x is not equal to the index of the stabilizer subgroup G_x in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # Case 1: witness is a tuple (PermutationGroup, x)
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and hasattr(witness[0], 'orbit'):
            G, x = witness
            h1 = True
            h2 = True
            h3 = x in G.domain
            orbit = G.orbit(x)
            stab = G.stabilizer(x)
            index = G.order() / stab.order()
            neg_q = (len(orbit) != index)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Case 2: witness is a tuple (G, X, action, x)
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            G, X, action, x = witness
            h1, h2, h3, neg_q = False, False, False, False
            
            # Check H1
            if G in (sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
                h1 = True
                is_infinite_sym = True
            elif hasattr(G, 'orbit') and hasattr(G, 'stabilizer'):
                h1 = True
                is_infinite_sym = False
                is_perm_group = True
            else:
                elements = list(G)
                h1 = True
                is_infinite_sym = False
                is_perm_group = False
                
            # Check H3
            try:
                if hasattr(X, 'contains'):
                    h3 = (X.contains(x) == sympy.true)
                else:
                    h3 = x in X
            except Exception:
                h3 = False
                
            # Check H2 and neg_Q
            if is_infinite_sym:
                try:
                    # Check identity and a simple associativity case for the action
                    if action(0, x) == x and action(1, action(2, x)) == action(3, x):
                        h2 = True
                except Exception:
                    h2 = False
                    
                if h1 and h2 and h3:
                    orbit = set()
                    for i in range(-100, 100):
                        orbit.add(action(i, x))
                    
                    if len(orbit) >= 100:
                        orbit_size = sympy.oo
                        index = sympy.oo
                    else:
                        orbit_size = len(orbit)
                        # For an infinite group with a finite orbit, the stabilizer must be infinite.
                        # The index |G| / |G_x| becomes oo / oo, which is undefined (nan).
                        index = sympy.nan
                        
                    neg_q = (orbit_size != index)
                    
            elif is_perm_group:
                h2 = True
                orbit = G.orbit(x)
                stab = G.stabilizer(x)
                index = G.order() / stab.order()
                neg_q = (len(orbit) != index)
                
            else:
                try:
                    _ = action(elements[0], x)
                    h2 = True
                except Exception:
                    h2 = False
                    
                if h1 and h2 and h3:
                    orbit = set()
                    stab_count = 0
                    for g in elements:
                        res = action(g, x)
                        orbit.add(res)
                        if res == x:
                            stab_count += 1
                    
                    index = len(elements) / stab_count if stab_count > 0 else float('inf')
                    neg_q = (len(orbit) != index)
                    
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Case 3: witness is a custom object with methods
    try:
        if hasattr(witness, 'is_group') and hasattr(witness, 'orbit_cardinality'):
            h1 = bool(witness.is_group())
            h2 = bool(witness.acts_on_X())
            h3 = bool(witness.x_in_X())
            orbit_card = witness.orbit_cardinality()
            stab_index = witness.stabilizer_index()
            neg_q = (orbit_card != stab_index)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Case 4: witness is a dictionary
    try:
        if isinstance(witness, dict) and 'orbit_cardinality' in witness:
            h1 = bool(witness.get('is_group', False))
            h2 = bool(witness.get('acts_on_X', False))
            h3 = bool(witness.get('x_in_X', False))
            orbit_card = witness.get('orbit_cardinality')
            stab_index = witness.get('stabilizer_index')
            neg_q = (orbit_card != stab_index)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]