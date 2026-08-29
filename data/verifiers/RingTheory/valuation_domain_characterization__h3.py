import sympy
from sympy.abc import x, y, z
from sympy import ZZ, QQ

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture.
    The witness should be a SymPy domain (e.g., ZZ, QQ.poly_ring(x)).
    """
    # H_1: R is an integral domain
    try:
        # In SymPy, domains that have a fraction field are integral domains.
        # We also ensure it's not the trivial ring (zero != one).
        h1 = hasattr(witness, 'get_field') and witness.zero != witness.one
    except Exception:
        h1 = False

    # H_2: K is the field of fractions of R
    try:
        # This hypothesis simply establishes K as the fraction field of R.
        # It holds as long as R has a well-defined field of fractions.
        h2 = hasattr(witness, 'get_field')
    except Exception:
        h2 = False

    # ¬Q: The ideals of R are not totally ordered by inclusion (R is not a valuation domain)
    # A valuation domain requires that for any a, b in R, either a divides b or b divides a.
    # We search for a pair of elements (a, b) such that a does not divide b AND b does not divide a.
    neg_q = False
    try:
        elements = []
        
        # Generate some test elements from the ring
        try:
            one = witness.one
            elements.append(one + one)
            elements.append(one + one + one)
            elements.append(one + one + one + one + one)
        except Exception:
            pass
            
        if hasattr(witness, 'gens') and witness.gens:
            for g in witness.gens:
                elements.append(g)
                try:
                    elements.append(g + witness.one)
                except Exception:
                    pass
                    
        # Filter out zero and duplicates
        try:
            zero = witness.zero
            unique_elements = []
            for e in elements:
                if e != zero and e not in unique_elements:
                    unique_elements.append(e)
            elements = unique_elements
        except Exception:
            pass

        # Check for the valuation domain property
        for a in elements:
            for b in elements:
                if a == b:
                    continue
                
                # Check if a divides b
                try:
                    witness.exquo(b, a)
                    a_div_b = True
                except Exception:
                    a_div_b = False
                    
                # Check if b divides a
                try:
                    witness.exquo(a, b)
                    b_div_a = True
                except Exception:
                    b_div_a = False
                    
                # If neither divides the other, the ideals (a) and (b) are not comparable
                if not a_div_b and not b_div_a:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "¬Q: The ideals of R are not totally ordered by inclusion (R is not a valuation domain)"
]

N_HYP = 2
NEG_Q_INDEX = 2