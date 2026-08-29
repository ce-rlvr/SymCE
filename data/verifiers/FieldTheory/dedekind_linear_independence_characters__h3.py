import sympy
from sympy import Matrix
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a dictionary with keys:
    'M': list of elements in the monoid
    'op': callable f(x, y) for the monoid operation
    'id': the identity element of M
    'L': a sympy domain representing the field (e.g., sympy.QQ)
    'S': list of functions (callables or dicts) from M to L
    """
    
    # H_1: M is a monoid
    h1_ok = False
    try:
        M = witness['M']
        op = witness['op']
        id_elem = witness['id']
        
        is_monoid = True
        # Check closure
        for x in M:
            for y in M:
                if op(x, y) not in M:
                    is_monoid = False
                    break
            if not is_monoid:
                break
                
        # Check associativity
        if is_monoid:
            for x in M:
                for y in M:
                    for z in M:
                        if op(x, op(y, z)) != op(op(x, y), z):
                            is_monoid = False
                            break
                    if not is_monoid:
                        break
                if not is_monoid:
                    break
                    
        # Check identity
        if is_monoid:
            for x in M:
                if op(id_elem, x) != x or op(x, id_elem) != x:
                    is_monoid = False
                    break
                    
        h1_ok = is_monoid
    except Exception:
        h1_ok = False

    # H_2: L is a field
    h2_ok = False
    try:
        L = witness['L']
        if hasattr(L, 'is_Field') and L.is_Field:
            h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: The set S is not linearly independent over L
    neg_q_ok = False
    try:
        S = witness['S']
        M = witness['M']
        L = witness['L']
        
        if len(S) > 0:
            # Check that S contains distinct functions
            distinct = True
            for i in range(len(S)):
                for j in range(i + 1, len(S)):
                    same = True
                    for x in M:
                        val_i = S[i][x] if isinstance(S[i], dict) else S[i](x)
                        val_j = S[j][x] if isinstance(S[j], dict) else S[j](x)
                        if val_i != val_j:
                            same = False
                            break
                    if same:
                        distinct = False
                        break
                if not distinct:
                    break
            
            if distinct:
                # Construct matrix A where A[x, i] = S_i(x)
                # Rows correspond to elements of M, columns to functions in S
                rows = []
                for x in M:
                    row = []
                    for s in S:
                        val = s[x] if isinstance(s, dict) else s(x)
                        row.append(sympy.sympify(val))
                    rows.append(row)
                
                A = Matrix(rows)
                # S is linearly dependent if the rank of A is less than the number of functions in S
                if A.rank() < len(S):
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: M is a monoid",
    "H_2: L is a field",
    "¬Q: The set S is not linearly independent over L"
]

N_HYP = 2
NEG_Q_INDEX = 2