import math
import sympy
from sympy import Rational, eye, zeros

# Standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity 1",
    "H_2: J(R) is the Jacobson radical of R",
    "H_3: x is an element of J(R)",
    "¬Q: The element 1 - xy is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    witness can be:
    1. ('Z_p', p, x, y) where R is the localization of Z at prime p.
       p: int (prime)
       x: sympy.Rational (element of J(R), so p divides numerator)
       y: sympy.Rational
    2. (n, x, y) or (n, J_set, x, y) for Z/nZ as a fallback.
    3. A dictionary with the above keys.
    """
    if isinstance(witness, dict):
        try:
            if witness.get('R') == 'Z_p' or witness.get('type') == 'Z_p':
                witness = ('Z_p', witness['p'], witness['x'], witness['y'])
            elif 'n' in witness:
                if 'J_set' in witness or 'J' in witness:
                    J = witness.get('J_set', witness.get('J'))
                    witness = (witness['n'], J, witness['x'], witness['y'])
                else:
                    witness = (witness['n'], witness['x'], witness['y'])
            elif 'R' in witness:
                if isinstance(witness['R'], int):
                    if 'J_set' in witness or 'J' in witness:
                        J = witness.get('J_set', witness.get('J'))
                        witness = (witness['R'], J, witness['x'], witness['y'])
                    else:
                        witness = (witness['R'], witness['x'], witness['y'])
        except Exception:
            pass

    # Try Z_p logic (Localization of Z at prime p)
    try:
        if isinstance(witness, tuple) and len(witness) == 4 and witness[0] == 'Z_p':
            _, p, x, y = witness
            
            try:
                H1 = sympy.isprime(p)
            except Exception:
                H1 = False
                
            H2 = True
            
            try:
                x_rat = sympy.Rational(x)
                # In Z_{(p)}, an element is in the Jacobson radical iff its numerator is divisible by p
                H3 = (x_rat.q % p != 0) and (x_rat.p % p == 0)
            except Exception:
                H3 = False
                
            try:
                y_rat = sympy.Rational(y)
                val = 1 - x_rat * y_rat
                # val is a unit in Z_{(p)} iff it is in Z_{(p)} and its numerator is not divisible by p
                is_in_R = (val.q % p != 0)
                is_unit = is_in_R and (val.p % p != 0)
                neg_Q = not is_unit
            except Exception:
                neg_Q = True
                
            return [bool(H1), bool(H2), bool(H3), bool(neg_Q)]
    except Exception:
        pass

    # Try Z/nZ logic
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                n, J_set, x, y = witness
            elif len(witness) == 3:
                n, x, y = witness
                J_set = None
            else:
                return [False, False, False, False]
                
            try:
                H1 = isinstance(n, int) and n >= 2
            except Exception:
                H1 = False
                
            try:
                if H1:
                    rad_n = math.prod(sympy.primefactors(n))
                    expected_J = set(k for k in range(n) if k % rad_n == 0)
                    if J_set is not None:
                        H2 = (set(J_set) == expected_J)
                    else:
                        H2 = True
                else:
                    H2 = False
            except Exception:
                H2 = False
                
            try:
                if H1 and isinstance(x, int):
                    if J_set is not None:
                        H3 = x in J_set
                    else:
                        H3 = (x % n) in expected_J
                else:
                    H3 = False
            except Exception:
                H3 = False
                
            try:
                if not H1:
                    neg_Q = False
                else:
                    val = 1 - x * y
                    is_int = False
                    val_int = None
                    
                    if isinstance(val, int):
                        is_int = True
                        val_int = val
                    elif isinstance(val, sympy.Rational) and val.q == 1:
                        is_int = True
                        val_int = int(val.p)
                    elif isinstance(val, float) and val.is_integer():
                        is_int = True
                        val_int = int(val)
                    elif hasattr(val, 'is_integer') and val.is_integer == True:
                        val_int = int(val)
                        is_int = True
                        
                    if is_int and val_int is not None:
                        is_u = (math.gcd(val_int % n, n) == 1)
                    else:
                        is_u = False
                        
                    neg_Q = not is_u
            except Exception:
                neg_Q = True
                
            return [bool(H1), bool(H2), bool(H3), bool(neg_Q)]
    except Exception:
        pass

    return [False, False, False, False]