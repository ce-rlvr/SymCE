import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: C_1, ..., C_k are the distinct conjugacy classes of G that contain more than one element",
    "¬Q: The order of G is not equal to the order of Z(G) plus the sum of the sizes of C_1, ..., C_k"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_elements(G):
    try:
        attr = getattr(G, 'elements', [])
        return list(attr() if callable(attr) else attr)
    except Exception:
        return []

def conditions(witness):
    try:
        if isinstance(witness, dict) and 'G' in witness and 'C_list' in witness:
            G = witness['G']
            C_list = list(witness['C_list'])
            provided_C = True
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, C_list = witness
            C_list = list(C_list)
            provided_C = True
        else:
            G = witness
            provided_C = False
    except Exception:
        return [False, False]

    # H1: C_1, ..., C_k are the distinct conjugacy classes of G that contain more than one element
    h1 = False
    if not provided_C:
        try:
            C_list = []
            if hasattr(G, 'conjugacy_classes'):
                for c in G.conjugacy_classes():
                    if getattr(c, 'size', 0) > 1:
                        C_list.append(c)
                h1 = True
            else:
                elements = get_elements(G)
                if not elements:
                    raise ValueError("No elements found")
                seen = set()
                for x in elements:
                    if x in seen:
                        continue
                    cls = set()
                    for g in elements:
                        try:
                            cls.add(g * x * (~g))
                        except Exception:
                            cls.add(g * x * (g**-1))
                    cls_frozen = frozenset(cls)
                    if len(cls_frozen) > 1:
                        C_list.append(cls_frozen)
                    seen.update(cls_frozen)
                h1 = True
        except Exception:
            h1 = False
    else:
        try:
            actual_classes = set()
            elements = get_elements(G)
            if hasattr(G, 'conjugacy_classes') and elements:
                for c in G.conjugacy_classes():
                    size = getattr(c, 'size', None)
                    if size is None or size > 1:
                        rep = getattr(c, 'element', None)
                        if rep is not None:
                            try:
                                cls = frozenset(g * rep * (~g) for g in elements)
                            except Exception:
                                cls = frozenset(g * rep * (g**-1) for g in elements)
                            if len(cls) > 1:
                                actual_classes.add(cls)
            elif elements:
                seen = set()
                for x in elements:
                    if x in seen:
                        continue
                    cls = set()
                    for g in elements:
                        try:
                            cls.add(g * x * (~g))
                        except Exception:
                            cls.add(g * x * (g**-1))
                    cls_frozen = frozenset(cls)
                    if len(cls_frozen) > 1:
                        actual_classes.add(cls_frozen)
                    seen.update(cls_frozen)
            else:
                raise ValueError("Cannot compute actual classes without elements")
                
            provided_classes = set()
            for c in C_list:
                if hasattr(c, 'element') and elements:
                    rep = c.element
                    try:
                        cls = frozenset(g * rep * (~g) for g in elements)
                    except Exception:
                        cls = frozenset(g * rep * (g**-1) for g in elements)
                    provided_classes.add(cls)
                else:
                    provided_classes.add(frozenset(c))
            h1 = (provided_classes == actual_classes)
        except Exception:
            h1 = False

    # ¬Q: The order of G is not equal to the order of Z(G) plus the sum of the sizes of C_1, ..., C_k
    try:
        order_G = G.order() if callable(getattr(G, 'order', None)) else G.order
        Z = G.center() if callable(getattr(G, 'center', None)) else G.center
        order_Z = Z.order() if callable(getattr(Z, 'order', None)) else Z.order
        
        sum_C = 0
        for c in C_list:
            if hasattr(c, 'size'):
                sum_C += c.size
            else:
                sum_C += len(list(c))
                
        q = (order_G == order_Z + sum_C)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]