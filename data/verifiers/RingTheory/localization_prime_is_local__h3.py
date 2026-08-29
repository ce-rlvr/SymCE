import sympy

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, P = witness
        else:
            R = "ZZ"
            P = witness
            
        R_str = str(R)
        
        # H1: R is a commutative ring
        if R_str in ["ZZ", "QQ", "2ZZ", "Z[x]", "Z"]:
            h1 = True
        else:
            h1 = False
            
        # H2: R has a multiplicative identity
        if R_str in ["ZZ", "QQ", "Z[x]", "Z"]:
            h2 = True
        else:
            h2 = False
            
        # neg_Q: R_P is NOT a local ring with unique maximal ideal PR_P
        neg_q = False
        if R_str in ["ZZ", "Z"]:
            try:
                if isinstance(P, list) and len(P) == 1:
                    P = P[0]
                if isinstance(P, str):
                    P_str = P.replace("ZZ", "").replace("Z", "").strip()
                    if P_str == "":
                        n = 1
                    else:
                        n = abs(int(P_str))
                else:
                    n = abs(int(P))
                    
                if n == 0:
                    neg_q = False
                elif n == 1:
                    neg_q = True
                elif sympy.isprime(n):
                    neg_q = False
                else:
                    neg_q = True
            except Exception:
                neg_q = False
        elif R_str == "QQ":
            try:
                if isinstance(P, list) and len(P) == 1:
                    P = P[0]
                if isinstance(P, str):
                    P_str = P.replace("QQ", "").replace("Q", "").strip()
                    if P_str == "":
                        n = 1
                    else:
                        n = abs(int(P_str))
                else:
                    n = abs(int(P))
                    
                if n == 0:
                    neg_q = False
                else:
                    neg_q = True
            except Exception:
                neg_q = False
        elif R_str == "2ZZ":
            neg_q = True
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "¬Q: R_P is not a local ring with unique maximal ideal PR_P"
]

N_HYP = 2
NEG_Q_INDEX = 2