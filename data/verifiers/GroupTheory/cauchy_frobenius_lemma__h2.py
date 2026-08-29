import sympy
from sympy import S
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with:
      - 'G': list of group elements
      - 'op': function op(g1, g2) returning the group operation result
      - 'X': list of elements (if finite) OR a SymPy Set (e.g., S.Integers)
      - 'action': function action(g, x) returning the result of g acting on x
      - 'test_X': list of elements from X to test the action axioms (required if X is infinite)
    """
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
        
        G = witness.get('G')
        op = witness.get('op')
        X = witness.get('X')
        action = witness.get('action')
        test_X = witness.get('test_X', X if isinstance(X, (list, tuple, set)) else [])
        
        if G is None or op is None or X is None or action is None:
            return [False, False, False]
            
        # H_1: G is a finite group
        h1 = False
        if isinstance(G, (list, tuple, set)) and len(G) > 0:
            G_list = list(G)
            closure = True
            for a in G_list:
                for b in G_list:
                    if op(a, b) not in G_list:
                        closure = False
                        break
                if not closure:
                    break
            
            if closure:
                e = None
                for a in G_list:
                    is_e = True
                    for b in G_list:
                        if op(a, b) != b or op(b, a) != b:
                            is_e = False
                            break
                    if is_e:
                        e = a
                        break
                
                if e is not None:
                    inverses = True
                    for a in G_list:
                        has_inv = False
                        for b in G_list:
                            if op(a, b) == e and op(b, a) == e:
                                has_inv = True
                                break
                        if not has_inv:
                            inverses = False
                            break
                    
                    if inverses:
                        assoc = True
                        for a in G_list:
                            for b in G_list:
                                for c in G_list:
                                    if op(op(a, b), c) != op(a, op(b, c)):
                                        assoc = False
                                        break
                                if not assoc:
                                    break
                            if not assoc:
                                break
                        if assoc:
                            h1 = True

        # Determine if X is finite
        is_finite_X = False
        X_elements = []
        if isinstance(X, (list, tuple, set)):
            is_finite_X = True
            X_elements = list(X)
        elif hasattr(X, 'is_finite'):
            if X.is_finite:
                is_finite_X = True
                X_elements = list(X)
            else:
                is_finite_X = False
        else:
            return [False, False, False]

        # H_2: G acts on X
        h2 = False
        if h1 and isinstance(test_X, (list, tuple, set)) and len(test_X) > 0:
            acts = True
            for x in test_X:
                try:
                    if hasattr(X, 'contains'):
                        if not X.contains(x):
                            acts = False
                            break
                    elif isinstance(X, (list, tuple, set)):
                        found = False
                        for item in X:
                            if item == x:
                                found = True
                                break
                        if not found:
                            acts = False
                            break
                    else:
                        acts = False
                        break
                except Exception:
                    acts = False
                    break
                
                try:
                    if action(e, x) != x:
                        acts = False
                        break
                    for g in G_list:
                        res_g = action(g, x)
                        if hasattr(X, 'contains'):
                            if not X.contains(res_g):
                                acts = False
                                break
                        elif isinstance(X, (list, tuple, set)):
                            found = False
                            for item in X:
                                if item == res_g:
                                    found = True
                                    break
                            if not found:
                                acts = False
                                break
                        else:
                            acts = False
                            break
                            
                        for h in G_list:
                            if action(op(g, h), x) != action(g, action(h, x)):
                                acts = False
                                break
                        if not acts:
                            break
                except Exception:
                    acts = False
                    break
            if acts:
                h2 = True

        # ¬Q: The conclusion fails
        neg_q = False
        if is_finite_X:
            orbits = []
            for x in X_elements:
                orb = []
                for g in G_list:
                    try:
                        res = action(g, x)
                        found = False
                        for item in orb:
                            if item == res:
                                found = True
                                break
                        if not found:
                            orb.append(res)
                    except Exception:
                        pass
                
                is_new = True
                for existing_orb in orbits:
                    if len(existing_orb) == len(orb):
                        all_in = True
                        for e1 in orb:
                            found = False
                            for e2 in existing_orb:
                                if e1 == e2:
                                    found = True
                                    break
                            if not found:
                                all_in = False
                                break
                        if all_in:
                            is_new = False
                            break
                if is_new:
                    orbits.append(orb)
            num_orbits = len(orbits)
            
            sum_fixed = 0
            for g in G_list:
                fixed = 0
                for x in X_elements:
                    try:
                        if action(g, x) == x:
                            fixed += 1
                    except Exception:
                        pass
                sum_fixed += fixed
            
            # The conclusion holds if num_orbits == sum_fixed / |G|
            # It fails if they are not equal.
            if num_orbits * len(G_list) != sum_fixed:
                neg_q = True
            else:
                neg_q = False
        else:
            # For an infinite set, the number of orbits is not a finite integer,
            # so the integer equation conclusion fails.
            neg_q = True
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G acts on X",
    "¬Q: The orbit counting formula fails (e.g., X is infinite)"
]

N_HYP = 2
NEG_Q_INDEX = 2