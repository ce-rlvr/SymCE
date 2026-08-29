import sympy
from sympy import Symbol, Abs, diff, Interval, solveset, EmptySet
from sympy.calculus.util import maximum, minimum
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I is an interval",
    "H_2: There exists M > 0 such that |f'(x)| <= M for all x in I",
    "¬Q: There exist x, y in I such that |f(x) - f(y)| > M|x - y|"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the Bounded Derivative Theorem conjecture.
    The witness can be a dictionary or a tuple containing (f, I, M) and optionally (x, y).
    """
    try:
        if isinstance(witness, dict):
            f = witness['f']
            I = witness['I']
            M = witness['M']
            x_val = witness.get('x')
            y_val = witness.get('y')
        else:
            f = witness[0]
            I = witness[1]
            M = witness[2]
            x_val = witness[3] if len(witness) > 3 else None
            y_val = witness[4] if len(witness) > 4 else None
    except Exception:
        return [False, False, False]
        
    # H_1: I is an interval
    try:
        h1 = isinstance(I, Interval)
    except Exception:
        h1 = False
        
    # H_2: M > 0 and |f'(x)| <= M for all x in I
    h2 = False
    try:
        if M > 0:
            free_syms = f.free_symbols
            if Symbol('x') in free_syms:
                x_var = Symbol('x')
            elif free_syms:
                x_var = list(free_syms)[0]
            else:
                x_var = Symbol('x')
                
            f_prime = diff(f, x_var)
            try:
                f_prime_simp = sympy.simplify(f_prime)
            except Exception:
                f_prime_simp = f_prime
                
            if f_prime_simp.is_constant() and f_prime_simp.is_number:
                h2 = bool(f_prime_simp <= M and f_prime_simp >= -M)
            else:
                try:
                    max_val = maximum(f_prime_simp, x_var, I)
                    min_val = minimum(f_prime_simp, x_var, I)
                    if max_val.is_number and min_val.is_number:
                        h2 = bool(max_val <= M and min_val >= -M)
                    else:
                        sol = solveset(Abs(f_prime_simp) > M, x_var, domain=I)
                        if sol == EmptySet:
                            h2 = True
                except Exception:
                    # Fallback to grid check if symbolic methods fail
                    start = float(I.start) if I.start != -sympy.oo else -10.0
                    end = float(I.end) if I.end != sympy.oo else 10.0
                    points = [start + i * (end - start) / 50.0 for i in range(51)]
                    h2 = True
                    for p in points:
                        if I.contains(p):
                            val = abs(float(f_prime_simp.subs(x_var, p)))
                            if val > float(M) + 1e-9:
                                h2 = False
                                break
    except Exception:
        h2 = False
        
    # ¬Q: There exist x, y in I such that |f(x) - f(y)| > M|x - y|
    neg_q = False
    try:
        free_syms = f.free_symbols
        if Symbol('x') in free_syms:
            x_var = Symbol('x')
        elif free_syms:
            x_var = list(free_syms)[0]
        else:
            x_var = Symbol('x')
            
        # Check explicitly provided x and y if available
        if x_val is not None and y_val is not None:
            try:
                if I.contains(x_val) and I.contains(y_val):
                    lhs = abs(f.subs(x_var, x_val) - f.subs(x_var, y_val))
                    rhs = M * abs(x_val - y_val)
                    if bool(lhs > rhs):
                        neg_q = True
            except Exception:
                pass
                
        # Fallback to grid search to find a counterexample pair
        if not neg_q:
            start = float(I.start) if I.start != -sympy.oo else -10.0
            end = float(I.end) if I.end != sympy.oo else 10.0
            
            points = [start + i * (end - start) / 50.0 for i in range(51)]
            points.extend([0.0, -1.0, 1.0, start, end])
            
            valid_points = []
            for p in points:
                try:
                    if I.contains(p):
                        valid_points.append(p)
                except Exception:
                    pass
                    
            for i in range(len(valid_points)):
                for j in range(i + 1, len(valid_points)):
                    xv = valid_points[i]
                    yv = valid_points[j]
                    try:
                        lhs = abs(float(f.subs(x_var, xv)) - float(f.subs(x_var, yv)))
                        rhs = float(M) * abs(xv - yv)
                        if lhs > rhs + 1e-9:
                            neg_q = True
                            break
                    except Exception:
                        pass
                if neg_q:
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]