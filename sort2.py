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
data = pd.read_csv(csv, encoding=result['encoding'], skiprows=1, names=headers)

# convert the price columns to strings - this is to remove .0 from the end of the numbers
data.loc[data['price2'].notna(), 'price2'] = data.loc[data['price2'].notna(), 'price2'].astype(int).astype(str)
data.loc[data['price3'].notna(), 'price3'] = data.loc[data['price3'].notna(), 'price3'].astype(int).astype(str)


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

        if len(price2) == 1:
            price2 = '00' + price2
        if len(price2) == 2:
            price2 = '0' + price2
        if len(price3) == 1:
            price3 = '00' + price3
        if len(price3) == 2:
            price3 = '0' + price3

        total_price = price + price2 + price3
        
        # assign the total price to the new "total_price" column for the current row
        data.at[i, 'total_price'] = total_price
        
    return data



def sort_by_price_high(data):
    # convert total_price column to float
    data['total_price'] = data['total_price'].astype(float)
    
    # sort the data by total_price column in descending order
    data_sorted_high = data.sort_values(by=['total_price'], ascending=False)
    
    return f'The 5 highest selling:\n{data_sorted_high.head(5)}\n'
get_total_price(data)


def sort_by_price_low(data):
    # convert total_price column to float
    data['total_price'] = data['total_price'].astype(float)
    # sort the data by total_price column in ascending order
    data_sorted_low = data.sort_values(by=['total_price'], ascending=True)
    return f'The 5 lowest selling:\n{data_sorted_low.head(5)}\n'




def find_the_most_expensive_postcode():
    data['total_price'] = data['total_price'].astype(float)
    grouped = data.groupby('postcode')['total_price'].mean()
    sorted_postcodes = grouped.sort_values(ascending=False)
    most_expensive_postcode = sorted_postcodes.index[0]
    return f'The most expensive postcode is:\n {most_expensive_postcode.split()[0]}\n'



print(sort_by_price_low(data))
print(sort_by_price_high(data))
print(find_the_most_expensive_postcode())
