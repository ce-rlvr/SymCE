import sympy
from sympy import Matrix, eye, zeros, Symbol, solve
import math

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        if len(witness) == 3:
            R, e, f = witness
        elif len(witness) == 2:
            e, f = witness
            R = sympy.ZZ
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = False
        if hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif str(R) in ['ZZ', 'QQ', 'RR', 'CC', 'Integers', 'Reals', 'Rationals', 'Complexes']:
            h1 = True
        elif hasattr(R, 'is_CommutativeRing') and R.is_CommutativeRing:
            h1 = True
        elif R in [sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes]:
            h1 = True
    except Exception:
        h1 = False

    def flatten(x):
        if hasattr(x, 'flat'):
            return list(x.flat)
        if hasattr(x, 'flatten'):
            try:
                return x.flatten().tolist()
            except Exception:
                return list(x.flatten())
        if isinstance(x, list) or isinstance(x, tuple):
            res = []
            for item in x:
                res.extend(flatten(item))
            return res
        if hasattr(x, 'tolist'):
            return flatten(x.tolist())
        try:
            return list(x)
        except Exception:
            return [x]

    # H_2: e and f are orthogonal, meaning ef = 0
    try:
        prod = e * f
        h2 = False
        if hasattr(prod, 'is_zero_matrix') and prod.is_zero_matrix:
            h2 = True
        elif hasattr(prod, 'is_zero') and prod.is_zero:
            h2 = True
        elif prod == 0:
            h2 = True
        else:
            p_flat = flatten(prod)
            if all(v == 0 for v in p_flat):
                h2 = True
    except Exception:
        h2 = False

    # H_3: e + f = 1
    try:
        total = e + f
        h3 = False
        if hasattr(total, 'is_Identity') and total.is_Identity:
            h3 = True
        elif total == 1:
            h3 = True
        else:
            try:
                if hasattr(total, 'shape') and len(total.shape) == 2 and total.shape[0] == total.shape[1]:
                    if total == eye(total.shape[0]):
                        h3 = True
            except Exception:
                pass
            
            if not h3:
                t_flat = flatten(total)
                n = int(math.sqrt(len(t_flat)))
                if n * n == len(t_flat) and n > 0:
                    is_id = True
                    for i in range(n):
                        for j in range(n):
                            val = t_flat[i * n + j]
                            if i == j:
                                if val != 1: is_id = False
                            else:
                                if val != 0: is_id = False
                    if is_id:
                        h3 = True
                elif len(t_flat) == 1 and t_flat[0] == 1:
                    h3 = True
    except Exception:
        h3 = False

    # ¬Q: Ann_R(e) + Ann_R(f) != R
    # This is equivalent to checking that there does NOT exist a scalar 'a' in R 
    # such that a*e == 0 and a*f == f.
    try:
        a = Symbol('a')
        
        def get_eqs(matrix, scalar, target):
            eqs = []
            m_flat = flatten(matrix)
            t_flat = flatten(target)
            
            if len(t_flat) == 1 and len(m_flat) > 1:
                t_flat = [t_flat[0]] * len(m_flat)
                
            for m_val, t_val in zip(m_flat, t_flat):
                eqs.append(scalar * m_val - t_val)
            return eqs

        is_finite_ring = False
        elements = []
        try:
            if hasattr(R, '__iter__') and not isinstance(R, (str, dict)):
                elements = list(R)
                is_finite_ring = True
            elif hasattr(R, 'elements'):
                elements = list(R.elements)
                is_finite_ring = True
        except Exception:
            pass

        if is_finite_ring and len(elements) < 1000:
            found = False
            for a_val in elements:
                try:
                    ae = a_val * e
                    af = a_val * f
                    
                    ae_zero = False
                    if hasattr(ae, 'is_zero_matrix') and ae.is_zero_matrix: ae_zero = True
                    elif hasattr(ae, 'is_zero') and ae.is_zero: ae_zero = True
                    elif ae == 0: ae_zero = True
                    else:
                        ae_flat = flatten(ae)
                        if all(v == 0 for v in ae_flat): ae_zero = True
                        
                    af_eq_f = False
                    if af == f: af_eq_f = True
                    else:
                        af_flat = flatten(af)
                        f_flat = flatten(f)
                        if af_flat == f_flat: af_eq_f = True
                        
                    if ae_zero and af_eq_f:
                        found = True
                        break
                except Exception:
                    pass
            neg_q = not found
        else:
            eqs_e = get_eqs(e, a, 0)
            eqs_f = get_eqs(f, a, f)
            
            all_eqs = eqs_e + eqs_f
            
            sols = solve(all_eqs, a)
            
            if not sols:
                neg_q = True
            else:
                neg_q = True
                if isinstance(sols, dict):
                    sols = [sols[a]]
                elif isinstance(sols, list) and len(sols) > 0 and isinstance(sols[0], dict):
                    sols = [s[a] for s in sols]
                    
                for sol in sols:
                    if str(R) in ['ZZ', 'Integers', 'S.Integers']:
                        if sol.is_integer:
                            neg_q = False
                            break
                    elif str(R) in ['QQ', 'Rationals', 'S.Rationals']:
                        if sol.is_rational:
                            neg_q = False
                            break
                    else:
                        neg_q = False
                        break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: e and f are orthogonal (ef = 0)",
    "H_3: e + f = 1",
    "¬Q: Ann_R(e) + Ann_R(f) != R"
]

N_HYP = 3
NEG_Q_INDEX = 3