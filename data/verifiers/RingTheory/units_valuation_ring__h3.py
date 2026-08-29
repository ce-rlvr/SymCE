import sympy
from sympy import Rational, Integer, Poly, symbols
from sympy.abc import x, y, z
import sympy.ntheory

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    
    The witness must be a dictionary containing:
      'K': a field (e.g., sympy.QQ)
      'v': a valuation function v: K^x -> Gamma
      'R': a ring (e.g., sympy.ZZ)
      'u': an element of R
    """
    try:
        K = witness['K']
        v = witness['v']
        R = witness['R']
        u = witness['u']
    except Exception:
        return [False, False, False, False]

    # H_1: K is a field
    try:
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False

    # H_2: v is a valuation on K
    try:
        h2 = True
        try:
            k_zero = K.zero
        except AttributeError:
            k_zero = 0
            
        test_elements = []
        # Generate some test elements from K
        for i in range(1, 20):
            try:
                el = K(i)
                if el != k_zero:
                    test_elements.append(el)
                    test_elements.append(-el)
                    test_elements.append(K(1) / el)
                    test_elements.append(K(-1) / el)
            except Exception:
                pass
        
        # Also include u if it can be mapped to K
        try:
            el_u = K(u)
            if el_u != k_zero:
                test_elements.append(el_u)
                test_elements.append(-el_u)
                try:
                    test_elements.append(K(1) / el_u)
                except Exception:
                    pass
        except Exception:
            pass

        # Remove duplicates
        unique_elements = []
        for el in test_elements:
            if el not in unique_elements and el != k_zero:
                unique_elements.append(el)
        test_elements = unique_elements

        if not test_elements:
            h2 = False
        else:
            # Check valuation properties on the test elements
            for a in test_elements:
                for b in test_elements:
                    va = v(a)
                    vb = v(b)
                    
                    # v(ab) = v(a) + v(b)
                    if v(a * b) != va + vb:
                        h2 = False
                        break
                    
                    # v(a+b) >= min(v(a), v(b))
                    if a + b != k_zero:
                        vab_add = v(a + b)
                        min_v = va if va < vb else vb
                        if vab_add < min_v:
                            h2 = False
                            break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: u is a non-zero element of R
    try:
        try:
            r_zero = R.zero
        except AttributeError:
            r_zero = 0
        h3 = bool(u in R and u != r_zero)
    except Exception:
        h3 = False

    # ¬Q: The conclusion "u is a unit in R if and only if v(u) = 0" FAILS
    try:
        is_unit = bool(R.is_unit(u))
        try:
            val_u = v(u)
        except Exception:
            val_u = v(K(u))
        v_zero = bool(val_u == 0)
        
        # The biconditional fails if the truth values differ
        neg_q = (is_unit != v_zero)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: v is a valuation on K",
    "H_3: u is a non-zero element of R",
    "¬Q: u is a unit in R iff v(u) = 0 is false"
]

N_HYP = 3
NEG_Q_INDEX = 3