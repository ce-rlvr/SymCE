import z3
import math
import itertools
import functools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should represent a finite ring Z_q and a function f: Z_q -> Z_q.
    Expected witness format: a tuple (q, f) or a dict {'q': q, 'f': f},
    where q is an integer and f is a list, dict, or callable representing the function.
    """
    try:
        if hasattr(witness, 'q') and hasattr(witness, 'f'):
            q = witness.q
            f = witness.f
        elif isinstance(witness, dict):
            q = witness['q']
            f = witness['f']
        else:
            q, f = witness
            
        q = int(q)
        if q < 1 or q > 100:
            h1 = False
        else:
            if callable(f):
                f_list = [int(f(i)) for i in range(q)]
            elif isinstance(f, dict):
                f_list = []
                for i in range(q):
                    if i in f:
                        f_list.append(int(f[i]))
                    elif str(i) in f:
                        f_list.append(int(f[str(i)]))
                    else:
                        raise ValueError("Missing key in dict")
            else:
                f_list = [int(val) for val in f]
                
            h1 = len(f_list) == q and all(0 <= val < q for val in f_list)
    except Exception:
        h1 = False
        return [False, False]

    if not h1:
        return [False, False]

    try:
        solver = z3.Solver()
        solver.set("timeout", 4000)
        
        # Coefficients of the polynomial P(x) = c_0 + c_1 x + ... + c_{q-1} x^{q-1}
        coeffs = [z3.Int('c_%d' % i) for i in range(q)]
        for c in coeffs:
            solver.add(c >= 0, c < q)
        
        # P(a) = f(a) mod q for all a in Z_q
        for a in range(q):
            val = coeffs[0]
            for i in range(1, q):
                a_pow = (a ** i) % q
                val += coeffs[i] * a_pow
            k = z3.Int('k_%d' % a)
            solver.add(val - f_list[a] == q * k)
        
        count = 0
        while True:
            res = solver.check()
            if res == z3.sat:
                count += 1
                if count > 1:
                    break
                m = solver.model()
                block = []
                for c in coeffs:
                    block.append(c != m.evaluate(c))
                solver.add(z3.Or(block))
            elif res == z3.unsat:
                break
            else:
                # In case of timeout or unknown, we cannot verify the conclusion
                return [h1, False]
                
        # The conclusion states there is a UNIQUE polynomial.
        # The negation is true if the count of such polynomials is NOT exactly 1.
        neg_q = (count != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ['H_1: f is a function', 'not Q: P is not unique']
N_HYP = 1
NEG_Q_INDEX = 1