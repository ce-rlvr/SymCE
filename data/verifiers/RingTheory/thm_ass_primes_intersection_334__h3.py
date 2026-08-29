import sympy
import math
from sympy import symbols, ZZ, QQ

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "The set of associated primes Ass(R/(I \cap J)) is a subset of Ass(R/I) \cup Ass(R/J)"
    
    Remaining hypotheses:
      H_1: R is a Noetherian ring
      H_2: I is an ideal in R
    """
    h1, h2, neg_q = False, False, False
    
    # 1. Try dictionary interface (mock object)
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_Noetherian', False))
            h2 = bool(witness.get('is_ideal_I', False))
            ass_int = set(witness.get('Ass_intersection', []))
            ass_I = set(witness.get('Ass_I', []))
            ass_J = set(witness.get('Ass_J', []))
            neg_q = not ass_int.issubset(ass_I.union(ass_J))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. Try object with methods/properties (mock object)
    try:
        if hasattr(witness, 'Ass_intersection') or hasattr(witness, 'Ass_I_cap_J'):
            h1_attr = getattr(witness, 'is_Noetherian', getattr(witness, 'R_is_Noetherian', False))
            h1 = bool(h1_attr() if callable(h1_attr) else h1_attr)
            
            h2_attr = getattr(witness, 'is_ideal_I', getattr(witness, 'I_is_ideal', False))
            h2 = bool(h2_attr() if callable(h2_attr) else h2_attr)
            
            ass_int_attr = getattr(witness, 'Ass_intersection', getattr(witness, 'Ass_I_cap_J', []))
            ass_int = set(ass_int_attr() if callable(ass_int_attr) else ass_int_attr)
            
            ass_I_attr = getattr(witness, 'Ass_I', [])
            ass_I = set(ass_I_attr() if callable(ass_I_attr) else ass_I_attr)
            
            ass_J_attr = getattr(witness, 'Ass_J', [])
            ass_J = set(ass_J_attr() if callable(ass_J_attr) else ass_J_attr)
            
            neg_q = not ass_int.issubset(ass_I.union(ass_J))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try tuple (R, I, J) or (I, J) for R = ZZ
    # In this interpretation, J is a subset (not an ideal), and R/S means R/<S>.
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                R, I, J = witness
            elif len(witness) == 2:
                R = 'ZZ'
                I, J = witness
            else:
                R, I, J = None, None, None
                
            if R == 'ZZ' or str(R) == 'ZZ' or R == sympy.ZZ:
                h1 = True
                h2 = isinstance(I, (int, sympy.Integer))
                
                if isinstance(J, (int, sympy.Integer)):
                    J_list = [int(J)]
                else:
                    J_list = [int(val) for val in J]
                    
                I_val = int(I)
                
                if I_val == 0:
                    I_cap_J = [val for val in J_list if val == 0]
                else:
                    I_cap_J = [val for val in J_list if val % I_val == 0]
                
                def get_gen(lst):
                    if not lst: return 0
                    g = abs(lst[0])
                    for val in lst[1:]:
                        g = math.gcd(g, abs(val))
                    return g
                    
                gen_int = get_gen(I_cap_J)
                gen_J = get_gen(J_list)
                
                def get_ass(n):
                    n = abs(n)
                    if n == 0: return {0}
                    if n == 1: return set()
                    return set(sympy.primefactors(n))
                    
                ass_int = get_ass(gen_int)
                ass_I = get_ass(I_val)
                ass_J = get_ass(gen_J)
                
                neg_q = not ass_int.issubset(ass_I.union(ass_J))
                return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: I is an ideal in R",
    "¬Q: Ass(R/(I \\cap J)) is not a subset of Ass(R/I) \\cup Ass(R/J)"
]

N_HYP = 2
NEG_Q_INDEX = 2