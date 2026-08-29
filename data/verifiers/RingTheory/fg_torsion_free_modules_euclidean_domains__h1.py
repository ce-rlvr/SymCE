import sympy
from sympy import symbols, ZZ, QQ, Matrix

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "Finitely generated torsion-free modules over any ring are free."
    (The dropped hypothesis was that the ring is a Euclidean domain / PID).
    
    The witness is expected to be a list of generators for an ideal in a 
    polynomial ring (like ZZ[x] or QQ[x, y]), representing a module over that ring.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, str):
            return [False, False, False]
            
        if isinstance(witness, sympy.Matrix):
            if witness.rows == 1 or witness.cols == 1:
                witness = list(witness)
            else:
                return [False, False, False]
                
        gens = None
        explicit_domain = None
        
        if isinstance(witness, dict):
            gens = witness.get('gens', witness.get('generators', None))
            ring = witness.get('ring', None)
            if ring is not None:
                if hasattr(ring, 'domain'):
                    explicit_domain = ring.domain
                elif type(ring).__module__.startswith('sympy.polys.domains'):
                    explicit_domain = ring
                    
        elif isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], (list, tuple)):
                gens = witness[0]
                ring = witness[1]
            else:
                gens = witness[1]
                ring = witness[0]
                
            if hasattr(ring, 'domain'):
                explicit_domain = ring.domain
            elif type(ring).__module__.startswith('sympy.polys.domains'):
                explicit_domain = ring

        if gens is None:
            if isinstance(witness, (list, tuple)):
                gens = witness
            elif hasattr(witness, '__iter__'):
                gens = list(witness)
            else:
                return [False, False, False]
                
        if not isinstance(gens, (list, tuple)) or len(gens) == 0:
            return [False, False, False]
            
        exprs = [sympy.nsimplify(sympy.sympify(g)) for g in gens]
        
        # H1: M is a finitely generated module over R
        # A finite list of generators trivially defines a finitely generated module (ideal).
        h1 = True
        
        # H2: M is a torsion-free module
        # We assume the module is an ideal in the polynomial ring over ZZ or QQ.
        # Polynomial rings over ZZ or QQ are integral domains, so their ideals are torsion-free.
        h2 = True
        
        # neg_Q: M is not a free module
        # An ideal in an integral domain is free if and only if it is principal.
        # It is principal if and only if the GCD of its generators is contained in the ideal.
        if all(e == 0 for e in exprs):
            # The zero ideal is free
            neg_q = False
        else:
            free_symbols = set()
            for e in exprs:
                if hasattr(e, 'free_symbols'):
                    free_symbols.update(e.free_symbols)
            vars = sorted(list(free_symbols), key=lambda s: s.name)
            
            if len(vars) == 0:
                # Over ZZ or QQ (which are PIDs), all ideals are principal and thus free.
                neg_q = False
            else:
                if explicit_domain is not None:
                    domain = explicit_domain
                else:
                    # Auto-detect domain: use ZZ if all coefficients are integers, else QQ
                    domain = sympy.ZZ
                    for e in exprs:
                        try:
                            poly = sympy.Poly(e, *vars)
                            if not all(a.is_integer for a in poly.coeffs()):
                                domain = sympy.QQ
                                break
                        except Exception:
                            domain = sympy.QQ
                            break
                
                # Compute the greatest common divisor of the generators
                d = exprs[0]
                for e in exprs[1:]:
                    d = sympy.gcd(d, e)
                
                # Check if the GCD is in the ideal using Groebner bases
                gb = sympy.groebner(exprs, *vars, domain=domain)
                _, rem = sympy.reduced(d, gb, *vars, domain=domain)
                
                is_principal = (rem == 0)
                neg_q = not is_principal
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is a finitely generated module over R",
    "H_2: M is a torsion-free module",
    "¬Q: M is not a free module"
]

N_HYP = 2
NEG_Q_INDEX = 2