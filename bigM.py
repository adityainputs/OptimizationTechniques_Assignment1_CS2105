import numpy as np

def print_tableau(tableau, iteration):
    print(f"\n--- Iteration {iteration} ---")
    # Formatting to make the tableau look neat in the output
    print(np.array_str(tableau, precision=2, suppress_small=True))

def solve_specific_big_m():
    # M is a very large positive number used as a penalty
    M = 1000.0 
    
    # Variables order: [x1, x2, x3, s1, s2, a1, a2, RHS]
    # Initial Table setup based on standard form:
    # Row 0: x1 - 2x2 + x3 + s1 = 11
    # Row 1: -4x1 + x2 + 2x3 - s2 + a1 = 3
    # Row 2: -2x1 + 0x2 + x3 + a2 = 1
    
    tableau = np.array([
        [ 1.0, -2.0,  1.0,  1.0,  0.0,  0.0,  0.0, 11.0],
        [-4.0,  1.0,  2.0,  0.0, -1.0,  1.0,  0.0,  3.0],
        [-2.0,  0.0,  1.0,  0.0,  0.0,  0.0,  1.0,  1.0],
        [-3.0,  1.0,  1.0,  0.0,  0.0,   M,   M,  0.0] # Initial Objective row for Max Z'
    ])
    
    # Drive out the artificial variables (a1, a2) from the objective row
    # Obj Row = Obj Row - M*(Row 1) - M*(Row 2)
    tableau[3] = tableau[3] - M * tableau[1] - M * tableau[2]
    
    iteration = 0
    print_tableau(tableau, iteration)
    
    while True:
        # Check if optimal (all values in objective row >= 0 for this setup)
        # We look at all columns except the RHS
        if all(tableau[3, :-1] >= -1e-5):
            print("\nOptimal solution found!")
            break
            
        # Entering variable: Most negative value in the objective row
        enter_col = np.argmin(tableau[3, :-1])
        
        # Leaving variable: Minimum positive ratio test (RHS / entering column)
        ratios = []
        for i in range(3): # We have 3 constraint rows
            if tableau[i, enter_col] > 1e-5:
                ratios.append(tableau[i, -1] / tableau[i, enter_col])
            else:
                ratios.append(float('inf'))
                
        leave_row = np.argmin(ratios)
        if ratios[leave_row] == float('inf'):
            print("Unbounded solution.")
            return
            
        # Pivot Operations
        pivot = tableau[leave_row, enter_col]
        tableau[leave_row] = tableau[leave_row] / pivot
        
        # Row operations to make other elements in entering column 0
        for i in range(4): # 3 constraints + 1 objective row
            if i != leave_row:
                tableau[i] = tableau[i] - tableau[i, enter_col] * tableau[leave_row]
                
        iteration += 1
        print_tableau(tableau, iteration)
        
    # Since we maximized Z' = -z, the minimum z is -Z' (the RHS of the objective row)
    min_z = tableau[3, -1]
    print(f"\nOptimal Objective Value (Minimize z): {round(min_z, 2)}")
    print("Check the RHS values in the final tableau to find the values for the basic variables.")

if __name__ == "__main__":
    solve_specific_big_m()