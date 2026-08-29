import sympy
from sympy import ZZ, QQ
from sympy.abc import x

# Top-level setup
Z = ZZ
Q = QQ

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            R = witness
            M = witness
            
        def normalize(obj):
            if obj is int: return 'ZZ'
            if obj is float: return 'RR'
            s = str(obj)
            if obj == ZZ or s in ['ZZ', 'Z', 'Integers', 'S.Integers']: return 'ZZ'
            if obj == QQ or s in ['QQ', 'Q', 'Rationals', 'S.Rationals']: return 'QQ'
            if s in ['RR', 'R', 'Reals', 'S.Reals']: return 'RR'
            if s in ['CC', 'C', 'Complexes', 'S.Complexes']: return 'CC'
            if s in ['Z2', 'Z/2Z', 'Z_2']: return 'Z2'
            if s in ['Q/Z', 'QQ/ZZ']: return 'Q/Z'
            return s
            
        R_norm = normalize(R)
        M_norm = normalize(M)
            
        # H1: R is an integral domain
        try:
            h1 = False
            if hasattr(R, 'is_domain') and R.is_domain:
                h1 = True
            else:
                if R_norm in ['ZZ', 'QQ', 'RR', 'CC', 'ZZ[x]', 'QQ[x]', 'RR[x]', 'CC[x]']:
                    h1 = True
                    
            # Implicit hypothesis: M must be a valid R-module
            if R_norm in ['QQ', 'RR', 'CC'] and M_norm in ['ZZ', 'Z2', 'ZZ[x]']:
                h1 = False
        except Exception:
            h1 = False
            
        # neg_Q: M is NOT a divisible R-module
        try:
            divisible = True # Default to True so unknown pairs are not falsely accepted
            
            if R_norm == 'ZZ':
                if M_norm in ['ZZ', 'Z2', 'ZZ[x]']:
                    divisible = False
                elif M_norm in ['QQ', 'RR', 'CC', 'Q/Z', 'QQ[x]']:
                    divisible = True
            elif R_norm in ['QQ', 'RR', 'CC']:
                if M_norm in ['QQ', 'RR', 'CC', 'QQ[x]', 'RR[x]', 'CC[x]']:
                    divisible = True
            elif R_norm == M_norm:
                is_field = False
                if hasattr(R, 'is_Field'):
                    is_field = bool(R.is_Field)
                elif R_norm in ['QQ', 'RR', 'CC']:
                    is_field = True
                
                if not is_field:
                    divisible = False
                    
            neg_q = not divisible
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: M is not a divisible R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1