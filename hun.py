import numpy as np

def hungarian_algorithm(cost_matrix):
    # Step 1: Create cost matrix
    cost_matrix = np.array(cost_matrix)
    
    # Step 2: Subtract row minimums
    cost_matrix -= np.min(cost_matrix, axis=1, keepdims=True)
    
    # Step 3: Subtract column minimums
    cost_matrix -= np.min(cost_matrix, axis=0, keepdims=True)
    
    n = cost_matrix.shape[0]  # Number of tasks or resources
    
    lines = np.zeros_like(cost_matrix, dtype=bool)
    assignment = np.zeros(n, dtype=int)
    
    while True:
        # Step 4: Cover all zeros
        zeros = np.argwhere(cost_matrix == 0)
        row_covered = np.zeros(n, dtype=bool)
        col_covered = np.zeros(n, dtype=bool)
        
        for zero in zeros:
            r, c = zero
            if not row_covered[r] and not col_covered[c]:
                lines[r, c] = True
                row_covered[r] = True
                col_covered[c] = True
        
        # Step 5: Check for optimality
        if np.sum(lines) == n:
            break
        
        # Step 6: Find minimum uncovered value
        min_uncovered = np.min(cost_matrix[~row_covered, ~col_covered])
        
        # Step 7: Adjust cost matrix
        cost_matrix[row_covered, col_covered] += min_uncovered
        cost_matrix[~row_covered, ~col_covered] -= min_uncovered
    
    # Step 8: Extract assignment
    assignment = np.argmax(lines, axis=1)
    
    return assignment

# Example usage
cost_matrix = [
    [4, 1, 3],
    [2, 0, 5],
    [3, 2, 2]
]

assignment = hungarian_algorithm(cost_matrix)
print("Task assignment:", assignment)
