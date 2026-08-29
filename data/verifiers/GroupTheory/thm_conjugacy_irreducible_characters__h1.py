import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    try:
        G, x, y = witness
    except Exception:
        return [False, False]
    
    # H_1: x and y are elements of G
    h1 = False
    try:
        if hasattr(G, '__contains__'):
            h1 = (x in G) and (y in G)
        elif hasattr(G, 'contains'):
            c_x = G.contains(x)
            c_y = G.contains(y)
            if callable(c_x): c_x = c_x()
            if callable(c_y): c_y = c_y()
            h1 = bool(c_x and c_y)
        elif hasattr(G, 'elements'):
            elements = G.elements
            if callable(elements): elements = elements()
            h1 = (x in elements) and (y in elements)
    except Exception:
        pass

    # neg_Q: Conjugacy of x and y is not equivalent to them having the same irreducible complex characters
    neg_q = False
    try:
        conjugate = None
        if hasattr(G, 'is_conjugate'):
            conjugate = G.is_conjugate(x, y)
            if callable(conjugate): conjugate = conjugate()
        elif hasattr(G, 'are_conjugate'):
            conjugate = G.are_conjugate(x, y)
            if callable(conjugate): conjugate = conjugate()
        elif hasattr(G, 'conjugate'):
            conjugate = G.conjugate(x, y)
            if callable(conjugate): conjugate = conjugate()
        elif hasattr(G, 'conjugacy_classes'):
            classes = G.conjugacy_classes()
            if callable(classes): classes = classes()
            idx_x = next(i for i, c in enumerate(classes) if x in c)
            idx_y = next(i for i, c in enumerate(classes) if y in c)
            conjugate = (idx_x == idx_y)
        elif hasattr(G, 'elements'):
            elements = G.elements
            if callable(elements): elements = elements()
            conjugate = False
            for i, g in enumerate(elements):
                if i > 2000:
                    break
                try:
                    if g * x * g**-1 == y:
                        conjugate = True
                        break
                except Exception:
                    pass
                try:
                    if g * x * ~g == y:
                        conjugate = True
                        break
                except Exception:
                    pass

        same_chars = None
        if hasattr(G, 'has_same_characters'):
            same_chars = G.has_same_characters(x, y)
            if callable(same_chars): same_chars = same_chars()
        elif hasattr(G, 'same_characters'):
            same_chars = G.same_characters(x, y)
            if callable(same_chars): same_chars = same_chars()
        elif hasattr(G, 'characters'):
            cx = G.characters(x)
            cy = G.characters(y)
            if callable(cx): cx = cx()
            if callable(cy): cy = cy()
            same_chars = (cx == cy)
        elif hasattr(G, 'character_table') and hasattr(G, 'conjugacy_classes'):
            classes = G.conjugacy_classes()
            if callable(classes): classes = classes()
            idx_x = next(i for i, c in enumerate(classes) if x in c)
            idx_y = next(i for i, c in enumerate(classes) if y in c)
            table = G.character_table()
            if callable(table): table = table()
            same_chars = True
            for row in table:
                diff = row[idx_x] - row[idx_y]
                if diff != 0:
                    try:
                        if sympy.simplify(diff) != 0:
                            same_chars = False
                            break
                    except Exception:
                        same_chars = False
                        break
                        
        if conjugate is not None and same_chars is not None:
            conclusion = (bool(conjugate) == bool(same_chars))
            neg_q = not conclusion
            
    except Exception:
        pass

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "¬Q: Conjugacy of x and y is not equivalent to them having the same irreducible complex characters"
]

N_HYP = 1
NEG_Q_INDEX = 1