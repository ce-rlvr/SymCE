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

def is_cayley_table(G):
    if isinstance(G, (list, tuple)) and len(G) > 0 and all(isinstance(row, (list, tuple)) for row in G):
        n = len(G)
        return all(len(row) == n for row in G)
    return False

def cayley_identity(G):
    n = len(G)
    for i in range(n):
        is_id = True
        for j in range(n):
            if G[i][j] != j or G[j][i] != j:
                is_id = False
                break
        if is_id:
            return i
    return None

def cayley_order_2_count(G):
    e = cayley_identity(G)
    if e is None:
        return 0
    count = 0
    n = len(G)
    for i in range(n):
        if i != e and G[i][i] == e:
            count += 1
    return count

def conditions(witness):
    # H1: The order of G is an even integer
    h1 = False
    try:
        if is_cayley_table(witness):
            order_G = len(witness)
        elif hasattr(witness, 'order') and callable(witness.order):
            order_G = witness.order()
        else:
            order_G = len(list(witness))
        
        if isinstance(order_G, (int, sympy.Integer)) and order_G % 2 == 0:
            h1 = True
    except Exception:
        h1 = False

    # neg_Q: The number of elements g in G such that the order of g is 2 is NOT an odd integer
    neg_q = False
    try:
        if is_cayley_table(witness):
            count = cayley_order_2_count(witness)
            neg_q = (count % 2 == 0)
        else:
            count = 0
            elements = list(witness.elements) if hasattr(witness, 'elements') else list(witness)
            
            evaluated_any = False
            for g in elements:
                if hasattr(g, 'order') and callable(g.order):
                    evaluated_any = True
                    if g.order() == 2:
                        count += 1
                elif hasattr(g, 'is_Matrix') and g.is_Matrix:
                    evaluated_any = True
                    if g.shape[0] == g.shape[1]:
                        I = eye(g.shape[0])
                        if g**2 == I and g != I:
                            count += 1
            
            if evaluated_any or len(elements) == 0:
                neg_q = (count % 2 == 0)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is an even integer",
    "¬Q: The number of elements of order 2 is an even integer"
]

N_HYP = 1
NEG_Q_INDEX = 1