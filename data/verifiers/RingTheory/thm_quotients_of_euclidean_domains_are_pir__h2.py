import sympy
from sympy import symbols
from sympy.polys.domains import ZZ, QQ

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = symbols('x y z')

def conditions(witness):
    try:
        R, I = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is an integral domain
    try:
        # In SymPy, polynomial domains and base rings (ZZ, QQ) represent integral domains.
        # We duck-type check for standard SymPy Domain properties.
        h1_ok = hasattr(R, 'from_sympy') and hasattr(R, 'zero')
    except Exception:
        h1_ok = False

    # H_2: I is an ideal of R
    try:
        if isinstance(I, (list, tuple)):
            h2_ok = True
            for elem in I:
                if elem in R:
                    continue
                try:
                    if hasattr(elem, 'as_expr'):
                        sym_elem = elem.as_expr()
                    else:
                        sym_elem = elem
                    R.from_sympy(sym_elem)
                except Exception:
                    if elem != 0:
                        h2_ok = False
                        break
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: R/I is NOT a principal ideal ring
    try:
        is_zero = True
        if I:
            for elem in I:
                if elem in R:
                    if elem != R.zero:
                        is_zero = False
                        break
                else:
                    try:
                        if hasattr(elem, 'as_expr'):
                            sym_elem = elem.as_expr()
                        else:
                            sym_elem = elem
                        dom_elem = R.from_sympy(sym_elem)
                        if dom_elem != R.zero:
                            is_zero = False
                            break
                    except Exception:
                        if elem != 0:
                            is_zero = False
                            break
        
        if is_zero:
            # If I is the zero ideal, R/I is isomorphic to R.
            # Since R is an integral domain, it is a PIR iff it is a PID.
            if getattr(R, 'is_PID', None) is not None:
                is_pir = R.is_PID
            else:
                if getattr(R, 'is_Field', False):
                    is_pir = True
                elif R == ZZ or R == QQ:
                    is_pir = True
                elif hasattr(R, 'gens'):
                    if len(R.gens) > 1:
                        is_pir = False
                    elif R.domain == ZZ:
                        is_pir = False
                    elif getattr(R.domain, 'is_Field', False):
                        is_pir = True
                    else:
                        is_pir = False
                else:
                    is_pir = False
        else:
            # If I is not the zero ideal, we attempt to determine if R/I is a PIR.
            if getattr(R, 'is_Field', False):
                is_pir = True
            elif R == ZZ or R == QQ:
                is_pir = True
            elif hasattr(R, 'gens'):
                gens_in_I = []
                is_simple = True
                for elem in I:
                    if hasattr(elem, 'as_expr'):
                        expr = elem.as_expr()
                    else:
                        expr = elem
                    
                    if expr in R.gens:
                        gens_in_I.append(expr)
                    elif expr != 0:
                        is_simple = False
                        break
                if is_simple:
                    remaining_gens = [g for g in R.gens if g not in gens_in_I]
                    if R.domain == ZZ:
                        is_pir = (len(remaining_gens) == 0)
                    elif getattr(R.domain, 'is_Field', False):
                        is_pir = (len(remaining_gens) <= 1)
                    else:
                        raise ValueError("Cannot determine if R/I is a PIR")
                else:
                    raise ValueError("Cannot determine if R/I is a PIR")
            else:
                raise ValueError("Cannot determine if R/I is a PIR")
        
        neg_q_ok = not is_pir
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: I is an ideal of R",
    "¬Q: R/I is not a principal ideal ring"
]

N_HYP = 2
NEG_Q_INDEX = 2