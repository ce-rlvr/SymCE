import sympy
from sympy import QQ, ZZ, Rational, Matrix, eye, zeros, S
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        R = None
        n = None
        
        # Parse witness
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M_obj = witness
        elif isinstance(witness, dict):
            R = witness.get('R')
            M_obj = witness.get('M', witness.get('n'))
        elif hasattr(witness, 'shape') and len(witness.shape) == 2:
            # If witness is a matrix, assume it represents End_R(M) over Q
            R = QQ
            M_obj = witness.shape[0]
        else:
            return [False, False]
            
        # Extract the rank/dimension n of the module M
        if isinstance(M_obj, (int, sympy.Integer)):
            n = int(M_obj)
        elif hasattr(M_obj, 'shape'):
            n = int(M_obj.shape[0])
        elif hasattr(M_obj, 'sets'):
            n = len(M_obj.sets)
        elif hasattr(M_obj, '__len__') and not isinstance(M_obj, str):
            n = len(M_obj)
            
        # Parse string representations of common rings
        if isinstance(R, str):
            if R in ('QQ', 'Q', 'Rational', 'Rationals'):
                R = QQ
            elif R in ('ZZ', 'Z', 'Integer', 'Integers'):
                R = ZZ
            elif R in ('RR', 'R', 'Reals'):
                R = S.Reals
            elif R in ('CC', 'C', 'Complexes'):
                R = S.Complexes
                
        # H_1: R is a right Artinian ring
        # Fields and finite rings are Artinian. ZZ is not.
        h1_ok = False
        if R in (QQ, S.Rationals, S.Reals, S.Complexes):
            h1_ok = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1_ok = True
        elif hasattr(R, 'is_finite') and R.is_finite:
            h1_ok = True
            
        # ¬Q: The endomorphism ring End_R(M) is not a local ring
        # For a field R, End_R(R^n) is isomorphic to M_n(R).
        # M_n(R) is a local ring if and only if n = 1.
        # Thus, it is NOT a local ring when n > 1.
        neg_q_ok = False
        if h1_ok and n is not None:
            try:
                if int(n) > 1:
                    neg_q_ok = True
            except Exception:
                pass
                
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: The endomorphism ring End_R(M) is not a local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1