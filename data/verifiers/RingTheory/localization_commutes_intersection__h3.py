import sympy
from sympy.abc import *

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        # witness is expected to be a tuple (n, S, I, J)
        # where n is an integer representing the ring Z/nZ (or Z if n=0),
        # or a sympy domain. S, I, J are lists of elements.
        n, S, I, J = witness
        
        # H_1: R is a commutative ring with identity
        if isinstance(n, int):
            h1 = (n >= 0)
        else:
            h1 = True
            
        # H_2: S is a multiplicatively closed subset of R
        S_list = list(S)
        has_one = False
        for s in S_list:
            if isinstance(n, int) and n > 0:
                if s % n == 1:
                    has_one = True
                    break
            else:
                if s == 1:
                    has_one = True
                    break
                try:
                    if sympy.simplify(s - 1) == 0:
                        has_one = True
                        break
                except Exception:
                    pass
                    
        is_closed = True
        for a in S_list:
            for b in S_list:
                prod = a * b
                found = False
                for s in S_list:
                    if isinstance(n, int) and n > 0:
                        if prod % n == s % n:
                            found = True
                            break
                    else:
                        if prod == s:
                            found = True
                            break
                        try:
                            if sympy.simplify(prod - s) == 0:
                                found = True
                                break
                        except Exception:
                            pass
                if not found:
                    is_closed = False
                    break
            if not is_closed:
                break
                
        h2 = has_one and is_closed
        
        # Conclusion: S^{-1}(I \cap J) = S^{-1}I \cap S^{-1}J
        I_list = list(I)
        J_list = list(J)
        
        # Compute I \cap J
        I_cap_J = []
        for i in I_list:
            for j in J_list:
                if isinstance(n, int) and n > 0:
                    if i % n == j % n:
                        I_cap_J.append(i)
                        break
                else:
                    if i == j:
                        I_cap_J.append(i)
                        break
                    try:
                        if sympy.simplify(i - j) == 0:
                            I_cap_J.append(i)
                            break
                    except Exception:
                        pass
                        
        # Helper to check equivalence of fractions in S^{-1}R
        def is_equiv(p1, p2):
            r1, s1 = p1
            r2, s2 = p2
            for u in S_list:
                val = u * (r1 * s2 - r2 * s1)
                if isinstance(n, int) and n > 0:
                    if val % n == 0:
                        return True
                else:
                    if val == 0:
                        return True
                    try:
                        if sympy.simplify(val) == 0:
                            return True
                    except Exception:
                        pass
            return False

        # Check if S^{-1}I \cap S^{-1}J \subseteq S^{-1}(I \cap J)
        # Since the reverse inclusion always holds, this checks set equality.
        subset_holds = True
        for i in I_list:
            for s1 in S_list:
                p1 = (i, s1)
                
                # Check if p1 is in S^{-1}J
                in_S_inv_J = False
                for j in J_list:
                    for s2 in S_list:
                        if is_equiv(p1, (j, s2)):
                            in_S_inv_J = True
                            break
                    if in_S_inv_J:
                        break
                
                if in_S_inv_J:
                    # p1 is in S^{-1}I \cap S^{-1}J
                    # Check if p1 is in S^{-1}(I \cap J)
                    in_S_inv_I_cap_J = False
                    for x in I_cap_J:
                        for s3 in S_list:
                            if is_equiv(p1, (x, s3)):
                                in_S_inv_I_cap_J = True
                                break
                        if in_S_inv_I_cap_J:
                            break
                    
                    if not in_S_inv_I_cap_J:
                        subset_holds = False
                        break
            if not subset_holds:
                break
                
        neg_q = not subset_holds
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    r"H_1: R is a commutative ring with identity",
    r"H_2: S is a multiplicatively closed subset of R",
    r"¬Q: S^{-1}(I \cap J) \neq S^{-1}I \cap S^{-1}J"
]

N_HYP = 2
NEG_Q_INDEX = 2