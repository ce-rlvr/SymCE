import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def is_topological_space(space):
    try:
        if not isinstance(space, (tuple, list)) or len(space) != 2:
            return False
        pts, top = space
        if not isinstance(pts, (list, set, tuple, frozenset)):
            return False
        if not isinstance(top, (list, set, tuple, frozenset)):
            return False
            
        pts_set = set(pts)
        top_sets = []
        for U in top:
            if not isinstance(U, (list, set, tuple, frozenset)):
                return False
            top_sets.append(set(U))
            
        if set() not in top_sets: return False
        if pts_set not in top_sets: return False
        
        for U in top_sets:
            if not U.issubset(pts_set): return False
            for V in top_sets:
                if (U | V) not in top_sets: return False
                if (U & V) not in top_sets: return False
                
        return True
    except Exception:
        return False

def is_connected(space):
    try:
        pts, top = space
        if not pts: 
            return True
        pts_set = set(pts)
        top_sets = [set(U) for U in top]
        
        for U in top_sets:
            if not U or U == pts_set: 
                continue
            comp = pts_set - U
            if comp in top_sets:
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    witness should be a tuple: (X, Y, x0, y0)
    where X and Y are topological spaces represented as (points, topology),
    and x0, y0 are the points to be identified.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 4:
            return [False, False, False, False]
        X, Y, x0, y0 = witness
    except Exception:
        return [False, False, False, False]
        
    h1 = is_topological_space(X) and is_topological_space(Y)
    h2 = is_connected(X) and is_connected(Y)
    
    h3 = False
    neg_q = False
    
    try:
        if h1:
            ptsX, topX = X
            ptsY, topY = Y
            
            # Disjoint union Z = X \sqcup Y
            ptsZ = [(0, x) for x in ptsX] + [(1, y) for y in ptsY]
            topZ = []
            for UX in topX:
                for UY in topY:
                    UZ = [(0, x) for x in UX] + [(1, y) for y in UY]
                    topZ.append(UZ)
                    
            # Equivalence classes for the wedge sum
            classes = []
            identified = set()
            p1 = (0, x0)
            p2 = (1, y0)
            
            if p1 in ptsZ and p2 in ptsZ:
                classes.append(frozenset([p1, p2]))
                identified.add(p1)
                identified.add(p2)
                
            for p in ptsZ:
                if p not in identified:
                    classes.append(frozenset([p]))
                    
            # Quotient space W = Z / ~
            ptsW = classes
            topW = []
            
            # A set in the quotient topology is open iff its preimage is open in Z
            for UZ in topZ:
                is_union = True
                for c in classes:
                    intersect = [p for p in c if p in UZ]
                    if intersect and len(intersect) != len(c):
                        is_union = False
                        break
                if is_union:
                    UW = frozenset([c for c in classes if any(p in UZ for p in c)])
                    topW.append(UW)
                    
            # Remove duplicates from topW
            topW_unique = []
            for UW in topW:
                if UW not in topW_unique:
                    topW_unique.append(UW)
                    
            W = (ptsW, topW_unique)
            h3 = True
            
            # Conclusion: The wedge sum is connected
            # Negated conclusion: The wedge sum is NOT connected
            neg_q = not is_connected(W)
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X and Y are topological spaces",
    "H_2: X and Y are connected",
    "H_3: X \\vee Y is the wedge sum of X and Y formed by identifying x0 and y0",
    "¬Q: The wedge sum X \\vee Y is not connected"
]

N_HYP = 3
NEG_Q_INDEX = 3