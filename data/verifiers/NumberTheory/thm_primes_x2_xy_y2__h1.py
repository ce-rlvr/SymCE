import sympy
from sympy.ntheory import factorint

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # Witness must be an integer
        if isinstance(witness, bool):
            return [False]
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        
        p = int(witness)
        
        # Evaluate P(p): There exist integers x, y such that x^2 + xy + y^2 = p
        # A non-negative integer p can be represented by the quadratic form x^2 + xy + y^2
        # if and only if every prime factor q ≡ 2 (mod 3) appears with an even exponent.
        if p < 0:
            P_p = False
        elif p == 0:
            P_p = True
        else:
            P_p = True
            factors = factorint(p)
            for q, e in factors.items():
                if q % 3 == 2 and e % 2 != 0:
                    P_p = False
                    break
                    
        # Evaluate Q(p): p = 3 or p ≡ 1 (mod 3)
        Q_p = (p == 3) or (p % 3 == 1)
        
        # The conclusion is P(p) <=> Q(p).
        # The negated conclusion is that this equivalence fails.
        neg_Q = bool(P_p != Q_p)
        
        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: (∃x,y: x^2+xy+y^2=p) is not equivalent to (p=3 or p≡1 mod 3)"
]

N_HYP = 0
NEG_Q_INDEX = 0