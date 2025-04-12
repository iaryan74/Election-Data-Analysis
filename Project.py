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

# --- Objective 2: Voter Data Analysis (General, Overseas, Proxy, Postal) --- #

# Filter the data for Voters categories (General, Overseas, Proxy, Postal)
voters_data = df[df['Category'].str.contains('Voters')]

# Group by Category and sum the values for Men, Women, and Third Gender
voters_data_grouped = voters_data.groupby('Category').sum()[['Men', 'Women', 'Third Gender']]

# Calculate the total voters (sum of Men, Women, Third Gender)
voters_data_grouped['Total Voters'] = voters_data_grouped.sum(axis=1)

# Filter out categories with no voters
filtered_voters_data = voters_data_grouped[voters_data_grouped['Total Voters'] > 0]

# Display the filtered result for better clarity
print("\nFiltered Total Voters by Category:")
print(filtered_voters_data)

# Plotting the Total Voters for each category with adjusted y-axis scale
plt.figure(figsize=(10, 6))

# Plotting the total voters for each category
filtered_voters_data['Total Voters'].plot(kind='bar', color='lightcoral')

# Adding a title and labels
plt.title('Total Number of Voters by Category')
plt.xlabel('Category')
plt.ylabel('Total Voters')

# Automatically adjust y-axis to fit all values properly
plt.yscale('linear')

# Adjusting the xticks for better readability
plt.xticks(rotation=45)

# Adding data labels to bars for clarity
for index, value in enumerate(filtered_voters_data['Total Voters']):
    plt.text(index, value, str(int(value)), ha='center', va='bottom')

# Display the plot
plt.tight_layout()
plt.show()

# --- Objective 3: Invalid & Deducted Votes Analysis ---

# Categories of interest
invalid_deducted_categories = [
    'Votes - Total Deducted Votes From Evm',
    'Votes - Postal Votes Deducted'
]

# Filter relevant data
invalid_deducted_df = df[df['Category'].isin(invalid_deducted_categories)]

# Calculate total invalid/deducted votes
invalid_deducted_total = invalid_deducted_df.groupby('Category')[['Men', 'Women', 'Third Gender']].sum().sum(axis=1)

# Display or show a fallback message
print("\nTotal Invalid & Deducted Votes by Category (Without Gender Breakdown):")
print(invalid_deducted_total)

# Plot if data is available
if invalid_deducted_total.sum() > 0:
    plt.figure(figsize=(10, 6))
    invalid_deducted_total.plot(kind='bar', color='lightcoral')

    plt.title('Total Invalid & Deducted Votes by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Invalid Votes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
print("\nNo data available for Invalid or Deducted Votes in the selected categories.")


# Objective 4: Gender Representation in Elections
# =============================

# Filter data only for "Candidates - Contested"
contested_candidates = df[df['Category'] == 'Candidates - Contested']

# Sum gender-wise contested candidates
gender_representation = contested_candidates[['Men', 'Women', 'Third Gender']].sum()

# Display the result
print("\nTotal Candidates Contested by Gender:")
print(gender_representation)

# Plotting
plt.figure(figsize=(8, 6))
colors = ['skyblue', 'orange', 'red']
gender_representation.plot(kind='bar', color=colors)

plt.title('Gender Representation Among Contesting Candidates')
plt.xlabel('Gender')
plt.ylabel('Number of Candidates')
plt.xticks(rotation=0)
plt.tight_layout()

# Show the plot
plt.show()


