import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
# No specific named bindings needed for this number theory problem.

def get_a(witness, n):
    if callable(witness):
        return witness(n)
    else:
        return witness[n]

def is_integer(x):
    if isinstance(x, bool):
        return False
    return isinstance(x, (int, sympy.Integer))

def conditions(witness) -> list[bool]:
    # H_1: a_0 is an integer
    try:
        a0 = get_a(witness, 0)
        h1 = is_integer(a0)
    except Exception:
        h1 = False

    # H_2: (a_n)_{n >= 1} is an infinite sequence of strictly positive integers
    try:
        h2 = True
        for n in range(1, 100):
            an = get_a(witness, n)
            if not is_integer(an) or an <= 0:
                h2 = False
                break
        if h2:
            # Check if it's a finite collection like a list or tuple
            if hasattr(witness, '__len__'):
                try:
                    if isinstance(len(witness), int):
                        h2 = False
                except Exception:
                    pass
            # Check if we can access a large index
            if h2:
                try:
                    get_a(witness, 1000)
                except Exception:
                    h2 = False
    except Exception:
        h2 = False

    # ¬Q: The sequence of convergents does not converge to a unique irrational limit
    try:
        p_minus2, p_minus1 = 0, 1
        q_minus2, q_minus1 = 1, 0
        C = []
        for n in range(105):
            try:
                an = get_a(witness, n)
            except Exception:
                break
            
            pn = an * p_minus1 + p_minus2
            qn = an * q_minus1 + q_minus2
            
            if qn == 0:
                C.append(None)
            else:
                if is_integer(pn) and is_integer(qn):
                    C.append(sympy.Rational(int(pn), int(qn)))
                else:
                    C.append(pn / qn)
                    
            p_minus2, p_minus1 = p_minus1, pn
            q_minus2, q_minus1 = q_minus1, qn
        
        neg_q = False
        if len(C) < 105:
            neg_q = True
        else:
            valid_C = [c for c in C[-10:] if c is not None]
            if len(valid_C) < 10:
                neg_q = True
            else:
                diffs = []
                for i in range(1, 10):
                    c_curr = valid_C[i]
                    c_prev = valid_C[i-1]
                    
                    if hasattr(c_curr, 'evalf'):
                        v_curr = float(c_curr.evalf(15))
                    else:
                        v_curr = float(c_curr)
                        
                    if hasattr(c_prev, 'evalf'):
                        v_prev = float(c_prev.evalf(15))
                    else:
                        v_prev = float(c_prev)
                        
                    diffs.append(abs(v_curr - v_prev))
                
                # If it doesn't converge
                if any(d > 1e-4 for d in diffs):
                    neg_q = True
                # If it converges to a rational number (sequence becomes exactly constant)
                elif valid_C[-1] == valid_C[-2] == valid_C[-3]:
                    neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a_0 is an integer",
    "H_2: (a_n)_{n >= 1} is an infinite sequence of strictly positive integers",
    "¬Q: The sequence of convergents does not converge to a unique irrational limit"
]

N_HYP = 2
NEG_Q_INDEX = 2