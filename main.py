import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_crypto_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table')
            data = []
            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                if columns:
                    coin_name = columns[0].text.strip()
                    price = columns[1].text.strip()
                    change_24h = re.findall(r'[+-]?\d*\.?\d+', columns[2].text.strip())[0]
                    market_cap = columns[3].text.strip()
                    volume_24h = columns[4].text.strip()
                    data.append({'Coin name': coin_name, 'Price': price, 'Change(24h)': change_24h, 'Market cap': market_cap, 'Volume(24h)': volume_24h})
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(e)
    else:
        print("Failed to retrieve data.")

def save_settings(url_entry, settings_label):
    url = url_entry.get()
    with open("settings.txt", "w") as f:
        f.write(url)
    settings_label.config(text=f"Website URL saved: {url}")

def load_settings(settings_label):
    try:
        with open("settings.txt", "r") as f:
            url = f.read()
            settings_label.config(text=f"Website URL loaded: {url}")
    except FileNotFoundError:
        settings_label.config(text="No saved settings found.")

def create_gui(data, tab):
    root = tk.Tk()
    root.title("Cryptocurrency Data")
    
    #Create tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)
    
    #Live Updates Tab
    live_updates_frame = ttk.Frame(notebook)
    notebook.add(live_updates_frame, text="Live Updates")
    
    #Treeview widget
    tree = ttk.Treeview(live_updates_frame, show="headings")
    tree["columns"] = ("Coin name", "Price", "Change(24h)", "Market cap", "Volume(24h)")
    tree.heading("#1", text="Coin name", anchor="w")
    tree.heading("#2", text="Price", anchor="w")
    tree.heading("#3", text="Change(24h)", anchor="w")
    tree.heading("#4", text="Market cap", anchor="w")
    tree.heading("#5", text="Volume(24h)", anchor="w")
    
    #Data insertion to tree view
    if data is not None:
        for index, row in data.iterrows():
            tree.insert("", "end", values=(row["Coin name"], row["Price"], row["Change(24h)"], row["Market cap"], row["Volume(24h)"]))
    
    #Style settings
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview.Heading", font=('Helvetica', 14), background="lightgrey")
    style.configure("Treeview", font=('Helvetica', 12), background="white", foreground="black")
    
    #Add scrollbar
    scrollbar = ttk.Scrollbar(live_updates_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    
    #Pack the treeview widget
    tree.pack(fill="both", expand=True)
    
    #Settings Tab
    settings_frame = ttk.Frame(notebook)
    notebook.add(settings_frame, text="Settings")
    
    #Settings sidebar
    settings_sidebar = tk.Frame(settings_frame, bg="lightgrey", width=150)
    settings_sidebar.pack(fill="y", side="left", padx=10)
    
    #Change Source Label
    change_source_label = tk.Label(settings_sidebar, text="Change Source", bg="lightgrey", font=("Helvetica", 12))
    change_source_label.pack(pady=10, anchor="w")
    
    #Main Settings frame
    main_settings_frame = ttk.Frame(settings_frame)
    main_settings_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    #URL Entry
    url_label = tk.Label(main_settings_frame, text="Enter URL:", font=("Helvetica", 12))
    url_label.grid(row=0, column=0, sticky="w")
    
    url_entry = ttk.Entry(main_settings_frame, width=50)
    url_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")
    
    #Save Settings Button
    save_settings_button = ttk.Button(main_settings_frame, text="Save Settings", command=lambda: save_settings(url_entry, settings_label))
    save_settings_button.grid(row=1, column=0, pady=5, padx=5, sticky="w")
    
    #Load Settings Button
    load_settings_button = ttk.Button(main_settings_frame, text="Load Settings", command=lambda: load_settings(settings_label))
    load_settings_button.grid(row=1, column=1, pady=5, padx=5, sticky="w")
    
    #Settings label
    settings_label = ttk.Label(main_settings_frame, text="")
    settings_label.grid(row=2, columnspan=2, pady=20, padx=10, sticky="w")
    
    root.mainloop()

if __name__ == "__main__":
    url = "https://www.gadgets360.com/finance/crypto-currency-price-in-india-inr-compare-bitcoin-ether-dogecoin-ripple-litecoin"
    data = scrape_crypto_data(url=url)
    create_gui(data, "Live Updates")
