import math
import sympy
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        P = witness['P']
        leq = witness['leq']
        R = witness['R']
        f = witness['f']
    except Exception:
        return [False, False, False, False]
    
    # H1: P is a locally finite partially ordered set
    try:
        h1 = True
        if not isinstance(P, (list, tuple, set)): 
            h1 = False
        if not isinstance(leq, (list, tuple, set)): 
            h1 = False
        
        if h1:
            P_list = list(P)
            leq_list = list(leq)
            
            # reflexive
            for x in P_list:
                if (x, x) not in leq_list: 
                    h1 = False
            # antisymmetric
            for x in P_list:
                for y in P_list:
                    if (x, y) in leq_list and (y, x) in leq_list and x != y: 
                        h1 = False
            # transitive
            for x in P_list:
                for y in P_list:
                    for z in P_list:
                        if (x, y) in leq_list and (y, z) in leq_list and (x, z) not in leq_list: 
                            h1 = False
    except Exception:
        h1 = False

    # H2: R is a commutative ring with identity
    try:
        h2 = False
        R_str = str(R).strip()
        if R_str in ['Z', 'Q', 'R', 'C', 'ZZ', 'QQ', 'RR', 'CC']:
            h2 = True
        elif R_str.startswith('Z_'):
            n = int(R_str[2:])
            if n >= 2:
                h2 = True
        elif R_str.startswith('Z') and R_str[1:].isdigit():
            n = int(R_str[1:])
            if n >= 2:
                h2 = True
    except Exception:
        h2 = False

    # H3: I(P, R) is the incidence algebra of P over R
    h3 = True

    # neg_Q: f is a unit in I(P, R) iff f(x, x) is a unit in R for all x \in P
    try:
        def is_unit(val, R):
            R_str = str(R).strip()
            if R_str in ['Z', 'ZZ']:
                try:
                    return int(val) in [1, -1]
                except Exception:
                    return False
            elif R_str in ['Q', 'R', 'C', 'QQ', 'RR', 'CC']:
                try:
                    return float(val) != 0.0
                except Exception:
                    return False
            elif R_str.startswith('Z_'):
                try:
                    n = int(R_str[2:])
                    return math.gcd(int(val) % n, n) == 1
                except Exception:
                    return False
            elif R_str.startswith('Z') and R_str[1:].isdigit():
                try:
                    n = int(R_str[1:])
                    return math.gcd(int(val) % n, n) == 1
                except Exception:
                    return False
            return False

        def get_f(x, y):
            try:
                if isinstance(f, dict):
                    return f.get((x, y), 0)
                elif hasattr(f, '__call__'):
                    return f(x, y)
                elif isinstance(f, (list, tuple)):
                    for item in f:
                        if len(item) == 2 and item[0] == (x, y):
                            return item[1]
                    return 0
                else:
                    return 0
            except Exception:
                return 0

        f_in_I = True
        for x in P_list:
            for y in P_list:
                if (x, y) not in leq_list:
                    if get_f(x, y) != 0:
                        f_in_I = False
                        break
            if not f_in_I:
                break
        
        rhs = True
        for x in P_list:
            if not is_unit(get_f(x, x), R):
                rhs = False
                break
        
        # f is a unit in I(P, R) implies f is an element of I(P, R)
        # By the true theorem, if f is in I(P, R), it is a unit iff f(x,x) is a unit for all x.
        lhs = f_in_I and rhs
        
        neg_q = not (lhs == rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P is a locally finite partially ordered set",
    "H_2: R is a commutative ring with identity",
    "H_3: I(P, R) is the incidence algebra of P over R",
    "¬Q: The equivalence 'f is a unit in I(P, R) iff f(x, x) is a unit in R for all x' fails"
]

N_HYP = 3
NEG_Q_INDEX = 3