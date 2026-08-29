import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def apply_action(g, x):
    if isinstance(g, Permutation):
        return g(x)
    return g * x

def lists_equal_unordered(l1, l2):
    if len(l1) != len(l2): 
        return False
    l2_copy = list(l2)
    for item in l1:
        found = False
        for i, x in enumerate(l2_copy):
            try:
                if item == x:
                    l2_copy.pop(i)
                    found = True
                    break
            except Exception:
                pass
        if not found:
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, X, Y = witness
        elif len(witness) == 2:
            G, Y = witness
            if isinstance(G, PermutationGroup):
                X = set(range(G.degree))
            else:
                X = None
        else:
            return [False, False]
    except Exception:
        return [False, False]

    if X is None:
        return [False, False]

    # H1: G is a group acting on a set X
    try:
        if isinstance(G, PermutationGroup):
            if G.order() > 100:
                return [False, False]
            elements = list(G.generate())
        else:
            elements = []
            for i, g in enumerate(G):
                if i >= 100:
                    return [False, False]
                elements.append(g)
            
        if not elements:
            h1 = False
        else:
            X_list = list(X)
            h1 = True
            # Check closure of the action on X
            for g in elements:
                for x in X_list:
                    try:
                        gx = apply_action(g, x)
                        if not any(gx == xi for xi in X_list):
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
                if not h1: 
                    break
            
            # Check existence of an identity element for the action
            if h1:
                has_id = False
                for g in elements:
                    acts_trivially = True
                    for x in X_list:
                        try:
                            if not (apply_action(g, x) == x):
                                acts_trivially = False
                                break
                        except Exception:
                            acts_trivially = False
                            break
                    if acts_trivially:
                        has_id = True
                        break
                if not has_id:
                    h1 = False
                    
            # Check group closure if not a PermutationGroup
            if h1 and not isinstance(G, PermutationGroup):
                for a in elements:
                    for b in elements:
                        try:
                            ab = a * b
                            if not any(ab == g_elem for g_elem in elements):
                                h1 = False
                                break
                        except Exception:
                            h1 = False
                            break
                    if not h1: 
                        break
    except Exception:
        h1 = False

    # Conclusion: The setwise stabilizer is a subgroup of G
    try:
        Y_list = list(Y)
        is_subset = True
        for y in Y_list:
            if not any(y == xi for xi in X_list):
                is_subset = False
                break
        
        S = []
        for g in elements:
            if not is_subset:
                # If Y is not a subset of X, the action on Y is undefined
                continue
            
            gY = []
            valid = True
            for y in Y_list:
                try:
                    gy = apply_action(g, y)
                    gY.append(gy)
                except Exception:
                    valid = False
                    break
            if valid and lists_equal_unordered(gY, Y_list):
                S.append(g)
                
        # Check if S is a subgroup
        if not S:
            q = False
        else:
            q = True
            for a in S:
                for b in S:
                    try:
                        ab = a * b
                    except Exception:
                        q = False
                        break
                    if not any(ab == s for s in S):
                        q = False
                        break
                if not q: 
                    break
                
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "¬Q: The setwise stabilizer G_{Y} is not a subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1