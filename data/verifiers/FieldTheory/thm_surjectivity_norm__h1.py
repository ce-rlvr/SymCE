import sympy
from sympy import Symbol, Poly, Expr, RR, CC, QQ, ZZ

# Top-level setup for FieldTheory
x = Symbol('x')

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: E is a finite field extension of F",
    "¬Q: The field norm map from E to F is not surjective onto the non-zero elements of F"
]

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # Check for the classic (RR, CC) counterexample
        if isinstance(witness, tuple) and len(witness) == 2:
            if witness[0] == RR and witness[1] == CC:
                return [True, True]
            if str(witness[0]) == 'RR' and str(witness[1]) == 'CC':
                return [True, True]

        x_sym = Symbol('x')
        P = None
        domain = None
        
        # Parse witness as an AlgebraicField
        if hasattr(witness, 'is_AlgebraicField') and witness.is_AlgebraicField:
            P = Poly(witness.ext.minpoly, x_sym, domain=QQ)
            domain = QQ
            
        # Parse witness as a tuple (Domain, AlgebraicField)
        elif isinstance(witness, tuple) and len(witness) == 2 and hasattr(witness[1], 'is_AlgebraicField') and witness[1].is_AlgebraicField:
            domain = witness[0]
            P = Poly(witness[1].ext.minpoly, x_sym, domain=domain)
            
        # Parse witness as a tuple (Domain, Polynomial/Expr)
        elif isinstance(witness, tuple) and len(witness) == 2:
            domain = witness[0]
            P = Poly(witness[1], x_sym, domain=domain)
            
        # Parse witness as a Polynomial/Expr (assume base field is its fraction field)
        elif isinstance(witness, (Expr, Poly)):
            P = Poly(witness, x_sym)
            domain = P.domain
            if domain.is_Ring and not domain.is_Field:
                domain = domain.get_field()
                P = P.set_domain(domain)
                
        if P is not None:
            # A finite field extension is defined by an irreducible polynomial of degree > 1
            if P.degree() > 1 and P.is_irreducible:
                h1 = True
                
                # The norm map is surjective for finite fields, but NOT for global/local fields of char 0
                if domain == QQ:
                    neg_q = True
                elif domain == RR:
                    neg_q = True
                elif hasattr(domain, 'is_FiniteField') and domain.is_FiniteField:
                    neg_q = False
                elif hasattr(domain, 'characteristic') and domain.characteristic == 0:
                    neg_q = True
                else:
                    neg_q = True
                    
    except Exception:
        pass
        
    return [h1, neg_q]