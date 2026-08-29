import sympy

# Top-level setup
x = sympy.Symbol('x')

CONDITION_LABELS = [
    "H_1: R is a Dedekind domain",
    "¬Q: I is primary but not a power of a prime ideal, or vice versa"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    # Extract generator if witness is a tuple or list (e.g., (Ring, Ideal_Generator))
    try:
        if isinstance(witness, (tuple, list)):
            gen = witness[-1]
        else:
            gen = witness
    except Exception:
        gen = witness

    # Check if the ideal is the zero ideal or the unit ideal.
    # In a Dedekind domain, the zero ideal is primary but not a power of a non-zero prime ideal.
    # The unit ideal is a power of a prime ideal (P^0) but not primary.
    # Both are standard counterexamples depending on which hypothesis was dropped 
    # ("I is non-zero" or "I is proper").
    try:
        if gen == 0 or (hasattr(gen, 'is_zero') and gen.is_zero):
            return [True, True]
        if gen == 1 or (hasattr(gen, 'is_one') and gen.is_one):
            return [True, True]
    except Exception:
        pass

    # Check if the witness is a fractional ideal (e.g., 1/2 in ZZ)
    # Fractional ideals are not primary (not integral) but can be powers of prime ideals.
    try:
        if isinstance(gen, sympy.Rational) and not gen.is_integer:
            num = gen.p
            den = gen.q
            factors_num = sympy.factorint(abs(num))
            factors_den = sympy.factorint(abs(den))
            # It is a power of a single prime ideal iff exactly one prime divides the numerator or denominator
            if len(factors_num) + len(factors_den) == 1:
                return [True, True]
            else:
                return [True, False]
    except Exception:
        pass

    # Standard integer ideal case in ZZ
    try:
        n = int(gen)
        h1 = True
        n = abs(n)
        
        if n == 0:
            is_prim = True
            is_pow = False
        elif n == 1:
            is_prim = False
            is_pow = True
        else:
            factors = sympy.factorint(n)
            # In ZZ, an ideal (n) is primary iff n is a prime power
            is_prim = (len(factors) == 1)
            # In ZZ, an ideal (n) is a power of a prime ideal iff n is a prime power
            is_pow = (len(factors) == 1)
            
        iff_holds = (is_prim == is_pow)
        neg_q = not iff_holds
        return [h1, neg_q]
    except Exception:
        pass

    return [False, False]