import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


#load and clean the data from xlsx file

df = pd.read_csv('C:/Users/aryan/OneDrive/Desktop/temp/32_Constituency_Data_Summary_Report.csv')

print("Initial Data Overview:")
print(df.info())

# 1. Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

df['Men'].fillna(df['Men'].median(), inplace=True)
df['Women'].fillna(df['Women'].median(), inplace=True)
df['Third Gender'].fillna(df['Third Gender'].median(), inplace=True)

# 2. Data Integrity Checks
print("\nData Types Integrity:")
print(df.dtypes)

# 3. Outlier Detection using IQR method
def detect_outliers(df, column):
    Q1 = df[column].quantile(0.25) 
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

outliers_men = detect_outliers(df, 'Men')
outliers_women = detect_outliers(df, 'Women')
outliers_third_gender = detect_outliers(df, 'Third Gender')

print("\nOutliers in 'Men' column:")
print(outliers_men)
print("\nOutliers in 'Women' column:")
print(outliers_women)
print("\nOutliers in 'Third Gender' column:")
print(outliers_third_gender)



# 4. Duplicate Check
duplicates = df[df.duplicated()]
print("\nDuplicate Rows:")
print(duplicates)

df.drop_duplicates(inplace=True)

# 5. EDA - Basic Statistics
print("\nBasic Statistics:")
print(df.describe())

# Visualize outliers in Men, Women, and Third Gender columns
plt.figure(figsize=(12, 6))

plt.subplot(1, 3, 1)
plt.boxplot(df['Men'])
plt.title('Outlier Detection: Men')

plt.subplot(1, 3, 2)
plt.boxplot(df['Women'])
plt.title('Outlier Detection: Women')

plt.subplot(1, 3, 3)
plt.boxplot(df['Third Gender'])
plt.title('Outlier Detection: Third Gender')

plt.tight_layout()
plt.show()

# --- Objective 1: Candidate Category Analysis ---

# Filter relevant candidate categories
candidate_categories = [
    'Candidates - Nominated',
    'Candidates - Nomination Rejected',
    'Candidates - Withdrawn',
    'Candidates - Contested'
]

candidates_df = df[df['Category'].isin(candidate_categories)]

# Group by category and sum gender-wise counts
grouped = candidates_df.groupby('Category')[['Men', 'Women', 'Third Gender']].sum()

# Plotting with custom colors
colors = ['#1f77b4', '#ff7f0e', '#d62728']  # Blue for Men, Orange for Women, Red for Third Gender
grouped.plot(kind='bar', stacked=True, figsize=(10, 6), color=colors)
plt.title('Gender-wise Distribution of Candidates by Category')
plt.ylabel('Number of Candidates')
plt.xlabel('Candidate Category')
plt.xticks(rotation=45)
plt.legend(title='Gender')
plt.tight_layout()
plt.show()

