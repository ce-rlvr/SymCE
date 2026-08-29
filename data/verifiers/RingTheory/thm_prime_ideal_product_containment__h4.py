import sympy
from sympy import ZZ, QQ, Poly, rem
from sympy.ntheory import isprime
from sympy.abc import x, y, z

# Top-level setup for witness evaluation
# (ZZ, QQ, x, y, z are available for ring/ideal definitions)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should represent the ideals P, A, B in a commutative ring R.
    Supported formats:
      - tuple: (P, A, B) or (R, P, A, B)
      - dict: {'P': P, 'A': A, 'B': B}
    Ideals are represented by their generators (e.g., integers for R=ZZ, polynomials for R=F[x]).
    """
    try:
        if isinstance(witness, dict):
            P = witness.get('P')
            A = witness.get('A')
            B = witness.get('B')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                P, A, B = witness
            elif len(witness) == 4:
                _, P, A, B = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        # Unwrap 1-element tuples/lists (e.g., if ideal is passed as `(2,)`)
        def unwrap(val):
            if isinstance(val, (list, tuple, set)) and len(val) == 1:
                return list(val)[0]
            return val
            
        P = unwrap(P)
        A = unwrap(A)
        B = unwrap(B)
        
        # 1. Try evaluating as integers (ideals in the commutative ring ZZ)
        try:
            P_val = int(P)
            A_val = int(A)
            B_val = int(B)
            
            h1 = True  # ZZ is a commutative ring
            h2 = (P_val == 0) or isprime(abs(P_val))  # Prime ideal check in ZZ
            h3 = True  # Any integer generates an ideal in ZZ
            
            if P_val == 0:
                a_in_p = (A_val == 0)
                b_in_p = (B_val == 0)
            else:
                a_in_p = (A_val % P_val == 0)
                b_in_p = (B_val % P_val == 0)
                
            neg_q = (not a_in_p) and (not b_in_p)
            return [h1, h2, h3, neg_q]
        except (ValueError, TypeError):
            pass
            
        # 2. Try evaluating as polynomials (ideals in a polynomial ring F[x])
        try:
            gens = set()
            for expr in (P, A, B):
                if hasattr(expr, 'free_symbols'):
                    gens.update(expr.free_symbols)
            gens = list(gens)
            if not gens:
                gens = [x]
                
            P_poly = Poly(P, *gens)
            A_poly = Poly(A, *gens)
            B_poly = Poly(B, *gens)
            
            h1 = True  # Polynomial rings over fields are commutative
            h2 = bool(P_poly.is_zero or P_poly.is_irreducible)
            h3 = True  # Any polynomial generates an ideal
            
            if P_poly.is_zero:
                a_in_p = bool(A_poly.is_zero)
                b_in_p = bool(B_poly.is_zero)
            else:
                a_in_p = bool(rem(A_poly, P_poly).is_zero)
                b_in_p = bool(rem(B_poly, P_poly).is_zero)
                
            neg_q = (not a_in_p) and (not b_in_p)
            return [h1, h2, h3, neg_q]
        except Exception:
            pass
            
        return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal of R",
    "H_3: A and B are ideals of R",
    "¬Q: A is not contained in P and B is not contained in P"
]

N_HYP = 3
NEG_Q_INDEX = 3