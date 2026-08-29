import sympy
from sympy import gcd, groebner, cancel
from sympy.abc import x, y, z

class Module:
    """
    Generic module representation for cases where explicit computation is difficult.
    """
    def __init__(self, is_fg, is_direct_sum_of_free_and_cyclic_torsion):
        self.is_fg = bool(is_fg)
        self.is_direct_sum_of_free_and_cyclic_torsion = bool(is_direct_sum_of_free_and_cyclic_torsion)

class IdealModule:
    """
    Represents an ideal in a polynomial ring R = domain[vars], viewed as a module over R.
    gens: list of generators (SymPy expressions)
    vars: tuple of variables (SymPy symbols)
    domain: string representing the base domain (e.g., 'QQ', 'ZZ')
    """
    def __init__(self, gens, vars, domain='QQ'):
        self.gens = list(gens)
        self.vars = tuple(vars) if isinstance(vars, (list, tuple)) else (vars,)
        self.domain = domain

# Standard counterexample: Ideal (x, y) in QQ[x, y]
# It is finitely generated but not a direct sum of free and cyclic torsion modules.
M_counterexample = IdealModule([x, y], (x, y), 'QQ')

def conditions(witness):
    try:
        if isinstance(witness, Module):
            h1 = witness.is_fg
            neg_q = not witness.is_direct_sum_of_free_and_cyclic_torsion
            return [h1, neg_q]
            
        if isinstance(witness, IdealModule):
            # An ideal given by a finite list of generators is finitely generated
            h1 = True 
            
            gens = witness.gens
            variables = witness.vars
            domain = witness.domain
            
            if not gens:
                is_principal = True
            else:
                g = gens[0]
                for gen in gens[1:]:
                    g = gcd(g, gen)
                
                if g == 0:
                    is_principal = True
                else:
                    reduced_gens = [cancel(gen / g) for gen in gens]
                    try:
                        gb = groebner(reduced_gens, *variables, domain=domain)
                        is_principal = False
                        if len(gb) == 1:
                            basis_elem = gb[0]
                            if basis_elem.is_constant():
                                if str(domain) == 'ZZ':
                                    if abs(basis_elem) == 1:
                                        is_principal = True
                                else:
                                    if basis_elem != 0:
                                        is_principal = True
                    except Exception:
                        is_principal = False
            
            # Since M is an ideal in an integral domain, it is torsion-free.
            # Thus, if it were a direct sum of free and cyclic torsion modules, 
            # the torsion part must be 0, meaning M would be free.
            # An ideal in an integral domain is free if and only if it is principal.
            neg_q = not is_principal
            return [h1, neg_q]
            
    except Exception:
        pass
        
    return [False, False]

CONDITION_LABELS = [
    "H_1: M is a finitely generated module over R",
    "¬Q: M is not isomorphic to the direct sum of a free R-module and a finite number of cyclic torsion R-modules"
]

N_HYP = 1
NEG_Q_INDEX = 1