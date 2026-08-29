import sympy

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a dictionary with keys 'R', 'd', 'a', 'b',
    or a tuple (R, d, a, b), or a tuple (d, a, b) assuming R='Z'.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', 'Z')
            d = witness.get('d')
            a = witness.get('a')
            b = witness.get('b')
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                R, d, a, b = witness
            elif len(witness) == 3:
                R = 'Z'
                d, a, b = witness
            else:
                return [False] * 5
        else:
            return [False] * 5
            
        # H1: R is a Euclidean domain
        # For simplicity and fast verification, we restrict R to the integers.
        h1 = (str(R) in ['Z', 'ZZ', 'Integers'])
        if h1:
            if not isinstance(a, (int, sympy.Integer)) or not isinstance(b, (int, sympy.Integer)):
                h1 = False
            else:
                a = int(a)
                b = int(b)
                
        # H2: d is a submultiplicative Euclidean function on R
        h2 = False
        if h1 and callable(d):
            h2 = True
            # Check Euclidean property on a bounded grid
            for x in range(-30, 31):
                for y in range(-30, 31):
                    if y == 0:
                        continue
                    found = False
                    q_base = int(x / y)
                    # Check nearby quotients
                    for q in [q_base - 2, q_base - 1, q_base, q_base + 1, q_base + 2]:
                        r = x - q * y
                        try:
                            if r == 0 or d(r) < d(y):
                                found = True
                                break
                        except Exception:
                            pass
                    if not found:
                        h2 = False
                        break
                if not h2:
                    break
            
            # Check submultiplicative property: d(xy) <= d(x)d(y)
            if h2:
                for x in range(-30, 31):
                    for y in range(-30, 31):
                        try:
                            if d(x * y) > d(x) * d(y):
                                h2 = False
                                break
                        except Exception:
                            h2 = False
                            break
                    if not h2:
                        break
                        
            # Check monotone property: d(x) <= d(xy) for y != 0
            # (Often included in the definition of a Euclidean function or submultiplicativity)
            if h2:
                for x in range(-30, 31):
                    for y in range(-30, 31):
                        if y == 0:
                            continue
                        try:
                            if d(x) > d(x * y):
                                h2 = False
                                break
                        except Exception:
                            h2 = False
                            break
                    if not h2:
                        break

        # H3: a divides b
        h3 = False
        if h1:
            if a == 0:
                h3 = (b == 0)
            else:
                h3 = (b % a == 0)
                
        # H4: d(a) == d(b)
        h4 = False
        if callable(d):
            try:
                h4 = bool(d(a) == d(b))
            except Exception:
                h4 = False
            
        # neg_Q: a and b are NOT associate elements in R
        # In Z, associates are equal up to sign.
        neg_q = False
        if h1:
            neg_q = bool(abs(a) != abs(b))
            
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: d is a submultiplicative Euclidean function on R",
    "H_3: a divides b",
    "H_4: d(a) = d(b)",
    "¬Q: a and b are not associate elements in R"
]

N_HYP = 4
NEG_Q_INDEX = 4