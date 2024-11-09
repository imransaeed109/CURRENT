import streamlit as st

# Title of the app
with st.sidebar:
    st.title("Current Design Calculator")

# Step 1: Input fields for user to calculate the current
with st.sidebar:
    load = st.number_input("Enter Load", min_value=0.0, format="%.2f")
    load_type = st.selectbox("Load Type", ("Watt", "VA"))
    phase_type = st.selectbox("Phase Type", ("Single Phase", "Three Phase"))
    voltage = st.number_input("Enter Voltage (V)", min_value=0.0, format="%.2f")
    power_factor = st.number_input("Enter Power Factor", min_value=0.0, max_value=1.0, format="%.2f")
  
    # Calculate current based on phase type
    if st.button("Calculate Current"):
        if load_type == "Watt":
            effective_load = load
        else:
            effective_load = load * power_factor  # Assuming VA input requires conversion to effective load (Watt)

        if phase_type == "Single Phase":
            current = effective_load / (voltage * power_factor)
        elif phase_type == "Three Phase":
            current = effective_load / (1.732 * voltage * power_factor)

        st.write(f"The calculated nominal current based on input load is: {current:.2f} A")

 # Step 2: Adjustment for Ambient Temperature
with st.sidebar:
    st.header("Adjustment for Ambient Temperature")
    nominal_current = st.number_input("Enter Nominal Current (A)", min_value=0.0, format="%.2f")
    ambient_temp = st.selectbox("Ambient Temperature (°C)", [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60])
    insulation_type = st.selectbox("Insulation Type", ["PVC", "XLPE", "Mineral"])

    # Nested option for Mineral insulation type
    if insulation_type == "Mineral":
        mineral_option = st.radio("Mineral Type", ["PVC covered or bare and exposed to touch", "Bare and not exposed to touch"])

    # Define adjustment factors
    adjustment_factors = {
        (10, "PVC"):1.10, (15, "PVC"):1.05, (20, "PVC"):1.00, (25, "PVC"):0.95, (30, "PVC"):0.89, (35, "PVC"):0.84, (40, "PVC"):0.77, (45, "PVC"): 0.79, (50, "PVC"): 0.71, (55, "PVC"): 0.61, (60, "PVC"): 0.51,
        (10, "XLPE"):1.07, (15, "XLPE"):1.04, (20, "XLPE"):1.00, (25, "XLPE"):0.96, (30, "XLPE"):0.93, (35, "XLPE"):0.89, (40, "XLPE"):0.85, (45, "XLPE"): 0.87, (50, "XLPE"): 0.82, (55, "XLPE"): 0.76, (60, "XLPE"): 0.71,
        (45, "Mineral", "PVC covered or bare and exposed to touch"): 0.78,
        (50, "Mineral", "PVC covered or bare and exposed to touch"): 0.67,
        (55, "Mineral", "PVC covered or bare and exposed to touch"): 0.57,
        (60, "Mineral", "PVC covered or bare and exposed to touch"): 0.45,
        (45, "Mineral", "Bare and not exposed to touch"): 0.88,
        (50, "Mineral", "Bare and not exposed to touch"): 0.84,
        (55, "Mineral", "Bare and not exposed to touch"): 0.80,
        (60, "Mineral", "Bare and not exposed to touch"): 0.75,
    }

    # Get the adjustment factor
    adjustment_factor = adjustment_factors[(ambient_temp, insulation_type, mineral_option)] if insulation_type == "Mineral" else adjustment_factors[(ambient_temp, insulation_type)]
    adjusted_current = nominal_current / adjustment_factor
    st.write(f"Adjusted Current for Ambient Conditions: {adjusted_current:.2f} A")

# Step 3: Correction Factors for Group of More Than Three Single-Core Cables
with st.sidebar:
    st.header("Correction Factors for Group of More Than Three Single-Core Cables")
    num_conductors = st.selectbox("Select Number of Conductors", [6, 8, 10, 12, 16, 20, 24, 28, 32, 36, 40])
    correction_factors = {
        6: 0.69, 8: 0.62, 10: 0.59, 12: 0.55, 16: 0.51,
        20: 0.48, 24: 0.43, 28: 0.41, 32: 0.39, 36: 0.38, 40: 0.36
    }
    correction_factor = correction_factors[num_conductors]
    final_adjusted_current = adjusted_current / correction_factor
    st.write(f"Final Adjusted Current for Group of Cables: {final_adjusted_current:.2f} A") 
    
# Cross-sectional area ratings data
cross_sectional_area_ratings = {
    1: [11, 10.5, 13.5, 12, 15.5, 14, None, None, None, None, None],
    1.5: [14.5, 13.5, 17.5, 15.5, 20, 18, None, None, None, None, None],
    2.5: [20, 18, 24, 21, 27, 25, None, None, None, None, None],
    4: [26, 24, 32, 28, 37, 33, None, None, None, None, None],
    6: [34, 31, 41, 36, 47, 43, None, None, None, None, None],
    10: [46, 42, 57, 50, 65, 59, None, None, None, None, None],
    16: [61, 56, 76, 68, 87, 79, None, None, None, None, None],
    25: [80, 73, 101, 89, 114, 104, 131, 114, 110, 146, 130],
    35: [99, 89, 125, 110, 141, 129, 162, 143, 137, 181, 162],
    50: [119, 108, 151, 134, 182, 167, 196, 174, 167, 219, 197],
    70: [151, 136, 192, 171, 234, 214, 251, 225, 216, 281, 254],
    95: [182, 164, 232, 207, 284, 261, 304, 275, 264, 341, 311],
    120: [210, 188, 269, 239, 300, 303, 352, 321, 308, 396, 362],
    150: [240, 216, 300, 262, 381, 349, 406, 372, 356, 456, 419],
    185: [273, 245, 341, 296, 436, 400, 463, 427, 409, 521, 480],
    240: [231, 286, 400, 346, 515, 472, 546, 507, 485, 615, 569],
    300: [367, 328, 458, 394, 594, 545, 629, 587, 561, 709, 659],
    400: [None, None, 546, 467, 694, 634, 754, 689, 656, 852, 795],
    500: [None, None, 626, 533, 792, 723, 868, 789, 749, 982, 920],
    630: [None, None, 720, 611, 904, 826, 1005, 905, 855, 1138, 1070],
    800: [None, None, None, None, 1030, 943, 1086, 1020, 971, 1265, 1188],
    1000: [None, None, None, None, 1154, 1058, 1216, 1149, 1079, 1420, 1337],
}

# Step 4: Installation Method Options
st.header("Single core PVC insulated cables, non-armoured, with or without sheath (COPPER CONDUCTORS)")

# Installation Method Selection
installation_method = st.selectbox("Select Installation Method", [
    "Method 1 (enclosed in conduit in thermally insulating well)",
    "Method 2, 3, 4 & 5 (enclosed in conduit on wall or in trunking)",
    "Method 6 (directly to the surface of wall or structure)",
    "Method 8, 9 & 10 (in free air or on a ventilated cable tray)"
])

# Mapping each installation method to the correct index range
if installation_method == "Method 1 (enclosed in conduit in thermally insulating well)":
    method_index = st.selectbox("Choose number of cables:", ["2 cables Single-phase a.c.", "3 or 4 cables Three-phase a.c."])
    method_index = 0 if method_index == "2 cables Single-phase a.c." else 1

elif installation_method == "Method 2, 3, 4 & 5 (enclosed in conduit on wall or in trunking)":
    method_index = st.selectbox("Choose number of cables:", ["2 cables Single-phase a.c.", "3 or 4 cables Three-phase a.c."])
    method_index = 2 if method_index == "2 cables Single-phase a.c." else 3

elif installation_method == "Method 6 (directly to the surface of wall or structure)":
    method_index = st.selectbox("Choose cable configuration", [
        "2 cables Single-phase a.c. flat and touching",
        "3 or 4 cables Three-phase a.c. flat and touching or trefoil"
    ])
    method_index = 4 if method_index == "2 cables Single-phase a.c. flat and touching" else 5

elif installation_method == "Method 8, 9 & 10 (in free air or on a ventilated cable tray)":
    spacing_option = st.selectbox("Select Spacing Option", [
        "Touching", 
        "Spaced by One Diameter (2 cables, single-phase a.c. or 3 cables three-phase a.c. flat)"
    ])
    
    if spacing_option == "Touching":
        touching_option = st.selectbox(
            "Select Configuration for Touching",
            ["2 cables, Single-phase a.c. Flat", "3 cables, Three-phase a.c. Flat", "3 cables, Three-phase a.c. Trefoil"]
        )
        method_index = 6 if touching_option == "2 cables, Single-phase a.c. Flat" else 7 if touching_option == "3 cables, Three-phase a.c. Flat" else 8
    else:
        spacing_arrangement = st.selectbox("Select Arrangement for Spacing", ["Horizontal", "Vertical"])
        method_index = 9 if spacing_arrangement == "Horizontal" else 10

# New input for current, to find suitable cross-sectional area
current = st.number_input("Enter Current (A)", min_value=0.0, format="%.2f")

# Determine the minimum cross-sectional area that can handle the entered current
suitable_area = None
for area, ratings in cross_sectional_area_ratings.items():
    if ratings[method_index] is not None and ratings[method_index] >= current:
        suitable_area = area
        break

if suitable_area:
    st.write(f"The minimum recommended cross-sectional area for {current} A is: {suitable_area} mm²")
else:
    st.write("No suitable cross-sectional area found for the given current and configuration.")
