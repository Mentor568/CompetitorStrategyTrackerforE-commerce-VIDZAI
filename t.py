import streamlit as st

# Define the coffee menu and prices
coffee_menu = {
    "Espresso": 100,
    "Cappuccino": 150,
    "Latte": 200,
    "Mocha": 250,
    "Americano": 120
}

# Function to display the total bill
def display_bill(selected_coffees):
    total_bill = 0
    st.write("## Order Summary")
    for coffee, qty in selected_coffees.items():
        if qty > 0:
            cost = coffee_menu[coffee] * qty
            st.write(f"{coffee}: {qty} x {coffee_menu[coffee]} = {cost}")
            total_bill += cost
    st.write("## Total Bill:", total_bill)

# Streamlit app layout
st.title("Welcome to the Coffee Shop")
st.write("### Please select your coffee:")

# Dictionary to store the selected coffees and their quantities
selected_coffees = {}

# Display the coffee menu
for coffee, price in coffee_menu.items():
    qty = st.number_input(f"{coffee} ({price})", min_value=0, step=1)
    selected_coffees[coffee] = qty

# Order Now button
if st.button("Order Now"):
    display_bill(selected_coffees)
