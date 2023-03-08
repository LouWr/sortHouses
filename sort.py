import pandas as pd
import chardet
import re

# chardet is package to detect encoding of file
# this check encoding type to be passed to the pandas read_csv function
with open('house_list.csv', 'rb') as f:
    result = chardet.detect(f.read())  # or readline if the file is large


# pass the encoding to this function from above. 
# error_bad_lines handles any bad formatting but this could cause issues with dataloss. Might be a smart way to format on input...
data = pd.read_csv('data.csv', encoding=result['encoding'], on_bad_lines='skip')

# get the headers - store in List for mutability
headers = list(data.columns.values)
formatted_headers = [s.strip().lower() for s in headers]

# get the index of the headers we want to sort by
price_index = formatted_headers.index('price')
postcode_index = formatted_headers.index('postcode')
address_index = formatted_headers.index('address')

# regex to remove non numeric characters - price includes £ sign and commas etc
def remove_non_numeric(string):
    return re.sub(r'\D', '', string)

# sort the data by price
def sort_by_price_high():
    # try except added to check code only applied to string values - error thrown on ints and code not necessary
    try: 
        data[data.columns[price_index]] = data[data.columns[price_index]].apply(remove_non_numeric).astype(int)
    except:
        pass
    data_sorted_high = data.sort_values(data.columns[price_index], ascending=False)
    return f'The 5 highest selling:\n {data_sorted_high.head(5)}\n'

# sort price from low to high
def sort_by_price_low():
    # try except added to check code only applied to string values - error thrown on ints and code not necessary
    try:
        data[data.columns[price_index]] = data[data.columns[price_index]].apply(remove_non_numeric).astype(int)
    except:
         pass
    data_sorted_low = data.sort_values(data.columns[price_index], ascending=True)
    return f'The 5 lowest selling:\n {data_sorted_low.head(5)}\n'


# find the most expensive postcode
# iloc is used to get the column by index number rather than by string as could be issues with spaces etc
def find_most_expensive_postcode():
    # try except added to check code only applied to string values - error thrown on ints and code not necessary
    try:
        data[data.columns[price_index]] = data[data.columns[price_index]].apply(remove_non_numeric).astype(int)
    except:
        pass
    # group by postcode and get the mean price
    grouped = data.groupby(data[data.columns[postcode_index]])[data.columns[price_index]].mean()
    sorted_prices = grouped.sort_values(ascending=False)
    most_expensive_postcode = sorted_prices.index[0]
    first_characters_of_postcode = most_expensive_postcode.split()
    return f'The most expensive postcode is:\n {first_characters_of_postcode[0]}\n'




print(sort_by_price_high())
print(sort_by_price_low())
print(find_most_expensive_postcode())