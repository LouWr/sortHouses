import tkinter as tk
from tkinter import filedialog
import chardet
import pandas as pd
import re

# Create a Tkinter window
window = tk.Tk()


def open_file():
    # User dropped file - assign filename below
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
        data = pd.read_csv(filepath, encoding=result['encoding'], on_bad_lines='skip', index_col=False)

        # get the headers - store in List for mutability
        headers = list(data.columns.values)
        formatted_headers = [s.strip().lower() for s in headers]

        # get the index of the headers we want to sort by
        price_index = formatted_headers.index('price')
        postcode_index = formatted_headers.index('postcode')
        address_index = formatted_headers.index('address')

        # Define functions to manipulate the data
        def remove_non_numeric(string):
            return re.sub(r'\D', '', string)

        def sort_by_price_high():
            # try except added to check code only applied to string values - error thrown on ints and code not necessary
            try: 
                data[data.columns[price_index]] = data[data.columns[price_index]].apply(remove_non_numeric).astype(int)
            except:
                pass
            data_sorted_high = data.sort_values(data.columns[price_index], ascending=False)
            return f'The 5 highest selling:\n {data_sorted_high.head(5).to_string(index=False)}\n'

        def sort_by_price_low():
            # try except added to check code only applied to string values - error thrown on ints and code not necessary
            try:
                data[data.columns[price_index]] = data[data.columns[price_index]].apply(remove_non_numeric).astype(int)
            except:
                 pass
            data_sorted_low = data.sort_values(data.columns[price_index], ascending=True)
            return f'The 5 lowest selling:\n {data_sorted_low.head(5).to_string(index=False)}\n'
        
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
            
        # onClick button functions
        def handle_high_click():
            result_text.delete("1.0", tk.END) # clear previous result
            result_text.insert(tk.END, sort_by_price_high())

        def handle_low_click():
            result_text.delete("1.0", tk.END) # clear previous result
            result_text.insert(tk.END, sort_by_price_low())

        def handle_most_expensive_postcode():
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, find_most_expensive_postcode())

        # add buttons to window and add commands
        high_button = tk.Button(window, text="Sort by Price (High to Low)", command=handle_high_click)
        high_button.pack()

        low_button = tk.Button(window, text="Sort by Price (Low to High)", command=handle_low_click)
        low_button.pack()

        most_expensive_postcode_button = tk.Button(window, text="Find Most Expensive Postcode", command=handle_most_expensive_postcode)
        most_expensive_postcode_button.pack()

# button to open file - command + text
open_button = tk.Button(window, text="Open File", command=open_file)
open_button.pack()

# text box to displayu
result_text = tk.Text(window, height=50, width=100)
result_text.pack()


window.mainloop()
