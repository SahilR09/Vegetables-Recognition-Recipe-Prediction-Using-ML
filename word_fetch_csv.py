# import pandas as pd
# import numpy as np  # Add this import to handle NaN values
#
# # Step 1: Read the CSV file into a pandas DataFrame
# df = pd.read_csv('/home/daxit/Desktop/ML/IndianFoodDatasetCSV.csv')
#
# # Step 2: Define a function to fetch a specific word based on some condition
# def fetch_word(sentence):
#     if isinstance(sentence, str):  # Check if sentence is a string
#         words = sentence.split()  # Split the sentence into words
#         for word in words:
#             if 'Cabbage' in word:  # Replace 'specific_word' with the word you are looking for
#                 return word
#     return None  # Return None if the specific word is not found or if sentence is not a string
#
# # Step 3: Apply the function to each row in the DataFrame and create a new column
# df['VegNames'] = df['Ingredients'].apply(fetch_word)
#
# # Step 4: Write the modified DataFrame back to CSV
# df.to_csv('/home/daxit/Desktop/ML/IndianFoodDatasetCSV_1.csv', index=False)
#


import pandas as pd

# Step 1: Read the CSV file into a pandas DataFrame
df = pd.read_csv('/home/daxit/Desktop/ML/IndianFoodDatasetCSV.csv')

# Step 2: Define a function to fetch a specific word from a list of words
def fetch_word(sentence):
    if isinstance(sentence, str):  # Check if sentence is a string
        words = sentence.split()  # Split the sentence into words
        word_list = ['Bean', 'Bitter Gourd', 'Bottle Gourd', 'BitterGourd', 'BottleGourd', 'Brinjal', 'Broccoli',
                     'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Cucumber',
                     'Papaya', 'Potato', 'Pumpkin', 'Radish', 'Tomato']
        for word in words:
            if any(veg_word in word for veg_word in word_list):
                return word
    return None  # Return None if no matching word is found or if sentence is not a string

# Step 3: Apply the function to each row in the DataFrame and create a new column
df['VegNames'] = df['Ingredients'].apply(fetch_word)

# Step 4: Write the modified DataFrame back to CSV
df.to_csv('/home/daxit/Desktop/ML/IndianFoodDatasetCSV_1.csv', index=False)
