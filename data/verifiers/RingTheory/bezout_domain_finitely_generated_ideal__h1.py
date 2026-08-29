import sympy
from sympy import isprime

# Top-level setup for common finite rings (represented by their modulus n for Z/nZ)
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture:
    "R is a Bezout domain if and only if every finitely generated ideal of R is a principal ideal."
    
    A Bezout domain is an integral domain where every finitely generated ideal is principal.
    The equivalence fails if a ring has all finitely generated ideals principal, 
    but is not an integral domain (e.g., Z/nZ for composite n > 1).
    """
    try:
        n = None
        
        # Handle integer witnesses representing Z/nZ
        if isinstance(witness, int):
            n = abs(witness)
        elif hasattr(witness, 'is_Integer') and witness.is_Integer:
            n = abs(int(witness))
        # Handle tuple/list of integers representing a product of rings Z/n_i Z
        elif isinstance(witness, (tuple, list)) and all(isinstance(x, int) for x in witness):
            if len(witness) > 1:
                # A product of multiple rings has zero divisors, so it's not an integral domain.
                # However, a finite product of principal ideal rings is a principal ideal ring.
                is_bezout = False
                all_fg_principal = True
                p_iff_q = (is_bezout == all_fg_principal)
                return [not p_iff_q]
            elif len(witness) == 1:
                n = abs(witness[0])
        # Handle string representations like "Z/6Z"
        elif isinstance(witness, str):
            witness_upper = witness.strip().upper()
            if '[' in witness_upper or 'POLY' in witness_upper:
                return [False]
            if witness_upper == 'Z':
                n = 0
            else:
                nums = []
                current_num = ""
                for char in witness_upper:
                    if char.isdigit():
                        current_num += char
                    else:
                        if current_num:
                            nums.append(int(current_num))
                            current_num = ""
                if current_num:
                    nums.append(int(current_num))
                
                if len(nums) == 1:
                    n = nums[0]
                elif len(nums) > 1:
                    # Likely a product of rings, e.g., "Z/2Z x Z/3Z"
                    is_bezout = False
                    all_fg_principal = True
                    p_iff_q = (is_bezout == all_fg_principal)
                    return [not p_iff_q]
        
        if n is not None:
            if n == 0:
                # Z is an integral domain and a PID
                is_bezout = True
                all_fg_principal = True
            elif n == 1:
                # Z/1Z is the zero ring (not an integral domain by convention)
                is_bezout = False
                all_fg_principal = True
            else:
                # Z/nZ is an integral domain iff n is prime.
                # It is always a principal ideal ring.
                is_bezout = isprime(n)
                all_fg_principal = True
            
            p_iff_q = (is_bezout == all_fg_principal)
            return [not p_iff_q]
            
    except Exception:
        pass
    
    return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence 'R is a Bezout domain iff every finitely generated ideal is principal' fails"
]

N_HYP = 0
NEG_Q_INDEX = 0