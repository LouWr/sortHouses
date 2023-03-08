import pandas as pd
import chardet
import re

csv = 'house_list.csv'

# chardet is package to detect encoding of file
# check encoding type and assign to result variable to use below.
with open(csv, 'rb') as f:
    result = chardet.detect(f.read())


# pass the encoding to this function from above. 
# error_bad_lines handles any bad formatting but this could cause issues with dataloss. Might be a smart way to format on input...
data = pd.read_csv(csv, encoding=result['encoding'], on_bad_lines='skip', index_col=False)



# drop empty cols
data = data.dropna(axis=1, how='all')

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
def find_most_expensive_postcode():
    # try except added to check code only applied to string values - error thrown on ints and code not necessary
    try:
        data[data.columns[price_index]] = data[data.columns[price_index]].apply(remove_non_numeric).astype(int)
    except:
        pass
    # group by postcode and get the mean price - multiple houses in same postcode might be sold at differnet price tags
    grouped = data.groupby(data[data.columns[postcode_index]])[data.columns[price_index]].mean()
    sorted_prices = grouped.sort_values(ascending=False)
    most_expensive_postcode = sorted_prices.index[0]
    #convert to array to return first half below.
    first_characters_of_postcode = most_expensive_postcode.split()
    return f'The most expensive postcode is:\n {first_characters_of_postcode[0]}\n'


print(data)
# print(sort_by_price_high())
# print(sort_by_price_low())
# print(find_most_expensive_postcode())