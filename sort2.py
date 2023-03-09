import pandas as pd
import chardet
import re

csv = 'house_list.csv'

# chardet is package to detect encoding of file
# check encoding type and assign to result variable to use below.
with open(csv, 'rb') as f:
    result = chardet.detect(f.read())

headers = ['address', 'postcode', 'price', 'price2', 'price3', 'total_price']

# pass the encoding to this function from above. 
# error_bad_lines handles any bad formatting but this could cause issues with dataloss. Might be a smart way to format on input...
data = pd.read_csv(csv, encoding=result['encoding'], on_bad_lines='skip',names=headers, header=None)

# convert the price columns to strings - this is to remove .0 from the end of the numbers
data.loc[data['price2'].notna(), 'price2'] = data.loc[data['price2'].notna(), 'price2'].astype(int).astype(str)
data.loc[data['price3'].notna(), 'price3'] = data.loc[data['price3'].notna(), 'price3'].astype(int).astype(str)

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


# get the total price of the house - add the three cols together and return the total in a new col
def get_total_price(data):
    for i in range(len(data)):
        # get the values of the price column and the two columns next to it for the current row
        price = str(data.iloc[i, 2])
        price2 = str(data.iloc[i, 3])
        price3 = str(data.iloc[i, 4])

        # remove non-numeric characters from the price columns
        price = re.sub(r'\D', '', price)
        price2 = re.sub(r'\D', '', price2)
        price3 = re.sub(r'\D', '', price3)

        total_price = price + price2 + price3
        
        # assign the total price to the new "total_price" column for the current row
        data.at[i, 'total_price'] = total_price
        
    return data
get_total_price(data)


data['total_price'] = pd.to_numeric(data['total_price'])
data = data.sort_values(by='total_price', ascending=False)
print(data['total_price'])





# sort the data by price
def sort_by_price_high(data):
    # try except added to check code only applied to string values - error thrown on ints and code not necessary
    try: 
        data['total_price'] = data['total_price'].astype(int)
    except:
        pass
    data_sorted_high = data.sort_values(data['total_price'], ascending=False)
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


# print(data)
# print(sort_by_price_high())
# print(sort_by_price_low())
# print(find_most_expensive_postcode())
