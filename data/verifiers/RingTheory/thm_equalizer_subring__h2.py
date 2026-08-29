import itertools
from sympy.matrices import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = list(witness.get('R', []))
            S = list(witness.get('S', []))
            add_R = witness.get('add_R')
            mul_R = witness.get('mul_R')
            add_S = witness.get('add_S')
            mul_S = witness.get('mul_S')
            f = witness.get('f')
            g = witness.get('g')
            E = list(witness.get('E', []))
        else:
            R = list(getattr(witness, 'R', []))
            S = list(getattr(witness, 'S', []))
            add_R = getattr(witness, 'add_R', None)
            mul_R = getattr(witness, 'mul_R', None)
            add_S = getattr(witness, 'add_S', None)
            mul_S = getattr(witness, 'mul_S', None)
            f = getattr(witness, 'f', None)
            g = getattr(witness, 'g', None)
            E = list(getattr(witness, 'E', []))
            
        def get_op(op):
            if isinstance(op, dict):
                return lambda a, b: op.get((a, b), op.get(str((a, b))))
            return op
        
        def get_func(func):
            if isinstance(func, dict):
                return lambda a: func.get(a, func.get(str(a)))
            return func
            
        add_R_fn = get_op(add_R)
        mul_R_fn = get_op(mul_R)
        add_S_fn = get_op(add_S)
        mul_S_fn = get_op(mul_S)
        f_fn = get_func(f)
        g_fn = get_func(g)
        
        def is_ring(elements, add, mul):
            if not elements: 
                return False
            # closure
            for a in elements:
                for b in elements:
                    if not any(add(a, b) == x for x in elements): return False
                    if not any(mul(a, b) == x for x in elements): return False
            # add associativity
            for a in elements:
                for b in elements:
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): return False
            # add commutativity
            for a in elements:
                for b in elements:
                    if add(a, b) != add(b, a): return False
            # zero
            zero = None
            for e in elements:
                if all(add(e, a) == a for a in elements):
                    zero = e
                    break
            if zero is None: 
                return False
            # add inverse
            for a in elements:
                if not any(add(a, b) == zero for b in elements): return False
            # mul associativity
            for a in elements:
                for b in elements:
                    for c in elements:
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
            # distributivity
            for a in elements:
                for b in elements:
                    for c in elements:
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
            return True

        try:
            h1_ok = is_ring(R, add_R_fn, mul_R_fn) and is_ring(S, add_S_fn, mul_S_fn)
        except Exception:
            h1_ok = False
            
        try:
            expected_E = [r for r in R if f_fn(r) == g_fn(r)]
            h2_ok = True
            for x in E:
                if not any(x == y for y in expected_E): 
                    h2_ok = False
            for y in expected_E:
                if not any(x == y for x in E): 
                    h2_ok = False
        except Exception:
            h2_ok = False
            
        try:
            def is_subring(E_set, R_set, add, mul):
                for x in E_set:
                    if not any(x == y for y in R_set): return False
                if not E_set: 
                    return False
                zero = None
                for e in R_set:
                    if all(add(e, a) == a for a in R_set):
                        zero = e
                        break
                if not any(x == zero for x in E_set): 
                    return False
                for a in E_set:
                    for b in E_set:
                        if not any(add(a, b) == x for x in E_set): return False
                        if not any(mul(a, b) == x for x in E_set): return False
                for a in E_set:
                    inv_found = False
                    for b in E_set:
                        if add(a, b) == zero:
                            inv_found = True
                            break
                    if not inv_found: 
                        return False
                return True
                
            neg_q_ok = not is_subring(E, R, add_R_fn, mul_R_fn)
        except Exception:
            neg_q_ok = False
            
        return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: E is the set {r in R | f(r) = g(r)}",
    "¬Q: E is not a subring of R"
]

N_HYP = 2
NEG_Q_INDEX = 2