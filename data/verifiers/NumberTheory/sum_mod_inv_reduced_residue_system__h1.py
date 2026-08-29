import sympy

def conditions(witness):
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        m = int(witness)
        if m < 1:
            return [False]
        
        coprimes = [x for x in range(1, m) if sympy.igcd(x, m) == 1]
        inverses = [sympy.mod_inverse(x, m) for x in coprimes]
        total_sum = sum(inverses)
        
        neg_q = (total_sum % m) != 0
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The sum of the modular inverses of all positive integers less than m and coprime to m is not congruent to 0 mod m"
]

N_HYP = 0
NEG_Q_INDEX = 0