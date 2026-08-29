import sympy as sp
from sympy.abc import x, y, z
from sympy.polys.domains import ZZ, QQ
from sympy import factor_list, isprime

def check_finite_ring(R, P, add, mul):
    try:
        h1 = True
        for a in R:
            for b in R:
                if mul(a, b) != mul(b, a):
                    h1 = False
                    break
            if not h1: break
            
        h2 = True
        if len(P) == len(R) or len(P) == 0:
            h2 = False
            
        if h2:
            for p1 in P:
                for p2 in P:
                    if add(p1, p2) not in P:
                        h2 = False
                        break
                if not h2: break
                
        if h2:
            for p in P:
                for r in R:
                    if mul(p, r) not in P:
                        h2 = False
                        break
                if not h2: break
                
        if h2:
            for a in R:
                for b in R:
                    if mul(a, b) in P:
                        if a not in P and b not in P:
                            h2 = False
                            break
                if not h2: break
                
        neg_q = False
        S = [e for e in R if e not in P]
        
        def divides_in_RP(r1, r2):
            for v in S:
                for w in R:
                    if mul(r2, v) == mul(r1, w):
                        return True
            return False

        is_val_ring = True
        for a in R:
            for b in R:
                if not divides_in_RP(a, b) and not divides_in_RP(b, a):
                    is_val_ring = False
                    break
            if not is_val_ring:
                break
                
        neg_q = not is_val_ring
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

def check_poly_ring_duck(R, P_gens):
    try:
        h1 = getattr(R, 'is_commutative', True)
        h2 = False
        
        gens_set = set(P_gens)
        
        if hasattr(R, 'gens'):
            R_gens_str = [str(g) for g in R.gens]
            
            is_field_domain = False
            if hasattr(R, 'domain') and getattr(R.domain, 'is_Field', False):
                is_field_domain = True
                
            is_valid_prime_ideal = True
            for g in gens_set:
                s = str(g)
                if s in R_gens_str:
                    continue
                try:
                    val = int(s)
                    if isprime(val):
                        if is_field_domain:
                            is_valid_prime_ideal = False
                            break
                        continue
                except Exception:
                    pass
                is_valid_prime_ideal = False
                
            if is_valid_prime_ideal:
                h2 = True
        else:
            is_valid_prime_ideal = False
            
        if is_valid_prime_ideal:
            pass
        elif len(P_gens) == 1:
            try:
                factors = factor_list(P_gens[0])
                if len(factors[1]) == 1 and factors[1][0][1] == 1:
                    h2 = True
            except Exception:
                pass
                
        if is_valid_prime_ideal:
            height = len(gens_set)
        else:
            height = len(gens_set)
            
        neg_q = (height > 1)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

def conditions(witness):
    try:
        R, P = None, None
        add, mul = None, None
        
        if isinstance(witness, tuple) and len(witness) == 2:
            R, P = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'P'):
            R = witness.R
            P = witness.P
            if hasattr(witness, 'add'): add = witness.add
            if hasattr(witness, 'mul'): mul = witness.mul
        elif hasattr(witness, 'elements') and hasattr(witness, 'P'):
            R = witness.elements
            P = witness.P
            if hasattr(witness, 'add'): add = witness.add
            if hasattr(witness, 'mul'): mul = witness.mul
        else:
            return [False, False, False]
            
        if isinstance(R, (list, tuple, set)):
            R = list(R)
            P = list(P)
            if len(R) > 0:
                if add is None or mul is None:
                    a = R[0]
                    if hasattr(a, '__add__') and hasattr(a, '__mul__'):
                        add = lambda x, y: x + y
                        mul = lambda x, y: x * y
                    else:
                        return [False, False, False]
                return check_finite_ring(R, P, add, mul)
            return [False, False, False]
            
        if hasattr(R, 'gens') or hasattr(R, 'domain'):
            if hasattr(P, 'gens'):
                P_gens = P.gens
            elif isinstance(P, (list, tuple, set)):
                P_gens = list(P)
            else:
                P_gens = [P]
            return check_poly_ring_duck(R, P_gens)
            
        from sympy.polys.domains import ZZ, QQ, RR, CC
        if R in (ZZ, QQ, RR, CC) or getattr(R, 'is_Field', False) or R in (sp.S.Integers, sp.S.Rationals, sp.S.Reals, sp.S.Complexes):
            return [True, True, False]
            
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal of R",
    "¬Q: The localized ring R_P is NOT a valuation ring"
]

N_HYP = 2
NEG_Q_INDEX = 2