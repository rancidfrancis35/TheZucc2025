import pandas as pd

# Given data from the problem statement

# TAM (Total Addressable Market) per quarter (in billion GBs)
TAM_per_quarter = [21.8, 27.4, 34.9, 39.0, 44.7, 51.5, 52.5, 53.5]  # in billion GBs

# Convert TAM to GBs (1 billion GBs = 1e9 GBs)
TAM_per_quarter = [tam * 1e9 for tam in TAM_per_quarter]

# GB per wafer for each Node
GB_per_wafer = {
    "Node 1": 100000,  # 100k GB per wafer
    "Node 2": 150000,  # 150k GB per wafer
    "Node 3": 270000,  # 270k GB per wafer
}

# Yield per quarter for each Node
yield_per_quarter = {
    "Node 1": [0.98] * 8,  # Constant 98% yield
    "Node 2": [0.60, 0.82, 0.95, 0.98, 0.98, 0.98, 0.98, 0.98],  # Varies over quarters
    "Node 3": [0.20, 0.25, 0.35, 0.50, 0.65, 0.85, 0.95, 0.98],  # Varies over quarters
}

# Initial loading in Q1'26
initial_loading = {
    "Node 1": 12000,
    "Node 2": 5000,
    "Node 3": 1000,
}

# Number of weeks per quarter
weeks_per_quarter = 13

# Function to calculate required loading per node per quarter
def calculate_loading(TAM_per_quarter, initial_loading, GB_per_wafer, yield_per_quarter, max_change=2500):
    loading_per_quarter = {node: [initial_loading[node]] for node in GB_per_wafer}

    for q in range(1, len(TAM_per_quarter)):  # Start from Q2'26 since Q1'26 is given
        required_GB = TAM_per_quarter[q]
        
        # Solve for number of wafers required for each node while considering constraints
        node_contributions = {}
        for node in GB_per_wafer:
            node_contributions[node] = GB_per_wafer[node] * yield_per_quarter[node][q] * weeks_per_quarter

        # Distribute required GB among nodes based on past loading and constraints
        total_contribution = sum(node_contributions.values())
        node_ratios = {node: node_contributions[node] / total_contribution for node in GB_per_wafer}

        new_loading = {}
        for node in GB_per_wafer:
            suggested_loading = (required_GB * node_ratios[node]) / node_contributions[node] * weeks_per_quarter
            previous_loading = loading_per_quarter[node][-1]

            # Ensure loading change does not exceed max_change constraint
            change = min(max_change, max(-max_change, suggested_loading - previous_loading))
            new_loading[node] = previous_loading + change

        # Append calculated loading values for this quarter
        for node in GB_per_wafer:
            loading_per_quarter[node].append(round(new_loading[node]))

    return loading_per_quarter

# Calculate loading profile
loading_profile = calculate_loading(TAM_per_quarter, initial_loading, GB_per_wafer, yield_per_quarter)

# Create DataFrame for display
df_loading = pd.DataFrame(loading_profile, index=[f"Q{i+1}'26" if i < 4 else f"Q{i-3}'27" for i in range(8)])
df_loading.index.name = "Quarter"

# Display results
import ace_tools as tools
tools.display_dataframe_to_user(name="Loading Profile of Nodes 1, 2, and 3", dataframe=df_loading)
