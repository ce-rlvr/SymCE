import sympy
import math
import itertools

# Top-level setup: named object bindings that the witness expression may reference
x, n = sympy.symbols('x n')
oo = sympy.oo
pi = sympy.pi

def is_euler_seq(seq):
    """
    Checks if the given sequence matches the Euler numbers (either with alternating signs or absolute values).
    The Euler numbers defined by the Taylor series of sec(x) are:
    E_0=1, E_1=0, E_2=-1 (or 1), E_3=0, E_4=5, E_5=0, E_6=-61 (or 61), etc.
    """
    if not seq: 
        return False
    try:
        n_terms = min(len(seq), 10)
        if n_terms < 4:
            return False
        match_reg = True
        match_abs = True
        for i in range(n_terms):
            val = sympy.sympify(seq[i])
            e_val = sympy.euler(i)
            if val != e_val: 
                match_reg = False
            if val != abs(e_val): 
                match_abs = False
        return match_reg or match_abs
    except Exception:
        return False

def check_radius(radius):
    """
    Checks if the radius of convergence is exactly pi/2.
    """
    if radius is None:
        return False
    try:
        if hasattr(radius, 'evalf'):
            val = float(radius.evalf())
        else:
            val = float(radius)
        return abs(val - math.pi / 2) < 1e-7
    except Exception:
        return False

def analyze_witness(witness):
    """
    Attempts to extract the sequence of coefficients and the radius of convergence from the witness.
    The witness could be a sympy.Sum, a dictionary, an object with attributes, or a tuple.
    """
    seq = None
    radius = None
    
    if isinstance(witness, dict):
        if 'sequence' in witness:
            seq = witness['sequence']
        if 'radius' in witness:
            radius = witness['radius']
        elif 'radius_of_convergence' in witness:
            radius = witness['radius_of_convergence']
            
    elif hasattr(witness, 'sequence') and (hasattr(witness, 'radius') or hasattr(witness, 'radius_of_convergence')):
        seq = witness.sequence
        radius = getattr(witness, 'radius', getattr(witness, 'radius_of_convergence', None))
        
    elif isinstance(witness, (tuple, list)) and len(witness) == 2:
        if isinstance(witness[0], (list, tuple)) or callable(witness[0]):
            seq = witness[0]
            radius = witness[1]
            
    elif isinstance(witness, sympy.Sum):
        term = witness.args[0]
        sum_var = witness.args[1][0]
        free = term.free_symbols - {sum_var}
        if len(free) == 1:
            var_x = list(free)[0]
            try:
                # Evaluate the first 11 terms of the sum to extract coefficients
                partial_sum = sum(term.subs(sum_var, i) for i in range(11)).expand()
                c_k_seq = []
                for k in range(11):
                    if k == 0:
                        c_k_seq.append(partial_sum.subs(var_x, 0))
                    else:
                        c_k_seq.append(partial_sum.coeff(var_x, k))
                
                # Check if it's the Ordinary Generating Function (OGF)
                if is_euler_seq(c_k_seq):
                    seq = c_k_seq
                    radius = 0
                else:
                    # Check if it's the Exponential Generating Function (EGF)
                    e_k_seq = [c_k_seq[k] * math.factorial(k) for k in range(11)]
                    if is_euler_seq(e_k_seq):
                        seq = e_k_seq
                        radius = sympy.pi / 2
            except Exception:
                pass
                
    if callable(seq):
        try:
            seq = [seq(i) for i in range(11)]
        except Exception:
            pass
            
    if hasattr(seq, '__next__') or hasattr(seq, '__iter__'):
        if not isinstance(seq, (list, tuple)):
            try:
                seq = list(itertools.islice(seq, 11))
            except Exception:
                pass
                
    return seq, radius

def conditions(witness) -> list[bool]:
    seq, radius = analyze_witness(witness)
    
    # H_1: The sequence {E_n} represents the Euler numbers
    try:
        h1_ok = is_euler_seq(seq)
    except Exception:
        h1_ok = False
        
    # neg_Q: The radius of convergence of the power series is NOT pi/2
    try:
        if radius is None:
            neg_q_ok = False
        else:
            neg_q_ok = not check_radius(radius)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The sequence represents the Euler numbers",
    "¬Q: The radius of convergence of the power series is not pi/2"
]

N_HYP = 1
NEG_Q_INDEX = 1