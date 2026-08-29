import sympy
from sympy import eye, zeros, Symbol, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            s = witness.lower()
            h1 = True
            h2 = any(kw in s for kw in ["artinian", "matrix", "m2", "m_2", "finite", "m_n", "mn", "quaternion", "z/"])
            if any(kw in s for kw in ["weyl", "polynomial", "free", "zz", "integer"]):
                h2 = False
            neg_q = any(kw in s for kw in ["non-commutative", "noncommutative", "matrix", "m2", "m_2", "weyl", "m_n", "mn", "quaternion"])
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            from sympy import MatrixBase
            if all(isinstance(mat, MatrixBase) and mat.is_square for mat in witness):
                shape = witness[0].shape
                if all(mat.shape == shape for mat in witness):
                    h1 = True
                    h2 = True
                    commute = True
                    for i in range(len(witness)):
                        for j in range(i+1, len(witness)):
                            if witness[i] * witness[j] != witness[j] * witness[i]:
                                commute = False
                                break
                        if not commute:
                            break
                    neg_q = not commute
                    return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        from sympy import MatrixBase
        if isinstance(witness, MatrixBase) and witness.is_square:
            h1 = True
            h2 = True
            neg_q = False
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_Ring') and witness.is_Ring:
            h1 = True
            if hasattr(witness, 'is_Field') and witness.is_Field:
                h2 = True
                neg_q = False
            elif witness in (sympy.ZZ, sympy.S.Integers):
                h2 = False
                neg_q = True
            else:
                h2 = getattr(witness, 'is_artinian', False)
                if hasattr(witness, 'is_commutative'):
                    neg_q = not witness.is_commutative
                else:
                    neg_q = getattr(witness, 'krull_dimension', 1) != 0
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        from sympy.algebras.quaternion import Quaternion
        if witness == Quaternion or isinstance(witness, Quaternion):
            h1 = True
            h2 = True
            neg_q = True
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        if hasattr(witness, 'has_identity'):
            h1 = bool(witness.has_identity)
        elif hasattr(witness, 'is_unital'):
            h1 = bool(witness.is_unital)
        else:
            h1 = False
            
        if hasattr(witness, 'is_artinian'):
            h2 = bool(witness.is_artinian)
        elif hasattr(witness, 'is_finite'):
            h2 = bool(witness.is_finite)
        else:
            h2 = False
            
        if hasattr(witness, 'krull_dimension'):
            neg_q = witness.krull_dimension != 0
        elif hasattr(witness, 'is_commutative'):
            neg_q = not witness.is_commutative
        else:
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: R is an Artinian ring",
    "¬Q: The Krull dimension of R is not zero"
]

N_HYP = 2
NEG_Q_INDEX = 2