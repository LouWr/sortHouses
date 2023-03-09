import tkinter as tk
from tkinter import filedialog
import chardet
import pandas as pd
import re

# create window
window = tk.Tk()

def open_file():
    # file path = user droped file
    filepath = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")],
        title="Select a CSV file"
    )
    if filepath:
        # chardet is package to detect encoding of file
        # check encoding type and assign to result variable to use below.
        with open(filepath, 'rb') as f:
            result = chardet.detect(f.read())
        
        # pass the encoding to this function from above. 
        # error_bad_lines handles any bad formatting but this could cause issues with dataloss. Might be a smart way to format on input...
        headers = ['address', 'postcode', 'price', 'price2', 'price3', 'total_price']
        data = pd.read_csv(filepath, encoding=result['encoding'], skiprows=1, names=headers)

        data.loc[data['price2'].notna(), 'price2'] = data.loc[data['price2'].notna(), 'price2'].astype(int).astype(str)
        data.loc[data['price3'].notna(), 'price3'] = data.loc[data['price3'].notna(), 'price3'].astype(int).astype(str)

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
        get_total_price(data)

        def sort_by_price_high():
            # convert total_price column to float
            data['total_price'] = data['total_price'].astype(float)
            
            # sort the data by total_price column in descending order
            data_sorted_high = data.sort_values(by=['total_price'], ascending=False)
            
            return f'The 5 highest selling:\n{data_sorted_high.head(5)}\n'


        def sort_by_price_low():
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
            
        #handle clicjk functions for buttons
        def handle_high_click():
            result_text.delete("1.0", tk.END) # clear previous result
            result_text.insert(tk.END, sort_by_price_high())

        def handle_low_click():
            result_text.delete("1.0", tk.END) # clear previous result
            result_text.insert(tk.END, sort_by_price_low())

        def handle_most_expensive_postcode():
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, find_the_most_expensive_postcode())

        # buttons to manipulate the data
        high_button = tk.Button(window, text="Sort by Price (High to Low)", command=handle_high_click)
        high_button.pack()

        low_button = tk.Button(window, text="Sort by Price (Low to High)", command=handle_low_click)
        low_button.pack()

        most_expensive_postcode_button = tk.Button(window, text="Find Most Expensive Postcode", command=handle_most_expensive_postcode)
        most_expensive_postcode_button.pack()

# button to open the file dialog
open_button = tk.Button(window, text="Open File", command=open_file)
open_button.pack()

# text box to display the results ----
result_text = tk.Text(window, height=50, width=100)
result_text.pack()

# event loop
window.mainloop()