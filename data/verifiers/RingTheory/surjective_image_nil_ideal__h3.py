import sympy
from sympy import ZZ, QQ
from sympy.ntheory import primefactors

# Top-level setup for common finite rings (represented by their modulus)
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Handle dictionary witness
        if isinstance(witness, dict):
            if 'n' in witness and 'm' in witness and 'k' in witness:
                n, m, k = int(witness['n']), int(witness['m']), int(witness['k'])
                h1 = (n >= 0 and m >= 0)
                h2 = (n == 0) if m == 0 else (n % m == 0)
                
                if m == 0:
                    is_nil = (k == 0)
                elif m == 1:
                    is_nil = True
                else:
                    r = 1
                    for p in primefactors(m):
                        r *= p
                    is_nil = (k % r == 0)
                neg_q = not is_nil
                return [h1, h2, neg_q]
                
            if 'R' in witness and 'S' in witness and 'f' in witness and 'I' in witness:
                witness = (witness['R'], witness['S'], witness['f'], witness['I'])
                
        # Handle tuple witness (n, m, k) representing Z/nZ, Z/mZ, and ideal (k)
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            if all(isinstance(x, (int, sympy.Integer)) for x in witness):
                n, m, k = int(witness[0]), int(witness[1]), int(witness[2])
                h1 = (n >= 0 and m >= 0)
                h2 = (n == 0) if m == 0 else (n % m == 0)
                
                if m == 0:
                    is_nil = (k == 0)
                elif m == 1:
                    is_nil = True
                else:
                    r = 1
                    for p in primefactors(m):
                        r *= p
                    is_nil = (k % r == 0)
                neg_q = not is_nil
                return [h1, h2, neg_q]
                
        # Handle tuple witness (R, S, f, I)
        if isinstance(witness, (tuple, list)) and len(witness) == 4:
            R, S, f, I = witness
            
            # Case A: R and S are integers representing Z/nZ and Z/mZ
            if isinstance(R, (int, sympy.Integer)) and isinstance(S, (int, sympy.Integer)):
                n, m = int(R), int(S)
                h1 = (n >= 0 and m >= 0)
                h2 = (n == 0) if m == 0 else (n % m == 0)
                
                if isinstance(I, (int, sympy.Integer)):
                    k = int(I)
                elif isinstance(I, (list, tuple)) and len(I) > 0 and isinstance(I[0], (int, sympy.Integer)):
                    k = int(I[0])
                else:
                    k = 1
                    
                if m == 0:
                    is_nil = (k == 0)
                elif m == 1:
                    is_nil = True
                else:
                    r = 1
                    for p in primefactors(m):
                        r *= p
                    is_nil = (k % r == 0)
                neg_q = not is_nil
                return [h1, h2, neg_q]
                
            # Case B: R and S are standard SymPy domains (e.g., ZZ, QQ)
            valid_domains = (sympy.ZZ, sympy.QQ, sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals)
            if R in valid_domains and S in valid_domains:
                h1 = True
                if R == S:
                    if callable(f):
                        try:
                            h2 = (f(1) == 1 and f(0) == 0)
                        except Exception:
                            h2 = False
                    else:
                        h2 = False
                else:
                    h2 = False
                    
                try:
                    if isinstance(I, (list, tuple)):
                        fk = f(I[0]) if callable(f) else I[0]
                    else:
                        fk = f(I) if callable(f) else I
                    # In these domains, only 0 is nilpotent
                    is_nil = (fk == 0)
                    neg_q = not is_nil
                except Exception:
                    neg_q = False
                    
                return [h1, h2, neg_q]
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: f: R -> S is a surjective ring homomorphism",
    "¬Q: The image f(I) is not a nil ideal of S"
]

N_HYP = 2
NEG_Q_INDEX = 2