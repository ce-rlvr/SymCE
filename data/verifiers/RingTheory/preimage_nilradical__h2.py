import sympy

# The witness is expected to be a tuple (n, m, f_dict)
# where n and m are positive integers representing the rings Z/nZ and Z/mZ,
# and f_dict is a dictionary, list, or callable mapping int to int 
# representing the function f: Z/nZ -> Z/mZ.

def conditions(witness) -> list[bool]:
    try:
        n, m, f_dict = witness
        
        # Check that n and m are valid moduli for Z/nZ and Z/mZ
        if not (isinstance(n, int) and n >= 1):
            return [False, False]
        if not (isinstance(m, int) and m >= 1):
            return [False, False]
            
        # Parse the function f
        if isinstance(f_dict, list):
            if len(f_dict) != n:
                return [False, False]
            f_map = {i: f_dict[i] for i in range(n)}
        elif isinstance(f_dict, dict):
            if set(f_dict.keys()) != set(range(n)):
                return [False, False]
            f_map = f_dict
        elif callable(f_dict):
            f_map = {i: int(f_dict(i)) for i in range(n)}
        else:
            return [False, False]
            
        # Check that f maps into Z/mZ
        if not all(isinstance(v, int) and 0 <= v < m for v in f_map.values()):
            return [False, False]
            
        # H_1: R and S are commutative rings
        # Z/nZ and Z/mZ are commutative rings for any integers n, m >= 1.
        h1 = True
        
        # Evaluate the conclusion: 
        # "The preimage of the nilradical of S under f is equal to the radical of the kernel of f."
        
        # Nilradical of S = Z/mZ (elements y such that y^k = 0 for some k >= 1)
        # In Z/mZ, y is nilpotent iff y^m == 0 mod m.
        nil_S = {y for y in range(m) if pow(y, m, m) == 0}
        
        # Preimage of the nilradical of S under f
        pre_nil = {x for x in range(n) if f_map[x] in nil_S}
        
        # Kernel of f (elements x such that f(x) = 0 in S)
        ker_f = {x for x in range(n) if f_map[x] == 0}
        
        # Radical of the kernel of f (elements x such that x^k in ker_f for some k >= 1)
        # In Z/nZ, the sequence x^k is periodic and will hit ker_f within n steps if it ever does.
        rad_ker = {x for x in range(n) if any(pow(x, k, n) in ker_f for k in range(1, n + 1))}
        
        # Negated conclusion: they are NOT equal
        neg_q = (pre_nil != rad_ker)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "¬Q: The preimage of the nilradical of S under f is NOT equal to the radical of the kernel of f"
]

N_HYP = 1
NEG_Q_INDEX = 1