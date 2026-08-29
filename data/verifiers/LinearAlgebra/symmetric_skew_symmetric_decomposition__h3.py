import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import MatrixBase, Matrix, eye, zeros
from sympy.abc import x, y, z

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    B = witness
    if isinstance(witness, tuple):
        B = witness[-1]
    elif isinstance(witness, dict) and 'B' in witness:
        B = witness['B']

    # H_1: V is a vector space over a field F
    # We assume this holds for any mathematical object provided as a witness.
    h1 = True

    # H_2: The characteristic of F is not 2
    h2 = True
    try:
        if isinstance(B, MatrixBase) and len(B) > 0:
            elem = B[0]
            if hasattr(elem, 'p') and getattr(elem, 'p') == 2:
                h2 = False
            elif hasattr(elem, 'mod') and getattr(elem, 'mod') == 2:
                h2 = False
            elif type(elem).__name__ == 'GaloisFieldElement' and getattr(getattr(elem, 'field', None), 'mod', None) == 2:
                h2 = False
    except Exception:
        pass

    # ¬Q: B cannot be uniquely expressed as the sum of a symmetric bilinear form and a skew-symmetric bilinear form
    neg_q = False
    try:
        if isinstance(B, MatrixBase):
            neg_q = not B.is_square
        elif isinstance(B, list) and len(B) > 0 and isinstance(B[0], list):
            neg_q = any(len(row) != len(B) for row in B)
        elif callable(B):
            from sympy import symbols, expand
            a, b = symbols('a b')
            
            is_bilinear = False
            evaluated_successfully = False
            for dim in [1, 2, 3, 4]:
                try:
                    X = symbols(f'x1:{dim+1}')
                    Y = symbols(f'y1:{dim+1}')
                    Z = symbols(f'z1:{dim+1}')
                    
                    aX_bY = [a*x_val + b*y_val for x_val, y_val in zip(X, Y)]
                    
                    res1 = B(aX_bY, Z)
                    res2 = a*B(X, Z) + b*B(Y, Z)
                    
                    res3 = B(Z, aX_bY)
                    res4 = a*B(Z, X) + b*B(Z, Y)
                    
                    evaluated_successfully = True
                    
                    if expand(res1 - res2) == 0 and expand(res3 - res4) == 0:
                        is_bilinear = True
                    else:
                        is_bilinear = False
                    break
                except Exception:
                    continue
            
            if not evaluated_successfully:
                is_bilinear = False
                
            neg_q = not is_bilinear
        else:
            neg_q = True
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: The characteristic of F is not 2",
    "¬Q: B cannot be uniquely expressed as the sum of a symmetric bilinear form and a skew-symmetric bilinear form"
]

N_HYP = 2
NEG_Q_INDEX = 2