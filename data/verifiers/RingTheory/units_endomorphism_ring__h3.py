import sympy as sp
from sympy import Matrix, eye, zeros, Rational
from sympy.combinatorics import Permutation

# Standard bindings relevant to modules and endomorphisms
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    
    Hypotheses:
      H1: R is a ring.
      H2: M is a left R-module.
      H3: f is an element of End_R(M).
      
    Conclusion to fail:
      f is a unit in End_R(M) if and only if f is an R-module automorphism of M.
    """
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        # 1. Custom mock object (allows explicit counterexamples)
        if hasattr(witness, 'is_unit') and (hasattr(witness, 'is_automorphism') or hasattr(witness, 'is_auto')):
            h1 = bool(getattr(witness, 'is_ring', True))
            h2 = bool(getattr(witness, 'is_module', True))
            h3 = bool(getattr(witness, 'is_endomorphism', True))
            
            is_unit = witness.is_unit() if callable(witness.is_unit) else witness.is_unit
            
            if hasattr(witness, 'is_automorphism'):
                is_auto = witness.is_automorphism() if callable(witness.is_automorphism) else witness.is_automorphism
            else:
                is_auto = witness.is_auto() if callable(witness.is_auto) else witness.is_auto
                
            neg_q = not (bool(is_unit) == bool(is_auto))
            return [h1, h2, h3, neg_q]

        # 2. Tuple of (matrix, domain)
        if isinstance(witness, tuple) and len(witness) == 2:
            mat, domain = witness
            if hasattr(mat, 'rows') and hasattr(mat, 'cols') and hasattr(mat, 'det'):
                h1 = True
                h2 = True
                h3 = (mat.rows == mat.cols)
                if h3:
                    det = mat.det()
                    if domain == sp.ZZ or str(domain) == 'ZZ':
                        is_unit = (det == 1 or det == -1)
                        is_auto = (det == 1 or det == -1)
                    else:
                        try:
                            is_unit = bool(det != 0)
                            is_auto = bool(det != 0)
                        except TypeError:
                            is_unit = (det is not sp.S.Zero)
                            is_auto = (det is not sp.S.Zero)
                    neg_q = not (is_unit == is_auto)
                return [h1, h2, h3, neg_q]

        # 3. SymPy Matrix
        if hasattr(witness, 'rows') and hasattr(witness, 'cols') and hasattr(witness, 'det'):
            h1 = True
            h2 = True
            h3 = (witness.rows == witness.cols)
            if h3:
                det = witness.det()
                if all(getattr(val, 'is_integer', False) for val in witness):
                    is_unit = (det == 1 or det == -1)
                    is_auto = (det == 1 or det == -1)
                else:
                    try:
                        is_unit = bool(det != 0)
                        is_auto = bool(det != 0)
                    except TypeError:
                        is_unit = (det is not sp.S.Zero)
                        is_auto = (det is not sp.S.Zero)
                neg_q = not (is_unit == is_auto)
            return [h1, h2, h3, neg_q]

        # 4. Integer or Rational (1x1 matrix equivalent)
        if isinstance(witness, (int, sp.Integer, sp.Rational)):
            h1 = True
            h2 = True
            h3 = True
            if isinstance(witness, (int, sp.Integer)):
                is_unit = (witness == 1 or witness == -1)
                is_auto = (witness == 1 or witness == -1)
            else:
                is_unit = (witness != 0)
                is_auto = (witness != 0)
            neg_q = not (is_unit == is_auto)
            return [h1, h2, h3, neg_q]

        # 5. Permutation (represents a permutation matrix)
        if isinstance(witness, Permutation):
            h1 = True
            h2 = True
            h3 = True
            is_unit = True
            is_auto = True
            neg_q = not (is_unit == is_auto)
            return [h1, h2, h3, neg_q]

    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M is a left R-module",
    "H_3: f is an element of End_R(M)",
    "¬Q: f is a unit in End_R(M) is not equivalent to f being an R-module automorphism of M"
]

N_HYP = 3
NEG_Q_INDEX = 3