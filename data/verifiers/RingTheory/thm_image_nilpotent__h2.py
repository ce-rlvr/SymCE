import sympy as sp

# Top-level setup: named object bindings
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)
Z = sp.S.Integers
Q = sp.S.Rationals
R_field = sp.S.Reals
C = sp.S.Complexes

def is_ring_table(add, mul):
    try:
        if not isinstance(add, list) or not isinstance(mul, list): return False
        n = len(add)
        if n == 0 or len(mul) != n: return False
        for row in add + mul:
            if len(row) != n: return False
            for val in row:
                if not (isinstance(val, int) and 0 <= val < n): return False
        # + commutativity
        for i in range(n):
            for j in range(n):
                if add[i][j] != add[j][i]: return False
        # + associativity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add[add[i][j]][k] != add[i][add[j][k]]: return False
        # + identity
        zero = None
        for i in range(n):
            if all(add[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None: return False
        # + inverses
        for i in range(n):
            if not any(add[i][j] == zero for j in range(n)): return False
        # * associativity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
        # distributivity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                    if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
        return True
    except Exception:
        return False

def check_ring(R):
    if R is None: return False
    if R == "NonSquareMatrix": return False
    if isinstance(R, int) and R <= 1: return False
    if isinstance(R, tuple) and len(R) == 2:
        return is_ring_table(R[0], R[1])
    return True

def evaluate_f(f, x):
    if isinstance(f, dict):
        if x in f:
            return f[x]
        try:
            if int(x) in f:
                return f[int(x)]
        except Exception:
            pass
        return f[x]
    elif isinstance(f, (list, tuple)):
        return f[int(x)]
    elif hasattr(f, 'subs') and not callable(f):
        free = f.free_symbols
        if len(free) == 1:
            var = list(free)[0]
            return f.subs(var, x)
        elif len(free) == 0:
            return f
        else:
            raise ValueError("Cannot evaluate expression with multiple free symbols")
    elif not callable(f):
        # If f is not callable and not a dict/list/sympy expr, assume it's the constant output value
        return f
    else:
        return f(x)

def get_implied_ring(elem):
    if isinstance(elem, sp.MatrixBase):
        if elem.shape[0] == elem.shape[1]:
            return "MatrixRing"
        else:
            return "NonSquareMatrix"
    if isinstance(elem, (int, sp.Integer)):
        return sp.S.Integers
    return "UnknownRing"

def parse_witness(witness):
    if isinstance(witness, dict):
        R = witness.get('R', witness.get('ring'))
        S = witness.get('S', witness.get('codomain'))
        x = witness.get('x', witness.get('element'))
        f = witness.get('f', witness.get('f(x)', witness.get('fx', witness.get('mapping'))))
        
        if R is not None and S is not None and x is not None and f is not None:
            return R, S, x, f
        elif x is not None and f is not None:
            R = get_implied_ring(x) if R is None else R
            try:
                fx = evaluate_f(f, x)
                S = get_implied_ring(fx) if S is None else S
            except Exception:
                S = None if S is None else S
            return R, S, x, f
            
    if isinstance(witness, (tuple, list)):
        if len(witness) == 4:
            return witness[0], witness[1], witness[2], witness[3]
        elif len(witness) == 2:
            x, f = witness[0], witness[1]
            R = get_implied_ring(x)
            try:
                fx = evaluate_f(f, x)
                S = get_implied_ring(fx)
            except Exception:
                S = None
            return R, S, x, f
        elif len(witness) == 6:
            R_add, R_mul, S_add, S_mul, x, f = witness
            return (R_add, R_mul), (S_add, S_mul), x, f
            
    return None, None, None, None

def is_nilpotent_elem(x, R):
    try:
        if isinstance(R, str):
            s = R.upper()
            if s.startswith('Z_'):
                s = s[2:]
            elif s.startswith('Z'):
                s = s[1:]
            if s.isdigit():
                n = int(s)
                if n > 1:
                    if not isinstance(x, (int, sp.Integer)): return False
                    curr = int(x) % n
                    for _ in range(n):
                        if curr == 0:
                            return True
                        curr = (curr * int(x)) % n
                    return False

        if isinstance(R, int) and R > 1:
            if not isinstance(x, (int, sp.Integer)): return False
            curr = int(x) % R
            for _ in range(R):
                if curr == 0:
                    return True
                curr = (curr * int(x)) % R
            return False
            
        if isinstance(x, sp.MatrixBase):
            n = x.shape[0]
            if n != x.shape[1]: return False
            curr = x
            for _ in range(n):
                if curr == sp.zeros(n, n):
                    return True
                curr = curr * x
            return False
            
        if isinstance(x, (int, sp.Integer)):
            return int(x) == 0
            
        if isinstance(R, tuple) and len(R) == 2:
            add, mul = R
            n = len(add)
            zero = None
            for i in range(n):
                if all(add[i][j] == j for j in range(n)):
                    zero = i
                    break
            if zero is None: return False
            if not (isinstance(x, (int, sp.Integer)) and 0 <= x < n): return False
            curr = int(x)
            for _ in range(n):
                if curr == zero:
                    return True
                curr = mul[curr][int(x)]
            return False
            
        try:
            if sp.simplify(x) == 0:
                return True
        except Exception:
            pass
            
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    R, S, x, f = parse_witness(witness)
    
    # H1: R and S are rings
    try:
        h1 = check_ring(R) and check_ring(S)
    except Exception:
        h1 = False
        
    # H2: x in R is a nilpotent element
    try:
        h2 = is_nilpotent_elem(x, R)
    except Exception:
        h2 = False
        
    # neg_Q: f(x) is NOT a nilpotent element in S
    try:
        fx = evaluate_f(f, x)
        neg_q = not is_nilpotent_elem(fx, S)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: x in R is a nilpotent element",
    "¬Q: f(x) is not a nilpotent element in S"
]

N_HYP = 2
NEG_Q_INDEX = 2