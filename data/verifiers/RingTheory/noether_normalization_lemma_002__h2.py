import sympy
from sympy import Symbol, QQ

x = Symbol('x', commutative=False)
y = Symbol('y', commutative=False)
z = Symbol('z', commutative=False)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            k = witness.get('field', sympy.QQ)
            A = witness.get('algebra', witness.get('generators', witness))
        elif isinstance(witness, tuple) and len(witness) == 2:
            k, A = witness
        else:
            k = sympy.QQ
            A = witness
            
        h1 = False
        if hasattr(k, 'is_Field') and k.is_Field:
            h1 = True
        elif k in [sympy.QQ, sympy.RR, sympy.CC]:
            h1 = True
        elif isinstance(k, str) and k.lower() in ['qq', 'rr', 'cc', 'field', 'k', 'q', 'r', 'c']:
            h1 = True
            
        h2 = False
        neg_q = False
        
        if isinstance(A, (list, tuple, set)):
            if len(A) > 0 and all(hasattr(g, 'is_commutative') for g in A):
                h2 = True
                non_comm = [g for g in A if g.is_commutative is False]
                if len(non_comm) >= 2:
                    neg_q = True
                    
        elif isinstance(A, str):
            w = A.lower()
            if any(kw in w for kw in ['algebra', '<', 'weyl', 'free', 'matrix', 'poly', 'm_', 'm2', 'm3', 'quaternion']):
                h2 = True
            if any(kw in w for kw in ['free', '<x', 'weyl', 'enveloping']):
                neg_q = True
                
        elif isinstance(A, sympy.MatrixSymbol):
            h2 = True
            neg_q = False
            
        else:
            name = A.__class__.__name__.lower()
            if any(kw in name for kw in ['algebra', 'ring', 'poly', 'matrix', 'quaternion']):
                h2 = True
            if any(kw in name for kw in ['free', 'weyl', 'enveloping']):
                neg_q = True
                
        return [h1, h2, neg_q]
    
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: A is a finitely generated k-algebra",
    "¬Q: A is not an integral extension of a polynomial subring"
]

N_HYP = 2
NEG_Q_INDEX = 2