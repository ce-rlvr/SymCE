import sympy as sp
import itertools

# Top-level setup for potential witness expressions
x, y, z = sp.symbols('x y z')
I = sp.I

def get_complex_val(expr):
    try:
        if isinstance(expr, (int, float, complex)):
            return complex(expr)
        c = complex(sp.N(expr))
        return c
    except Exception:
        return None

def conditions(witness):
    try:
        # If the witness is a field (e.g. QQ), the norm N(a+bi) = a^2+b^2 
        # does not map all elements to integers (e.g. N(1/2) = 1/4).
        # Thus it cannot be a Euclidean domain with respect to this norm.
        if hasattr(witness, 'is_Field') and getattr(witness, 'is_Field'):
            return [True]
            
        try:
            if isinstance(witness, (list, tuple, set)):
                gens = list(witness)
            else:
                gens = [witness]
        except Exception:
            gens = [witness]
            
        gens_sym = []
        for g in gens:
            try:
                gens_sym.append(sp.sympify(g))
            except Exception:
                gens_sym.append(g)
                
        has_one = False
        for g in gens_sym:
            try:
                if g == 1:
                    has_one = True
                    break
            except Exception:
                pass
        if not has_one:
            gens_sym.insert(0, sp.sympify(1))
        gens = gens_sym
        
        basis = []
        c_basis = []
        for deg in range(1, 3):
            for prod in itertools.product(gens, repeat=deg):
                try:
                    val = sp.simplify(sp.Mul(*prod))
                except Exception:
                    continue
                if val == 0:
                    continue
                c_val = get_complex_val(val)
                if c_val is None:
                    return [False]
                
                is_dup = False
                for cb in c_basis:
                    if abs(c_val - cb) < 1e-9:
                        is_dup = True
                        break
                if not is_dup:
                    basis.append(val)
                    c_basis.append(c_val)
                    
                if len(basis) >= 4:
                    break
            if len(basis) >= 4:
                break
                
        if len(basis) == 1:
            large_coeffs = range(-50, 51)
            small_coeffs = range(-5, 6)
        elif len(basis) == 2:
            large_coeffs = range(-15, 16)
            small_coeffs = range(-4, 5)
        elif len(basis) == 3:
            large_coeffs = range(-6, 7)
            small_coeffs = range(-2, 3)
        else:
            large_coeffs = range(-3, 4)
            small_coeffs = range(-1, 2)
            
        R_sub = []
        for coeffs in itertools.product(small_coeffs, repeat=len(basis)):
            val = sum(c * b for c, b in zip(coeffs, c_basis))
            R_sub.append(val)
            
        R_sub_unique = []
        for val in R_sub:
            if not any(abs(val - v) < 1e-9 for v in R_sub_unique):
                R_sub_unique.append(val)
                
        # A valid Euclidean norm must map non-zero elements to non-negative integers.
        # If we find an element whose norm is not an integer, it's not a Euclidean domain w.r.t this norm.
        for z in R_sub_unique:
            norm_val = z.real**2 + z.imag**2
            if abs(norm_val - round(norm_val)) > 1e-5:
                return [True]
                
        R_sub_unique.sort(key=lambda v: abs(v))
        test_a = R_sub_unique[:50]
        test_b = [v for v in R_sub_unique if abs(v) > 1e-9][:50]
        
        Q_large = []
        for coeffs in itertools.product(large_coeffs, repeat=len(basis)):
            val = sum(c * b for c, b in zip(coeffs, c_basis))
            Q_large.append(val)
            
        neg_Q = False
        # Check if there exists x = a/b in Frac(R) such that for all q in R, N(x - q) >= 1
        for a in test_a:
            for b in test_b:
                x = a / b
                found_q = False
                for q in Q_large:
                    diff = x - q
                    dist_sq = diff.real**2 + diff.imag**2
                    if dist_sq < 0.999999:
                        found_q = True
                        break
                if not found_q:
                    neg_Q = True
                    break
            if neg_Q:
                break
                
        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: R is not a Euclidean domain with respect to the norm function N(a+bi) = a^2 + b^2"
]
N_HYP = 0
NEG_Q_INDEX = 0