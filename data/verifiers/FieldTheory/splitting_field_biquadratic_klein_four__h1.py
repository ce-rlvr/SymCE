import sympy
from sympy import fraction, factor, cancel, Mul, Pow, sympify, isprime
from sympy.abc import x, y, z, u, v, w
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_square(expr, char):
    expr = cancel(sympify(expr))
    num, den = fraction(expr)
    
    if char > 0:
        try:
            den_mod = factor(den, modulus=char)
            if den_mod == 0:
                return False
        except Exception:
            pass

    p = num * den

    if char > 0:
        try:
            factored = factor(p, modulus=char)
        except Exception:
            factored = factor(p)
    else:
        factored = factor(p)
        
    if factored == 0:
        return True
        
    if isinstance(factored, Mul):
        args = factored.args
    else:
        args = [factored]
        
    for arg in args:
        if arg.is_number:
            if char == 0:
                if arg < 0: return False
                from sympy import sqrt
                if not sqrt(arg).is_Rational: return False
            else:
                val = int(arg) % char
                if not any((i*i)%char == val for i in range(char)): return False
        elif isinstance(arg, Pow):
            base, exp = arg.args
            if exp % 2 != 0:
                return False
        else:
            return False
    return True

def conditions(witness):
    """
    witness is expected to be a tuple: (char, a, b)
    where char is the characteristic of the field F (0 or a prime),
    and a, b are SymPy expressions representing elements of F.
    """
    try:
        char, a, b = witness
    except Exception:
        return [False, False, False]
        
    # H_1: a and b are elements of F
    try:
        a_sym = sympify(a)
        b_sym = sympify(b)
        
        if char != 0 and not isprime(char):
            h1_ok = False
        else:
            def is_valid_element(expr):
                expr = cancel(expr)
                _, den = fraction(expr)
                if char > 0:
                    try:
                        den_mod = factor(den, modulus=char)
                        if den_mod == 0:
                            return False
                    except Exception:
                        pass
                return True
                
            h1_ok = is_valid_element(a_sym) and is_valid_element(b_sym)
    except Exception:
        h1_ok = False
        
    # H_2: none of a, b, or ab is a perfect square in F
    try:
        a_sym = sympify(a)
        b_sym = sympify(b)
        a_sq = is_square(a_sym, char)
        b_sq = is_square(b_sym, char)
        ab_sq = is_square(a_sym * b_sym, char)
        h2_ok = not (a_sq or b_sq or ab_sq)
    except Exception:
        h2_ok = False
        
    # neg_Q: The conclusion fails
    try:
        if char == 2:
            # In characteristic 2, the extension is purely inseparable, 
            # so the Galois group is trivial, not the Klein four-group.
            neg_q_ok = True
        else:
            # If char != 2, the conclusion holds iff a, b, ab are not squares.
            # So the conclusion fails iff any of them IS a square.
            a_sym = sympify(a)
            b_sym = sympify(b)
            neg_q_ok = is_square(a_sym, char) or is_square(b_sym, char) or is_square(a_sym * b_sym, char)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: a and b are elements of F",
    "H_2: none of a, b, or ab is a perfect square in F",
    "¬Q: The splitting field of (x^2 - a)(x^2 - b) over F does not have degree 4 or its Galois group is not isomorphic to the Klein four-group"
]

N_HYP = 2
NEG_Q_INDEX = 2