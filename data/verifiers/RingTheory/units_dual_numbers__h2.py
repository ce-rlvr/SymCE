import sympy
import math
from sympy import ZZ, QQ, RR, CC

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: x = a + be is an element of D with a, b in R",
    "¬Q: x is a unit in D if and only if a is a unit in R fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
            
        R, a, b = witness
        
        # Case 1: R is represented as an integer n, meaning the ring Z/nZ
        if isinstance(R, int) and R >= 1:
            h1 = True
            if isinstance(a, int) and isinstance(b, int):
                h2 = True
                
                a_mod = a % R
                b_mod = b % R
                
                # In Z/nZ, a is a unit iff gcd(a, n) == 1 (for n >= 2)
                if R >= 2:
                    a_is_unit = (math.gcd(a_mod, R) == 1)
                else:
                    a_is_unit = True # In Z/1Z, 0 is a unit
                
                # x = a + be is a unit in D iff there exist c, d in R such that
                # (a+be)(c+de) = 1 + 0e => ac = 1 and ad+bc = 0
                x_is_unit = False
                for c in range(R):
                    if (a_mod * c) % R == 1 % R:
                        for d in range(R):
                            if (a_mod * d + b_mod * c) % R == 0:
                                x_is_unit = True
                                break
                        if x_is_unit:
                            break
                            
                q = (x_is_unit == a_is_unit)
                neg_q = not q
                
        # Case 2: R is given as an explicit finite set/list of elements
        elif isinstance(R, (list, tuple, set)):
            R_list = list(R)
            if not R_list:
                return [False, False, False]
                
            is_comm = True
            for x in R_list:
                for y in R_list:
                    try:
                        if x * y != y * x:
                            is_comm = False
                            break
                    except Exception:
                        is_comm = False
                        break
                if not is_comm:
                    break
                    
            id_elem = None
            for e in R_list:
                try:
                    if all(x * e == x and e * x == x for x in R_list):
                        id_elem = e
                        break
                except Exception:
                    pass
                    
            zero_elem = None
            for z in R_list:
                try:
                    if all(x + z == x and z + x == x for x in R_list):
                        zero_elem = z
                        break
                except Exception:
                    pass
                    
            if is_comm and id_elem is not None and zero_elem is not None:
                h1 = True
                
            if a in R_list and b in R_list:
                h2 = True
                
            if h2 and id_elem is not None and zero_elem is not None:
                a_is_unit = False
                for c in R_list:
                    try:
                        if a * c == id_elem and c * a == id_elem:
                            a_is_unit = True
                            break
                    except Exception:
                        pass
                        
                x_is_unit = False
                for c in R_list:
                    try:
                        if a * c == id_elem and c * a == id_elem:
                            for d in R_list:
                                if a * d + b * c == zero_elem and d * a + c * b == zero_elem:
                                    x_is_unit = True
                                    break
                            if x_is_unit:
                                break
                    except Exception:
                        pass
                        
                q = (x_is_unit == a_is_unit)
                neg_q = not q
                
        # Case 3: R is a sympy Domain (like ZZ, QQ)
        elif hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
            
            try:
                h2 = (a in R) and (b in R)
            except Exception:
                h2 = False
                
            if h1 and h2:
                a_is_unit = False
                if hasattr(R, 'is_unit'):
                    a_is_unit = bool(R.is_unit(a))
                elif R == ZZ:
                    a_is_unit = (abs(a) == 1)
                elif hasattr(R, 'is_Field') and R.is_Field:
                    a_is_unit = (a != 0)
                    
                # In any commutative ring with identity, x = a + be is a unit in D iff a is a unit in R.
                # (The inverse is c + de where c = a^{-1} and d = -a^{-2}b)
                x_is_unit = a_is_unit
                
                q = (x_is_unit == a_is_unit)
                neg_q = not q
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]