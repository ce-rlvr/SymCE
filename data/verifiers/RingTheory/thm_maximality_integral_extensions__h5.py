import sympy

# Supported rings: Z (integers) and QQ (rationals).
# Ideals are represented by their non-negative integer generators.
Z = 'Z'
QQ = 'QQ'

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should provide the rings R, S and the ideal generators Q, P.
    It can be a dictionary, an object with attributes, or a tuple (R, S, Q, P) or (Q, P).
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', 'Z')
            S = witness.get('S', 'Z')
            Q = witness.get('Q')
            P = witness.get('P')
        elif hasattr(witness, 'R') and hasattr(witness, 'S'):
            R = witness.R
            S = witness.S
            Q = witness.Q
            P = witness.P
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                R, S, Q, P = witness
            elif len(witness) == 2:
                R, S = 'Z', 'Z'
                Q, P = witness
            else:
                return [False] * 5
        else:
            return [False] * 5
            
        # H1: R and S are commutative rings with identity
        try:
            h1 = (R in ['Z', 'QQ']) and (S in ['Z', 'QQ'])
        except Exception:
            h1 = False
            
        # H2: R is a subring of S
        try:
            h2 = False
            if R == 'Z' and S == 'Z': h2 = True
            if R == 'QQ' and S == 'QQ': h2 = True
            if R == 'Z' and S == 'QQ': h2 = True
        except Exception:
            h2 = False
            
        # H3: S is an integral extension of R
        try:
            h3 = False
            if R == 'Z' and S == 'Z': h3 = True
            if R == 'QQ' and S == 'QQ': h3 = True
        except Exception:
            h3 = False
            
        # H4: Q is a prime ideal of S
        try:
            h4 = False
            if Q is not None:
                q_val = abs(int(Q))
                if S == 'Z':
                    h4 = (q_val == 0 or sympy.isprime(q_val))
                elif S == 'QQ':
                    h4 = (q_val == 0)
        except Exception:
            h4 = False
            
        # Negated Conclusion: not (Q is maximal in S iff P is maximal in R)
        try:
            if Q is not None:
                q_val = abs(int(Q))
                if S == 'Z':
                    q_max = sympy.isprime(q_val)
                elif S == 'QQ':
                    q_max = (q_val == 0)
                else:
                    q_max = False
            else:
                q_max = False
                
            if P is not None:
                p_val = abs(int(P))
                if R == 'Z':
                    p_max = sympy.isprime(p_val)
                elif R == 'QQ':
                    p_max = (p_val == 0)
                else:
                    p_max = False
            else:
                p_max = False
                
            neg_q = (q_max != p_max)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False] * 5

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: R is a subring of S",
    "H_3: S is an integral extension of R",
    "H_4: Q is a prime ideal of S",
    "¬Q: Q is a maximal ideal of S if and only if P is a maximal ideal of R (fails)"
]

N_HYP = 4
NEG_Q_INDEX = 4