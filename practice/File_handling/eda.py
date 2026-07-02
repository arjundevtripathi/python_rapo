"""
╔══════════════════════════════════════════════════════════════════════╗
║   Python EDA – Complete Streamlit Reference App                     ║
║   Data Inspection · Cleaning · Visualization · 100 Examples         ║
║   Run:  streamlit run eda.py                                        ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io
import contextlib
import sys
import random
import time
import math
from collections import Counter, defaultdict
from itertools import accumulate, chain, combinations, permutations
from scipy import stats

# ------------------------------------------------------------
# sklearn imports
# ------------------------------------------------------------
from sklearn.datasets import load_iris, load_diabetes, load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.inspection import permutation_importance, PartialDependenceDisplay
from sklearn.feature_selection import SelectKBest, mutual_info_classif, RFE
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer

# ------------------------------------------------------------
# statsmodels imports
# ------------------------------------------------------------
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

# ------------------------------------------------------------
# scipy imports
# ------------------------------------------------------------
from scipy.stats import f_oneway, chi2_contingency, pearsonr, zscore, probplot, shapiro, ttest_ind
from scipy.cluster.hierarchy import linkage, dendrogram

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Python EDA – Complete Reference",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
.main .block-container { padding-top: 1rem; padding-bottom: 2rem; }

.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem 2rem 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.hero h1 { color: #e94560; font-size: 2.6rem; margin: 0; }
.hero p  { color: #a8dadc; font-size: 1.1rem; margin-top: 0.5rem; }

.sec-header {
    background: linear-gradient(90deg, #e94560, #0f3460);
    color: white;
    padding: 0.55rem 1.2rem;
    border-radius: 8px;
    font-size: 1.15rem;
    font-weight: 700;
    margin: 1.2rem 0 0.8rem 0;
}

.card {
    background: #1e1e2e;
    border: 1px solid #2d2d3f;
    border-left: 4px solid #e94560;
    border-radius: 10px;
    padding: 1rem 1.2rem 0.7rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.card-title { color: #e94560; font-size: 1.05rem; font-weight: 700; margin-bottom: 0.25rem; }
.card-def { color: #a8dadc; font-size: 0.88rem; margin-bottom: 0.6rem; font-style: italic; }
.card-syntax {
    background: #12121f;
    color: #c9d1d9;
    border-radius: 6px;
    padding: 0.5rem 0.8rem;
    font-family: 'Courier New', monospace;
    font-size: 0.83rem;
    border-left: 3px solid #58a6ff;
    white-space: pre-wrap;
}

.badge-beg  { background:#2e7d32; color:white; padding:2px 8px; border-radius:12px; font-size:0.78rem; font-weight:700; }
.badge-int  { background:#1565c0; color:white; padding:2px 8px; border-radius:12px; font-size:0.78rem; font-weight:700; }
.badge-adv  { background:#6a1b9a; color:white; padding:2px 8px; border-radius:12px; font-size:0.78rem; font-weight:700; }

.stat-row { display:flex; gap:1rem; margin-bottom:1.2rem; flex-wrap:wrap; }
.stat-box {
    flex:1; min-width:120px;
    background:#1e1e2e;
    border:1px solid #2d2d3f;
    border-radius:10px;
    padding:0.8rem 1rem;
    text-align:center;
}
.stat-num { font-size:1.8rem; font-weight:800; color:#e94560; }
.stat-lbl { color:#8b949e; font-size:0.78rem; }

.out-box {
    background:#0d1117;
    color:#58a6ff;
    border-radius:8px;
    padding:0.7rem 1rem;
    font-family:'Courier New', monospace;
    font-size:0.85rem;
    margin-top:0.5rem;
    border:1px solid #21262d;
    white-space: pre-wrap;
}

section[data-testid="stSidebar"] { background:#0d1117 !important; }
section[data-testid="stSidebar"] * { color:#c9d1d9 !important; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# DATA DEFINITIONS
# ------------------------------------------------------------

EDA_METHODS = [
    {"name": "df.head(n=5)", "syntax": "DataFrame.head(n=5)", "definition": "Return the first n rows.", "example": "df = pd.read_csv('data.csv')\ndf.head()", "tip": "Always start EDA with .head()"},
    {"name": "df.tail(n=5)", "syntax": "DataFrame.tail(n=5)", "definition": "Return the last n rows.", "example": "df.tail()", "tip": "Use with head() to get data boundaries."},
    {"name": "df.info()", "syntax": "DataFrame.info(verbose=True, ...)", "definition": "Print a concise summary: columns, non-null counts, dtypes.", "example": "df.info()", "tip": "Quickly detect missing values and column types."},
    {"name": "df.describe()", "syntax": "DataFrame.describe(percentiles=None, include=None, exclude=None)", "definition": "Generate descriptive statistics for numeric columns.", "example": "df.describe()", "tip": "Use include='all' to include object/string columns."},
    {"name": "df.shape", "syntax": "DataFrame.shape", "definition": "Return a tuple (rows, columns).", "example": "df.shape  # (1000, 10)", "tip": "Used to assess dataset size."},
    {"name": "df.columns", "syntax": "DataFrame.columns", "definition": "Return the column labels as an Index.", "example": "df.columns", "tip": "Use to rename or standardise column names."},
    {"name": "df.dtypes", "syntax": "DataFrame.dtypes", "definition": "Return the data types of each column.", "example": "df.dtypes", "tip": "Check for mixed types."},
    {"name": "df.isnull().sum()", "syntax": "DataFrame.isnull().sum()", "definition": "Count missing values per column.", "example": "df.isnull().sum()", "tip": "Combine with df.isnull().sum() / len(df) for percentage missing."},
    {"name": "df.dropna()", "syntax": "DataFrame.dropna(axis=0, how='any', ...)", "definition": "Remove rows (or columns) with missing values.", "example": "df_clean = df.dropna()", "tip": "Use with caution; often better to impute."},
    {"name": "df.fillna(value)", "syntax": "DataFrame.fillna(value, method=None, ...)", "definition": "Fill missing values with a specified value or method.", "example": "df.fillna(0, inplace=True)", "tip": "Use median/mean for numeric; mode for categorical."},
    {"name": "df.groupby(by)", "syntax": "DataFrame.groupby(by, ...)", "definition": "Group rows using a column, enabling aggregate operations.", "example": "df.groupby('category')['sales'].mean()", "tip": "Often followed by .agg() with multiple functions."},
    {"name": "df.agg() / df.aggregate()", "syntax": "DataFrame.agg(func, axis=0, ...)", "definition": "Apply one or more aggregation functions.", "example": "df.agg({'col1': 'sum', 'col2': ['mean', 'std']})", "tip": "Use with groupby for grouped aggregations."},
    {"name": "df.pivot_table()", "syntax": "DataFrame.pivot_table(values, index, columns, ...)", "definition": "Create a spreadsheet-style pivot table.", "example": "df.pivot_table(values='sales', index='region', columns='product', aggfunc='sum')", "tip": "Powerful for summarising multidimensional data."},
    {"name": "df.merge()", "syntax": "DataFrame.merge(right, how='inner', ...)", "definition": "Combine two DataFrames using SQL-like joins.", "example": "df1.merge(df2, on='key', how='left')", "tip": "Use `on` for common keys, else specify left_on/right_on."},
    {"name": "df.plot()", "syntax": "DataFrame.plot(x=None, y=None, kind='line', ...)", "definition": "Plot using matplotlib.", "example": "df['column'].plot(kind='hist')", "tip": "Use seaborn for more advanced visualisations."},
    {"name": "sns.histplot()", "syntax": "seaborn.histplot(data=None, x=None, y=None, hue=None, ...)", "definition": "Plot univariate or bivariate histograms with KDE.", "example": "sns.histplot(x='age', data=df, bins=20)", "tip": "Set kde=True to overlay density curve."},
    {"name": "sns.boxplot()", "syntax": "seaborn.boxplot(x=None, y=None, hue=None, data=None, ...)", "definition": "Draw a box plot to show distributions.", "example": "sns.boxplot(x='category', y='value', data=df)", "tip": "Check for outliers easily."},
    {"name": "sns.scatterplot()", "syntax": "seaborn.scatterplot(x=None, y=None, hue=None, ...)", "definition": "Scatter plot for two continuous variables.", "example": "sns.scatterplot(x='height', y='weight', hue='gender', data=df)", "tip": "Use alpha to handle overlapping points."},
    {"name": "sns.pairplot()", "syntax": "seaborn.pairplot(data, hue=None, vars=None, ...)", "definition": "Plot pairwise relationships in a dataset.", "example": "sns.pairplot(df, hue='species')", "tip": "Useful for quickly spotting correlations."},
    {"name": "sns.heatmap()", "syntax": "seaborn.heatmap(data, annot=False, fmt='.2g', ...)", "definition": "Plot a heatmap, often used for correlation matrices.", "example": "sns.heatmap(df.corr(), annot=True)", "tip": "Use with corr() to identify multicollinearity."},
]

BUILTIN_FUNCTIONS = [
    {"name": "pd.read_csv()", "definition": "Read a CSV file into a DataFrame.", "example": "pd.read_csv('data.csv')"},
    {"name": "pd.read_excel()", "definition": "Read an Excel file.", "example": "pd.read_excel('data.xlsx', sheet_name='Sheet1')"},
    {"name": "pd.read_json()", "definition": "Read JSON data.", "example": "pd.read_json('data.json')"},
    {"name": "df.to_csv()", "definition": "Write DataFrame to CSV.", "example": "df.to_csv('out.csv', index=False)"},
    {"name": "df.to_excel()", "definition": "Write to Excel.", "example": "df.to_excel('out.xlsx')"},
    {"name": "pd.concat()", "definition": "Concatenate DataFrames along rows or columns.", "example": "pd.concat([df1, df2], axis=0)"},
    {"name": "pd.merge()", "definition": "Database-style join.", "example": "pd.merge(df1, df2, on='key')"},
    {"name": "df.corr()", "definition": "Compute pairwise correlation of columns.", "example": "df.corr()"},
    {"name": "df.cov()", "definition": "Compute pairwise covariance.", "example": "df.cov()"},
    {"name": "df.value_counts()", "definition": "Count unique values in a Series.", "example": "df['col'].value_counts()"},
    {"name": "df.nunique()", "definition": "Count distinct values per column.", "example": "df.nunique()"},
    {"name": "df.duplicated()", "definition": "Return boolean Series for duplicate rows.", "example": "df.duplicated().sum()"},
    {"name": "df.drop_duplicates()", "definition": "Remove duplicate rows.", "example": "df.drop_duplicates(inplace=True)"},
    {"name": "df.rename()", "definition": "Change column or index labels.", "example": "df.rename(columns={'old':'new'})"},
    {"name": "df.replace()", "definition": "Replace values in the DataFrame.", "example": "df.replace(to_replace=0, value=np.nan)"},
    {"name": "df.apply()", "definition": "Apply a function along an axis.", "example": "df['col'].apply(lambda x: x*2)"},
    {"name": "df.map()", "definition": "Apply a function elementwise on a Series.", "example": "df['col'].map({'A':1, 'B':2})"},
    {"name": "df.query()", "definition": "Query columns using a boolean expression.", "example": "df.query('age > 30 and gender == \"M\"')"},
    {"name": "df.sample()", "definition": "Return a random sample of rows.", "example": "df.sample(100)"},
    {"name": "df.memory_usage()", "definition": "Memory usage of DataFrame columns.", "example": "df.memory_usage(deep=True)"},
    {"name": "pd.get_dummies()", "definition": "One-hot encode categorical variables.", "example": "pd.get_dummies(df, columns=['category'])"},
    {"name": "pd.cut()", "definition": "Bin continuous values into intervals.", "example": "pd.cut(df['age'], bins=[0,18,65,99])"},
    {"name": "df.pivot()", "definition": "Reshape data (long to wide).", "example": "df.pivot(index='date', columns='variable', values='value')"},
    {"name": "df.melt()", "definition": "Unpivot a DataFrame (wide to long).", "example": "df.melt(id_vars=['id'], value_vars=['col1','col2'])"},
    {"name": "df.isna()", "definition": "Alias for isnull, detect missing values.", "example": "df.isna().sum()"},
]

# ------------------------------------------------------------
# 100 EXAMPLES – corrected to avoid chained assignment
# ------------------------------------------------------------
EXAMPLES = [
    (1, "Load a dataset (iris)", "Beginner", "Load Iris dataset.", """import seaborn as sns
df = sns.load_dataset('iris')
print(df.head())
print(df.shape)"""),
    (2, "Inspect first and last rows", "Beginner", "Use head() and tail().", """df = sns.load_dataset('titanic')
print("First 3 rows:")
print(df.head(3))
print("Last 2 rows:")
print(df.tail(2))"""),
    (3, "Get DataFrame info", "Beginner", "Display column types and non-null counts.", """df = sns.load_dataset('titanic')
df.info()"""),
    (4, "Summary statistics", "Beginner", "Describe numeric columns.", """df = sns.load_dataset('iris')
print(df.describe())"""),
    (5, "Describe all columns including categorical", "Beginner", "Use include='all'.", """df = sns.load_dataset('titanic')
print(df.describe(include='all'))"""),
    (6, "Check for missing values", "Beginner", "Count nulls per column.", """df = sns.load_dataset('titanic')
print(df.isnull().sum())"""),
    (7, "Visualise missing data with heatmap", "Beginner", "Heatmap for missing pattern.", """import seaborn as sns
import matplotlib.pyplot as plt
df = sns.load_dataset('titanic')
sns.heatmap(df.isnull(), cbar=False)
plt.show()"""),
    (8, "Drop missing rows", "Beginner", "Remove rows with any null.", """df = sns.load_dataset('titanic')
df_clean = df.dropna()
print(f"Rows before: {len(df)}, after: {len(df_clean)}")"""),
    (9, "Fill missing values with mean", "Beginner", "Impute numeric columns. (No inplace)", """df = sns.load_dataset('titanic')
df['age'] = df['age'].fillna(df['age'].mean())
print(df['age'].isnull().sum())"""),
    (10, "Fill missing with mode", "Beginner", "For categorical columns. (No inplace)", """df = sns.load_dataset('titanic')
mode_val = df['embark_town'].mode()[0]
df['embark_town'] = df['embark_town'].fillna(mode_val)
print(df['embark_town'].isnull().sum())"""),
    (11, "Count distinct values per column", "Beginner", "nunique()", """df = sns.load_dataset('iris')
print(df.nunique())"""),
    (12, "Frequency table for a column", "Beginner", "value_counts()", """df = sns.load_dataset('titanic')
print(df['class'].value_counts())"""),
    (13, "Select a column", "Beginner", "Use bracket or dot notation.", """df = sns.load_dataset('iris')
print(df['sepal_length'].head())
print(df.sepal_length.head())"""),
    (14, "Filter rows by condition", "Beginner", "Boolean indexing.", """df = sns.load_dataset('iris')
filtered = df[df['sepal_length'] > 5.0]
print(filtered.head())"""),
    (15, "Multiple conditions", "Beginner", "Use & and |.", """df = sns.load_dataset('iris')
mask = (df['sepal_length'] > 5.0) & (df['species'] == 'setosa')
print(df[mask].head())"""),
    (16, "Sort by a column", "Beginner", "sort_values()", """df = sns.load_dataset('iris')
df_sorted = df.sort_values('sepal_length', ascending=False)
print(df_sorted.head())"""),
    (17, "Add a new column", "Beginner", "Create column based on existing.", """df = sns.load_dataset('iris')
df['sepal_area'] = df['sepal_length'] * df['sepal_width']
print(df.head())"""),
    (18, "Rename columns", "Beginner", "rename()", """df = sns.load_dataset('iris')
df = df.rename(columns={'sepal_length': 'sl', 'sepal_width': 'sw'})
print(df.columns)"""),
    (19, "Drop columns", "Beginner", "drop() axis=1.", """df = sns.load_dataset('iris')
df = df.drop(columns=['petal_length', 'petal_width'])
print(df.head())"""),
    (20, "Drop rows by index", "Beginner", "drop() axis=0.", """df = sns.load_dataset('iris')
df = df.drop(index=[0, 1, 2])
print(df.head())"""),
    (21, "Sample random rows", "Beginner", "sample(n).", """df = sns.load_dataset('iris')
print(df.sample(5))"""),
    (22, "Get correlation matrix", "Beginner", "corr()", """df = sns.load_dataset('iris')
print(df.corr(numeric_only=True))"""),
    (23, "Plot histogram for a column", "Beginner", "matplotlib histogram.", """import matplotlib.pyplot as plt
df = sns.load_dataset('iris')
plt.hist(df['sepal_length'], bins=20)
plt.title('Sepal Length Distribution')
plt.show()"""),
    (24, "Box plot for a column", "Beginner", "seaborn boxplot.", """import seaborn as sns
import matplotlib.pyplot as plt
df = sns.load_dataset('iris')
sns.boxplot(y='sepal_length', data=df)
plt.show()"""),
    (25, "Box plot by category", "Beginner", "Group by species.", """sns.boxplot(x='species', y='sepal_length', data=df)
plt.show()"""),
    (26, "Scatter plot", "Beginner", "Scatter of two numeric columns.", """sns.scatterplot(x='sepal_length', y='sepal_width', data=df)
plt.show()"""),
    (27, "Scatter plot with hue", "Beginner", "Color by species.", """sns.scatterplot(x='sepal_length', y='sepal_width', hue='species', data=df)
plt.show()"""),
    (28, "Count plot", "Beginner", "Bar chart of categorical counts.", """sns.countplot(x='species', data=df)
plt.show()"""),
    (29, "Pairplot", "Beginner", "Pairwise relationships.", """sns.pairplot(df, hue='species')
plt.show()"""),
    (30, "Export to CSV", "Beginner", "Save DataFrame.", """df = sns.load_dataset('iris')
df.to_csv('iris_export.csv', index=False)
print('Saved.')"""),

    # Intermediate 31-70
    (31, "Group by and aggregate", "Intermediate", "Compute mean per group.", """df = sns.load_dataset('iris')
grouped = df.groupby('species')['sepal_length'].mean()
print(grouped)"""),
    (32, "Multiple aggregations with agg()", "Intermediate", "Use dict or list.", """df = sns.load_dataset('iris')
agg = df.groupby('species').agg({
    'sepal_length': ['mean', 'std'],
    'sepal_width': 'median'
})
print(agg)"""),
    (33, "Pivot table", "Intermediate", "Summarise two categorical variables.", """df = sns.load_dataset('titanic')
pivot = df.pivot_table(values='survived', index='class', columns='sex', aggfunc='mean')
print(pivot)"""),
    (34, "Crosstab", "Intermediate", "Cross-tabulation of two categorical columns.", """df = sns.load_dataset('titanic')
ct = pd.crosstab(df['class'], df['survived'])
print(ct)"""),
    (35, "One-hot encoding", "Intermediate", "Convert categorical to dummy variables.", """df = sns.load_dataset('iris')
dummies = pd.get_dummies(df, columns=['species'])
print(dummies.head())"""),
    (36, "Apply function to column", "Intermediate", "Custom transformation.", """df = sns.load_dataset('iris')
df['sepal_length_sq'] = df['sepal_length'].apply(lambda x: x**2)
print(df.head())"""),
    (37, "Map values", "Intermediate", "Replace categorical codes.", """df = sns.load_dataset('iris')
species_map = {'setosa': 1, 'versicolor': 2, 'virginica': 3}
df['species_code'] = df['species'].map(species_map)
print(df.head())"""),
    (38, "Query method", "Intermediate", "Filter using query string.", """df = sns.load_dataset('iris')
filtered = df.query('sepal_length > 5.0 and species == "setosa"')
print(filtered.head())"""),
    (39, "Merge two DataFrames", "Intermediate", "Simulated merge.", """df1 = pd.DataFrame({'id': [1,2,3], 'name': ['A','B','C']})
df2 = pd.DataFrame({'id': [2,3,4], 'score': [10,20,30]})
merged = pd.merge(df1, df2, on='id', how='inner')
print(merged)"""),
    (40, "Concatenate DataFrames", "Intermediate", "Concat along rows.", """df1 = pd.DataFrame({'A': [1,2]})
df2 = pd.DataFrame({'A': [3,4]})
concat = pd.concat([df1, df2], axis=0, ignore_index=True)
print(concat)"""),
    (41, "Melt (wide to long)", "Intermediate", "Unpivot.", """df = pd.DataFrame({'id': [1,2], 'A': [3,4], 'B': [5,6]})
melted = df.melt(id_vars=['id'], value_vars=['A','B'], var_name='var', value_name='val')
print(melted)"""),
    (42, "Pivot (long to wide)", "Intermediate", "Reshape.", """df_long = pd.DataFrame({
    'date': ['2023-01','2023-01','2023-02','2023-02'],
    'city': ['NY','LA','NY','LA'],
    'temp': [40,60,45,65]
})
pivoted = df_long.pivot(index='date', columns='city', values='temp')
print(pivoted)"""),
    (43, "Handle outliers with IQR", "Intermediate", "Detect outliers using IQR method.", """df = sns.load_dataset('iris')
Q1 = df['sepal_length'].quantile(0.25)
Q3 = df['sepal_length'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5*IQR
upper = Q3 + 1.5*IQR
outliers = df[(df['sepal_length'] < lower) | (df['sepal_length'] > upper)]
print(f'Number of outliers: {len(outliers)}')"""),
    (44, "Standardise / Normalise", "Intermediate", "Scale numeric columns.", """from sklearn.preprocessing import StandardScaler
df = sns.load_dataset('iris')
scaler = StandardScaler()
df_scaled = df.copy()
df_scaled[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']] = scaler.fit_transform(df_scaled[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']])
print(df_scaled.describe())"""),
    (45, "Binning continuous variable", "Intermediate", "Use pd.cut.", """df = sns.load_dataset('titanic')
df['age_group'] = pd.cut(df['age'], bins=[0,18,65,100], labels=['child','adult','elder'])
print(df['age_group'].value_counts())"""),
    (46, "Correlation heatmap", "Intermediate", "Visual correlation matrix.", """import seaborn as sns
import matplotlib.pyplot as plt
df = sns.load_dataset('iris')
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='RdBu_r')
plt.show()"""),
    (47, "Pairplot with hue and diag_kind", "Intermediate", "Custom pairplot.", """sns.pairplot(df, hue='species', diag_kind='kde', markers=['o','s','D'])
plt.show()"""),
    (48, "Histogram with KDE", "Intermediate", "Overlay density.", """sns.histplot(df['sepal_length'], kde=True, bins=20)
plt.show()"""),
    (49, "Violin plot", "Intermediate", "Combine boxplot and KDE.", """sns.violinplot(x='species', y='sepal_length', data=df)
plt.show()"""),
    (50, "Strip plot", "Intermediate", "Show individual data points.", """sns.stripplot(x='species', y='sepal_length', data=df, jitter=True)
plt.show()"""),
    (51, "Swarm plot", "Intermediate", "Categorical scatter with non-overlapping points.", """sns.swarmplot(x='species', y='sepal_length', data=df)
plt.show()"""),
    (52, "Joint plot", "Intermediate", "Scatter + marginal distributions.", """sns.jointplot(x='sepal_length', y='sepal_width', data=df, kind='scatter')
plt.show()"""),
    (53, "Joint plot with hexbin", "Intermediate", "For large datasets.", """sns.jointplot(x='sepal_length', y='sepal_width', data=df, kind='hex')
plt.show()"""),
    (54, "KDE plot", "Intermediate", "Kernel density estimate.", """sns.kdeplot(x='sepal_length', data=df, hue='species', fill=True)
plt.show()"""),
    (55, "ECDF plot", "Intermediate", "Empirical cumulative distribution.", """sns.ecdfplot(x='sepal_length', data=df, hue='species')
plt.show()"""),
    (56, "Time series: line plot", "Intermediate", "Create a simple time series.", """dates = pd.date_range('2023-01-01', periods=100)
data = np.cumsum(np.random.randn(100)) + 100
df_ts = pd.DataFrame({'date': dates, 'value': data})
plt.plot(df_ts['date'], df_ts['value'])
plt.show()"""),
    (57, "Rolling mean", "Intermediate", "Smooth time series.", """df_ts['rolling_mean'] = df_ts['value'].rolling(window=10).mean()
plt.plot(df_ts['date'], df_ts['value'], alpha=0.5)
plt.plot(df_ts['date'], df_ts['rolling_mean'], color='red')
plt.show()"""),
    (58, "Difference transformation", "Intermediate", "For stationarity.", """df_ts['diff'] = df_ts['value'].diff()
plt.plot(df_ts['date'], df_ts['diff'])
plt.show()"""),
    (59, "Check normality with QQ plot", "Intermediate", "scipy.stats.probplot.", """import scipy.stats as stats
stats.probplot(df['sepal_length'], dist="norm", plot=plt)
plt.show()"""),
    (60, "Shapiro-Wilk test", "Intermediate", "Test for normality.", """stat, p = stats.shapiro(df['sepal_length'])
print(f'Statistic: {stat}, p-value: {p}')"""),
    (61, "T-test (independent)", "Intermediate", "Compare two groups.", """setosa = df[df['species']=='setosa']['sepal_length']
versicolor = df[df['species']=='versicolor']['sepal_length']
stat, p = stats.ttest_ind(setosa, versicolor)
print(f'T-statistic: {stat}, p-value: {p}')"""),
    (62, "ANOVA", "Intermediate", "Compare multiple groups.", """from scipy.stats import f_oneway
setosa = df[df['species']=='setosa']['sepal_length']
versicolor = df[df['species']=='versicolor']['sepal_length']
virginica = df[df['species']=='virginica']['sepal_length']
stat, p = f_oneway(setosa, versicolor, virginica)
print(f'F-statistic: {stat}, p-value: {p}')"""),
    (63, "Chi-square test", "Intermediate", "Test independence between categorical variables.", """from scipy.stats import chi2_contingency
df = sns.load_dataset('titanic')
contingency = pd.crosstab(df['class'], df['survived'])
chi2, p, dof, expected = chi2_contingency(contingency)
print(f'Chi2: {chi2}, p: {p}')"""),
    (64, "Correlation with p-values", "Intermediate", "Compute correlation matrix with significance.", """from scipy.stats import pearsonr
df_num = df.select_dtypes(include=[np.number])
corr_matrix = df_num.corr()
p_matrix = df_num.corr(method=lambda x, y: pearsonr(x, y)[1])
print(corr_matrix)
print(p_matrix)"""),
    (65, "Feature engineering: polynomial features", "Intermediate", "Create interaction terms.", """df = sns.load_dataset('iris')
df['sl_sw_interact'] = df['sepal_length'] * df['sepal_width']
print(df.head())"""),
    (66, "Log transformation", "Intermediate", "Reduce skewness.", """df = sns.load_dataset('titanic')
df['log_fare'] = np.log1p(df['fare'])
print(df['log_fare'].describe())"""),
    (67, "Square root transformation", "Intermediate", "Stabilise variance.", """df['sqrt_fare'] = np.sqrt(df['fare'])
print(df['sqrt_fare'].describe())"""),
    (68, "Skewness and kurtosis", "Intermediate", "Compute moments.", """print('Skewness:', df['fare'].skew())
print('Kurtosis:', df['fare'].kurtosis())"""),
    (69, "Outlier removal using Z-score", "Intermediate", "Remove points beyond 3 standard deviations.", """from scipy.stats import zscore
df = sns.load_dataset('iris')
z_scores = np.abs(zscore(df['sepal_length']))
filtered = df[z_scores < 3]
print(f'Rows removed: {len(df) - len(filtered)}')"""),
    (70, "Save cleaned data", "Intermediate", "Export to Excel.", """df_clean = df.dropna()
df_clean.to_excel('cleaned_data.xlsx', index=False)
print('Cleaned data saved.')"""),

    # Advanced 71-100
    (71, "Automated exploratory data report (pandas-profiling)", "Advanced", "Generate a full report with ydata-profiling.", """# from ydata_profiling import ProfileReport
# profile = ProfileReport(df, title='Pandas Profiling Report')
# profile.to_file('report.html')"""),
    (72, "Dimensionality reduction: PCA", "Advanced", "Principal Component Analysis.", """from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
df = sns.load_dataset('iris')
X = df.drop('species', axis=1)
X_scaled = StandardScaler().fit_transform(X)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print(pca.explained_variance_ratio_)"""),
    (73, "PCA visualisation", "Advanced", "Plot PCA results.", """plt.figure(figsize=(8,6))
sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=df['species'])
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()"""),
    (74, "t-SNE for high-dimensional data", "Advanced", "Non-linear dimensionality reduction.", """from sklearn.manifold import TSNE
X_tsne = TSNE(n_components=2, random_state=42).fit_transform(X_scaled)
sns.scatterplot(x=X_tsne[:,0], y=X_tsne[:,1], hue=df['species'])
plt.show()"""),
    (75, "Clustering: KMeans", "Advanced", "Unsupervised grouping.", """from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)
print(df['cluster'].value_counts())"""),
    (76, "Silhouette score", "Advanced", "Evaluate clustering.", """from sklearn.metrics import silhouette_score
score = silhouette_score(X_scaled, df['cluster'])
print(f'Silhouette score: {score}')"""),
    (77, "Hierarchical clustering dendrogram", "Advanced", "Dendrogram for agglomerative clustering.", """from scipy.cluster.hierarchy import dendrogram, linkage
linked = linkage(X_scaled, method='ward')
dendrogram(linked, orientation='top', distance_sort='descending', show_leaf_counts=False)
plt.show()"""),
    (78, "Decision Tree for understanding features", "Advanced", "Fit a tree and plot importance.", """from sklearn.tree import DecisionTreeClassifier
X = df.drop(['species', 'cluster'], axis=1)
y = df['species']
tree = DecisionTreeClassifier()
tree.fit(X, y)
print('Feature importances:', dict(zip(X.columns, tree.feature_importances_)))"""),
    (79, "Random Forest feature importance", "Advanced", "More robust importance.", """from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(X, y)
importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print(importances)"""),
    (80, "Permutation importance", "Advanced", "Using sklearn.inspection.", """from sklearn.inspection import permutation_importance
result = permutation_importance(rf, X, y, n_repeats=10, random_state=42)
print('Permutation importances:', result.importances_mean)"""),
    (81, "Partial dependence plots", "Advanced", "Visualise effect of a feature.", """from sklearn.inspection import PartialDependenceDisplay
PartialDependenceDisplay.from_estimator(rf, X, features=['sepal_length', 'petal_length'])
plt.show()"""),
    (82, "SHAP values for model interpretation", "Advanced", "Requires shap library.", """# import shap
# explainer = shap.TreeExplainer(rf)
# shap_values = explainer.shap_values(X)
# shap.summary_plot(shap_values, X)"""),
    (83, "LIME for local interpretability", "Advanced", "Explain individual predictions.", """# from lime.lime_tabular import LimeTabularExplainer
# explainer = LimeTabularExplainer(X.values, feature_names=X.columns, class_names=rf.classes_)
# exp = explainer.explain_instance(X.iloc[0].values, rf.predict_proba)
# exp.show_in_notebook()"""),
    (84, "Time series decomposition", "Advanced", "Seasonal-Trend decomposition.", """from statsmodels.tsa.seasonal import seasonal_decompose
# result = seasonal_decompose(df_ts['value'], model='additive', period=30)
# result.plot()
# plt.show()"""),
    (85, "Autocorrelation plot (ACF)", "Advanced", "Detect autocorrelation.", """from statsmodels.graphics.tsaplots import plot_acf
plot_acf(df_ts['value'].dropna())
plt.show()"""),
    (86, "Partial autocorrelation (PACF)", "Advanced", "plot_pacf", """from statsmodels.graphics.tsaplots import plot_pacf
plot_pacf(df_ts['value'].dropna())
plt.show()"""),
    (87, "ADF test for stationarity", "Advanced", "Augmented Dickey-Fuller test.", """from statsmodels.tsa.stattools import adfuller
result = adfuller(df_ts['value'])
print(f'ADF Statistic: {result[0]}, p-value: {result[1]}')"""),
    (88, "ARIMA model fitting (example)", "Advanced", "Fit ARIMA to time series.", """from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(df_ts['value'], order=(1,1,1))
model_fit = model.fit()
print(model_fit.summary())"""),
    (89, "Forecast with ARIMA", "Advanced", "Predict future values.", """forecast = model_fit.forecast(steps=10)
print(forecast)"""),
    (90, "Cross-validation for time series", "Advanced", "TimeSeriesSplit.", """from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=3)
for train_index, test_index in tscv.split(df_ts):
    print('Train indices:', train_index, 'Test indices:', test_index)"""),
    (91, "Outlier detection with Isolation Forest", "Advanced", "Anomaly detection.", """from sklearn.ensemble import IsolationForest
iso = IsolationForest(contamination=0.05, random_state=42)
preds = iso.fit_predict(X_scaled)
df['outlier'] = preds == -1
print(f'Outlier count: {df["outlier"].sum()}')"""),
    (92, "Data imbalance handling: SMOTE", "Advanced", "Synthetic Minority Oversampling.", """# from imblearn.over_sampling import SMOTE
# sm = SMOTE(random_state=42)
# X_resampled, y_resampled = sm.fit_resample(X, y)
# print(pd.Series(y_resampled).value_counts())"""),
    (93, "Feature selection with mutual information", "Advanced", "SelectKBest.", """from sklearn.feature_selection import SelectKBest, mutual_info_classif
selector = SelectKBest(mutual_info_classif, k=2)
X_selected = selector.fit_transform(X, y)
print('Selected features:', X.columns[selector.get_support()])"""),
    (94, "RFE (Recursive Feature Elimination)", "Advanced", "Select features recursively.", """from sklearn.feature_selection import RFE
rfe = RFE(estimator=DecisionTreeClassifier(), n_features_to_select=2)
rfe.fit(X, y)
print('RFE ranking:', rfe.ranking_)"""),
    (95, "Grid search for hyperparameter tuning", "Advanced", "Find best parameters.", """from sklearn.model_selection import GridSearchCV
param_grid = {'max_depth': [3,5,7], 'min_samples_split': [2,5]}
grid = GridSearchCV(DecisionTreeClassifier(), param_grid, cv=3)
grid.fit(X, y)
print('Best params:', grid.best_params_)"""),
    (96, "Pipeline for preprocessing and modeling", "Advanced", "Chain transformers.", """from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', LogisticRegression())
])
pipe.fit(X, y)
print('Pipeline score:', pipe.score(X, y))"""),
    (97, "Automated feature engineering with featuretools", "Advanced", "Deep feature synthesis.", """# import featuretools as ft
# es = ft.EntitySet(id='data')
# es = es.add_dataframe(dataframe_name='iris', dataframe=df, index='index')
# feature_matrix, feature_defs = ft.dfs(entityset=es, target_dataframe_name='iris')
# print(feature_matrix.columns)"""),
    (98, "Custom transformer with sklearn", "Advanced", "Create a class implementing fit/transform.", """from sklearn.base import BaseEstimator, TransformerMixin
class LogTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return np.log1p(X)
# Usage in pipeline: LogTransformer()"""),
    (99, "EDA on text data (word count, TF-IDF)", "Advanced", "Basic text EDA.", """from sklearn.feature_extraction.text import CountVectorizer
texts = ['apple banana', 'orange apple', 'banana banana']
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
print(pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out()))"""),
    (100, "Automated EDA with sweetviz", "Advanced", "Generate a report quickly.", """# import sweetviz as sv
# report = sv.analyze(df)
# report.show_html('sweet_report.html')"""),
]

# ------------------------------------------------------------
# EXEC GLOBALS
# ------------------------------------------------------------
EXEC_GLOBALS = {
    "__builtins__": __builtins__,
    "pd": pd, "np": np, "sns": sns, "plt": plt, "stats": stats,
    "os": __import__('os'), "sys": sys, "io": io,
    "random": random, "time": time, "math": math,
    "Counter": Counter, "defaultdict": defaultdict,
    "accumulate": accumulate, "chain": chain,
    "combinations": combinations, "permutations": permutations,
    "load_iris": load_iris, "load_diabetes": load_diabetes, "load_wine": load_wine,
    "sklearn": __import__('sklearn'),
    "StandardScaler": StandardScaler, "PCA": PCA, "TSNE": TSNE,
    "KMeans": KMeans, "silhouette_score": silhouette_score,
    "DecisionTreeClassifier": DecisionTreeClassifier,
    "RandomForestClassifier": RandomForestClassifier,
    "IsolationForest": IsolationForest,
    "permutation_importance": permutation_importance,
    "PartialDependenceDisplay": PartialDependenceDisplay,
    "SelectKBest": SelectKBest, "mutual_info_classif": mutual_info_classif,
    "RFE": RFE, "GridSearchCV": GridSearchCV, "TimeSeriesSplit": TimeSeriesSplit,
    "Pipeline": Pipeline, "LogisticRegression": LogisticRegression,
    "BaseEstimator": BaseEstimator, "TransformerMixin": TransformerMixin,
    "CountVectorizer": CountVectorizer,
    "seasonal_decompose": seasonal_decompose,
    "plot_acf": plot_acf, "plot_pacf": plot_pacf,
    "adfuller": adfuller, "ARIMA": ARIMA,
    "f_oneway": f_oneway, "chi2_contingency": chi2_contingency,
    "pearsonr": pearsonr, "zscore": zscore, "probplot": probplot,
    "shapiro": shapiro, "ttest_ind": ttest_ind,
    "linkage": linkage, "dendrogram": dendrogram,
}

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("## 📊 EDA Reference")
    section = st.radio("Navigate to", [
        "🏠 Overview",
        "📚 All EDA Methods",
        "🔧 Built-in Functions",
        "🟢 Beginner (1–30)",
        "🔵 Intermediate (31–70)",
        "🟣 Advanced (71–100)",
        "🎮 Interactive Playground",
        "📊 Visual Explorer",
    ])
    st.markdown("---")
    st.markdown("**Quick Stats**")
    st.markdown("• 20 EDA methods")
    st.markdown("• 24 built-in functions")
    st.markdown("• 100 code examples")
    st.markdown("• Beginner → Advanced")

# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------
st.markdown("""
<div class='hero'>
  <h1>📊 Python EDA — Complete Reference</h1>
  <p>Data Inspection · Cleaning · Transformation · Visualisation · 100 Examples</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# OVERVIEW
# ------------------------------------------------------------
if section == "🏠 Overview":
    st.markdown("""
<div class='stat-row'>
  <div class='stat-box'><div class='stat-num'>20</div><div class='stat-lbl'>EDA Methods</div></div>
  <div class='stat-box'><div class='stat-num'>24</div><div class='stat-lbl'>Functions</div></div>
  <div class='stat-box'><div class='stat-num'>100</div><div class='stat-lbl'>Code Examples</div></div>
  <div class='stat-box'><div class='stat-num'>3</div><div class='stat-lbl'>Difficulty Levels</div></div>
</div>
""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📖 What is Exploratory Data Analysis (EDA)?")
        st.markdown("""
**Exploratory Data Analysis** is the process of investigating datasets to summarise their main characteristics, often with visual methods.

| Common Steps | Tools |
|---|---|
| Data loading | `pandas.read_csv()` |
| Data inspection | `.head()`, `.info()`, `.describe()` |
| Missing data | `.isnull()`, `.dropna()`, `.fillna()` |
| Transformation | `.apply()`, `.map()`, `.groupby()` |
| Visualisation | `matplotlib`, `seaborn`, `plotly` |
| Statistical tests | `scipy.stats` |
""")
    with c2:
        st.markdown("### 🗂️ What's Inside This App?")
        st.markdown("""
| Section | Contents |
|---|---|
| 📚 All EDA Methods | Data inspection, cleaning, transformation, plotting |
| 🔧 Built-in Functions | `pandas`, `numpy`, `scipy`, `sklearn` helpers |
| 🟢 Beginner | Basics: loading, summary, simple plots (1–30) |
| 🔵 Intermediate | Grouping, pivoting, advanced plots, statistical tests (31–70) |
| 🟣 Advanced | Dimensionality reduction, clustering, interpretability (71–100) |
| 🎮 Playground | Upload data, run EDA code interactively |
| 📊 Explorer | Visual data profiling and summary |
""")
    st.markdown("### ⚡ Quick Cheatsheet")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.code("""# Load & inspect
import pandas as pd
df = pd.read_csv('data.csv')
df.head()
df.info()""", language="python")
    with col2:
        st.code("""# Clean & transform
df.dropna()
df.fillna(value)
df.groupby().agg()
pd.get_dummies()""", language="python")
    with col3:
        st.code("""# Visualise
import seaborn as sns
sns.histplot()
sns.boxplot()
sns.pairplot()
sns.heatmap(df.corr())""", language="python")

# ------------------------------------------------------------
# ALL EDA METHODS
# ------------------------------------------------------------
elif section == "📚 All EDA Methods":
    st.markdown("<div class='sec-header'>📚 All 20 Essential EDA Methods</div>", unsafe_allow_html=True)
    for m in EDA_METHODS:
        with st.expander(f"🔹 `{m['name']}`", expanded=False):
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown(f"**Definition:** {m['definition']}")
                st.markdown(f"**Syntax:** `{m['syntax']}`")
                st.info(f"💡 {m['tip']}")
            with c2:
                st.code(m["example"], language="python")

# ------------------------------------------------------------
# BUILT-IN FUNCTIONS
# ------------------------------------------------------------
elif section == "🔧 Built-in Functions":
    st.markdown("<div class='sec-header'>🔧 24 Built-in Functions & Modules for EDA</div>", unsafe_allow_html=True)
    for fn in BUILTIN_FUNCTIONS:
        st.markdown(f"""
<div class='card'>
  <div class='card-title'><code>{fn['name']}</code></div>
  <div class='card-def'>{fn['definition']}</div>
  <div class='card-syntax'>{fn['example']}</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# EXAMPLE SECTIONS
# ------------------------------------------------------------
elif section in ("🟢 Beginner (1–30)", "🔵 Intermediate (31–70)", "🟣 Advanced (71–100)"):
    level_map = {
        "🟢 Beginner (1–30)":       ("Beginner",     "🟢", "badge-beg"),
        "🔵 Intermediate (31–70)":  ("Intermediate", "🔵", "badge-int"),
        "🟣 Advanced (71–100)":     ("Advanced",     "🟣", "badge-adv"),
    }
    level_name, emoji, badge_cls = level_map[section]
    filtered = [(n, t, l, d, c) for n, t, l, d, c in EXAMPLES if l == level_name]
    st.markdown(
        f"<div class='sec-header'>{emoji} {level_name} — {len(filtered)} Examples</div>",
        unsafe_allow_html=True,
    )
    search = st.text_input("🔍 Search examples by title or keyword", "")
    for num, title, level, defn, code_src in filtered:
        if search and search.lower() not in title.lower() and search.lower() not in code_src.lower():
            continue
        with st.expander(f"#{num} — {title}", expanded=False):
            st.markdown(f"<span class='{badge_cls}'>{level}</span>", unsafe_allow_html=True)
            st.markdown(f"**📖 Definition:** {defn}")
            st.code(code_src, language="python")
            if st.button(f"▶ Run Example #{num}", key=f"run_{num}"):
                st.markdown("**Output:**")
                try:
                    buf = io.StringIO()
                    with contextlib.redirect_stdout(buf):
                        exec(code_src, EXEC_GLOBALS)
                    out = buf.getvalue()
                    st.markdown(f"<div class='out-box'>{out if out else '(no output)'}</div>",
                                unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# ------------------------------------------------------------
# INTERACTIVE PLAYGROUND
# ------------------------------------------------------------
elif section == "🎮 Interactive Playground":
    st.markdown("<div class='sec-header'>🎮 Interactive EDA Playground</div>", unsafe_allow_html=True)
    st.markdown("### 📤 Upload your dataset (CSV)")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.markdown("**Preview:**")
        st.dataframe(df.head())
        st.markdown("**Info:**")
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())
    st.markdown("---")
    st.markdown("### ✏️ Custom EDA Code")
    default_code = """# Perform EDA on uploaded data (if any)
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# If you uploaded a file, it's in variable `df`
# For demonstration, we'll load iris if df is not defined.
try:
    df
except NameError:
    df = sns.load_dataset('iris')

# Basic summary
print("Shape:", df.shape)
print("\\nColumns:")
print(df.columns.tolist())
print("\\nMissing values:")
print(df.isnull().sum())

# Display some statistics
print("\\nDescribe:")
print(df.describe())

print("\\nEDA complete.")
"""
    user_code = st.text_area("Python code:", default_code, height=250)
    if st.button("▶ Run Code", type="primary"):
        buf = io.StringIO()
        try:
            local_globals = EXEC_GLOBALS.copy()
            if uploaded_file is not None:
                local_globals['df'] = df
            else:
                local_globals['df'] = sns.load_dataset('iris')
            with contextlib.redirect_stdout(buf):
                exec(user_code, local_globals)
            st.markdown(f"<div class='out-box'>{buf.getvalue()}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")

# ------------------------------------------------------------
# VISUAL EXPLORER – fixed for Arrow compatibility
# ------------------------------------------------------------
elif section == "📊 Visual Explorer":
    st.markdown("<div class='sec-header'>📊 Data Visual Explorer</div>", unsafe_allow_html=True)

    dataset_name = st.selectbox("Choose a dataset", ["iris", "titanic", "tips", "penguins"])
    try:
        df = sns.load_dataset(dataset_name)
    except:
        df = sns.load_dataset("iris")

    # Convert object columns to string type to avoid Arrow serialisation issues
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype('string')

    st.markdown(f"**Dataset:** {dataset_name} ({df.shape[0]} rows, {df.shape[1]} columns)")
    st.dataframe(df.head())

    st.markdown("### Summary")
    st.write("**Describe:**")
    st.write(df.describe(include='all'))

    st.markdown("### Correlation Heatmap")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        fig, ax = plt.subplots(figsize=(8,6))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='RdBu_r', ax=ax)
        st.pyplot(fig)
    else:
        st.info("Not enough numeric columns for correlation.")

    st.markdown("### Pairplot (if not too many columns)")
    if len(numeric_cols) >= 2 and len(numeric_cols) <= 6:
        cols_to_plot = numeric_cols[:4]
        if len(cols_to_plot) > 1:
            fig = sns.pairplot(df[cols_to_plot])
            st.pyplot(fig)
        else:
            st.info("Not enough numeric columns.")
    else:
        st.info("Pairplot skipped due to too many numeric columns (or too few).")

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#666; font-size:0.85rem;'>"
    "📊 Python EDA Complete Reference · 20 Methods · 24 Functions · 100 Examples"
    "</p>",
    unsafe_allow_html=True,
)