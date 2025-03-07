import streamlit as st
import math

# Title of the app
st.title("Liquidity Pool Calculator with Smooth Conversion")

# Input fields
st.header("Input Parameters")
current_price = st.number_input("Current Price of SOL/USDC", value=200.0)
initial_sol = st.number_input("Amount of SOL Initially Deposited", value=1.0)
initial_usdc = st.number_input("Amount of USDC Initially Deposited", value=151.0)
initial_price = st.number_input("Price of SOL/USDC at Time of Deposit", value=151.0)
lower_price = st.number_input("Lower Price Bound of Your Liquidity Range", value=100.0)
upper_price = st.number_input("Upper Price Bound of Your Liquidity Range", value=200.0)

# Function to calculate liquidity position
def calculate_liquidity_position(current_price, initial_sol, initial_usdc, initial_price, lower_price, upper_price):
    # Calculate liquidity constant L
    L_sol = initial_sol / (1 / math.sqrt(initial_price) - 1 / math.sqrt(upper_price))
    L_usdc = initial_usdc / (math.sqrt(initial_price) - math.sqrt(lower_price))
    L = min(L_sol, L_usdc)  # Use the smaller value to ensure consistency

    # Calculate current amounts of SOL and USDC
    if lower_price <= current_price <= upper_price:
        # Price is within the range: use smooth conversion formulas
        current_sol = L * (1 / math.sqrt(current_price) - 1 / math.sqrt(upper_price))
        current_usdc = L * (math.sqrt(current_price) - math.sqrt(lower_price))
        pool_value = (current_sol * current_price) + current_usdc
    elif current_price > upper_price:
        # Price is above the range: liquidity is fully in USDC
        current_sol = 0
        current_usdc = initial_usdc + (initial_sol * upper_price)
        pool_value = current_usdc
    else:
        # Price is below the range: liquidity is fully in SOL
        current_sol = initial_sol + (initial_usdc / lower_price)
        current_usdc = 0
        pool_value = current_sol * current_price

    # Calculate the value of holding
    holding_value = (initial_sol * current_price) + initial_usdc

    # Calculate impermanent loss (only if price is within the range)
    if lower_price <= current_price <= upper_price:
        impermanent_loss = (pool_value - holding_value) / holding_value
    else:
        impermanent_loss = 0  # No impermanent loss outside the range

    # Return results
    return {
        "current_sol": current_sol,
        "current_usdc": current_usdc,
        "pool_value": pool_value,
        "holding_value": holding_value,
        "impermanent_loss": impermanent_loss
    }

# Calculate button
if st.button("Calculate"):
    results = calculate_liquidity_position(current_price, initial_sol, initial_usdc, initial_price, lower_price, upper_price)

    # Display results
    st.header("Results")
    st.write(f"Current Amount of SOL: {results['current_sol']:.6f}")
    st.write(f"Current Amount of USDC: {results['current_usdc']:.6f}")
    st.write(f"Value of Pool Position: {results['pool_value']:.6f} USDC")
    st.write(f"Value of Holding: {results['holding_value']:.6f} USDC")
    st.write(f"Impermanent Loss: {results['impermanent_loss'] * 100:.6f}%")