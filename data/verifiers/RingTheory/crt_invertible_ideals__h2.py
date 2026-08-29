import math
from sympy import ZZ, QQ, Poly
from sympy.polys.rings import ring

from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are comaximal ideals",
    "¬Q: I \\cap J is not an invertible ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2

def extract_int_gens(obj):
    if isinstance(obj, int):
        return obj
    if isinstance(obj, (tuple, list)) and len(obj) == 1 and isinstance(obj[0], int):
        return obj[0]
    return None

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, (tuple, list)):
            # Case 1: witness is (i, j) or ([i], [j]) representing ideals in Z
            if len(witness) == 2:
                i = extract_int_gens(witness[0])
                j = extract_int_gens(witness[1])
                if i is not None and j is not None:
                    h1 = True
                    h2 = math.gcd(i, j) == 1
                    intersection = 0 if (i == 0 or j == 0) else abs(i * j) // math.gcd(i, j)
                    neg_q = intersection == 0
                    return [h1, h2, neg_q]
                
                # Case 2: witness is (I, J) as SymPy ideals
                I, J = witness
                if hasattr(I, 'ring') and hasattr(J, 'ring') and I.ring == J.ring:
                    R = I.ring
                    h1 = getattr(R, 'is_commutative', True)
                    try:
                        sum_ideal = I + J
                        try:
                            h2 = sum_ideal == R.ideal(1) or sum_ideal.contains(R.one) or sum_ideal.contains(1)
                        except Exception:
                            h2 = R.one in sum_ideal.gens or 1 in sum_ideal.gens
                    except Exception:
                        h2 = False
                    try:
                        K = I.intersect(J)
                        is_zero = K == R.ideal(0) or all(g == 0 for g in K.gens)
                        if is_zero:
                            is_invertible = False
                        else:
                            try:
                                is_invertible = K.is_principal
                            except AttributeError:
                                is_invertible = len(K.gens) == 1
                        neg_q = not is_invertible
                    except Exception:
                        neg_q = False
                    return [bool(h1), bool(h2), bool(neg_q)]
                    
            # Case 3: witness is (R, I, J)
            elif len(witness) == 3:
                R, I, J = witness
                
                # Subcase 3a: R is ZZ and I, J are ints or lists of ints
                if R == ZZ:
                    i = extract_int_gens(I)
                    j = extract_int_gens(J)
                    if i is not None and j is not None:
                        h1 = True
                        h2 = math.gcd(i, j) == 1
                        intersection = 0 if (i == 0 or j == 0) else abs(i * j) // math.gcd(i, j)
                        neg_q = intersection == 0
                        return [h1, h2, neg_q]
                
                # Subcase 3b: R is a SymPy ring, I and J are ideals or lists of generators
                h1 = getattr(R, 'is_commutative', True)
                
                if isinstance(I, (list, tuple)) and hasattr(R, 'ideal'):
                    try: I = R.ideal(*I)
                    except Exception: pass
                if isinstance(J, (list, tuple)) and hasattr(R, 'ideal'):
                    try: J = R.ideal(*J)
                    except Exception: pass
                    
                try:
                    sum_ideal = I + J
                    try:
                        h2 = sum_ideal == R.ideal(1) or sum_ideal.contains(R.one) or sum_ideal.contains(1)
                    except Exception:
                        h2 = R.one in sum_ideal.gens or 1 in sum_ideal.gens
                except Exception:
                    h2 = False
                    
                try:
                    K = I.intersect(J)
                    is_zero = K == R.ideal(0) or all(g == 0 for g in K.gens)
                    if is_zero:
                        is_invertible = False
                    else:
                        try:
                            is_invertible = K.is_principal
                        except AttributeError:
                            is_invertible = len(K.gens) == 1
                    neg_q = not is_invertible
                except Exception:
                    neg_q = False
                    
                return [bool(h1), bool(h2), bool(neg_q)]
                
    except Exception:
        pass
        
    return [False, False, False]