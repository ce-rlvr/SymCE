import sympy
from sympy import symbols, Poly, ZZ, QQ
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
from functools import reduce

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans corresponding to the remaining hypotheses and the negated conclusion.
    """
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        # If witness is a dictionary
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative_ring', False))
            h2 = bool(witness.get('are_comaximal_in_Rx', False))
            h3 = bool(witness.get('a_in_R', False))
            neg_q = not bool(witness.get('eval_ideals_comaximal', True))
            return [h1, h2, h3, neg_q]
            
        # If witness is a custom object with methods
        if hasattr(witness, 'is_commutative_ring'):
            h1 = bool(witness.is_commutative_ring())
            h2 = bool(witness.are_comaximal_in_Rx())
            h3 = bool(witness.a_in_R())
            neg_q = not bool(witness.eval_ideals_comaximal())
            return [h1, h2, h3, neg_q]
            
        # If witness is a tuple (R, I, J, a)
        if isinstance(witness, tuple) and len(witness) == 4:
            R, I, J, a = witness
            
            if not isinstance(I, (list, tuple, set)): I = [I]
            if not isinstance(J, (list, tuple, set)): J = [J]
            
            # H1: R is a commutative ring
            try:
                h1 = getattr(R, 'is_commutative', True)
            except Exception:
                h1 = False
                
            # H2: I and J are comaximal in the polynomial ring
            try:
                if hasattr(I, 'is_comaximal'):
                    h2 = bool(I.is_comaximal(J))
                else:
                    gens = list(I) + list(J)
                    try:
                        gb = sympy.groebner(gens, domain=R)
                        h2 = (list(gb) == [1])
                    except Exception:
                        if 1 in gens or sympy.core.numbers.One() in gens:
                            h2 = True
                        else:
                            h2 = False
            except Exception:
                h2 = False
                
            # H3: a is an element of R
            try:
                if hasattr(R, '__contains__'):
                    h3 = a in R
                else:
                    h3 = True
            except Exception:
                h3 = False
                
            # neg_Q: I(a) and J(a) are not comaximal in R
            try:
                if hasattr(I, 'evaluate'):
                    Ia = I.evaluate(a)
                    Ja = J.evaluate(a)
                    neg_q = not bool(Ia.is_comaximal(Ja))
                else:
                    x_sym = sympy.symbols('x')
                    Ia = [f.subs(x_sym, a) if hasattr(f, 'subs') else f for f in I]
                    Ja = [g.subs(x_sym, a) if hasattr(g, 'subs') else g for g in J]
                    
                    if R == sympy.ZZ:
                        all_evals = [int(val) for val in Ia + Ja]
                        gcd_val = reduce(math.gcd, all_evals)
                        neg_q = (gcd_val != 1 and gcd_val != -1)
                    else:
                        gb = sympy.groebner(Ia + Ja, domain=R)
                        neg_q = not (list(gb) == [1])
            except Exception:
                neg_q = False
                
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are comaximal in the polynomial ring",
    "H_3: a is an element of R",
    "¬Q: The evaluation ideals I(a) and J(a) are not comaximal in R"
]

N_HYP = 3
NEG_Q_INDEX = 3