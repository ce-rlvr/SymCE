import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import itertools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    def get_attr(w, name):
        if hasattr(w, name):
            return getattr(w, name)
        elif isinstance(w, dict) and name in w:
            return w[name]
        else:
            raise AttributeError(f"Missing {name}")

    try:
        # Support tuple format: (R_elements, S_elements, f, u)
        if isinstance(witness, tuple) and len(witness) == 4:
            R_elements, S_elements, f, u = witness
            R_elements = list(R_elements)
            S_elements = list(S_elements)
            add_R = lambda a, b: a + b
            mul_R = lambda a, b: a * b
            add_S = lambda a, b: a + b
            mul_S = lambda a, b: a * b
            
            def find_zero(elements, add):
                for z_elem in elements:
                    if all(add(a, z_elem) == a and add(z_elem, a) == a for a in elements):
                        return z_elem
                raise ValueError("No zero found")
                
            def find_one(elements, mul):
                for o_elem in elements:
                    if all(mul(a, o_elem) == a and mul(o_elem, a) == a for a in elements):
                        return o_elem
                raise ValueError("No one found")
                
            zero_R = find_zero(R_elements, add_R)
            one_R = find_one(R_elements, mul_R)
            zero_S = find_zero(S_elements, add_S)
            one_S = find_one(S_elements, mul_S)
        else:
            # Support dictionary or object format with explicit methods
            R_elements = list(get_attr(witness, 'R_elements'))
            S_elements = list(get_attr(witness, 'S_elements'))
            add_R = get_attr(witness, 'add_R')
            mul_R = get_attr(witness, 'mul_R')
            add_S = get_attr(witness, 'add_S')
            mul_S = get_attr(witness, 'mul_S')
            zero_R = get_attr(witness, 'zero_R')
            one_R = get_attr(witness, 'one_R')
            zero_S = get_attr(witness, 'zero_S')
            one_S = get_attr(witness, 'one_S')
            f = get_attr(witness, 'f')
            u = get_attr(witness, 'u')
    except Exception:
        return [False, False, False]

    def check_ring(elements, add, mul, zero, one):
        if not any(e == zero for e in elements): return False
        if not any(e == one for e in elements): return False
        
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a: return False
            if mul(a, one) != a or mul(one, a) != a: return False
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in elements:
                if add(a, b) != add(b, a): return False
        
        n = len(elements)
        if n <= 20:
            for a in elements:
                for b in elements:
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): return False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                        if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        else:
            for a, b, c in itertools.islice(itertools.product(elements, repeat=3), 1000):
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        return True

    # H_1: f is a ring homomorphism from R to S such that f(1_R) = 1_S
    try:
        h1_ok = False
        if check_ring(R_elements, add_R, mul_R, zero_R, one_R) and \
           check_ring(S_elements, add_S, mul_S, zero_S, one_S):
            if f(one_R) == one_S:
                homo_ok = True
                for a in R_elements:
                    if not any(f(a) == s for s in S_elements):
                        homo_ok = False
                        break
                    for b in R_elements:
                        if f(add_R(a, b)) != add_S(f(a), f(b)):
                            homo_ok = False
                            break
                        if f(mul_R(a, b)) != mul_S(f(a), f(b)):
                            homo_ok = False
                            break
                    if not homo_ok: break
                h1_ok = homo_ok
    except Exception:
        h1_ok = False

    # H_2: There exists a unit u in R such that u in ker(f)
    try:
        h2_ok = False
        if any(u == r for r in R_elements):
            is_unit = False
            for v in R_elements:
                if mul_R(u, v) == one_R and mul_R(v, u) == one_R:
                    is_unit = True
                    break
            if is_unit and f(u) == zero_S:
                h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: S is not the zero ring
    try:
        neg_q_ok = False
        for s in S_elements:
            if s != zero_S:
                neg_q_ok = True
                break
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S such that f(1_R) = 1_S",
    "H_2: There exists a unit u in R such that u in ker(f)",
    "¬Q: S is not the zero ring"
]

N_HYP = 2
NEG_Q_INDEX = 2