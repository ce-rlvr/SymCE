import math
import sympy

Z = sympy.S.Integers
Q = sympy.S.Rationals

# Top-level setup
# We represent commutative rings R = Z/nZ and S = Z/mZ by their moduli n and m.
# Ideals I and J in R are represented by their generators I_gen and J_gen.
# The homomorphism f: R -> S is the natural projection, which is valid and surjective if m divides n.
# A witness should be a tuple: (n, m, I_gen, J_gen)
# Alternatively, it can be a dictionary with these keys, or a 5-tuple (n, m, f, I_gen, J_gen).

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            m = witness.get('m')
            I_gen = witness.get('I_gen')
            J_gen = witness.get('J_gen')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                n, m, I_gen, J_gen = witness
            elif len(witness) == 5:
                n, m, _, I_gen, J_gen = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        if n == sympy.S.Integers:
            n = 0
        if m == sympy.S.Integers:
            m = 0

        def get_gen(gen):
            if isinstance(gen, int):
                return gen
            elif isinstance(gen, (list, tuple, set)):
                g = 0
                for x in gen:
                    g = math.gcd(g, int(x))
                return g
            else:
                return int(gen)

        n = int(n)
        m = int(m)
        I_gen = get_gen(I_gen)
        J_gen = get_gen(J_gen)

        # H1: R and S are commutative rings
        h1 = (n >= 0 and m >= 0)
        
        # H2: f: R -> S is a surjective ring homomorphism
        if not h1:
            h2 = False
        else:
            if m == 0:
                h2 = (n == 0)
            elif n == 0:
                h2 = True
            else:
                h2 = (n % m == 0)
                
        # neg_Q: f(I) and f(J) are NOT coprime ideals in S
        if not h1:
            neg_q = False
        else:
            if m == 0:
                g = math.gcd(I_gen, J_gen)
            else:
                g = math.gcd(math.gcd(I_gen, J_gen), m)
            neg_q = (g != 1)
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings (represented by Z/nZ and Z/mZ)",
    "H_2: f: R -> S is a surjective ring homomorphism (m divides n)",
    "¬Q: f(I) and f(J) are not coprime ideals in S (gcd(I_gen, J_gen, m) != 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2