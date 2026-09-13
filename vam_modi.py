import numpy as np

def vam(costs, supply, demand):
    supply_copy = supply.copy().astype(float)
    demand_copy = demand.copy().astype(float)
    allocations = np.zeros(costs.shape)
    
    print("--- Vogel's Approximation Method (VAM) ---")
    while sum(supply_copy) > 0 and sum(demand_copy) > 0:
        # Penalties
        row_penalties = []
        for i in range(costs.shape[0]):
            if supply_copy[i] > 0:
                valid_costs = [costs[i][j] for j in range(costs.shape[1]) if demand_copy[j] > 0]
                if len(valid_costs) > 1:
                    sorted_costs = sorted(valid_costs)
                    row_penalties.append((sorted_costs[1] - sorted_costs[0], i))
                elif len(valid_costs) == 1:
                    row_penalties.append((valid_costs[0], i))
            else:
                row_penalties.append((-1, i))
                
        col_penalties = []
        for j in range(costs.shape[1]):
            if demand_copy[j] > 0:
                valid_costs = [costs[i][j] for i in range(costs.shape[0]) if supply_copy[i] > 0]
                if len(valid_costs) > 1:
                    sorted_costs = sorted(valid_costs)
                    col_penalties.append((sorted_costs[1] - sorted_costs[0], j))
                elif len(valid_costs) == 1:
                    col_penalties.append((valid_costs[0], j))
            else:
                col_penalties.append((-1, j))
                
        # maximum penalty
        max_row_pen = max(row_penalties, key=lambda x: x[0])
        max_col_pen = max(col_penalties, key=lambda x: x[0])
        
        if max_row_pen[0] >= max_col_pen[0]:
            row = max_row_pen[1]
            valid_cols = [(costs[row][j], j) for j in range(costs.shape[1]) if demand_copy[j] > 0]
            col = min(valid_cols, key=lambda x: x[0])[1]
        else:
            col = max_col_pen[1]
            valid_rows = [(costs[i][col], i) for i in range(costs.shape[0]) if supply_copy[i] > 0]
            row = min(valid_rows, key=lambda x: x[0])[1]
            
        # Allocation
        qty = min(supply_copy[row], demand_copy[col])
        allocations[row][col] = qty
        supply_copy[row] -= qty
        demand_copy[col] -= qty
        
    print("Initial Basic Feasible Solution (VAM) Allocations:")
    print(allocations)
    
    total_cost = np.sum(allocations * costs)
    print(f"Total Initial Cost (VAM): {total_cost}\n")
    return allocations

def modi(costs, allocations):
    print("--- MODI Method (Optimality Check) ---")
    rows, cols = costs.shape
    u = [None] * rows
    v = [None] * cols
    u[0] = 0 # Set first u to 0 to begin
    
    # Finding basic cells (allocations > 0)
    basic_cells = [(i, j) for i in range(rows) for j in range(cols) if allocations[i][j] > 0]
    
    #(Ui + Vj = Cij for basic cells)
    while None in u or None in v:
        progress = False
        for i, j in basic_cells:
            if u[i] is not None and v[j] is None:
                v[j] = costs[i][j] - u[i]
                progress = True
            elif v[j] is not None and u[i] is None:
                u[i] = costs[i][j] - v[j]
                progress = True
                
        # Degeneracy handler: If we get stuck, assign 0 to the next available 'u'
        if not progress and (None in u or None in v):
            for i in range(rows):
                if u[i] is None:
                    u[i] = 0
                    break
                    
    print(f"u values (Sources): {u}")
    print(f"v values (Destinations): {v}")
    
    # (Delta_ij = Cij - (Ui + Vj))
    is_optimal = True
    for i in range(rows):
        for j in range(cols):
            if allocations[i][j] == 0:
                delta = costs[i][j] - (u[i] + v[j])
                if delta < 0:
                    is_optimal = False
                    print(f"Negative penalty found at non-basic cell ({i},{j}): {delta}")
                    
    if is_optimal:
        print("\nAll opportunity costs >= 0. The current solution is OPTIMAL.")
        print(f"Optimal Transportation Cost: {np.sum(allocations * costs)}")
    else:
        print("\nSolution is NOT optimal yet. A closed loop must be formed to shift allocations.")

if __name__ == "__main__":
    # problem matrix
    costs = np.array([
        [2, 2, 3],
        [4, 1, 2],
        [1, 3, 1]
    ])
    
    supply = np.array([10, 15, 40])
    demand = np.array([20, 15, 30])
    
    print("Problem Matrix:")
    print("Costs:\n", costs)
    print("Supply:", supply)
    print("Demand:", demand, "\n")
    
    #  VAM followed by MODI
    initial_allocations = vam(costs, supply, demand)
    modi(costs, initial_allocations)