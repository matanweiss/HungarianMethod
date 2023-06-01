import numpy as np

def matching_augmentation(cost_matrix, assignment):
    n = cost_matrix.shape[0]  # Number of tasks or resources

    # Step 1: Build adjacency matrix
    adjacency_matrix = np.zeros((n, n), dtype=bool)
    for i, j in enumerate(assignment):
        adjacency_matrix[i, j] = True

    while True:
        # Step 2: Find an unmatched row
        unmatched_row = np.argmax(~np.any(adjacency_matrix, axis=1))
        if unmatched_row == n:
            break

        visited_rows = np.zeros(n, dtype=bool)
        visited_cols = np.zeros(n, dtype=bool)
        parent = np.zeros(n, dtype=int) - 1

        # Step 3: Find augmenting path
        def dfs(row):
            visited_rows[row] = True
            for col in range(n):
                if not visited_cols[col] and adjacency_matrix[row, col]:
                    visited_cols[col] = True
                    if parent[col] == -1 or dfs(parent[col]):
                        parent[col] = row
                        return True
            return False

        dfs(unmatched_row)

        # Step 4: Augment assignment
        while True:
            col = np.argmax(parent == -1)
            print(col)
            if col == n:
                break
            row = parent[col]
            prev_col = assignment[row]
            assignment[row] = col
            adjacency_matrix[row, prev_col] = False
            adjacency_matrix[row, col] = True
            parent[col] = row

    return assignment

# Example usage
cost_matrix = [
    [4, 1, 3],
    [2, 0, 5],
    [3, 2, 2]
]
initial_assignment = [0, 1, 2]

assignment = matching_augmentation(np.array(cost_matrix), initial_assignment)
print("Augmented assignment:", assignment)
