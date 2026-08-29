import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_B(witness):
    if callable(witness):
        return witness
    if isinstance(witness, sp.Matrix):
        return lambda x, y: (x.T * witness * y)[0]
    if isinstance(witness, dict):
        if 'B' in witness:
            return extract_B(witness['B'])
        if 'Q' in witness:
            return extract_B(witness['Q'])
    if hasattr(witness, 'B'):
        return extract_B(witness.B)
    if hasattr(witness, 'Q'):
        return extract_B(witness.Q)
    if isinstance(witness, (tuple, list)):
        for item in witness:
            res = extract_B(item)
            if res is not None:
                return res
    if isinstance(witness, sp.Expr):
        syms = list(witness.free_symbols)
        syms.sort(key=lambda s: s.name)
        if len(syms) == 1:
            return lambda x: witness.subs(syms[0], x)
        elif len(syms) == 2:
            return lambda x: witness.subs({syms[0]: x[0], syms[1]: x[1]})
    return None

def conditions(witness):
    try:
        B = extract_B(witness)
        if B is None:
            return [False, False, False]
            
        char = 0
        if isinstance(witness, dict) and 'char' in witness:
            char = witness['char']
        elif hasattr(witness, 'char'):
            char = witness.char
        elif hasattr(witness, 'field') and hasattr(witness.field, 'characteristic'):
            c = witness.field.characteristic
            char = c() if callable(c) else c
        elif isinstance(witness, (tuple, list)):
            for item in witness:
                if isinstance(item, dict) and 'char' in item:
                    char = item['char']
                elif hasattr(item, 'char'):
                    char = item.char
                elif hasattr(item, 'field') and hasattr(item.field, 'characteristic'):
                    c = item.field.characteristic
                    char = c() if callable(c) else c
                    
        h1 = (char != 2)
        h2 = True
        
        def Q_func(v):
            try:
                return B(v, v)
            except TypeError:
                return B(v)
                
        def check_neg_q(x, y):
            Q_x = Q_func(x)
            Q_y = Q_func(y)
            Q_x_plus_y = Q_func(x + y)
            Q_x_minus_y = Q_func(x - y)
            
            def to_sp(val):
                if isinstance(val, (list, tuple)):
                    return sp.Matrix(val)
                return val
                
            lhs = sp.simplify(to_sp(Q_x_plus_y) + to_sp(Q_x_minus_y))
            rhs = sp.simplify(2 * to_sp(Q_x) + 2 * to_sp(Q_y))
            diff = sp.simplify(lhs - rhs)
            
            if getattr(diff, 'is_zero_matrix', False):
                return False
            if diff == 0:
                return False
            if hasattr(diff, 'equals'):
                eq = diff.equals(0)
                if eq is True:
                    return False
            return True

        mat = None
        if isinstance(witness, sp.Matrix):
            mat = witness
        elif isinstance(witness, dict) and 'B' in witness and isinstance(witness['B'], sp.Matrix):
            mat = witness['B']
        elif hasattr(witness, 'B') and isinstance(witness.B, sp.Matrix):
            mat = witness.B
            
        if mat is not None:
            if mat.shape[0] != mat.shape[1]:
                return [False, False, False]
            n = mat.shape[0]
            x = sp.Matrix(sp.symbols(f'x1:{n+1}', real=True))
            y = sp.Matrix(sp.symbols(f'y1:{n+1}', real=True))
            neg_q = check_neg_q(x, y)
            return [h1, h2, neg_q]
            
        for n in [2, 3]:
            try:
                x = sp.Matrix(sp.symbols(f'x1:{n+1}', real=True))
                y = sp.Matrix(sp.symbols(f'y1:{n+1}', real=True))
                neg_q = check_neg_q(x, y)
                return [h1, h2, neg_q]
            except Exception:
                continue
                
        try:
            x, y = sp.symbols('x y', real=True)
            neg_q = check_neg_q(x, y)
            return [h1, h2, neg_q]
        except Exception:
            pass
            
        return [h1, h2, False]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F of characteristic not 2",
    "H_2: Q(x) = B(x, x) is the quadratic form associated with B",
    "¬Q: For all x, y in V, Q(x + y) + Q(x - y) = 2Q(x) + 2Q(y) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2