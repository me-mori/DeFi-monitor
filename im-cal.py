import math
import tkinter as tk
from tkinter import messagebox

# Function to calculate liquidity position
def calculate_liquidity_position():
    try:
        # Get inputs from the UI
        current_price = float(entry_current_price.get())
        initial_sol = float(entry_initial_sol.get())
        initial_usdc = float(entry_initial_usdc.get())
        initial_price = float(entry_initial_price.get())

        # Step 1: Calculate the constant k
        k = initial_sol * initial_usdc

        # Step 2: Calculate the current amount of SOL (x) and USDC (y)
        current_sol = math.sqrt(k / current_price)
        current_usdc = math.sqrt(k * current_price)

        # Step 3: Calculate the value of the pool position
        pool_value = (current_sol * current_price) + current_usdc

        # Step 4: Calculate the value of holding
        holding_value = (initial_sol * current_price) + initial_usdc

        # Step 5: Calculate impermanent loss
        impermanent_loss = (pool_value - holding_value) / holding_value

        # Display results in a messagebox
        result_message = (
            f"Current Amount of SOL: {current_sol:.6f}\n"
            f"Current Amount of USDC: {current_usdc:.6f}\n"
            f"Value of Pool Position: {pool_value:.6f} USDC\n"
            f"Value of Holding: {holding_value:.6f} USDC\n"
            f"Impermanent Loss: {impermanent_loss * 100:.6f}%"
        )
        messagebox.showinfo("Results", result_message)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers in all fields.")

# Create the main window
root = tk.Tk()
root.title("Liquidity Pool Calculator")

# Create input fields and labels
label_current_price = tk.Label(root, text="Current Price of SOL/USDC:")
label_current_price.grid(row=0, column=0, padx=10, pady=5)
entry_current_price = tk.Entry(root)
entry_current_price.grid(row=0, column=1, padx=10, pady=5)

label_initial_sol = tk.Label(root, text="Amount of SOL Initially Deposited:")
label_initial_sol.grid(row=1, column=0, padx=10, pady=5)
entry_initial_sol = tk.Entry(root)
entry_initial_sol.grid(row=1, column=1, padx=10, pady=5)

label_initial_usdc = tk.Label(root, text="Amount of USDC Initially Deposited:")
label_initial_usdc.grid(row=2, column=0, padx=10, pady=5)
entry_initial_usdc = tk.Entry(root)
entry_initial_usdc.grid(row=2, column=1, padx=10, pady=5)

label_initial_price = tk.Label(root, text="Price of SOL/USDC at Time of Deposit:")
label_initial_price.grid(row=3, column=0, padx=10, pady=5)
entry_initial_price = tk.Entry(root)
entry_initial_price.grid(row=3, column=1, padx=10, pady=5)

# Create a button to calculate
calculate_button = tk.Button(root, text="Calculate", command=calculate_liquidity_position)
calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()