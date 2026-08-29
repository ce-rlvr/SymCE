import sympy
import itertools
import functools
import math

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: The equivalence (I is primary iff every zero divisor in R/I is nilpotent) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If I is a proper ideal of R, then I is a primary ideal if and only if 
    every zero divisor in the quotient ring R/I is nilpotent."
    (The dropped hypothesis is that R is a commutative ring).
    
    The witness can be:
      - A dictionary with keys: 'elements', 'add', 'mult', 'zero', 'I'
      - A tuple (elements, I) where elements support + and * operators.
    """
    try:
        if isinstance(witness, dict):
            elements = witness['elements']
            
            _add = witness['add']
            if callable(_add):
                def add(x, y): return _add(x, y)
            else:
                def add(x, y): return _add[x][y]
                
            _mult = witness['mult']
            if callable(_mult):
                def mult(x, y): return _mult(x, y)
            else:
                def mult(x, y): return _mult[x][y]
                
            zero = witness['zero']
            I = witness['I']
        else:
            elements, I = witness
            def add(x, y): return x + y
            def mult(x, y): return x * y
            
            zero = None
            for e in elements:
                if all((add(e, x) == x) for x in elements):
                    zero = e
                    break
            if zero is None:
                return [False, False]

        def contains(lst, item):
            return any(x == item for x in lst)

        # H1: I is a proper ideal of R
        h1 = True
        if not contains(I, zero):
            h1 = False
        else:
            # Check closure under addition
            for x in I:
                for y in I:
                    if not contains(I, add(x, y)):
                        h1 = False
            # Check absorption under multiplication
            for r in elements:
                for x in I:
                    if not contains(I, mult(r, x)):
                        h1 = False
                    if not contains(I, mult(x, r)):
                        h1 = False
            # Check properness
            if len(I) == len(elements):
                h1 = False

    except Exception:
        return [False, False]

    try:
        # Evaluate if I is a primary ideal.
        # In non-commutative rings, the element-wise definition can be left-primary or right-primary.
        # We check both standard interpretations.
        is_left_prim = True
        is_right_prim = True
        for a in elements:
            for b in elements:
                if contains(I, mult(a, b)):
                    a_in_I = contains(I, a)
                    b_in_I = contains(I, b)
                    
                    # Check if b is nilpotent in R/I
                    curr = b
                    b_nilp = False
                    for _ in range(len(elements) + 1):
                        if contains(I, curr):
                            b_nilp = True
                            break
                        curr = mult(curr, b)
                        
                    # Check if a is nilpotent in R/I
                    curr = a
                    a_nilp = False
                    for _ in range(len(elements) + 1):
                        if contains(I, curr):
                            a_nilp = True
                            break
                        curr = mult(curr, a)
                        
                    if not (a_in_I or b_nilp):
                        is_left_prim = False
                    if not (b_in_I or a_nilp):
                        is_right_prim = False

        # Evaluate if every zero divisor in R/I is nilpotent
        every_zd_is_nilpotent = True
        for x in elements:
            if contains(I, x):
                continue
            
            # Check if x + I is a zero divisor in R/I
            is_zd = False
            for y in elements:
                if not contains(I, y):
                    if contains(I, mult(x, y)) or contains(I, mult(y, x)):
                        is_zd = True
                        break
                        
            if is_zd:
                # Check if x + I is nilpotent in R/I
                curr = x
                is_nilp = False
                for _ in range(len(elements) + 1):
                    if contains(I, curr):
                        is_nilp = True
                        break
                    curr = mult(curr, x)
                if not is_nilp:
                    every_zd_is_nilpotent = False
                    break

        # The conjecture claims: I is primary iff every zero divisor in R/I is nilpotent.
        # If the witness is a counterexample, this equivalence must fail.
        # We consider the conjecture to fail if the equivalence breaks under either 
        # the left-primary or right-primary interpretation.
        neg_q = (is_left_prim != every_zd_is_nilpotent) or (is_right_prim != every_zd_is_nilpotent)
        
    except Exception:
        neg_q = False

    return [h1, neg_q]