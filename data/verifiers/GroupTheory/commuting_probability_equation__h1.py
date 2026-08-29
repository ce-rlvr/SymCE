import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo, nan, Rational

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

CONDITION_LABELS = [
    "H_1: k is the number of distinct conjugacy classes of G",
    "¬Q: The probability that two uniformly randomly chosen elements of G commute is NOT exactly k/|G|"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        G, k = witness
    except Exception:
        return [False, False]
        
    def check_abelian(grp):
        is_ab = getattr(grp, 'is_abelian', False)
        if callable(is_ab):
            return is_ab()
        return bool(is_ab)

    # H_1: k is the number of distinct conjugacy classes of G
    try:
        if hasattr(G, 'conjugacy_classes'):
            cc = G.conjugacy_classes
            actual_k = len(cc()) if callable(cc) else len(cc)
        else:
            try:
                if hasattr(G, 'generate'):
                    elements = list(G.generate())
                elif hasattr(G, 'elements'):
                    elements = list(G.elements)
                else:
                    elements = list(G)
                
                classes = []
                for x in elements:
                    if any(x in c for c in classes):
                        continue
                    new_class = set()
                    for g in elements:
                        try:
                            inv_g = g**-1
                        except Exception:
                            inv_g = ~g
                        new_class.add(g * x * inv_g)
                    classes.append(new_class)
                actual_k = len(classes)
            except Exception:
                if check_abelian(G):
                    try:
                        if hasattr(G, 'order'):
                            actual_k = G.order() if callable(G.order) else G.order
                        elif hasattr(G, 'generate'):
                            actual_k = len(list(G.generate()))
                        elif hasattr(G, 'elements'):
                            actual_k = len(list(G.elements))
                        else:
                            actual_k = len(list(G))
                    except Exception:
                        actual_k = oo
                else:
                    actual_k = None
                    
        h1 = (k == actual_k)
    except Exception:
        h1 = False

    # neg_Q: The probability that two uniformly randomly chosen elements of G commute is NOT exactly k/|G|
    try:
        if check_abelian(G):
            prob = 1
        else:
            if hasattr(G, 'generate'):
                elements = list(G.generate())
            elif hasattr(G, 'elements'):
                elements = list(G.elements)
            else:
                elements = list(G)
                
            n = len(elements)
            if hasattr(G, 'centralizer'):
                commutes = 0
                for x in elements:
                    cx = G.centralizer(x)
                    commutes += cx.order() if callable(cx.order) else cx.order
            else:
                commutes = sum(1 for a in elements for b in elements if a * b == b * a)
            prob = Rational(commutes, n**2)
            
        try:
            if hasattr(G, 'order'):
                order = G.order() if callable(G.order) else G.order
            elif hasattr(G, 'generate'):
                order = len(list(G.generate()))
            elif hasattr(G, 'elements'):
                order = len(list(G.elements))
            else:
                order = len(list(G))
        except Exception:
            order = oo
            
        if order == oo:
            if k == oo:
                expected = nan
            else:
                expected = 0
        else:
            expected = Rational(k, order)
            
        if expected is nan:
            neg_q = True
        else:
            neg_q = (prob != expected)
            
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]