import numpy as np
import pandas as pd

df_loading_profile = pd.read_csv("Loading_Profile_of_Nodes_1__2__and_3.csv")
df_workstation = pd.read_excel("Workstation_Metrics.xlsx")

df_workstation["Utilization"] = df_workstation["Utilization"].str.rstrip('%').astype(float) / 100

time_factor = 7 * 24 * 60 

tool_requirements = pd.DataFrame(columns=df_workstation["Workstation"], index=df_loading_profile["Quarter"])

for quarter in df_loading_profile["Quarter"]:
    for workstation in df_workstation["Workstation"]:
        utilization = df_workstation.loc[df_workstation["Workstation"] == workstation, "Utilization"].values[0]

        total_tools = 0
        for node in ["Node 1", "Node 2", "Node 3"]:
            loading = df_loading_profile.loc[df_loading_profile["Quarter"] == quarter, node].values[0]
            minute_load = df_workstation.loc[df_workstation["Workstation"] == workstation, f"{node} Minute Load"].values[0]

            if minute_load > 0:
                total_tools += (loading * minute_load) / (time_factor * utilization)

        tool_requirements.at[quarter, workstation] = np.ceil(total_tools)

tool_requirements.insert(0, "Workstation", tool_requirements.index)
tool_requirements.reset_index(drop=True, inplace=True)

print(tool_requirements)

output_file = "Tool_Requirement.xlsx"
tool_requirements.to_excel(output_file, index=False)
