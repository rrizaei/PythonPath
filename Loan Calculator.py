"""
Loan Calculator - A Comprehensive Mortgage & Loan Analysis Tool

This script provides a complete loan analysis system that calculates monthly payments,
generates amortization schedules, and analyzes the impact of extra payments.

WHAT IT DOES:
1. Takes user input for loan amount, interest rate, and term (in years)
2. Calculates monthly payment using the standard amortization formula
3. Shows total loan cost and total interest paid
4. Generates a detailed amortization schedule (month-by-month breakdown)
5. Analyzes how extra monthly payments can save time and money
6. Provides yearly summaries for long-term loans

USE CASES:
- Mortgage calculations and comparison shopping
- Auto loan analysis
- Personal loan planning
- Student loan repayment strategies

KEY FEATURES:
- Handles 0% interest loans correctly
- Prevents negative/zero input validation
- Generates real payment dates (starting next month)
- Smart amortization display (shows first year + yearly summaries for long terms)
- Extra payment impact analysis (shows time and interest savings)
- Floating-point precision handling to avoid $0.01 errors

HOW TO USE:
Run the script and follow the interactive prompts. You'll be asked for:
- Loan amount (positive number)
- Annual interest rate (percentage, can be 0)
- Loan term (positive integer years)

After initial calculation, you can optionally:
- View full or partial amortization schedule
- Analyze the effect of extra monthly payments
- Run multiple scenarios in one session

EXAMPLE OUTPUT:
- Monthly payment amount
- Total paid over loan term
- Total interest paid
- Interest-to-principal ratio
- Month-by-month breakdown (principal, interest, remaining balance)
- Time/money saved with extra payments

REQUIREMENTS: Python 3.6+ (uses datetime module, no external dependencies)

AUTHOR: Ravi Rizaei
CREATED: 05.13.2026
"""

from datetime import datetime, timedelta
class LoanCalculator:
    def __init__(self):
        self.loan_amount = 0
        self.annual_interest_rate = 0
        self.loan_term_years = 0
        self.loan_term_months = 0

    def get_user_input(self):
        """Get loan details from user"""
        print("\n=== LOAN CALCULATOR ===\n")

        while True:
            try:
                self.loan_amount = float(input("Enter loan amount ($): "))
                if self.loan_amount <= 0:
                    print("Loan amount must be positive. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        while True:
            try:
                self.annual_interest_rate = float(input("Enter annual interest rate (%): "))
                if self.annual_interest_rate < 0:
                    print("Interest rate cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        while True:
            try:
                years = int(input("Enter loan term (years): "))
                if years <= 0:
                    print("Loan term must be positive. Please try again.")
                    continue
                self.loan_term_years = years
                self.loan_term_months = years * 12
                break
            except ValueError:
                print("Invalid input. Please enter a whole number.")

    def calculate_monthly_payment(self):
        """Calculate monthly payment using amortization formula"""
        if self.annual_interest_rate == 0:
            return self.loan_amount / self.loan_term_months

        monthly_rate = (self.annual_interest_rate / 100) / 12

        # Amortization formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
        numerator = monthly_rate * (1 + monthly_rate) ** self.loan_term_months
        denominator = (1 + monthly_rate) ** self.loan_term_months - 1

        monthly_payment = self.loan_amount * (numerator / denominator)
        return monthly_payment

    def calculate_total_cost(self, monthly_payment):
        """Calculate total cost of the loan"""
        total_paid = monthly_payment * self.loan_term_months
        total_interest = total_paid - self.loan_amount
        return total_paid, total_interest

    def generate_amortization_schedule(self, monthly_payment):
        """Generate detailed amortization schedule"""
        monthly_rate = (self.annual_interest_rate / 100) / 12
        balance = self.loan_amount
        schedule = []

        start_date = datetime.now().replace(day=1) + timedelta(days=32)
        start_date = start_date.replace(day=1)

        for month in range(1, self.loan_term_months + 1):
            interest_payment = balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment

            # Handle floating point precision issues
            if balance < 0.01:
                balance = 0

            payment_date = start_date + timedelta(days=32 * (month - 1))
            payment_date = payment_date.replace(day=1)

            schedule.append({
                'month': month,
                'date': payment_date.strftime('%b %Y'),
                'payment': monthly_payment,
                'principal': principal_payment,
                'interest': interest_payment,
                'balance': balance
            })

            if balance == 0:
                break

        return schedule

    def display_results(self):
        """Display loan calculation results"""
        monthly_payment = self.calculate_monthly_payment()
        total_paid, total_interest = self.calculate_total_cost(monthly_payment)

        print("\n" + "="*50)
        print("LOAN SUMMARY")
        print("="*50)
        print(f"Loan Amount: ${self.loan_amount:,.2f}")
        print(f"Annual Interest Rate: {self.annual_interest_rate:.2f}%")
        print(f"Loan Term: {self.loan_term_years} years ({self.loan_term_months} months)")
        print("-"*50)
        print(f"Monthly Payment: ${monthly_payment:,.2f}")
        print(f"Total Amount Paid: ${total_paid:,.2f}")
        print(f"Total Interest Paid: ${total_interest:,.2f}")
        print(f"Interest-to-Principal Ratio: {(total_interest/self.loan_amount)*100:.1f}%")
        print("="*50)

        return monthly_payment, total_paid, total_interest

    def display_amortization_schedule(self, schedule, show_all=False):
        """Display amortization schedule"""
        print("\n" + "="*80)
        print("AMORTIZATION SCHEDULE")
        print("="*80)
        print(f"{'Month':<8} {'Date':<12} {'Payment':>12} {'Principal':>12} {'Interest':>12} {'Balance':>12}")
        print("-"*80)

        if show_all:
            # Show all months
            for payment in schedule:
                print(f"{payment['month']:<8} {payment['date']:<12} "
                      f"${payment['payment']:>11,.2f} ${payment['principal']:>11,.2f} "
                      f"${payment['interest']:>11,.2f} ${payment['balance']:>11,.2f}")
        else:
            # Show first 12 months, then yearly summary
            for payment in schedule[:12]:
                print(f"{payment['month']:<8} {payment['date']:<12} "
                      f"${payment['payment']:>11,.2f} ${payment['principal']:>11,.2f} "
                      f"${payment['interest']:>11,.2f} ${payment['balance']:>11,.2f}")

            if len(schedule) > 12:
                print("..." * 16)
                print(f"(Showing first year. Full schedule has {len(schedule)} payments)")

                # Show yearly summaries
                print("\nYearly Summary:")
                print("-"*80)
                for year in range(1, self.loan_term_years + 1):
                    start_month = (year - 1) * 12
                    end_month = min(year * 12, len(schedule))
                    yearly_payments = schedule[start_month:end_month]

                    if yearly_payments:
                        total_year_principal = sum(p['principal'] for p in yearly_payments)
                        total_year_interest = sum(p['interest'] for p in yearly_payments)
                        total_year_payment = sum(p['payment'] for p in yearly_payments)
                        year_end_balance = yearly_payments[-1]['balance']

                        print(f"Year {year}: Total Paid: ${total_year_payment:,.2f} | "
                              f"Principal: ${total_year_principal:,.2f} | "
                              f"Interest: ${total_year_interest:,.2f} | "
                              f"Remaining: ${year_end_balance:,.2f}")

        print("="*80)

    def extra_payment_analysis(self, extra_monthly_payment):
        """Analyze the impact of making extra payments"""
        monthly_payment = self.calculate_monthly_payment()
        new_payment = monthly_payment + extra_monthly_payment
        monthly_rate = (self.annual_interest_rate / 100) / 12

        balance = self.loan_amount
        months_with_extra = 0
        total_interest_with_extra = 0

        while balance > 0 and months_with_extra < self.loan_term_months:
            interest = balance * monthly_rate
            principal = new_payment - interest
            if principal > balance:
                principal = balance
            balance -= principal
            total_interest_with_extra += interest
            months_with_extra += 1

        # Original total interest
        _, original_interest = self.calculate_total_cost(monthly_payment)

        time_saved = self.loan_term_months - months_with_extra
        interest_saved = original_interest - total_interest_with_extra

        return months_with_extra, time_saved, interest_saved

def main():
    """Main program loop"""
    calculator = LoanCalculator()

    while True:
        calculator.get_user_input()
        monthly_payment, total_paid, total_interest = calculator.display_results()

        # Ask if user wants to see amortization schedule
        while True:
            see_schedule = input("\nWould you like to see the amortization schedule? (yes/no): ").lower().strip()
            if see_schedule in ['yes', 'y']:
                schedule = calculator.generate_amortization_schedule(monthly_payment)

                show_all = input("Show all payments? (yes/no, default shows summary): ").lower().strip()
                calculator.display_amortization_schedule(schedule, show_all=show_all in ['yes', 'y'])
                break
            elif see_schedule in ['no', 'n']:
                break
            else:
                print("Please enter 'yes' or 'no'.")

        # Ask if user wants to analyze extra payments
        while True:
            analyze_extra = input("\nWould you like to analyze extra payments? (yes/no): ").lower().strip()
            if analyze_extra in ['yes', 'y']:
                try:
                    extra = float(input("Enter extra monthly payment amount ($): "))
                    if extra < 0:
                        print("Extra payment cannot be negative.")
                        continue

                    months, time_saved, interest_saved = calculator.extra_payment_analysis(extra)

                    print("\n" + "="*50)
                    print("EXTRA PAYMENT ANALYSIS")
                    print("="*50)
                    print(f"Regular Monthly Payment: ${monthly_payment:,.2f}")
                    print(f"Extra Monthly Payment: ${extra:,.2f}")
                    print(f"New Monthly Payment: ${monthly_payment + extra:,.2f}")
                    print("-"*50)
                    print(f"Loan Paid Off In: {months} months ({months/12:.1f} years)")
                    print(f"Time Saved: {time_saved} months ({time_saved/12:.1f} years)")
                    print(f"Interest Saved: ${interest_saved:,.2f}")
                    print("="*50)
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif analyze_extra in ['no', 'n']:
                break
            else:
                print("Please enter 'yes' or 'no'.")

        # Ask if user wants to calculate another loan
        again = input("\nWould you like to calculate another loan? (yes/no): ").lower().strip()
        if again not in ['yes', 'y']:
            print("\nThank you for using the Loan Calculator!")
            break

if __name__ == "__main__":
    main()