import operator
from sympy import eye, zeros, Matrix, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def get_add(witness, prefix):
    if isinstance(witness, dict) and f'{prefix}_add' in witness:
        return witness[f'{prefix}_add']
    if hasattr(witness, f'{prefix}_add'):
        return getattr(witness, f'{prefix}_add')
    return operator.add

def get_mul(witness, prefix):
    if isinstance(witness, dict) and f'{prefix}_mul' in witness:
        return witness[f'{prefix}_mul']
    if hasattr(witness, f'{prefix}_mul'):
        return getattr(witness, f'{prefix}_mul')
    return operator.mul

def get_zero(witness, prefix):
    if isinstance(witness, dict) and f'{prefix}_zero' in witness:
        return witness[f'{prefix}_zero']
    if hasattr(witness, f'{prefix}_zero'):
        return getattr(witness, f'{prefix}_zero')
    return 0

def get_elements(witness, prefix):
    if isinstance(witness, dict) and f'{prefix}_elements' in witness:
        return witness[f'{prefix}_elements']
    if hasattr(witness, f'{prefix}_elements'):
        return getattr(witness, f'{prefix}_elements')
    return None

def is_zero_elem(elem, zero_ref):
    try:
        if hasattr(elem, 'is_zero_matrix') and elem.is_zero_matrix:
            return True
    except Exception:
        pass
    try:
        if hasattr(elem, 'is_zero') and elem.is_zero:
            return True
    except Exception:
        pass
    try:
        eq = (elem == zero_ref)
        if isinstance(eq, bool) and eq:
            return True
        if hasattr(eq, '__iter__') and all(eq):
            return True
    except Exception:
        pass
    return False

def is_equal(a, b):
    try:
        if a is b:
            return True
        eq = (a == b)
        if isinstance(eq, bool):
            return eq
        try:
            return bool(eq)
        except Exception:
            pass
        if hasattr(eq, '__iter__'):
            return all(eq)
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # H1: f: R -> S is a ring homomorphism
    h1_ok = False
    try:
        if isinstance(witness, dict) and 'is_homomorphism' in witness:
            h1_ok = bool(witness['is_homomorphism']())
        elif hasattr(witness, 'is_homomorphism'):
            h1_ok = bool(witness.is_homomorphism())
        else:
            R_elements = get_elements(witness, 'R')
            if R_elements is not None:
                R_add = get_add(witness, 'R')
                R_mul = get_mul(witness, 'R')
                S_add = get_add(witness, 'S')
                S_mul = get_mul(witness, 'S')
                
                if isinstance(witness, dict):
                    f = witness.get('f')
                else:
                    f = getattr(witness, 'f')
                    
                f_func = (lambda a: f[a]) if isinstance(f, dict) else f
                
                h1_ok = True
                for a in R_elements:
                    for b in R_elements:
                        if not is_equal(f_func(R_add(a, b)), S_add(f_func(a), f_func(b))):
                            h1_ok = False
                            break
                        if not is_equal(f_func(R_mul(a, b)), S_mul(f_func(a), f_func(b))):
                            h1_ok = False
                            break
                    if not h1_ok:
                        break
    except Exception:
        h1_ok = False

    # H2: x in R is a nilpotent element
    h2_ok = False
    try:
        if isinstance(witness, dict) and 'is_x_nilpotent' in witness:
            h2_ok = bool(witness['is_x_nilpotent']())
        elif hasattr(witness, 'is_x_nilpotent'):
            h2_ok = bool(witness.is_x_nilpotent())
        else:
            R_elements = get_elements(witness, 'R')
            R_mul = get_mul(witness, 'R')
            R_zero = get_zero(witness, 'R')
            
            if isinstance(witness, dict):
                x_val = witness.get('x')
            else:
                x_val = getattr(witness, 'x')
                
            max_n = len(R_elements) if R_elements else 100
            
            curr = x_val
            for _ in range(1, max_n + 1):
                if is_zero_elem(curr, R_zero):
                    h2_ok = True
                    break
                curr = R_mul(curr, x_val)
    except Exception:
        h2_ok = False

    # neg_Q: f(x) is NOT a nilpotent element in S
    neg_q_ok = False
    try:
        if isinstance(witness, dict) and 'is_fx_nilpotent' in witness:
            neg_q_ok = not bool(witness['is_fx_nilpotent']())
        elif hasattr(witness, 'is_fx_nilpotent'):
            neg_q_ok = not bool(witness.is_fx_nilpotent())
        else:
            S_elements = get_elements(witness, 'S')
            S_mul = get_mul(witness, 'S')
            S_zero = get_zero(witness, 'S')
            
            if isinstance(witness, dict):
                f = witness.get('f')
                x_val = witness.get('x')
            else:
                f = getattr(witness, 'f')
                x_val = getattr(witness, 'x')
                
            f_func = (lambda a: f[a]) if isinstance(f, dict) else f
            fx = f_func(x_val)
                
            max_n = len(S_elements) if S_elements else 100
            
            is_fx_nil = False
            curr = fx
            for _ in range(1, max_n + 1):
                if is_zero_elem(curr, S_zero):
                    is_fx_nil = True
                    break
                curr = S_mul(curr, fx)
            
            neg_q_ok = not is_fx_nil
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f: R -> S is a ring homomorphism",
    "H_2: x in R is a nilpotent element",
    "¬Q: f(x) is not a nilpotent element in S"
]

N_HYP = 2
NEG_Q_INDEX = 2