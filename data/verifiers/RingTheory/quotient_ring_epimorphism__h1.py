import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The conjecture claims that the canonical projection pi: R -> R/I is an epimorphism
    in the category of rings. This fails if R is a rng (a ring without a multiplicative identity),
    because it is not an object in the category of rings (which requires an identity),
    making pi not a valid morphism in that category.
    """
    # Format 1: witness is an object with methods
    try:
        if hasattr(witness, 'is_ideal') and hasattr(witness, 'has_identity'):
            h1 = witness.is_ideal()
            h2 = True
            neg_q = not witness.has_identity()
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # Format 2: witness is a tuple (R_elements, I_elements)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            
            def contains(lst, item):
                for x in lst:
                    if x == item: return True
                return False

            zero = None
            for r in R:
                is_zero = True
                for x in R:
                    if not contains(R, r + x): is_zero = False
                if is_zero and r + r == r:
                    zero = r
                    break
            
            if zero is not None:
                is_rng = True
                for r1 in R:
                    for r2 in R:
                        if not contains(R, r1 + r2): is_rng = False
                        if not contains(R, r1 * r2): is_rng = False
                
                if is_rng:
                    h1 = True
                    if not contains(I, zero): h1 = False
                    for i in I:
                        for j in I:
                            if not contains(I, i + j): h1 = False
                        has_inv = False
                        for j in I:
                            if i + j == zero: has_inv = True
                        if not has_inv: h1 = False
                        for r in R:
                            if not contains(I, i * r): h1 = False
                            if not contains(I, r * i): h1 = False
                            
                    h2 = True
                    
                    has_id = False
                    for e in R:
                        is_id = True
                        for x in R:
                            if e * x != x or x * e != x:
                                is_id = False
                                break
                        if is_id:
                            has_id = True
                            break
                            
                    neg_q = not has_id
                    return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # Format 3: witness is a dict with 'R' and 'I'
    try:
        if isinstance(witness, dict) and 'R' in witness and 'I' in witness:
            R = witness['R']
            I = witness['I']
            
            def contains(lst, item):
                for x in lst:
                    if x == item: return True
                return False

            zero = None
            for r in R:
                is_zero = True
                for x in R:
                    if not contains(R, r + x): is_zero = False
                if is_zero and r + r == r:
                    zero = r
                    break
            
            if zero is not None:
                is_rng = True
                for r1 in R:
                    for r2 in R:
                        if not contains(R, r1 + r2): is_rng = False
                        if not contains(R, r1 * r2): is_rng = False
                
                if is_rng:
                    h1 = True
                    if not contains(I, zero): h1 = False
                    for i in I:
                        for j in I:
                            if not contains(I, i + j): h1 = False
                        has_inv = False
                        for j in I:
                            if i + j == zero: has_inv = True
                        if not has_inv: h1 = False
                        for r in R:
                            if not contains(I, i * r): h1 = False
                            if not contains(I, r * i): h1 = False
                            
                    h2 = True
                    
                    has_id = False
                    for e in R:
                        is_id = True
                        for x in R:
                            if e * x != x or x * e != x:
                                is_id = False
                                break
                        if is_id:
                            has_id = True
                            break
                            
                    neg_q = not has_id
                    return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # Format 4: witness is (n, add_table, mul_table, I_elements)
    try:
        if isinstance(witness, tuple) and len(witness) == 4 and isinstance(witness[0], int):
            n, add, mul, I = witness
            
            is_rng = True
            for i in range(n):
                for j in range(n):
                    if add[i][j] not in range(n): is_rng = False
                    if mul[i][j] not in range(n): is_rng = False
            
            zero = None
            for i in range(n):
                if all(add[i][j] == j for j in range(n)):
                    zero = i
                    break
            if zero is None:
                is_rng = False

            if is_rng:
                h1 = True
                if not I: h1 = False
                for i in I:
                    for j in I:
                        if add[i][j] not in I: h1 = False
                for i in I:
                    has_inv = False
                    for j in I:
                        if add[i][j] == zero: has_inv = True
                    if not has_inv: h1 = False
                for i in I:
                    for r in range(n):
                        if mul[i][r] not in I: h1 = False
                        if mul[r][i] not in I: h1 = False
                        
                h2 = True
                
                has_id = False
                for e in range(n):
                    is_id = True
                    for x in range(n):
                        if mul[e][x] != x or mul[x][e] != x:
                            is_id = False
                            break
                    if is_id:
                        has_id = True
                        break
                neg_q = not has_id
                return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a two-sided ideal of R",
    "H_2: pi is the canonical projection map",
    "¬Q: The map pi is not an epimorphism in the category of rings"
]

N_HYP = 2
NEG_Q_INDEX = 2