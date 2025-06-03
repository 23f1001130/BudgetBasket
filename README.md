# SmartGrocery – A Smart Budgeting Grocery Assistant

#### Video Demo: [URL HERE](https://www.youtube.com/watch?v=Gfta35sluH0)

#### Description:

SmartGrocery is a Python-based command-line budgeting assistant that helps users manage grocery shopping efficiently while staying within their defined budget. The goal of this project is to promote conscious spending and provide meaningful insights into one's grocery expenses. Users can add purchase items one at a time and the system automatically validates the inputs, updates total expenditure and alerts if the user is running low on budget or has exceeded it.

This project was designed with simplicity, functionality and user-friendliness in mind, especially for those who want a lightweight tool without needing a GUI. SmartGrocery supports core financial awareness and gives users a clear breakdown of their purchases and budget usage.

---

### Files and Functionality:

**1. `project.py`**  
This is the main logic file of the project and includes three key functions:
- `validate_purchase_input(product_name, price, quantity)`: Ensures that the input values are valid—e.g., no empty product names, and price/quantity must be non-negative numbers.
- `calculate_budget_status(budget, total_spent)`: Calculates the remaining budget, usage percentage, and triggers flags for low budget (10–20% remaining), critical budget (<10% remaining), or over budget.
- `format_purchase_summary(purchases)`: Neatly formats and displays a summary of all recorded purchases in a table-like structure with a total spent amount.

**2. `test_project.py`**  
This file contains comprehensive unit tests written using `pytest`. The test suite verifies:
- The correctness of input validation for a wide range of edge cases.
- The accuracy of budget calculations including over-budget, low-budget, and critical-budget conditions.
- The output formatting of the purchase summary.
- Edge scenarios like zero budget, very small and large values, and special characters in product names.

---

### How It Works:

Users are prompted to enter purchase details such as item name, price per unit, and quantity. The system keeps a running total and updates the user on how much of their budget has been used. The program is intelligent enough to:
- Reject invalid inputs with immediate feedback.
- Display warnings when the user is nearing their budget threshold.
- Format a clean purchase report that can be easily read or shared.

If the budget usage exceeds 100%, it clearly marks the purchase as “over budget,” making it easier for users to make financial adjustments next time. This allows SmartGrocery to act not just as a recording tool, but as a proactive budgeting partner.

---

### Design Considerations:

Several design decisions were considered carefully:
- **Simplicity over complexity**: The tool avoids GUI or database layers to keep the scope focused on the core budgeting logic.
- **Command-line interface**: Chosen for ease of portability and because it's ideal for early-stage prototypes or users who prefer lightweight tools.
- **Validation-first approach**: To ensure the user cannot corrupt data by entering invalid or illogical values.
- **Modular testing**: All functions were written in a way that makes unit testing straightforward and reliable.

---


### Conclusion:

SmartGrocery is a compact but powerful budgeting utility that blends user-centric design with Python’s functional capabilities. With clean validation, budget monitoring, and structured summaries, it serves as an ideal project for demonstrating applied Python, testing best practices, and simple but effective budgeting logic. This project helped me understand how to break down real-world problems into clean, testable Python modules and how to think critically about user experience even in a terminal environment.
