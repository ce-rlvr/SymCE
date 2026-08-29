import sympy

ZZ = sympy.ZZ
QQ = sympy.QQ

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: x is an element of R",
    "¬Q: The sequence of ideal quotients (I : x^n) fails to be an ascending chain or fails to stabilize"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        R, I, x = witness
    except Exception:
        return [False, False, False]
        
    h1 = False
    h2 = False
    neg_q = False
    
    if R == sympy.S.Integers or R == sympy.ZZ or str(R) == "ZZ":
        h1 = True
        try:
            h2 = isinstance(x, int) or (hasattr(x, 'is_integer') and x.is_integer)
            if h2:
                I_set = set(int(i) for i in I)
                x_val = int(x)
                
                def get_A_ZZ(k):
                    xk = x_val ** k
                    if xk == 0:
                        if 0 in I_set:
                            return "ZZ"
                        else:
                            return set()
                    res = set()
                    for i in I_set:
                        if i % xk == 0:
                            res.add(i // xk)
                    return res
                
                A = [get_A_ZZ(k) for k in range(1, 20)]
                
                is_ascending = True
                for i in range(len(A)-1):
                    if A[i] == "ZZ" and A[i+1] == "ZZ":
                        continue
                    if A[i] == "ZZ" and A[i+1] != "ZZ":
                        is_ascending = False
                        break
                    if A[i] != "ZZ" and A[i+1] == "ZZ":
                        continue
                    if not A[i].issubset(A[i+1]):
                        is_ascending = False
                        break
                        
                stabilizes = True
                for i in range(10, len(A)-1):
                    if A[i] != A[i+1]:
                        stabilizes = False
                        break
                        
                Q = is_ascending and stabilizes
                neg_q = not Q
        except Exception:
            pass
            
    elif isinstance(R, int) and R >= 2:
        n = R
        h1 = True
        try:
            h2 = isinstance(x, int) or (hasattr(x, 'is_integer') and x.is_integer)
            if h2:
                I_set = set(int(i) % n for i in I)
                x_val = int(x) % n
                
                def get_A_Zn(k):
                    xk = pow(x_val, k, n)
                    return set(r for r in range(n) if (r * xk) % n in I_set)
                
                A = [get_A_Zn(k) for k in range(1, 2*n + 2)]
                
                is_ascending = all(A[i].issubset(A[i+1]) for i in range(len(A)-1))
                stabilizes = all(A[i] == A[i+1] for i in range(n, len(A)-1))
                
                Q = is_ascending and stabilizes
                neg_q = not Q
        except Exception:
            pass

    return [h1, h2, neg_q]