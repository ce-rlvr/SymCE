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
        if isinstance(witness, (list, tuple)) and all(isinstance(row, (list, tuple)) for row in witness):
            n = len(witness)
            elements = list(range(n))
            def op(x, y):
                return witness[x][y]
        elif hasattr(witness, 'elements'):
            elements = list(witness.elements)
            def op(x, y):
                return x * y
        elif isinstance(witness, (set, list, tuple)):
            elements = list(witness)
            def op(x, y):
                return x * y
        else:
            return [False, False]

        n = len(elements)
        if n > 200:
            return [False, False]
            
        if n == 0:
            is_hom = True
            is_ab = False
            return [True, not (is_hom == is_ab)]

        table = []
        elem_to_idx = {e: i for i, e in enumerate(elements)}
        
        for x in elements:
            row = []
            for y in elements:
                try:
                    res = op(x, y)
                except Exception:
                    return [False, False]
                if res not in elem_to_idx:
                    return [False, False]
                row.append(elem_to_idx[res])
            table.append(row)

        is_hom = True
        for i in range(n):
            for j in range(n):
                xy = table[i][j]
                f_xy = table[xy][xy]
                f_x = table[i][i]
                f_y = table[j][j]
                if f_xy != table[f_x][f_y]:
                    is_hom = False
                    break
            if not is_hom:
                break

        is_ab = True
        for i in range(n):
            for j in range(n):
                if table[i][j] != table[j][i]:
                    is_ab = False
                    break
            if not is_ab:
                break
                
        if is_ab:
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if table[table[i][j]][k] != table[i][table[j][k]]:
                            is_ab = False
                            break
                    if not is_ab: break
                if not is_ab: break
                
        identity = -1
        if is_ab:
            for i in range(n):
                if all(table[i][j] == j and table[j][i] == j for j in range(n)):
                    identity = i
                    break
            if identity == -1:
                is_ab = False
                
        if is_ab:
            for i in range(n):
                has_inv = False
                for j in range(n):
                    if table[i][j] == identity and table[j][i] == identity:
                        has_inv = True
                        break
                if not has_inv:
                    is_ab = False
                    break

        h1 = True
        q = (is_hom == is_ab)
        neg_q = not q
        
        return [h1, neg_q]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: Let f: G -> G be the map defined by f(x) = x^2 for all x in G",
    "¬Q: The map f is a group homomorphism if and only if G is an abelian group is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1