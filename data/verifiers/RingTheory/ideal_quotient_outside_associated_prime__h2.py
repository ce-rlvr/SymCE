import math
import sympy

ZZ = "Z"
Z = "Z"

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R', 'Z')
            Q = witness.get('Q')
            P = witness.get('P')
            x = witness.get('x')
        else:
            R, Q, P, x = witness
            
        h1 = (R in ('Z', Z, ZZ, sympy.S.Integers, sympy.ZZ))
        
        if not h1:
            return [False, False, False]
            
        def get_gen(ideal):
            if isinstance(ideal, (int, sympy.Integer)):
                return int(ideal)
            if isinstance(ideal, (list, tuple, set)):
                g = 0
                for gen in ideal:
                    g = math.gcd(g, int(gen))
                return g
            return int(ideal)
            
        Q_gen = get_gen(Q)
        P_gen = get_gen(P)
        
        if not isinstance(x, (int, sympy.Integer)):
            h2 = False
            x_val = 1
        else:
            x_val = int(x)
            if P_gen == 0:
                h2 = (x_val != 0)
            else:
                h2 = (x_val % P_gen != 0)
            
        # neg_Q: (Q : x) != Q
        if Q_gen == 0:
            iq_gen = 0 if x_val != 0 else 1
        else:
            iq_gen = abs(Q_gen) // math.gcd(abs(Q_gen), abs(x_val))
            
        neg_q = (iq_gen != abs(Q_gen))
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: x is an element of R such that x ∉ P",
    "¬Q: The ideal quotient (Q : x) is not equal to Q"
]

N_HYP = 2
NEG_Q_INDEX = 2