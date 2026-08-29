import itertools
from sympy import eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness is expected to provide the ring R and elements e, f.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, e, f = witness
        else:
            R = witness.ring
            e = witness.e
            f = witness.f
    except Exception:
        return [False, False, False, False]

    def _add(a, b):
        try:
            if hasattr(witness, 'add'): return witness.add(a, b)
            if hasattr(R, 'add'): return R.add(a, b)
            return a + b
        except Exception:
            return None

    def _mul(a, b):
        try:
            if hasattr(witness, 'mul'): return witness.mul(a, b)
            if hasattr(R, 'mul'): return R.mul(a, b)
            return a * b
        except Exception:
            return None

    def _eq(a, b):
        try:
            if hasattr(witness, 'eq'): return witness.eq(a, b)
            if hasattr(R, 'eq'): return R.eq(a, b)
            return a == b
        except Exception:
            return False

    try:
        if hasattr(R, 'elements'):
            elements = list(R.elements)
        elif hasattr(R, '__iter__'):
            elements = list(R)
        else:
            elements = []
    except Exception:
        elements = []

    if not elements:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = True
        for a in elements:
            for b in elements:
                m1 = _mul(a, b)
                m2 = _mul(b, a)
                if m1 is None or m2 is None or not _eq(m1, m2):
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    # H_2: e and f are idempotent elements in R
    try:
        e_in = any(_eq(e, x_el) for x_el in elements)
        f_in = any(_eq(f, x_el) for x_el in elements)
        ee = _mul(e, e)
        ff = _mul(f, f)
        h2 = e_in and f_in and ee is not None and ff is not None and _eq(ee, e) and _eq(ff, f)
    except Exception:
        h2 = False

    # H_3: e and f are orthogonal, meaning ef = 0
    try:
        zero = None
        if hasattr(witness, 'zero'):
            zero = witness.zero
        elif hasattr(R, 'zero'):
            zero = R.zero
        else:
            for z_cand in elements:
                is_z = True
                for a in elements:
                    s = _add(z_cand, a)
                    if s is None or not _eq(s, a):
                        is_z = False
                        break
                if is_z:
                    zero = z_cand
                    break
        
        if zero is None:
            h3 = False
        else:
            ef = _mul(e, f)
            h3 = ef is not None and _eq(ef, zero)
    except Exception:
        h3 = False

    # ¬Q: Ann_R(e) + Ann_R(f) != R
    try:
        if zero is None:
            neg_q = False
        else:
            ann_e = []
            for x_el in elements:
                xe = _mul(x_el, e)
                if xe is not None and _eq(xe, zero):
                    ann_e.append(x_el)
                    
            ann_f = []
            for x_el in elements:
                xf = _mul(x_el, f)
                if xf is not None and _eq(xf, zero):
                    ann_f.append(x_el)
            
            sum_ideals = []
            for x_el in ann_e:
                for y_el in ann_f:
                    s = _add(x_el, y_el)
                    if s is not None:
                        sum_ideals.append(s)
            
            is_R = True
            for x_el in elements:
                if not any(_eq(x_el, s) for s in sum_ideals):
                    is_R = False
                    break
            
            neg_q = not is_R
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: e and f are idempotent elements in R",
    "H_3: e and f are orthogonal, meaning ef = 0",
    "¬Q: Ann_R(e) + Ann_R(f) != R"
]

N_HYP = 3
NEG_Q_INDEX = 3