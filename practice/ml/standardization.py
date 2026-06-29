import pandas as pd
from sklearn.preprocessing import StandardScaler

data = {
    "Salary":[30000,50000,70000,90000,110000]
}

df = pd.DataFrame(data)

scaler = StandardScaler()

df["Salary_Standardized"] = scaler.fit_transform(
    df[["Salary"]]
)

print(df)