import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
from sympy.abc import x, y

# Top-level setup
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

Z = sympy.Symbol('Z')
ZZ = sympy.Symbol('ZZ')
Q = sympy.Symbol('Q')
QQ = sympy.Symbol('QQ')
R = sympy.Symbol('R')
P = sympy.Symbol('P')
k = sympy.Symbol('k')

def extract_int(s):
    num_str = ''
    found_digit = False
    for char in s:
        if char.isdigit() or (char == '-' and not found_digit):
            num_str += char
            found_digit = True
        elif found_digit:
            break
    if num_str and num_str != '-':
        return int(num_str)
    return None

def parse_witness(witness):
    try:
        if isinstance(witness, (int, sympy.Integer)):
            return 'Z', int(witness)
            
        if isinstance(witness, sympy.Expr):
            syms = witness.free_symbols
            if len(syms) >= 1:
                if len(syms) == 1:
                    sym = list(syms)[0]
                    if str(sym) in ['Z', 'ZZ']:
                        val = extract_int(str(witness))
                        if val is not None:
                            return 'Z', val
                        else:
                            return 'Z', 1
                return 'poly', witness
            elif len(syms) == 0:
                return 'Z', int(witness)
                
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            R_obj, P_obj = witness
            
            if isinstance(P_obj, (int, sympy.Integer)):
                return 'Z', int(P_obj)
                
            if isinstance(P_obj, sympy.Expr):
                syms = P_obj.free_symbols
                if len(syms) >= 1:
                    if len(syms) == 1:
                        sym = list(syms)[0]
                        if str(sym) in ['Z', 'ZZ']:
                            val = extract_int(str(P_obj))
                            if val is not None:
                                return 'Z', val
                            else:
                                return 'Z', 1
                    return 'poly', P_obj
                elif len(syms) == 0:
                    return 'Z', int(P_obj)
                    
            P_str = str(P_obj)
            if 'x' in P_str or 'y' in P_str:
                try:
                    expr = sympy.sympify(P_str)
                    if len(expr.free_symbols) >= 1:
                        return 'poly', expr
                except:
                    pass
                    
            val = extract_int(P_str)
            if val is not None:
                return 'Z', val
                
        if isinstance(witness, str):
            if 'x' in witness or 'y' in witness:
                try:
                    expr = sympy.sympify(witness)
                    if len(expr.free_symbols) >= 1:
                        return 'poly', expr
                except:
                    pass
            val = extract_int(witness)
            if val is not None:
                return 'Z', val
    except Exception:
        pass
        
    return None, None

def conditions(witness) -> list[bool]:
    ring_type, gen = parse_witness(witness)
    
    if ring_type is None:
        return [False, False]
        
    # H_1: R is a commutative ring
    # Both Z and k[x, y, ...] are commutative rings.
    h1_ok = True
    
    # neg_Q: Krull dimension of R_P != height of P
    # This is True iff P is NOT a prime ideal.
    neg_q = False
    try:
        if ring_type == 'Z':
            n = abs(gen)
            if n == 0:
                neg_q = False # (0) is prime
            elif n == 1:
                neg_q = True  # (1) is not prime
            else:
                neg_q = not isprime(n)
                
        elif ring_type == 'poly':
            expr = gen
            if expr == 0:
                neg_q = False # (0) is prime in domain
            elif len(expr.free_symbols) == 0:
                neg_q = True # units are not prime
            else:
                from sympy import factor_list
                factors = factor_list(expr)
                # factors[1] is a list of (factor, multiplicity)
                # It's prime iff there is exactly one factor and its multiplicity is 1
                if len(factors[1]) == 1 and factors[1][0][1] == 1:
                    neg_q = False # irreducible, so prime ideal
                else:
                    neg_q = True # reducible or multiple factors, so not prime
    except Exception:
        neg_q = False
        
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The Krull dimension of the localized ring R_P is not equal to the height of P"
]

N_HYP = 1
NEG_Q_INDEX = 1