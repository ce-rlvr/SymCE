import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, X, action = witness
                provided_K = None
                provided_Gx = None
            elif len(witness) == 5:
                G, X, action, provided_K, provided_Gx = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        elif isinstance(G, (list, set, tuple)):
            elements = list(G)
        else:
            return [False, False, False]
            
        if not elements:
            return [False, False, False]
            
        identity = None
        for e in elements:
            is_id = True
            for x in elements:
                if e * x != x or x * e != x:
                    is_id = False
                    break
            if is_id:
                identity = e
                break
                
        if identity is None:
            return [False, False, False]

        def eval_action(g, x):
            if callable(action):
                return action(g, x)
            elif isinstance(action, dict):
                try:
                    return action.get((g, x))
                except TypeError:
                    return None
            elif isinstance(action, list):
                for pair, v in action:
                    if isinstance(pair, tuple) and len(pair) == 2:
                        kg, kx = pair
                        if kg == g and kx == x:
                            return v
                return None
            return None

        for g in elements:
            for x in X:
                res = eval_action(g, x)
                if res not in X:
                    return [False, False, False]

        def is_subset(list1, list2):
            return all(item in list2 for item in list1)
            
        def are_equal_lists(list1, list2):
            return is_subset(list1, list2) and is_subset(list2, list1)

        computed_K = []
        for g in elements:
            is_in_K = True
            for x in X:
                if eval_action(g, x) != x:
                    is_in_K = False
                    break
            if is_in_K:
                computed_K.append(g)
                
        if provided_K is not None:
            h1 = are_equal_lists(provided_K, computed_K)
            K = list(provided_K)
        else:
            h1 = True
            K = computed_K

        computed_Gx = []
        for x in X:
            Gx = []
            for g in elements:
                if eval_action(g, x) == x:
                    Gx.append(g)
            computed_Gx.append(Gx)
            
        if provided_Gx is not None:
            h2 = True
            for i, x in enumerate(X):
                try:
                    if callable(provided_Gx):
                        px = provided_Gx(x)
                    elif isinstance(provided_Gx, dict):
                        px = provided_Gx.get(x, [])
                    elif isinstance(provided_Gx, list):
                        px = []
                        for kx, v in provided_Gx:
                            if kx == x:
                                px = v
                                break
                    else:
                        px = []
                except TypeError:
                    px = []
                if not are_equal_lists(px, computed_Gx[i]):
                    h2 = False
                    break
        else:
            h2 = True

        intersection = list(elements)
        for Gx in computed_Gx:
            new_intersection = []
            for item in intersection:
                if item in Gx:
                    new_intersection.append(item)
            intersection = new_intersection
            
        is_equal = are_equal_lists(K, intersection)
        
        is_subgroup = True
        if not K:
            is_subgroup = False
        else:
            if identity not in K:
                is_subgroup = False
            else:
                for a in K:
                    has_inverse = False
                    for b in K:
                        if a * b == identity and b * a == identity:
                            has_inverse = True
                            break
                    if not has_inverse:
                        is_subgroup = False
                        break
                    for b in K:
                        if a * b not in K:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                        
        is_normal = True
        if is_subgroup:
            for g in elements:
                g_inv = None
                for h in elements:
                    if g * h == identity and h * g == identity:
                        g_inv = h
                        break
                if g_inv is None:
                    return [False, False, False]
                
                for k in K:
                    if g * k * g_inv not in K:
                        is_normal = False
                        break
                if not is_normal:
                    break
                    
        conclusion = is_subgroup and is_normal and is_equal
        neg_q = not conclusion
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K is the kernel of the action",
    "H_2: G_x denotes the stabilizer of x in G",
    "¬Q: K is not a normal subgroup of G or is not equal to the intersection of G_x"
]

N_HYP = 2
NEG_Q_INDEX = 2