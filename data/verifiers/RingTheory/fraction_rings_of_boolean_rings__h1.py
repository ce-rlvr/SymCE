import sympy

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Parse the witness
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        elif isinstance(witness, dict) and 'R' in witness and 'S' in witness:
            R = witness['R']
            S = witness['S']
        else:
            # Default to R = ZZ if only S is provided
            R = ZZ
            S = witness
            
        # If R is provided as a list of elements [0, 1, ..., n-1], treat it as Z/nZ
        if isinstance(R, (list, set, tuple)) and all(isinstance(x, int) for x in R):
            n = len(R)
            if sorted(list(R)) == list(range(n)):
                R = n
                
        # H1: S is a multiplicatively closed subset of R
        if R == ZZ or R == "ZZ" or R == QQ or R == "QQ":
            if isinstance(S, (list, set, tuple)) and all(isinstance(x, (int, sympy.Integer, float, sympy.Rational)) for x in S):
                if 1 in S:
                    h1 = all((a * b) in S for a in S for b in S)
        elif isinstance(R, int) and R >= 2:
            n = R
            if isinstance(S, (list, set, tuple)) and all(isinstance(x, int) and 0 <= x < n for x in S):
                if 1 in S:
                    h1 = all((a * b) % n in S for a in S for b in S)
                    
        # H2: S^-1 R is the ring of fractions of R with respect to S
        # This is a definitional hypothesis; it holds whenever H1 holds and the objects are valid.
        h2 = h1
        
        # neg_Q: S^-1 R is NOT a Boolean ring
        # A ring is Boolean if every element is idempotent (x^2 = x).
        # We check if there exists an element [r, s] in S^-1 R such that [r, s]^2 != [r, s].
        if R == ZZ or R == "ZZ" or R == QQ or R == "QQ":
            if 0 in S:
                # If 0 is in S, S^-1 R is the zero ring, which IS a Boolean ring (0^2 = 0).
                neg_q = False
            else:
                # In a domain, [r, s]^2 = [r, s] iff r^2/s^2 = r/s iff r^2 * s = r * s^2
                for r in [2, 3, 4]:
                    for s in S:
                        if r**2 * s != r * s**2:
                            neg_q = True
                            break
                    if neg_q:
                        break
        elif isinstance(R, int) and R >= 2:
            n = R
            # In Z/nZ, [r, s]^2 = [r, s] iff there exists t in S such that t * (r^2 * s - r * s^2) = 0 mod n
            for r in range(n):
                for s in S:
                    is_idempotent = False
                    for t in S:
                        if (t * (r**2 * s - r * s**2)) % n == 0:
                            is_idempotent = True
                            break
                    if not is_idempotent:
                        neg_q = True
                        break
                if neg_q:
                    break
                    
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: S^-1 R is the ring of fractions of R with respect to S",
    "¬Q: S^-1 R is not a Boolean ring"
]

N_HYP = 2
NEG_Q_INDEX = 2