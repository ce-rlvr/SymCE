import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: D is a divisible abelian group",
    "¬Q: D ⊗ T is not the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_n(G):
    if not isinstance(G, str): 
        return None
    G = G.strip().upper()
    if G.startswith("Z_"): 
        try: return int(G[2:])
        except: pass
    if G.startswith("Z") and len(G) > 1 and G[1:].isdigit(): 
        try: return int(G[1:])
        except: pass
    if G.startswith("Z/") and G.endswith("Z"):
        try: return int(G[2:-1])
        except: pass
    return None

def is_divisible(G):
    if isinstance(G, str):
        G_str = G.strip().upper()
        if G_str in ["Q", "R", "C", "Q/Z", "R/Z", "0"]:
            return True
        if G_str == "Z":
            return False
        if get_n(G_str) is not None:
            return False
    if G == sympy.S.Reals or G == sympy.S.Rationals or G == sympy.S.Complexes:
        return True
    if G == sympy.S.Integers:
        return False
    return False

def tensor_trivial(A, B):
    def to_str(G):
        if G == sympy.S.Reals: return "R"
        if G == sympy.S.Rationals: return "Q"
        if G == sympy.S.Complexes: return "C"
        if G == sympy.S.Integers: return "Z"
        if isinstance(G, str): return G.strip().upper()
        return str(G).strip().upper()
        
    A_str = to_str(A)
    B_str = to_str(B)
    
    if A_str == "0" or B_str == "0":
        return True
        
    divisible_torsion = ["Q/Z", "R/Z"]
    divisible_torsion_free = ["Q", "R", "C"]
    torsion = ["Q/Z", "R/Z"]
    
    def is_torsion(G):
        if G in torsion: return True
        if get_n(G) is not None: return True
        return False
        
    def is_div(G):
        return G in divisible_torsion or G in divisible_torsion_free
        
    if is_div(A_str) and is_torsion(B_str): return True
    if is_div(B_str) and is_torsion(A_str): return True
    
    if A_str in divisible_torsion_free and B_str in divisible_torsion_free: return False
    
    if A_str in divisible_torsion_free and B_str == "Z": return False
    if B_str in divisible_torsion_free and A_str == "Z": return False
    
    if A_str in divisible_torsion and B_str == "Z": return False
    if B_str in divisible_torsion and A_str == "Z": return False
    
    if A_str == "Z" and B_str == "Z": return False
    
    if A_str == "Z" and is_torsion(B_str): return False
    if B_str == "Z" and is_torsion(A_str): return False
    
    n = get_n(A_str)
    m = get_n(B_str)
    if n is not None and m is not None:
        return math.gcd(n, m) == 1
        
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            D = witness.get("D")
            T = witness.get("T")
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            D, T = witness
        else:
            return [False, False]
            
        h1 = is_divisible(D)
        neg_q = not tensor_trivial(D, T)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]