"""
SmartGrocery - Budget-Aware Grocery Shopping Tracker
CS50P Final Project Implementation
File: project.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List, Dict


class GroceryTracker:
    """Main class to handle grocery shopping tracking."""

    def __init__(self):
        self.budget = 0.0
        self.purchases = []
        self.remaining_budget = 0.0


def get_user_budget() -> float:
    """Get and validate the user's total grocery budget."""
    while True:
        try:
            budget = float(input("Enter your total grocery budget: $"))
            if budget < 0:
                print("Budget cannot be negative. Please enter a positive amount.")
                continue
            return budget
        except ValueError:
            print("Please enter a valid number.")


def validate_purchase_input(product_name: str, unit_price: float, quantity: float) -> bool:
    """Validate purchase input data and return True if valid, False otherwise."""
    if not product_name or product_name.strip() == "":
        return False
    if unit_price < 0:
        return False
    if quantity < 0:
        return False
    return True


def calculate_budget_status(budget: float, total_spent: float) -> Dict[str, any]:
    """Calculate and return budget status information."""
    remaining = budget - total_spent
    percentage_used = (total_spent / budget * 100) if budget > 0 else 0

    status = {
        'remaining_budget': remaining,
        'percentage_used': percentage_used,
        'is_over_budget': remaining < 0,
        'is_low_budget': remaining < (budget * 0.2) and remaining > 0,
        'is_critical_budget': remaining < (budget * 0.1) and remaining > 0
    }

    return status


def format_purchase_summary(purchases: List[Dict]) -> str:
    """Format purchases into a readable summary string."""
    if not purchases:
        return "No purchases made yet."

    summary_lines = []
    summary_lines.append("PURCHASE SUMMARY")
    summary_lines.append("=" * 70)
    summary_lines.append(f"{'Product Name':<20} {'Qty':<8} {'Unit Price':<12} {'Total Price':<12}")
    summary_lines.append("-" * 70)

    total_spent = 0
    for purchase in purchases:
        line = f"{purchase['name']:<20} {purchase['quantity']:<8.1f} ${purchase['unit_price']:<11.2f} ${purchase['total_price']:<11.2f}"
        summary_lines.append(line)
        total_spent += purchase['total_price']

    summary_lines.append("-" * 70)
    summary_lines.append(f"{'TOTAL SPENT:':<40} ${total_spent:.2f}")

    return "\n".join(summary_lines)


def add_purchase(tracker: GroceryTracker) -> None:
    """Handle adding new purchases to the tracker."""
    print("\n" + "="*60)
    print("ADD PURCHASE")
    print("="*60)

    display_budget_status(tracker)

    while True:
        try:
            # Get product details
            product_name = input("\nEnter product name: ").strip()
            if not product_name:
                print("Product name cannot be empty.")
                continue

            unit_price = float(input("Enter unit price: $"))
            quantity = float(input("Enter quantity: "))

            # Validate input
            if not validate_purchase_input(product_name, unit_price, quantity):
                print("Invalid input. Price and quantity must be non-negative.")
                continue

            # Calculate total
            total_price = unit_price * quantity

            print(f"\nTotal cost: ${total_price:.2f}")
            print(f"Current remaining budget: ${tracker.remaining_budget:.2f}")

            # Check budget with enhanced error message
            if total_price > tracker.remaining_budget:
                print(f"\n🚨 ERROR: YOU ARE RUNNING OUT OF MONEY! 🚨")
                print(f"This purchase (${total_price:.2f}) exceeds your remaining budget (${tracker.remaining_budget:.2f})")
                print(f"You need ${total_price - tracker.remaining_budget:.2f} more to afford this item.")
                confirm = input("Do you want to proceed anyway and go over budget? (y/n): ").lower()
                if confirm != 'y':
                    print("Purchase cancelled.")
                    break

            # Add purchase
            purchase = {
                'name': product_name,
                'quantity': quantity,
                'unit_price': unit_price,
                'total_price': total_price
            }
            tracker.purchases.append(purchase)
            tracker.remaining_budget -= total_price

            print(f"✅ Added {quantity} x {product_name} for ${total_price:.2f}")
            print(f"💰 Updated remaining budget: ${tracker.remaining_budget:.2f}")

            # Show warning if budget is getting low
            budget_status = calculate_budget_status(tracker.budget, sum(p['total_price'] for p in tracker.purchases))
            if budget_status['is_critical_budget']:
                print(f"⚠️  Critical: Only ${tracker.remaining_budget:.2f} left in budget!")
            elif budget_status['is_low_budget']:
                print(f"⚠️  Warning: Only ${tracker.remaining_budget:.2f} left in budget!")
            elif budget_status['is_over_budget']:
                print(f"🚨 ALERT: You have exceeded your budget by ${abs(tracker.remaining_budget):.2f}!")

            # Show updated table
            print("\n" + format_purchase_summary(tracker.purchases))
            display_budget_status(tracker)

            # Ask if user wants to add more
            more = input("\nAdd another item? (y/n): ").lower()
            if more != 'y':
                break

        except ValueError:
            print("Please enter valid numbers for price and quantity.")


def view_statistics(tracker: GroceryTracker) -> None:
    """Generate and display spending statistics with charts."""
    print("\n" + "="*60)
    print("SPENDING STATISTICS")
    print("="*60)

    if not tracker.purchases:
        print("No purchases to analyze yet.")
        return

    # Calculate basic stats
    total_items = len(tracker.purchases)
    total_spent = sum(p['total_price'] for p in tracker.purchases)
    budget_status = calculate_budget_status(tracker.budget, total_spent)

    print(f"Total items purchased: {total_items}")
    print(f"Total amount spent: ${total_spent:.2f}")
    print(f"Average per item: ${total_spent/total_items:.2f}")
    print(f"Budget used: {budget_status['percentage_used']:.1f}%")

    # Create DataFrame for analysis
    df = pd.DataFrame(tracker.purchases)

    # Generate charts
    try:
        plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('SmartGrocery - Shopping Analysis Dashboard', fontsize=16, fontweight='bold')

        # Chart 1: Spending by Product (Bar Chart)
        product_spending = df.groupby('name')['total_price'].sum().sort_values(ascending=False)
        ax1.bar(range(len(product_spending)), product_spending.values, color='skyblue')
        ax1.set_title('Spending by Product', fontweight='bold')
        ax1.set_xlabel('Products')
        ax1.set_ylabel('Amount Spent ($)')
        ax1.set_xticks(range(len(product_spending)))
        ax1.set_xticklabels(product_spending.index, rotation=45, ha='right')

        # Chart 2: Budget Usage (Pie Chart)
        remaining = max(0, tracker.remaining_budget)
        spent = total_spent
        if remaining > 0:
            sizes = [spent, remaining]
            labels = [f'Spent\n${spent:.2f}', f'Remaining\n${remaining:.2f}']
            colors = ['#ff9999', '#90EE90']
        else:
            over_budget = abs(tracker.remaining_budget)
            sizes = [tracker.budget, over_budget]
            labels = [f'Original Budget\n${tracker.budget:.2f}', f'Over Budget\n${over_budget:.2f}']
            colors = ['#ff9999', '#ff4444']

        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title(f'Budget Usage - {budget_status["percentage_used"]:.1f}% Used', fontweight='bold')

        # Chart 3: Price Distribution (Histogram)
        ax3.hist(df['total_price'], bins=min(10, len(df)), color='lightcoral', alpha=0.7, edgecolor='black')
        ax3.set_title('Price Distribution of Purchases', fontweight='bold')
        ax3.set_xlabel('Purchase Amount ($)')
        ax3.set_ylabel('Frequency')
        ax3.grid(True, alpha=0.3)

        # Chart 4: Quantity vs Price Scatter Plot
        scatter = ax4.scatter(df['quantity'], df['unit_price'],
                             s=df['total_price']*10, alpha=0.6,
                             c=df['total_price'], cmap='viridis')
        ax4.set_title('Quantity vs Unit Price\n(Bubble size = Total Spent)', fontweight='bold')
        ax4.set_xlabel('Quantity')
        ax4.set_ylabel('Unit Price ($)')
        ax4.grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=ax4, label='Total Price ($)')

        plt.tight_layout()

        # Save the chart
        chart_filename = f"grocery_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
        print(f"\n📊 Charts saved as: {chart_filename}")

        # Show the charts
        plt.show()

    except Exception as e:
        print(f"Error generating charts: {e}")

    # Additional statistics
    print(f"\n📈 DETAILED ANALYSIS:")
    print(f"   Most expensive item: {df.loc[df['total_price'].idxmax(), 'name']} (${df['total_price'].max():.2f})")
    print(f"   Cheapest item: {df.loc[df['total_price'].idxmin(), 'name']} (${df['total_price'].min():.2f})")
    print(f"   Average unit price: ${df['unit_price'].mean():.2f}")
    print(f"   Total quantity purchased: {df['quantity'].sum():.1f} units")


def generate_csv_report(tracker: GroceryTracker) -> str:
    """Generate a CSV report of all purchases."""
    print("\n" + "="*60)
    print("GENERATING CSV REPORT")
    print("="*60)

    if not tracker.purchases:
        print("No purchases to export.")
        return ""

    # Create DataFrame from purchases
    df = pd.DataFrame(tracker.purchases)

    # Add additional columns for better reporting
    df['purchase_date'] = datetime.now().strftime('%Y-%m-%d')
    df['purchase_time'] = datetime.now().strftime('%H:%M:%S')

    # Reorder columns for better readability
    df = df[['purchase_date', 'purchase_time', 'name', 'quantity', 'unit_price', 'total_price']]

    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f"grocery_report_{timestamp}.csv"

    try:
        # Save to CSV
        df.to_csv(csv_filename, index=False)

        print(f"✅ CSV report generated successfully!")
        print(f"📄 Filename: {csv_filename}")
        print(f"📊 Total records: {len(df)}")

        # Show preview of the CSV content
        print(f"\n📋 REPORT PREVIEW:")
        print("-" * 80)
        print(df.to_string(index=False))
        print("-" * 80)

        # Summary statistics in the report
        total_spent = df['total_price'].sum()
        total_items = len(df)
        avg_per_item = total_spent / total_items if total_items > 0 else 0

        print(f"\n📈 REPORT SUMMARY:")
        print(f"   Total Items: {total_items}")
        print(f"   Total Spent: ${total_spent:.2f}")
        print(f"   Average per Item: ${avg_per_item:.2f}")
        print(f"   Budget Used: {(total_spent/tracker.budget)*100:.1f}%")

        # Create a summary CSV as well
        summary_data = {
            'report_date': [datetime.now().strftime('%Y-%m-%d')],
            'report_time': [datetime.now().strftime('%H:%M:%S')],
            'original_budget': [tracker.budget],
            'total_spent': [total_spent],
            'remaining_budget': [tracker.remaining_budget],
            'total_items': [total_items],
            'average_per_item': [avg_per_item],
            'budget_used_percentage': [(total_spent/tracker.budget)*100]
        }

        summary_df = pd.DataFrame(summary_data)
        summary_filename = f"grocery_summary_{timestamp}.csv"
        summary_df.to_csv(summary_filename, index=False)

        print(f"📊 Summary report also saved as: {summary_filename}")

        return csv_filename

    except Exception as e:
        print(f"Error generating CSV report: {e}")
        return ""


def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "="*50)
    print("SMARTGROCERY - MAIN MENU")
    print("="*50)
    print("1. Add Purchase")
    print("2. View Statistics")
    print("3. Generate CSV Report")
    print("4. Exit")
    print("-"*50)


def display_budget_status(tracker: GroceryTracker) -> None:
    """Display current budget status with enhanced real-time information."""
    total_spent = sum(p['total_price'] for p in tracker.purchases)
    budget_status = calculate_budget_status(tracker.budget, total_spent)

    print(f"\n💰 REAL-TIME BUDGET STATUS:")
    print(f"   Original Budget:  ${tracker.budget:.2f}")
    print(f"   Total Spent:      ${total_spent:.2f}")
    print(f"   Remaining Budget: ${tracker.remaining_budget:.2f}")

    # Enhanced status indicators
    if budget_status['is_over_budget']:
        print(f"   🚨 OVER BUDGET BY: ${abs(tracker.remaining_budget):.2f}")
        print("   ❌ YOU ARE RUNNING OUT OF MONEY!")
    elif budget_status['is_critical_budget']:
        print("   ⚠️  CRITICAL: Very low budget remaining!")
    elif budget_status['is_low_budget']:
        print("   ⚠️  WARNING: Budget running low!")
    else:
        print("   ✅ Budget status: Good")

    # Show percentage of budget used
    print(f"   📊 Budget Used: {budget_status['percentage_used']:.1f}%")


def main():
    """Main function to run the SmartGrocery application."""
    print("🛒 Welcome to SmartGrocery - Your Budget Shopping Assistant!")
    print("Track your grocery purchases and stay within budget!")

    # Initialize application
    tracker = GroceryTracker()
    tracker.budget = get_user_budget()
    tracker.remaining_budget = tracker.budget

    print(f"\n✅ Budget set to ${tracker.budget:.2f}")

    # Main application loop
    while True:
        display_budget_status(tracker)
        display_menu()
        choice = input("Select an option (1-4): ").strip()

        if choice == '1':
            add_purchase(tracker)
        elif choice == '2':
            view_statistics(tracker)
        elif choice == '3':
            filename = generate_csv_report(tracker)
            if filename:
                print(f"Report saved as: {filename}")
        elif choice == '4':
            if tracker.purchases:
                print(f"\n📊 Final Summary:")
                print(format_purchase_summary(tracker.purchases))
                display_budget_status(tracker)
            print("\nThank you for using SmartGrocery! 🛒")
            break
        else:
            print("❌ Invalid option. Please choose 1-4.")


if __name__ == "__main__":
    main()