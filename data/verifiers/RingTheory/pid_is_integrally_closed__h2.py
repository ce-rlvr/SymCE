import sympy
from sympy import S, ZZ, QQ, Poly, I, sqrt
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)

# Top-level setup
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
trivial = CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: R is not integrally closed in K"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False
    
    try:
        R = None
        K = None
        val_x = None
        
        # Parse the witness
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, K, val_x = witness
            elif len(witness) == 2:
                R, K_or_x = witness
            elif len(witness) == 1:
                R = witness[0]
        else:
            R = witness
            
        # Map common SymPy sets to domains
        if R == S.Integers:
            R = ZZ
        if R == S.Rationals:
            R = QQ
            
        # Check H1: R is a PID
        try:
            h1_ok = bool(R.is_PID)
        except Exception:
            h1_ok = False
            
        # Helper to check if an element is in R
        def is_in_R(val, ring):
            try:
                if ring == ZZ:
                    return val in ZZ
                elif ring == QQ:
                    return val in QQ
                return False
            except Exception:
                return False

        # Helper to check if an element is integral over R
        def is_integral(val, ring):
            try:
                p = sympy.minpoly(val)
                pol = Poly(p)
                lc = pol.LC()
                
                if ring == QQ:
                    # Over a field like QQ, any algebraic element is integral
                    return True
                if ring == ZZ:
                    # Over ZZ, the minimal polynomial must be monic with integer coefficients
                    if lc != 1 and lc != -1:
                        return False
                    for c in pol.coeffs():
                        if not (c in ZZ):
                            return False
                    return True
                return False
            except Exception:
                return False

        # Helper to check if val is integral over R but NOT in R
        def check_x(val, ring):
            return is_integral(val, ring) and not is_in_R(val, ring)

        # Check neg_Q: R is not integrally closed in K
        # This means there exists an element in K (or provided as val_x) 
        # that is integral over R but not in R.
        found_x = False
        
        if val_x is not None:
            if check_x(val_x, R):
                found_x = True
        elif isinstance(witness, tuple) and len(witness) == 2:
            K_or_x = witness[1]
            # Try treating the second element directly as the witness element x
            if check_x(K_or_x, R):
                found_x = True
            else:
                # Otherwise, treat it as the field K and try to extract a generator
                K = K_or_x
                if hasattr(K, 'ext') and check_x(K.ext, R):
                    found_x = True
                elif hasattr(K, 'gen') and check_x(K.gen, R):
                    found_x = True
                elif isinstance(K, (list, tuple, set)):
                    for cand in K:
                        if check_x(cand, R):
                            found_x = True
                            break
                            
        neg_q_ok = found_x

    except Exception:
        pass

    return [h1_ok, neg_q_ok]