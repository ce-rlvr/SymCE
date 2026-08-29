import sympy
from sympy import sympify, factor_list, groebner, Expr
from sympy.matrices import MatrixBase
from sympy.abc import x, y, z

# Top-level setup
class CyclicTorsionModule:
    """
    Represents a cyclic torsion module M = R / (f) over a polynomial ring R.
    The witness should be an instance of this class, e.g., CyclicTorsionModule(x**2 - y**2),
    or simply the annihilator polynomial itself.
    """
    def __init__(self, annihilator):
        self.annihilator = annihilator

def conditions(witness) -> list[bool]:
    try:
        # Extract the annihilator polynomial from the witness
        if hasattr(witness, 'annihilator'):
            f = witness.annihilator
        elif isinstance(witness, MatrixBase):
            if witness.rows == witness.cols:
                f = witness.det()
            else:
                f = witness[0]
        elif isinstance(witness, Expr):
            f = witness
        elif isinstance(witness, str):
            f = sympify(witness)
        elif hasattr(witness, '__iter__'):
            f = list(witness)[0]
            f = sympify(f)
        else:
            f = sympify(witness)
    except Exception:
        return [False, False]

    # H_1: M is a torsion R-module
    # A cyclic module R/(f) over an integral domain is a torsion module iff f != 0.
    try:
        h1 = (f != 0)
    except Exception:
        h1 = False

    # ¬Q: M is NOT the direct sum of its p-primary components
    # For M = R/(f) to be a direct sum of its primary components, the primary components 
    # of the ideal (f) must be pairwise coprime. This means the prime factors of f 
    # must generate the unit ideal pairwise (i.e., their Groebner basis contains 1).
    try:
        if f == 0 or f.is_number:
            neg_q = False
        else:
            factors = factor_list(f)[1]
            bases = [b for b, e in factors]
            
            if len(bases) <= 1:
                neg_q = False
            else:
                is_direct_sum = True
                vars = list(f.free_symbols)
                for i in range(len(bases)):
                    for j in range(i + 1, len(bases)):
                        try:
                            gb = groebner([bases[i], bases[j]], *vars, domain='QQ')
                        except Exception:
                            gb = groebner([bases[i], bases[j]], *vars)
                        
                        # Check if the Groebner basis is trivial (generates the whole ring)
                        if not (len(gb) == 1 and gb[0].is_number and gb[0] != 0):
                            is_direct_sum = False
                            break
                    if not is_direct_sum:
                        break
                neg_q = not is_direct_sum
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: M is a torsion R-module",
    "¬Q: M is NOT the direct sum of its p-primary components"
]

N_HYP = 1
NEG_Q_INDEX = 1