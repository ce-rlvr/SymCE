import sympy
from sympy import S, Symbol, symbols
from sympy.polys.domains import ZZ, QQ, RR, CC, FF, GF

# Top-level setup
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    # 1. Dictionary support
    if isinstance(witness, dict):
        return [
            bool(witness.get('H1', False)),
            bool(witness.get('H2', False)),
            bool(witness.get('H3', False)),
            bool(witness.get('H4', False)),
            bool(witness.get('H5', False)),
            bool(witness.get('neg_Q', False))
        ]
    
    # 2. Object with methods support
    if hasattr(witness, 'H1') and callable(getattr(witness, 'H1')):
        try:
            return [
                bool(witness.H1()),
                bool(witness.H2()),
                bool(witness.H3()),
                bool(witness.H4()),
                bool(witness.H5()),
                bool(witness.neg_Q())
            ]
        except Exception:
            pass

    # 3. Tuple support
    try:
        R, K, L, A, S_set = witness
        
        h1 = h2 = h3 = h4 = h5 = neg_q = False
        
        # H1: R is an integral domain
        if hasattr(R, 'is_domain') and R.is_domain:
            h1 = True
        elif R in [ZZ, QQ, S.Integers, S.Rationals]:
            h1 = True
            
        # H2: L is an algebraic field extension of K
        if L == K:
            h2 = True
        elif hasattr(L, 'is_algebraic_extension') and L.is_algebraic_extension(K):
            h2 = True
            
        # H3: A is the integral closure of R in L
        if (R == ZZ or R == S.Integers) and hasattr(L, 'characteristic') and L.characteristic > 0 and A == L:
            h3 = True
        elif A == R and L == K:
            h3 = True
            
        # H4: S is a multiplicatively closed subset of R
        if isinstance(S_set, list):
            h4 = True  # Interpreted as generators of the multiplicatively closed set
        elif isinstance(S_set, set):
            h4 = all((a*b) in S_set for a in S_set for b in S_set)
        elif callable(S_set):
            h4 = True
            
        # H5: 0 is not an element of S
        if isinstance(S_set, (list, set)):
            h5 = 0 not in S_set
        elif callable(S_set):
            try:
                h5 = not S_set(0)
            except Exception:
                h5 = False
            
        # neg_Q: S^{-1}A is NOT the integral closure of S^{-1}R in L
        if (R == ZZ or R == S.Integers) and hasattr(L, 'characteristic') and L.characteristic > 0:
            p = L.characteristic
            if isinstance(S_set, (list, set)):
                for s in S_set:
                    try:
                        if int(s) % p == 0:
                            neg_q = True
                            break
                    except Exception:
                        pass
            elif callable(S_set):
                try:
                    if S_set(p):
                        neg_q = True
                except Exception:
                    pass
                
        return [h1, h2, h3, h4, h5, neg_q]
    except Exception:
        pass

    return [False] * 6

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: L is an algebraic field extension of K",
    "H_3: A is the integral closure of R in L",
    "H_4: S is a multiplicatively closed subset of R",
    "H_5: 0 is not an element of S",
    "¬Q: The localized ring S^{-1}A is NOT the integral closure of S^{-1}R in L"
]

N_HYP = 5
NEG_Q_INDEX = 5