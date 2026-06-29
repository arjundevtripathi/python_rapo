
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

data = {
    "Salary":[30000,50000,70000,90000,110000]
}

df = pd.DataFrame(data)

scaler = MinMaxScaler()

df["Salary_Normalized"] = scaler.fit_transform(
    df[["Salary"]]
)

print(df)