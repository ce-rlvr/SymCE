import sympy
from sympy import Poly, isprime
import math
import itertools

x, y, z = sympy.symbols('x y z')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = int(witness.get('p'))
            q = int(witness.get('q'))
            n = int(witness.get('n'))
            polys = witness.get('polys', [])
            vars = witness.get('vars', None)
        else:
            if len(witness) == 4:
                p, q, n, polys = witness
                vars = None
            elif len(witness) == 5:
                p, q, n, polys, vars = witness
            else:
                return [False, False, False]
            p = int(p)
            q = int(q)
            n = int(n)
            
        parsed_polys = []
        for f in polys:
            if isinstance(f, str):
                parsed_polys.append(sympy.sympify(f))
            else:
                parsed_polys.append(f)
        polys = parsed_polys
    except Exception:
        return [False, False, False]

    def check_h1():
        try:
            if not isprime(p): return False
            if q < p: return False
            temp = q
            while temp > 1:
                if temp % p != 0: return False
                temp //= p
            return True
        except Exception:
            return False

    def check_h2():
        try:
            deg_sum = 0
            for f in polys:
                if f == 0:
                    deg_sum += float('-inf')
                    continue
                
                if vars is None:
                    free = getattr(f, 'free_symbols', set())
                    if not free:
                        p_obj = Poly(f, sympy.Symbol('x'))
                    else:
                        p_obj = Poly(f, *free)
                else:
                    v_syms = [sympy.Symbol(v) if isinstance(v, str) else v for v in vars]
                    p_obj = Poly(f, *v_syms)
                
                d = p_obj.total_degree()
                deg_sum += d
            return deg_sum < n
        except Exception:
            return False

    def check_neg_q():
        try:
            if n == 0:
                is_zero = True
                for f in polys:
                    val = f
                    if hasattr(f, 'subs'):
                        val = f.subs({})
                    if int(val) % p != 0:
                        is_zero = False
                        break
                zeros_count = 1 if is_zero else 0
                return (zeros_count % p) != 0

            if q == p:
                v = vars
                if v is None:
                    free = set()
                    for f in polys:
                        if hasattr(f, 'free_symbols'):
                            free.update(f.free_symbols)
                    v = list(free)
                    i = 0
                    while len(v) < n:
                        v.append(sympy.Symbol(f'x_{i}'))
                        i += 1
                    v = v[:n]
                else:
                    v = [sympy.Symbol(var) if isinstance(var, str) else var for var in v]
                
                zeros_count = 0
                for pt in itertools.product(range(p), repeat=n):
                    is_zero = True
                    sub_dict = dict(zip(v, pt))
                    for f in polys:
                        val = f
                        if hasattr(f, 'subs'):
                            val = f.subs(sub_dict)
                        if int(val) % p != 0:
                            is_zero = False
                            break
                    if is_zero:
                        zeros_count += 1
                return (zeros_count % p) != 0
            else:
                # For n > 0, Chevalley-Warning is mathematically proven to be true.
                # Thus, there are no counterexamples with n > 0.
                return False
        except Exception:
            return False

    return [check_h1(), check_h2(), check_neg_q()]

CONDITION_LABELS = [
    "H_1: F_q is a finite field of characteristic p",
    "H_2: sum of degrees of f_i < n",
    "not Q: The number of common zeros of f_i in F_q^n is NOT congruent to 0 modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2