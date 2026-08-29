import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y
from sympy.polys.domains import Domain

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a surjective ring homomorphism",
    "¬Q: S is not a principal ideal ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        R = witness['R']
        S = witness['S']
    except Exception:
        return [False, False, False]
        
    # H1: R and S are rings
    try:
        h1 = getattr(R, 'is_Ring', False) and getattr(S, 'is_Ring', False)
    except Exception:
        h1 = False
        
    # H2: f is a surjective ring homomorphism
    try:
        f = witness['f']
        
        test_elems = []
        try:
            test_elems.extend([R.zero, R.one, R.one + R.one])
            if hasattr(R, 'gens'):
                test_elems.extend(R.gens)
                if len(R.gens) >= 1:
                    test_elems.append(R.gens[0] * (R.one + R.one) + R.one)
                if len(R.gens) >= 2:
                    test_elems.append(R.gens[0] + R.gens[1])
                    test_elems.append(R.gens[0] * R.gens[1])
        except Exception:
            pass
            
        hom_ok = True
        if f(R.one) != S.one or f(R.zero) != S.zero:
            hom_ok = False
        else:
            for a in test_elems:
                for b in test_elems:
                    if f(a + b) != f(a) + f(b):
                        hom_ok = False
                        break
                    if f(a * b) != f(a) * f(b):
                        hom_ok = False
                        break
                if not hom_ok:
                    break
                    
        surj_ok = False
        if hom_ok:
            f_inv = witness.get('f_inv')
            if f_inv is not None:
                S_test = []
                try:
                    S_test.extend([S.zero, S.one, S.one + S.one])
                    if hasattr(S, 'gens'):
                        S_test.extend(S.gens)
                        if len(S.gens) >= 1:
                            S_test.append(S.gens[0] * (S.one + S.one) + S.one)
                except Exception:
                    pass
                
                surj_ok = True
                for s in S_test:
                    try:
                        p = f_inv(s)
                        if f(p) != s:
                            surj_ok = False
                            break
                    except Exception:
                        surj_ok = False
                        break
            elif R == S:
                is_id = True
                for a in test_elems:
                    if f(a) != a:
                        is_id = False
                        break
                if is_id:
                    surj_ok = True
                    
        h2 = hom_ok and surj_ok
    except Exception:
        h2 = False
        
    # neg_Q: S is not a principal ideal ring
    try:
        # In SymPy, is_PID is True for PIDs. We want it to be False.
        neg_q = (getattr(S, 'is_PID', True) is False)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]