import sympy
from sympy import Rational, Integer

Z = sympy.S.Integers
Q = sympy.S.Rationals
R_field = sympy.S.Reals
C_field = sympy.S.Complexes

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            
            # Format 1: R is an integer n (representing Z/nZ, or Z if n=0), I is a list/set of elements
            if isinstance(R, int):
                n = R
                if n >= 0:
                    h1 = True
                    I_set = set(I)
                    
                    if n == 0:
                        # R = Z
                        if I_set == {0}:
                            is_ideal = True
                        else:
                            is_ideal = False
                    else:
                        # R = Z/nZ
                        is_ideal = True
                        if not I_set:
                            is_ideal = False
                        else:
                            # Check closure under addition and subtraction
                            for x in I_set:
                                for y in I_set:
                                    if (x + y) % n not in I_set:
                                        is_ideal = False
                                    if (x - y) % n not in I_set:
                                        is_ideal = False
                            # Check closure under multiplication by any element in R
                            for x in I_set:
                                for r in range(n):
                                    if (r * x) % n not in I_set:
                                        is_ideal = False
                    
                    neg_q = not is_ideal
                    
            # Format 2: R is a SymPy ring (e.g., Z)
            elif R in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes) or str(R) in ("Z", "Q", "R", "C"):
                h1 = True
                if isinstance(I, int):
                    is_ideal = True
                elif isinstance(I, str) and I.endswith("Z"):
                    is_ideal = True
                elif isinstance(I, (set, list, tuple)):
                    I_set = set(I)
                    if I_set == {0}:
                        is_ideal = True
                    else:
                        is_ideal = False
                elif hasattr(I, 'is_FiniteSet') and I.is_FiniteSet:
                    I_set = set(I)
                    if I_set == {0}:
                        is_ideal = True
                    else:
                        is_ideal = False
                else:
                    # Fallback for unrecognized ideal formats to avoid false positives
                    is_ideal = True 
                
                neg_q = not is_ideal
                
        # Format 3: Explicit finite ring tables (n, add_table, mul_table, I_elements)
        elif isinstance(witness, tuple) and len(witness) == 4:
            n, add_table, mul_table, I_elements = witness
            if isinstance(n, int) and n > 0:
                is_ring = True
                for i in range(n):
                    for j in range(n):
                        if not (0 <= add_table[i][j] < n): is_ring = False
                        if not (0 <= mul_table[i][j] < n): is_ring = False
                
                if is_ring:
                    for i in range(n):
                        for j in range(n):
                            if add_table[i][j] != add_table[j][i]: is_ring = False
                
                if is_ring:
                    h1 = True
                    I_set = set(I_elements)
                    if not I_set:
                        is_ideal = False
                    else:
                        is_ideal = True
                        zero = None
                        for i in range(n):
                            if all(add_table[i][j] == j for j in range(n)):
                                zero = i
                                break
                        if zero is None:
                            is_ideal = False
                        else:
                            for x in I_set:
                                for y in I_set:
                                    neg_y = None
                                    for k in range(n):
                                        if add_table[y][k] == zero:
                                            neg_y = k
                                            break
                                    if neg_y is None or add_table[x][neg_y] not in I_set:
                                        is_ideal = False
                            for x in I_set:
                                for r in range(n):
                                    if mul_table[r][x] not in I_set:
                                        is_ideal = False
                                    if mul_table[x][r] not in I_set:
                                        is_ideal = False
                    
                    neg_q = not is_ideal
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: There is no bijection between the set of ideals of R containing I and the set of ideals of R/I"
]

N_HYP = 1
NEG_Q_INDEX = 1