import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple (R, I, J, x) where:
      - R is a list of elements representing the ring.
      - I is a list of elements representing the ideal I.
      - J is a list of elements representing the ideal J.
      - x is an element of R.
    """
    try:
        R, I, J, x_elem = witness
    except Exception:
        return [False, False, False]

    def check_H1():
        if not isinstance(R, list) or not isinstance(I, list) or not isinstance(J, list):
            return False
        if not R: 
            return False
        
        # Check if R is closed under addition and multiplication
        for a in R:
            for b in R:
                if (a + b) not in R: return False
                if (a * b) not in R: return False
                
        # Check if I is a two-sided ideal
        if not I: return False
        for i in I:
            if i not in R: return False
            for j in I:
                if (i + j) not in I: return False
            for r in R:
                if (r * i) not in I: return False
                if (i * r) not in I: return False
                
        # Check if J is a two-sided ideal
        if not J: return False
        for j in J:
            if j not in R: return False
            for k in J:
                if (j + k) not in J: return False
            for r in R:
                if (r * j) not in J: return False
                if (j * r) not in J: return False
                
        # Check if I and J are comaximal (I + J == R)
        for r in R:
            found = False
            for i in I:
                for j in J:
                    if (i + j) == r:
                        found = True
                        break
                if found:
                    break
            if not found:
                return False
            
        return True

    try:
        h1 = check_H1()
    except Exception:
        h1 = False

    try:
        h2 = x_elem in R
    except Exception:
        h2 = False

    def check_neg_Q():
        # Intersection of I and J
        I_cap_J = [elem for elem in I if elem in J]
        
        def is_nilpotent_mod(elem, ideal):
            curr = elem
            # In a finite ring of size |R|, if an element is nilpotent modulo an ideal,
            # its sequence of powers must enter the ideal within |R| steps.
            for _ in range(len(R) + 1):
                if curr in ideal:
                    return True
                curr = curr * elem
            return False
            
        nil_I = is_nilpotent_mod(x_elem, I)
        nil_J = is_nilpotent_mod(x_elem, J)
        nil_I_cap_J = is_nilpotent_mod(x_elem, I_cap_J)
        
        # The conclusion is: x is nilpotent in R/(I \cap J) iff x is nilpotent in R/I and R/J
        # We return True if the conclusion FAILS (i.e., the equivalence does not hold)
        return not (nil_I_cap_J == (nil_I and nil_J))

    try:
        neg_q = check_neg_Q()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are comaximal ideals of R",
    "H_2: x is an element of R",
    "¬Q: The equivalence of nilpotency in R/(I \\cap J) and in R/I and R/J fails"
]

N_HYP = 2
NEG_Q_INDEX = 2