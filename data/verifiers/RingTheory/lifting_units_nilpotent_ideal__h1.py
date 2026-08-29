import sympy
import itertools

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        # The witness can be provided as (n, R, I, x) for rings modulo n,
        # or as (R, I, x) for exact rings, or as an object with R, I, x attributes.
        if isinstance(witness, tuple) and len(witness) == 4 and isinstance(witness[0], int):
            n, R_in, I_in, x = witness
            def eq(a, b):
                if hasattr(a, 'shape') and hasattr(b, 'shape') and a.shape != b.shape:
                    return False
                if hasattr(a, '__iter__') and hasattr(b, '__iter__'):
                    return all((va - vb) % n == 0 for va, vb in zip(a, b))
                return (a - b) % n == 0
            def is_zero(a):
                if hasattr(a, '__iter__'):
                    return all(va % n == 0 for va in a)
                return a % n == 0
            def mod_n_func(a):
                if hasattr(a, 'applyfunc'):
                    return a.applyfunc(lambda v: v % n)
                if hasattr(a, '__iter__'):
                    return type(a)(v % n for v in a)
                return a % n
            def op_add(a, b): return mod_n_func(a + b)
            def op_sub(a, b): return mod_n_func(a - b)
            def op_mul(a, b): return mod_n_func(a * b)
            
        elif isinstance(witness, tuple) and len(witness) == 3:
            R_in, I_in, x = witness
            def eq(a, b):
                try: return bool(a == b)
                except: return False
            def is_zero(a):
                try:
                    if hasattr(a, 'is_zero'):
                        res = a.is_zero
                        if res is not None: return res
                    if hasattr(a, '__iter__'):
                        return all(v == 0 for v in a)
                    return a == 0
                except: return False
            def op_add(a, b): return a + b
            def op_sub(a, b): return a - b
            def op_mul(a, b): return a * b
        else:
            R_in = witness.R
            I_in = witness.I
            x = witness.x
            def eq(a, b):
                try: return bool(a == b)
                except: return False
            def is_zero(a):
                try:
                    if hasattr(a, 'is_zero'):
                        res = a.is_zero
                        if res is not None: return res
                    if hasattr(a, '__iter__'):
                        return all(v == 0 for v in a)
                    return a == 0
                except: return False
            def op_add(a, b): return a + b
            def op_sub(a, b): return a - b
            def op_mul(a, b): return a * b

        if not hasattr(R_in, '__iter__') or not hasattr(I_in, '__iter__'):
            return [False, False, False, False]
            
        R = []
        for i, elem in enumerate(R_in):
            if i > 200: return [False, False, False, False]
            R.append(elem)
            
        I = []
        for i, elem in enumerate(I_in):
            if i > 200: return [False, False, False, False]
            I.append(elem)
            
    except Exception:
        return [False, False, False, False]

    def is_in(elem, lst):
        for a in lst:
            if eq(elem, a):
                return True
        return False

    # H1: I is a nilpotent two-sided ideal of R
    try:
        if not R:
            h1 = False
        else:
            is_ring = True
            for a in R:
                if not is_ring: break
                for b in R:
                    if not is_in(op_add(a, b), R) or not is_in(op_sub(a, b), R) or not is_in(op_mul(a, b), R):
                        is_ring = False
                        break
            
            is_ideal = True
            if not I:
                is_ideal = False
            else:
                for a in I:
                    if not is_ideal: break
                    if not is_in(a, R): 
                        is_ideal = False
                        break
                    for b in I:
                        if not is_in(op_add(a, b), I) or not is_in(op_sub(a, b), I):
                            is_ideal = False
                            break
                if is_ideal:
                    for r in R:
                        if not is_ideal: break
                        for i in I:
                            if not is_in(op_mul(r, i), I) or not is_in(op_mul(i, r), I):
                                is_ideal = False
                                break
            
            is_nilpotent = False
            if I:
                current_power = I
                for _ in range(len(I) + 1):
                    all_zero = True
                    for m in current_power:
                        if not is_zero(m):
                            all_zero = False
                            break
                    if all_zero:
                        is_nilpotent = True
                        break
                    next_power = []
                    for a in current_power:
                        for b in I:
                            prod = op_mul(a, b)
                            if not is_in(prod, next_power):
                                next_power.append(prod)
                    current_power = next_power

            h1 = is_ring and is_ideal and is_nilpotent
    except Exception:
        h1 = False

    # H2: x is an element of R
    try:
        h2 = is_in(x, R)
    except Exception:
        h2 = False

    # H3: The image of x in R/I is a unit in R/I
    try:
        identities_mod_I = []
        for e in R:
            is_id = True
            for r in R:
                if not is_in(op_sub(op_mul(e, r), r), I) or not is_in(op_sub(op_mul(r, e), r), I):
                    is_id = False
                    break
            if is_id:
                identities_mod_I.append(e)
        
        if not identities_mod_I:
            h3 = False
        else:
            e = identities_mod_I[0]
            is_unit_mod_I = False
            for y in R:
                if is_in(op_sub(op_mul(x, y), e), I) and is_in(op_sub(op_mul(y, x), e), I):
                    is_unit_mod_I = True
                    break
            h3 = is_unit_mod_I
    except Exception:
        h3 = False

    # neg_Q: x is NOT a unit in R
    try:
        identities = []
        for E in R:
            is_id = True
            for r in R:
                if not eq(op_mul(E, r), r) or not eq(op_mul(r, E), r):
                    is_id = False
                    break
            if is_id:
                identities.append(E)
        
        if not identities:
            is_unit = False
        else:
            E = identities[0]
            is_unit = False
            for Y in R:
                if eq(op_mul(x, Y), E) and eq(op_mul(Y, x), E):
                    is_unit = True
                    break
        
        neg_q = not is_unit
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: I is a nilpotent two-sided ideal of R",
    "H_2: x is an element of R",
    "H_3: The image of x in the quotient ring R/I is a unit in R/I",
    "¬Q: The element x is NOT a unit in the ring R"
]

N_HYP = 3
NEG_Q_INDEX = 3