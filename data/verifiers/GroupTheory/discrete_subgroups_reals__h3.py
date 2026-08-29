import sympy
from sympy import S, simplify, sympify, sqrt, pi

# Top-level setup
Rationals = S.Rationals
Reals = S.Reals
Integers = S.Integers
Z = S.Integers
Q = S.Rationals
R = S.Reals

CONDITION_LABELS = [
    "H_1: G is a subgroup of R",
    "¬Q: G is not {0} and not isomorphic to Z"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # Check if witness is a known subgroup like Q or R
        if witness in (S.Rationals, S.Reals):
            h1 = True
            neg_q = True
            
        # Check if witness is Z
        elif witness == S.Integers:
            h1 = True
            neg_q = False
            
        # Check if witness is the trivial group
        elif witness == {0} or witness == [0] or witness == (0,):
            h1 = True
            neg_q = False
            
        # Check if witness is a finitely generated subgroup represented by a list/tuple/set of generators
        elif isinstance(witness, (list, tuple, set)):
            gens = list(witness)
            all_real = True
            for g in gens:
                g_sym = sympify(g)
                if not g_sym.is_real:
                    all_real = False
                    break
                    
            if all_real and len(gens) > 0:
                h1 = True
                gens_nonzero = [sympify(g) for g in gens if sympify(g) != 0]
                
                if len(gens_nonzero) == 0:
                    neg_q = False
                elif len(gens_nonzero) == 1:
                    neg_q = False
                else:
                    # For a finitely generated subgroup of R, it is isomorphic to Z iff its rank over Q is 1.
                    # We check if all generators are rational multiples of the first non-zero generator.
                    rank_greater_than_1 = False
                    g0 = gens_nonzero[0]
                    for g in gens_nonzero[1:]:
                        ratio = simplify(g / g0)
                        if ratio.is_rational is False:
                            rank_greater_than_1 = True
                            break
                        elif ratio.is_rational is None:
                            # If SymPy cannot prove it's rational, we assume it's irrational for the counterexample
                            rank_greater_than_1 = True
                            break
                    neg_q = rank_greater_than_1
                    
        # Check if witness is an ImageSet over Integers (e.g., ImageSet(Lambda((x, y), x + y*sqrt(2)), S.Integers, S.Integers))
        elif hasattr(witness, 'base_sets') and hasattr(witness, 'lamda'):
            if all(b == S.Integers for b in witness.base_sets):
                expr = witness.lamda.expr
                vars = witness.lamda.variables
                zero_val = expr.subs({v: 0 for v in vars})
                
                # Must contain 0 when all coefficients are 0 to be a standard subgroup representation
                if zero_val == 0:
                    gens = []
                    for i in range(len(vars)):
                        subs_dict = {v: (1 if j == i else 0) for j, v in enumerate(vars)}
                        gens.append(expr.subs(subs_dict))
                    
                    all_real = True
                    for g in gens:
                        if not g.is_real:
                            all_real = False
                            break
                            
                    if all_real:
                        h1 = True
                        gens_nonzero = [g for g in gens if g != 0]
                        
                        if len(gens_nonzero) == 0:
                            neg_q = False
                        elif len(gens_nonzero) == 1:
                            neg_q = False
                        else:
                            rank_greater_than_1 = False
                            g0 = gens_nonzero[0]
                            for g in gens_nonzero[1:]:
                                ratio = simplify(g / g0)
                                if ratio.is_rational is False:
                                    rank_greater_than_1 = True
                                    break
                                elif ratio.is_rational is None:
                                    rank_greater_than_1 = True
                                    break
                            neg_q = rank_greater_than_1
    except Exception:
        pass

    return [h1, neg_q]