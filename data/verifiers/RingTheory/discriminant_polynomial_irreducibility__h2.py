import sympy
from sympy import Symbol, symbols, Poly, Integer

# Top-level setup for witness expressions
x = Symbol('x')
a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10 = symbols('a0:11')

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: a_0, ..., a_n are algebraically independent over K",
    "¬Q: The discriminant polynomial is not irreducible"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        h1 = False
        h2 = False
        neg_q = False
        
        # Determine n and the discriminant based on the type of witness
        if isinstance(witness, int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            n = int(witness)
            h1 = (n >= 0)
            h2 = (n >= 0)
            if not (h1 and h2):
                return [False, False, False]
            
            var_x = Symbol('x')
            A = symbols(f'a0:{n+1}')
            f = sum(A[i] * var_x**i for i in range(n+1))
            
            if n <= 1:
                disc = Integer(1)
            else:
                disc = sympy.discriminant(f, var_x)
                
        elif isinstance(witness, sympy.Expr):
            var_x = Symbol('x')
            if var_x in witness.free_symbols:
                f_poly = Poly(witness, var_x)
                n = f_poly.degree()
                coeffs = f_poly.all_coeffs()
            else:
                n = 0
                coeffs = [witness]
                
            h1 = True
            # Check if coefficients are independent symbols
            if all(isinstance(c, Symbol) for c in coeffs) and len(set(coeffs)) == len(coeffs):
                h2 = True
            else:
                h2 = False
                
            if n <= 1:
                disc = Integer(1)
            else:
                disc = sympy.discriminant(witness, var_x)
                
        elif isinstance(witness, (list, tuple)):
            if all(isinstance(c, Symbol) for c in witness):
                n = len(witness) - 1
                h1 = True
                h2 = len(set(witness)) == len(witness)
                var_x = Symbol('x')
                f = sum(c * var_x**i for i, c in enumerate(witness))
                if n <= 1:
                    disc = Integer(1)
                else:
                    disc = sympy.discriminant(f, var_x)
            else:
                # Fallback if witness is a tuple like (K, n)
                n = int(witness[-1])
                h1 = (n >= 0)
                h2 = (n >= 0)
                var_x = Symbol('x')
                A = symbols(f'a0:{n+1}')
                f = sum(A[i] * var_x**i for i in range(n+1))
                if n <= 1:
                    disc = Integer(1)
                else:
                    disc = sympy.discriminant(f, var_x)
        else:
            n = int(witness)
            h1 = (n >= 0)
            h2 = (n >= 0)
            if not (h1 and h2):
                return [False, False, False]
            
            var_x = Symbol('x')
            A = symbols(f'a0:{n+1}')
            f = sum(A[i] * var_x**i for i in range(n+1))
            
            if n <= 1:
                disc = Integer(1)
            else:
                disc = sympy.discriminant(f, var_x)
                
        # Check if the discriminant is irreducible
        if disc.is_number:
            is_irred = False
        else:
            _, factors = sympy.factor_list(disc)
            # Irreducible if there is exactly one factor and its multiplicity is 1
            if len(factors) == 1 and factors[0][1] == 1:
                is_irred = True
            else:
                is_irred = False
                
        neg_q = not is_irred
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]