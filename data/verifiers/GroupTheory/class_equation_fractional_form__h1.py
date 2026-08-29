import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, oo
import math

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

def get_elems(obj):
    if hasattr(obj, 'elements'):
        elems = obj.elements
        if callable(elems):
            return list(elems())
        return list(elems)
    elif hasattr(obj, 'generate'):
        return list(obj.generate())
    else:
        return list(obj)

def conditions(witness):
    is_tuple_witness = False
    try:
        if isinstance(witness, dict) and 'k' in witness:
            G = witness['G']
            k = witness['k']
            X = witness['X']
            C = witness['C']
            is_tuple_witness = True
        elif isinstance(witness, tuple) and len(witness) == 4:
            G, k, X, C = witness
            is_tuple_witness = True
    except Exception:
        pass

    if not is_tuple_witness:
        # Witness is just G; we compute the definitions to check the conclusion
        try:
            G = witness
            if hasattr(G, 'conjugacy_classes'):
                classes = G.conjugacy_classes()
                if callable(classes):
                    classes = classes()
            else:
                classes = G.classes
            k = len(classes)
            X = []
            for c in classes:
                if hasattr(c, 'elements'):
                    X.append(list(get_elems(c))[0])
                elif hasattr(c, 'list'):
                    X.append(c.list[0])
                elif isinstance(c, (list, tuple)):
                    X.append(c[0])
                elif isinstance(c, set):
                    X.append(next(iter(c)))
                else:
                    X.append(list(c)[0])
            C = []
            for x in X:
                if hasattr(G, 'centralizer'):
                    C.append(G.centralizer(x))
                elif hasattr(G, 'centraliser'):
                    C.append(G.centraliser(x))
                else:
                    G_elems = get_elems(G)
                    c_x = []
                    for g in G_elems:
                        try:
                            if g * x == x * g:
                                c_x.append(g)
                        except Exception:
                            pass
                    C.append(c_x)
            
            h1 = True
            h2 = True
            h3 = True
            
            total = Rational(0, 1)
            for c_x in C:
                if hasattr(c_x, 'order'):
                    order = c_x.order()
                    if callable(order):
                        order = order()
                elif hasattr(c_x, '__len__'):
                    order = len(c_x)
                else:
                    order = len(get_elems(c_x))
                
                if order == oo or (isinstance(order, float) and math.isinf(order)):
                    term = Rational(0, 1)
                elif int(order) == 0:
                    raise ValueError("Order cannot be zero")
                else:
                    term = Rational(1, int(order))
                total += term
            neg_q = (total != 1)
            return [h1, h2, h3, neg_q]
        except Exception:
            return [False, False, False, False]

    # Tuple witness: explicitly check the hypotheses
    try:
        if hasattr(G, 'conjugacy_classes'):
            classes = G.conjugacy_classes()
            if callable(classes):
                classes = classes()
        else:
            classes = G.classes
        h1 = (k == len(classes))
    except Exception:
        h1 = False

    try:
        if len(X) != k:
            h2 = False
        else:
            if hasattr(G, 'conjugacy_classes'):
                classes = G.conjugacy_classes()
                if callable(classes):
                    classes = classes()
            else:
                classes = G.classes
            
            covered_classes = []
            for x in X:
                for c in classes:
                    in_c = False
                    try:
                        if x in c: in_c = True
                    except Exception:
                        pass
                    if not in_c and hasattr(c, 'elements'):
                        try:
                            if x in get_elems(c): in_c = True
                        except Exception:
                            pass
                    if not in_c and hasattr(c, 'list'):
                        try:
                            if x in c.list: in_c = True
                        except Exception:
                            pass
                    if not in_c and isinstance(c, (list, set, tuple)):
                        try:
                            if x in c: in_c = True
                        except Exception:
                            pass
                    if in_c:
                        already_covered = False
                        for cov in covered_classes:
                            try:
                                if c is cov or c == cov:
                                    already_covered = True
                                    break
                            except Exception:
                                if c is cov:
                                    already_covered = True
                                    break
                        if not already_covered:
                            covered_classes.append(c)
                        break
            h2 = (len(covered_classes) == k)
    except Exception:
        h2 = False

    try:
        if len(C) != k:
            h3 = False
        else:
            h3 = True
            for x, c_x in zip(X, C):
                expected_c = None
                if hasattr(G, 'centralizer'):
                    expected_c = G.centralizer(x)
                elif hasattr(G, 'centraliser'):
                    expected_c = G.centraliser(x)
                else:
                    G_elems = get_elems(G)
                    expected_c = []
                    for g in G_elems:
                        try:
                            if g * x == x * g:
                                expected_c.append(g)
                        except Exception:
                            pass
                
                c_x_elems = get_elems(c_x)
                expected_c_elems = get_elems(expected_c)
                
                if len(c_x_elems) != len(expected_c_elems):
                    h3 = False
                    break
                
                for elem in c_x_elems:
                    found = False
                    for exp_elem in expected_c_elems:
                        try:
                            if elem is exp_elem or elem == exp_elem:
                                found = True
                                break
                        except Exception:
                            if elem is exp_elem:
                                found = True
                                break
                    if not found:
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    try:
        total = Rational(0, 1)
        for c_x in C:
            if hasattr(c_x, 'order'):
                order = c_x.order()
                if callable(order):
                    order = order()
            elif hasattr(c_x, '__len__'):
                order = len(c_x)
            else:
                order = len(get_elems(c_x))
            
            if order == oo or (isinstance(order, float) and math.isinf(order)):
                term = Rational(0, 1)
            elif int(order) == 0:
                raise ValueError("Order cannot be zero")
            else:
                term = Rational(1, int(order))
            total += term
        neg_q = (total != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: k is the number of distinct conjugacy classes of G",
    "H_2: x_1, ..., x_k are representatives of the k distinct conjugacy classes of G",
    "H_3: C_G(x_i) is the centralizer of x_i in G",
    "¬Q: \\sum_{i=1}^k \\frac{1}{|C_G(x_i)|} != 1"
]

N_HYP = 3
NEG_Q_INDEX = 3