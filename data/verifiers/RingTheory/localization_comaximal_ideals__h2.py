import sympy

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    try:
        # Extract P, I, J (represented by their generators in Z)
        if isinstance(witness, dict):
            p = witness.get('P', witness.get('p'))
            i = witness.get('I', witness.get('i'))
            j = witness.get('J', witness.get('j'))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                _, p, i, j = witness
            elif len(witness) == 3:
                p, i, j = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        # H1: R is a commutative ring
        # We assume R is Z for integer inputs, which is a commutative ring.
        h1 = True
        
        # H2: P is a prime ideal of R
        # In Z, an ideal (p) is prime iff p is 0 or a prime number.
        p = abs(int(p))
        if p == 0:
            h2 = True
        else:
            h2 = sympy.isprime(p)
            
        # neg_Q: neither I_P nor J_P is equal to R_P
        # I_P = R_P iff I is not contained in P.
        # So I_P != R_P iff I is contained in P.
        # In Z, (i) is contained in (p) iff p divides i.
        i = int(i)
        j = int(j)
        
        if p == 0:
            i_in_p = (i == 0)
            j_in_p = (j == 0)
        else:
            i_in_p = (i % p == 0)
            j_in_p = (j % p == 0)
            
        neg_q = bool(i_in_p and j_in_p)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal of R",
    "¬Q: Neither I_P nor J_P is equal to R_P"
]

N_HYP = 2
NEG_Q_INDEX = 2