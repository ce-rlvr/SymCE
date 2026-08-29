import sympy
from sympy import symbols, QQ, ZZ
from sympy.polys.polytools import groebner, reduced
from sympy.ntheory import factorint

# Standard symbols that might be used in the witness
x, y, z, t = symbols('x y z t')

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # Pre-process witness if it's an Ideal object
        if hasattr(witness, 'gens'):
            witness = list(witness.gens)
            
        # Pre-process witness if it's a tuple of (Ring, Ideal)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I_data = witness
            if hasattr(R, '__str__') and 'ZZ' in str(R):
                if isinstance(I_data, (list, tuple)) and len(I_data) == 1:
                    witness = I_data[0]
                else:
                    witness = I_data
            else:
                if isinstance(I_data, (int, sympy.Integer)):
                    witness = I_data
                elif isinstance(I_data, (list, tuple)):
                    witness = I_data
                elif hasattr(I_data, 'gens'):
                    witness = list(I_data.gens)
                else:
                    witness = [I_data]
                    
        # Pre-process witness if it's a single polynomial
        if hasattr(witness, 'free_symbols'):
            witness = [witness]

        # Case 1: witness is an integer n (representing ideal nZ in Z)
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            h1 = True  # Z is a commutative Noetherian ring
            if n != 0 and abs(n) != 1:
                factors = factorint(abs(n))
                if len(factors) > 1:
                    neg_q = True
            return [h1, neg_q]
            
        # Case 2: witness is a tuple (gens, a, b) demonstrating a*b in I, a not in I, b not in rad(I)
        if isinstance(witness, tuple) and len(witness) == 3:
            gens, a, b = witness
            
            # Subcase 2a: Integer ideal
            if isinstance(gens, (int, sympy.Integer)):
                n = int(gens)
                h1 = True
                if n != 0 and abs(n) != 1:
                    if (a * b) % n == 0 and a % n != 0:
                        factors = factorint(abs(n))
                        b_in_rad = all(b % p == 0 for p in factors)
                        if not b_in_rad:
                            neg_q = True
                return [h1, neg_q]
                
            # Subcase 2b: Polynomial ideal
            if isinstance(gens, (list, tuple)):
                if not gens:
                    return [True, False]
                h1 = True  # Polynomial ring over a field is commutative Noetherian
                free_syms = set()
                for poly in gens:
                    if hasattr(poly, 'free_symbols'):
                        free_syms.update(poly.free_symbols)
                if hasattr(a, 'free_symbols'): free_syms.update(a.free_symbols)
                if hasattr(b, 'free_symbols'): free_syms.update(b.free_symbols)
                
                syms = list(free_syms) if free_syms else [x, y, z]
                t_sym = sympy.Symbol('t_dummy_var')
                while t_sym in syms:
                    t_sym = sympy.Symbol(t_sym.name + '_')
                
                G = groebner(gens, *syms)
                G_list = list(G)
                if reduced(a*b, G_list, *syms)[1] == 0 and reduced(a, G_list, *syms)[1] != 0:
                    # Rabinowitsch trick to check if b is in the radical of I
                    G_rad = groebner(list(gens) + [1 - t_sym*b], *(syms + [t_sym]))
                    if list(G_rad) != [1]:
                        neg_q = True
                return [h1, neg_q]
                
        # Case 3: witness is a list of polynomials (we search for a and b)
        if isinstance(witness, (list, tuple)):
            gens = witness
            if not gens:
                return [True, False]
            h1 = True
            free_syms = set()
            for poly in gens:
                if hasattr(poly, 'free_symbols'):
                    free_syms.update(poly.free_symbols)
            
            syms = list(free_syms) if free_syms else [x, y, z]
            t_sym = sympy.Symbol('t_dummy_var')
            while t_sym in syms:
                t_sym = sympy.Symbol(t_sym.name + '_')
            
            G = groebner(gens, *syms)
            G_list = list(G)
            
            # Generate simple candidates for a and b
            candidates = list(syms)
            for s1 in syms:
                for s2 in syms:
                    candidates.append(s1 * s2)
            
            for a_cand in candidates:
                for b_cand in candidates:
                    if reduced(a_cand*b_cand, G_list, *syms)[1] == 0 and reduced(a_cand, G_list, *syms)[1] != 0:
                        G_rad = groebner(list(gens) + [1 - t_sym*b_cand], *(syms + [t_sym]))
                        if list(G_rad) != [1]:
                            neg_q = True
                            return [h1, neg_q]
            return [h1, neg_q]
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: I is not a primary ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1