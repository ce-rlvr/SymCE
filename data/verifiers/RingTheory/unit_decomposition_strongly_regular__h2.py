import itertools
import sympy
from sympy import symbols

# Top-level setup
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture:
    "Let R be a strongly regular ring. Then for any a in R, there exists an idempotent e 
    and a unit u such that a = eu."
    
    The witness should be a tuple (R, a) where R is a strongly regular ring (without identity)
    and a is an element of R.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, a = witness
        elif isinstance(witness, dict) and 'ring' in witness and 'a' in witness:
            R = witness['ring']
            a = witness['a']
        else:
            R = witness
            a = getattr(R, 'a', None)
    except Exception:
        return [False, False]

    # Cache elements if possible to avoid consuming generators multiple times
    elements_cache = []
    try:
        if hasattr(R, 'elements'):
            if callable(R.elements):
                elems = R.elements()
            else:
                elems = R.elements
            elements_cache = list(itertools.islice(elems, 200))
    except Exception:
        pass

    if a is None and elements_cache:
        a = elements_cache[0]

    # H_1: R is a strongly regular ring
    h1 = False
    try:
        if hasattr(R, 'is_strongly_regular'):
            if callable(R.is_strongly_regular):
                h1 = bool(R.is_strongly_regular())
            else:
                h1 = bool(R.is_strongly_regular)
        elif elements_cache:
            h1 = True
            for x_elem in elements_cache:
                found = False
                for y_elem in elements_cache:
                    try:
                        x2 = R.mul(x_elem, x_elem) if hasattr(R, 'mul') else x_elem * x_elem
                        x2y = R.mul(x2, y_elem) if hasattr(R, 'mul') else x2 * y_elem
                        if x2y == x_elem:
                            found = True
                            break
                    except Exception:
                        pass
                if not found:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # neg_Q: a cannot be written as eu for any idempotent e and unit u
    neg_q = False
    try:
        if hasattr(R, 'has_eu_decomposition'):
            if callable(R.has_eu_decomposition):
                neg_q = not R.has_eu_decomposition(a)
            else:
                neg_q = not R.has_eu_decomposition
        else:
            has_id = False
            identity = None
            if hasattr(R, 'has_identity'):
                if callable(R.has_identity):
                    has_id = bool(R.has_identity())
                else:
                    has_id = bool(R.has_identity)
            elif hasattr(R, 'one'):
                has_id = True
                identity = R.one
            elif hasattr(R, 'identity'):
                has_id = True
                identity = R.identity
            elif elements_cache:
                for e_elem in elements_cache:
                    is_id = True
                    for x_elem in elements_cache:
                        try:
                            ex = R.mul(e_elem, x_elem) if hasattr(R, 'mul') else e_elem * x_elem
                            xe = R.mul(x_elem, e_elem) if hasattr(R, 'mul') else x_elem * e_elem
                            if ex != x_elem or xe != x_elem:
                                is_id = False
                                break
                        except Exception:
                            is_id = False
                            break
                    if is_id:
                        has_id = True
                        identity = e_elem
                        break
            
            if not has_id:
                # If the ring has no identity, it has no units, so the decomposition is impossible.
                neg_q = True
            else:
                units = []
                if hasattr(R, 'units'):
                    if callable(R.units):
                        u_iter = R.units()
                    else:
                        u_iter = R.units
                    units = list(itertools.islice(u_iter, 200))
                else:
                    for u_elem in elements_cache:
                        is_unit = False
                        for v_elem in elements_cache:
                            try:
                                uv = R.mul(u_elem, v_elem) if hasattr(R, 'mul') else u_elem * v_elem
                                vu = R.mul(v_elem, u_elem) if hasattr(R, 'mul') else v_elem * u_elem
                                if uv == identity and vu == identity:
                                    is_unit = True
                                    break
                            except Exception:
                                pass
                        if is_unit:
                            units.append(u_elem)
                            
                idempotents = []
                if hasattr(R, 'idempotents'):
                    if callable(R.idempotents):
                        i_iter = R.idempotents()
                    else:
                        i_iter = R.idempotents
                    idempotents = list(itertools.islice(i_iter, 200))
                else:
                    for e_elem in elements_cache:
                        try:
                            ee = R.mul(e_elem, e_elem) if hasattr(R, 'mul') else e_elem * e_elem
                            if ee == e_elem:
                                idempotents.append(e_elem)
                        except Exception:
                            pass
                            
                found_decomp = False
                for e_elem in idempotents:
                    for u_elem in units:
                        try:
                            eu = R.mul(e_elem, u_elem) if hasattr(R, 'mul') else e_elem * u_elem
                            if eu == a:
                                found_decomp = True
                                break
                        except Exception:
                            pass
                    if found_decomp:
                        break
                        
                if found_decomp:
                    neg_q = False
                else:
                    # Mathematically, any strongly regular ring WITH identity guarantees a = eu.
                    # If h1 is True, the failure to find it is just due to the 200 element limit.
                    if h1:
                        neg_q = False
                    else:
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a strongly regular ring",
    "¬Q: a cannot be written as eu for any idempotent e and unit u"
]

N_HYP = 1
NEG_Q_INDEX = 1