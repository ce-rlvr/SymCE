import sympy
from sympy import groebner, reduced

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard variables for constructing polynomial rings and quotient rings.
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the conjecture.
    The witness is expected to be a dictionary defining a quotient ring R = QQ[vars] / I,
    a prime element p, and an element a such that (p) \subsetneq (a) \subsetneq R.
    
    Expected format:
    {
        'vars': (x, y, z),       # Tuple of variables
        'I': [x*(1 - y*z)],      # Generators of the ideal I
        'p': x,                  # The prime element p
        'a': y                   # The element a generating a strictly larger proper principal ideal
    }
    """
    try:
        if not isinstance(witness, dict):
            return [False, False]
            
        vars = witness.get('vars')
        I = witness.get('I')
        p = witness.get('p')
        a = witness.get('a')
        
        if vars is None or I is None or p is None or a is None:
            return [False, False]
            
        if not isinstance(vars, (list, tuple)):
            vars = [vars]
            
        if not isinstance(I, (list, tuple)):
            I = [I]
            
        I_gens = I if I else [sympy.S(0)]
        
        # H_1: p is a prime element in R
        # 1. p is irreducible in QQ[vars] (so (p) is a prime ideal in QQ[vars])
        factors = sympy.factor_list(p)
        is_irred = len(factors[1]) == 1 and factors[1][0][1] == 1
        
        # 2. I is contained in (p). This ensures R/(p) = QQ[vars]/(p), an integral domain.
        I_in_p = all(reduced(gen, [p], *vars, domain='QQ')[1] == 0 for gen in I_gens)
        
        # 3. p is not zero in R (p \notin I)
        G_I = list(groebner(I_gens, *vars, domain='QQ'))
        p_in_I = reduced(p, G_I, *vars, domain='QQ')[1] == 0
        
        # 4. p is not a unit in R (1 \notin I + (p))
        G_Ip = list(groebner(I_gens + [p], *vars, domain='QQ'))
        unit_in_Ip = reduced(1, G_Ip, *vars, domain='QQ')[1] == 0
        
        h1_ok = bool(is_irred and I_in_p and not p_in_I and not unit_in_Ip)
        
        # ¬Q: (p) is not maximal among proper principal ideals
        # We check if there exists 'a' such that (p) \subsetneq (a) \subsetneq R
        
        # 1. (p) \subseteq (a) in R  =>  p \in (a) + I
        G_a = list(groebner(I_gens + [a], *vars, domain='QQ'))
        p_in_a = reduced(p, G_a, *vars, domain='QQ')[1] == 0
        
        # 2. (p) \neq (a) in R  =>  a \notin (p) + I
        a_in_p = reduced(a, G_Ip, *vars, domain='QQ')[1] == 0
        
        # 3. (a) \neq R  =>  1 \notin (a) + I
        unit_in_a = reduced(1, G_a, *vars, domain='QQ')[1] == 0
        
        neg_q_ok = bool(p_in_a and not a_in_p and not unit_in_a)
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: p is a prime element in R",
    "¬Q: (p) is not maximal among proper principal ideals"
]

N_HYP = 1
NEG_Q_INDEX = 1