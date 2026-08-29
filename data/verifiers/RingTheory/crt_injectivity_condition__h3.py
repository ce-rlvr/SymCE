import math
from sympy import ZZ

# Top-level setup
Z = 'Z'

def Zm(m):
    return {'ring': 'Zm', 'm': m}

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I_1, ..., I_n are ideals of R",
    "¬Q: The map phi is NOT (injective iff the intersection of the ideals is the zero ideal)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness can be:
      - A list of integers representing ideals in Z.
      - A tuple (R, ideals) where R is 'Z', ZZ, or Zm(m), and ideals is a list of integers.
      - A dictionary with keys 'ring', 'm' (if Zm), and 'ideals'.
    """
    try:
        ring = None
        ideals = None
        m = 0
        
        if isinstance(witness, list) and all(isinstance(x, int) for x in witness):
            ring = 'Z'
            ideals = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if R == ZZ or R == 'Z':
                ring = 'Z'
                ideals = I
            elif isinstance(R, dict) and R.get('ring') == 'Zm':
                ring = 'Zm'
                m = R['m']
                ideals = I
        elif isinstance(witness, dict):
            ring = witness.get('ring', 'Z')
            ideals = witness.get('ideals', [])
            m = witness.get('m', 0)
            
        if ring not in ['Z', 'Zm'] or not isinstance(ideals, list):
            return [False, False, False]
            
        h1 = True
        if ring == 'Zm' and m <= 0:
            h1 = False
            
        h2 = all(isinstance(x, int) for x in ideals)
        
        if not (h1 and h2):
            return [h1, h2, False]
            
        # Evaluate the intersection and injectivity
        if ring == 'Z':
            if not ideals:
                # Empty intersection in Z is Z, which is not the zero ideal.
                # Map to empty product is Z -> 0, which is not injective.
                intersection_zero = False
                injective = False
            else:
                l = ideals[0]
                for a in ideals[1:]:
                    l = math.lcm(l, a)
                intersection_zero = (l == 0)
                injective = (l == 0)
        elif ring == 'Zm':
            if not ideals:
                # Empty intersection in Zm is Zm. Zero ideal iff m=1.
                intersection_zero = (m == 1)
                injective = (m == 1)
            else:
                l = math.gcd(ideals[0], m)
                for a in ideals[1:]:
                    l = math.lcm(l, math.gcd(a, m))
                intersection_zero = (l % m == 0)
                injective = (l % m == 0)
                
        # The conclusion states: phi is injective iff intersection is zero.
        # This is a mathematical tautology (ker phi = intersection of I_i).
        # Thus, the negated conclusion is always False for valid rings and ideals.
        neg_q = not (injective == intersection_zero)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]