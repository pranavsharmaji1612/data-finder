import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random

class FinanceAIAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Personal Finance AI Assistant")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a2e')
        
        # Data storage
        self.data_file = "finance_data.json"
        self.expenses = []
        self.income = []
        self.budget = {}
        self.load_data()
        
        # Categories
        self.expense_categories = [
            "Food & Dining", "Transportation", "Shopping", "Entertainment",
            "Bills & Utilities", "Healthcare", "Education", "Travel",
            "Investments", "Other"
        ]
        
        # Main container
        self.main_container = tk.Frame(root, bg='#1a1a2e')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_header()
        self.create_tabs()
        self.update_dashboard()
        
    def create_header(self):
        header = tk.Frame(self.main_container, bg='#16213e', height=80)
        header.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(
            header,
            text="💰 Personal Finance AI Assistant",
            font=("Arial", 28, "bold"),
            bg='#16213e',
            fg='#00ff88'
        )
        title.pack(pady=20)
        
        # Quick stats
        stats_frame = tk.Frame(header, bg='#16213e')
        stats_frame.pack(pady=10)
        
        self.total_income_label = tk.Label(
            stats_frame,
            text=f"Income: ₹0",
            font=("Arial", 14),
            bg='#16213e',
            fg='#00ff88'
        )
        self.total_income_label.pack(side=tk.LEFT, padx=20)
        
        self.total_expense_label = tk.Label(
            stats_frame,
            text=f"Expenses: ₹0",
            font=("Arial", 14),
            bg='#16213e',
            fg='#ff4757'
        )
        self.total_expense_label.pack(side=tk.LEFT, padx=20)
        
        self.balance_label = tk.Label(
            stats_frame,
            text=f"Balance: ₹0",
            font=("Arial", 14, "bold"),
            bg='#16213e',
            fg='#ffa502'
        )
        self.balance_label.pack(side=tk.LEFT, padx=20)
        
    def create_tabs(self):
        # Notebook for tabs
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#1a1a2e', borderwidth=0)
        style.configure('TNotebook.Tab', background='#16213e', foreground='white', 
                       padding=[20, 10], font=('Arial', 11, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#0f3460')])
        
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tabs
        self.dashboard_tab = tk.Frame(self.notebook, bg='#1a1a2e')
        self.add_transaction_tab = tk.Frame(self.notebook, bg='#1a1a2e')
        self.budget_tab = tk.Frame(self.notebook, bg='#1a1a2e')
        self.insights_tab = tk.Frame(self.notebook, bg='#1a1a2e')
        
        self.notebook.add(self.dashboard_tab, text='📊 Dashboard')
        self.notebook.add(self.add_transaction_tab, text='➕ Add Transaction')
        self.notebook.add(self.budget_tab, text='💵 Budget Planner')
        self.notebook.add(self.insights_tab, text='🤖 AI Insights')
        
        self.create_dashboard_tab()
        self.create_add_transaction_tab()
        self.create_budget_tab()
        self.create_insights_tab()
        
    def create_dashboard_tab(self):
        # Left side - Charts
        left_frame = tk.Frame(self.dashboard_tab, bg='#1a1a2e')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chart frame
        self.chart_frame = tk.Frame(left_frame, bg='#16213e')
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Right side - Recent transactions
        right_frame = tk.Frame(self.dashboard_tab, bg='#16213e', width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
        right_frame.pack_propagate(False)
        
        tk.Label(
            right_frame,
            text="Recent Transactions",
            font=("Arial", 16, "bold"),
            bg='#16213e',
            fg='#00ff88'
        ).pack(pady=10)
        
        # Scrollable transaction list
        transaction_canvas = tk.Canvas(right_frame, bg='#16213e', highlightthickness=0)
        scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=transaction_canvas.yview)
        self.transaction_list_frame = tk.Frame(transaction_canvas, bg='#16213e')
        
        self.transaction_list_frame.bind(
            "<Configure>",
            lambda e: transaction_canvas.configure(scrollregion=transaction_canvas.bbox("all"))
        )
        
        transaction_canvas.create_window((0, 0), window=self.transaction_list_frame, anchor="nw")
        transaction_canvas.configure(yscrollcommand=scrollbar.set)
        
        transaction_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
    def create_add_transaction_tab(self):
        container = tk.Frame(self.add_transaction_tab, bg='#1a1a2e')
        container.pack(expand=True)
        
        # Transaction type
        type_frame = tk.Frame(container, bg='#1a1a2e')
        type_frame.pack(pady=20)
        
        tk.Label(
            type_frame,
            text="Transaction Type:",
            font=("Arial", 14),
            bg='#1a1a2e',
            fg='white'
        ).pack(side=tk.LEFT, padx=10)
        
        self.transaction_type = tk.StringVar(value="Expense")
        
        type_buttons = tk.Frame(type_frame, bg='#1a1a2e')
        type_buttons.pack(side=tk.LEFT)
        
        tk.Radiobutton(
            type_buttons,
            text="💸 Expense",
            variable=self.transaction_type,
            value="Expense",
            font=("Arial", 12),
            bg='#1a1a2e',
            fg='white',
            selectcolor='#16213e',
            activebackground='#1a1a2e'
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(
            type_buttons,
            text="💰 Income",
            variable=self.transaction_type,
            value="Income",
            font=("Arial", 12),
            bg='#1a1a2e',
            fg='white',
            selectcolor='#16213e',
            activebackground='#1a1a2e'
        ).pack(side=tk.LEFT, padx=10)
        
        # Amount
        amount_frame = tk.Frame(container, bg='#1a1a2e')
        amount_frame.pack(pady=15)
        
        tk.Label(
            amount_frame,
            text="Amount (₹):",
            font=("Arial", 14),
            bg='#1a1a2e',
            fg='white'
        ).pack(side=tk.LEFT, padx=10)
        
        self.amount_entry = tk.Entry(
            amount_frame,
            font=("Arial", 14),
            width=20,
            bg='#16213e',
            fg='white',
            insertbackground='white'
        )
        self.amount_entry.pack(side=tk.LEFT, padx=10)
        
        # Category
        category_frame = tk.Frame(container, bg='#1a1a2e')
        category_frame.pack(pady=15)
        
        tk.Label(
            category_frame,
            text="Category:",
            font=("Arial", 14),
            bg='#1a1a2e',
            fg='white'
        ).pack(side=tk.LEFT, padx=10)
        
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            category_frame,
            textvariable=self.category_var,
            values=self.expense_categories,
            font=("Arial", 12),
            width=18,
            state='readonly'
        )
        self.category_dropdown.pack(side=tk.LEFT, padx=10)
        self.category_dropdown.current(0)
        
        # Description
        desc_frame = tk.Frame(container, bg='#1a1a2e')
        desc_frame.pack(pady=15)
        
        tk.Label(
            desc_frame,
            text="Description:",
            font=("Arial", 14),
            bg='#1a1a2e',
            fg='white'
        ).pack(side=tk.LEFT, padx=10)
        
        self.description_entry = tk.Entry(
            desc_frame,
            font=("Arial", 14),
            width=30,
            bg='#16213e',
            fg='white',
            insertbackground='white'
        )
        self.description_entry.pack(side=tk.LEFT, padx=10)
        
        # Add button
        tk.Button(
            container,
            text="➕ Add Transaction",
            font=("Arial", 14, "bold"),
            bg='#00ff88',
            fg='#1a1a2e',
            command=self.add_transaction,
            padx=30,
            pady=15,
            cursor='hand2'
        ).pack(pady=30)
        
    def create_budget_tab(self):
        container = tk.Frame(self.budget_tab, bg='#1a1a2e')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            container,
            text="Monthly Budget Planner",
            font=("Arial", 20, "bold"),
            bg='#1a1a2e',
            fg='#00ff88'
        ).pack(pady=20)
        
        # Budget input frame
        budget_input = tk.Frame(container, bg='#16213e')
        budget_input.pack(fill=tk.X, pady=10, padx=50)
        
        self.budget_entries = {}
        
        for i, category in enumerate(self.expense_categories):
            row = tk.Frame(budget_input, bg='#16213e')
            row.pack(fill=tk.X, pady=5, padx=20)
            
            tk.Label(
                row,
                text=category,
                font=("Arial", 12),
                bg='#16213e',
                fg='white',
                width=20,
                anchor='w'
            ).pack(side=tk.LEFT, padx=10)
            
            entry = tk.Entry(
                row,
                font=("Arial", 12),
                width=15,
                bg='#1a1a2e',
                fg='white',
                insertbackground='white'
            )
            entry.pack(side=tk.LEFT, padx=10)
            entry.insert(0, str(self.budget.get(category, 0)))
            self.budget_entries[category] = entry
            
            # Show current spending
            spent = sum(exp['amount'] for exp in self.expenses 
                       if exp['category'] == category)
            
            spent_label = tk.Label(
                row,
                text=f"Spent: ₹{spent:.0f}",
                font=("Arial", 11),
                bg='#16213e',
                fg='#ffa502'
            )
            spent_label.pack(side=tk.LEFT, padx=20)
        
        # Save button
        tk.Button(
            container,
            text="💾 Save Budget",
            font=("Arial", 14, "bold"),
            bg='#00ff88',
            fg='#1a1a2e',
            command=self.save_budget,
            padx=30,
            pady=15,
            cursor='hand2'
        ).pack(pady=30)
        
    def create_insights_tab(self):
        container = tk.Frame(self.insights_tab, bg='#1a1a2e')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            container,
            text="🤖 AI-Powered Financial Insights",
            font=("Arial", 20, "bold"),
            bg='#1a1a2e',
            fg='#00ff88'
        ).pack(pady=20)
        
        # Insights display area
        insights_frame = tk.Frame(container, bg='#16213e')
        insights_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        self.insights_text = tk.Text(
            insights_frame,
            font=("Arial", 12),
            bg='#16213e',
            fg='white',
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        self.insights_text.pack(fill=tk.BOTH, expand=True)
        
        # Generate insights button
        tk.Button(
            container,
            text="🔄 Generate New Insights",
            font=("Arial", 14, "bold"),
            bg='#00ff88',
            fg='#1a1a2e',
            command=self.generate_insights,
            padx=30,
            pady=15,
            cursor='hand2'
        ).pack(pady=20)
        
    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            description = self.description_entry.get()
            trans_type = self.transaction_type.get()
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive!")
                return
            
            transaction = {
                'type': trans_type,
                'amount': amount,
                'category': category if trans_type == "Expense" else "Income",
                'description': description,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            if trans_type == "Expense":
                self.expenses.append(transaction)
            else:
                self.income.append(transaction)
            
            self.save_data()
            self.update_dashboard()
            
            # Clear inputs
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            
            messagebox.showinfo("Success", f"{trans_type} of ₹{amount} added!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid amount!")
    
    def save_budget(self):
        try:
            for category, entry in self.budget_entries.items():
                value = entry.get()
                self.budget[category] = float(value) if value else 0
            
            self.save_data()
            messagebox.showinfo("Success", "Budget saved successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid budget amounts!")
    
    def update_dashboard(self):
        # Update header stats
        total_income = sum(i['amount'] for i in self.income)
        total_expenses = sum(e['amount'] for e in self.expenses)
        balance = total_income - total_expenses
        
        self.total_income_label.config(text=f"Income: ₹{total_income:,.0f}")
        self.total_expense_label.config(text=f"Expenses: ₹{total_expenses:,.0f}")
        self.balance_label.config(text=f"Balance: ₹{balance:,.0f}")
        
        # Update charts
        self.create_charts()
        
        # Update recent transactions
        self.update_transaction_list()
        
    def create_charts(self):
        # Clear existing charts
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        fig = Figure(figsize=(10, 8), facecolor='#16213e')
        
        # Expense by category pie chart
        ax1 = fig.add_subplot(221, facecolor='#16213e')
        
        if self.expenses:
            category_expenses = {}
            for exp in self.expenses:
                cat = exp['category']
                category_expenses[cat] = category_expenses.get(cat, 0) + exp['amount']
            
            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7',
                     '#dfe6e9', '#74b9ff', '#a29bfe', '#fd79a8', '#fdcb6e']
            
            ax1.pie(
                category_expenses.values(),
                labels=category_expenses.keys(),
                autopct='%1.1f%%',
                colors=colors,
                textprops={'color': 'white'}
            )
            ax1.set_title('Expenses by Category', color='white', fontsize=12, pad=10)
        else:
            ax1.text(0.5, 0.5, 'No expenses yet', ha='center', va='center',
                    color='white', fontsize=14)
            ax1.set_title('Expenses by Category', color='white', fontsize=12, pad=10)
        
        # Income vs Expenses bar chart
        ax2 = fig.add_subplot(222, facecolor='#16213e')
        
        total_income = sum(i['amount'] for i in self.income)
        total_expenses = sum(e['amount'] for e in self.expenses)
        
        bars = ax2.bar(['Income', 'Expenses'], [total_income, total_expenses],
                      color=['#00ff88', '#ff4757'])
        ax2.set_title('Income vs Expenses', color='white', fontsize=12, pad=10)
        ax2.tick_params(colors='white')
        ax2.spines['bottom'].set_color('white')
        ax2.spines['left'].set_color('white')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'₹{height:,.0f}',
                    ha='center', va='bottom', color='white')
        
        # Budget vs Actual
        ax3 = fig.add_subplot(223, facecolor='#16213e')
        
        if self.budget:
            categories = list(self.budget.keys())[:5]  # Top 5
            budget_amounts = [self.budget.get(cat, 0) for cat in categories]
            actual_amounts = [sum(e['amount'] for e in self.expenses 
                                 if e['category'] == cat) for cat in categories]
            
            x = range(len(categories))
            width = 0.35
            
            ax3.bar([i - width/2 for i in x], budget_amounts, width,
                   label='Budget', color='#00ff88')
            ax3.bar([i + width/2 for i in x], actual_amounts, width,
                   label='Actual', color='#ff4757')
            
            ax3.set_xticks(x)
            ax3.set_xticklabels([cat[:10] for cat in categories], rotation=45, ha='right')
            ax3.set_title('Budget vs Actual Spending', color='white', fontsize=12, pad=10)
            ax3.legend(facecolor='#16213e', edgecolor='white', labelcolor='white')
            ax3.tick_params(colors='white')
            ax3.spines['bottom'].set_color('white')
            ax3.spines['left'].set_color('white')
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
        else:
            ax3.text(0.5, 0.5, 'Set budget first', ha='center', va='center',
                    color='white', fontsize=14)
            ax3.set_title('Budget vs Actual Spending', color='white', fontsize=12, pad=10)
        
        # Spending trend (last 7 days)
        ax4 = fig.add_subplot(224, facecolor='#16213e')
        
        if self.expenses:
            # Group by date
            daily_expenses = {}
            for exp in self.expenses:
                date = exp['date'].split()[0]
                daily_expenses[date] = daily_expenses.get(date, 0) + exp['amount']
            
            dates = sorted(daily_expenses.keys())[-7:]  # Last 7 days
            amounts = [daily_expenses[d] for d in dates]
            
            ax4.plot(range(len(dates)), amounts, marker='o', color='#00ff88', linewidth=2)
            ax4.fill_between(range(len(dates)), amounts, alpha=0.3, color='#00ff88')
            ax4.set_xticks(range(len(dates)))
            ax4.set_xticklabels([d.split('-')[2] for d in dates])
            ax4.set_title('Daily Spending Trend', color='white', fontsize=12, pad=10)
            ax4.tick_params(colors='white')
            ax4.spines['bottom'].set_color('white')
            ax4.spines['left'].set_color('white')
            ax4.spines['top'].set_visible(False)
            ax4.spines['right'].set_visible(False)
            ax4.grid(True, alpha=0.2)
        else:
            ax4.text(0.5, 0.5, 'No data yet', ha='center', va='center',
                    color='white', fontsize=14)
            ax4.set_title('Daily Spending Trend', color='white', fontsize=12, pad=10)
        
        fig.tight_layout(pad=2)
        
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_transaction_list(self):
        # Clear existing
        for widget in self.transaction_list_frame.winfo_children():
            widget.destroy()
        
        # Combine and sort all transactions
        all_transactions = self.expenses + self.income
        all_transactions.sort(key=lambda x: x['date'], reverse=True)
        
        for trans in all_transactions[:15]:  # Show last 15
            frame = tk.Frame(self.transaction_list_frame, bg='#0f3460', relief=tk.RIDGE, bd=1)
            frame.pack(fill=tk.X, pady=5, padx=5)
            
            # Type indicator
            color = '#ff4757' if trans['type'] == 'Expense' else '#00ff88'
            symbol = '💸' if trans['type'] == 'Expense' else '💰'
            
            tk.Label(
                frame,
                text=symbol,
                font=("Arial", 16),
                bg='#0f3460'
            ).pack(side=tk.LEFT, padx=5)
            
            # Details
            details_frame = tk.Frame(frame, bg='#0f3460')
            details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            tk.Label(
                details_frame,
                text=trans['description'] or trans['category'],
                font=("Arial", 11, "bold"),
                bg='#0f3460',
                fg='white',
                anchor='w'
            ).pack(anchor='w')
            
            tk.Label(
                details_frame,
                text=f"{trans['category']} • {trans['date'].split()[0]}",
                font=("Arial", 9),
                bg='#0f3460',
                fg='#b0b0b0',
                anchor='w'
            ).pack(anchor='w')
            
            # Amount
            tk.Label(
                frame,
                text=f"₹{trans['amount']:,.0f}",
                font=("Arial", 13, "bold"),
                bg='#0f3460',
                fg=color
            ).pack(side=tk.RIGHT, padx=10)
    
    def generate_insights(self):
        self.insights_text.delete('1.0', tk.END)
        
        if not self.expenses and not self.income:
            self.insights_text.insert('1.0', "❌ No data available yet. Start adding transactions to get insights!")
            return
        
        insights = []
        
        # Total analysis
        total_income = sum(i['amount'] for i in self.income)
        total_expenses = sum(e['amount'] for e in self.expenses)
        balance = total_income - total_expenses
        savings_rate = (balance / total_income * 100) if total_income > 0 else 0
        
        insights.append(f"💰 FINANCIAL OVERVIEW\n")
        insights.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        insights.append(f"Total Income: ₹{total_income:,.0f}\n")
        insights.append(f"Total Expenses: ₹{total_expenses:,.0f}\n")
        insights.append(f"Current Balance: ₹{balance:,.0f}\n")
        insights.append(f"Savings Rate: {savings_rate:.1f}%\n\n")
        
        # Savings analysis
        insights.append(f"📊 SAVINGS ANALYSIS\n")
        insights.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        if savings_rate >= 30:
            insights.append(f"✅ Excellent! You're saving {savings_rate:.1f}% of your income.\n")
        elif savings_rate >= 20:
            insights.append(f"✅ Good job! You're saving {savings_rate:.1f}% of your income.\n")
        elif savings_rate >= 10:
            insights.append(f"⚠️ You're saving {savings_rate:.1f}%. Try to increase to 20%+\n")
        else:
            insights.append(f"⚠️ Low savings rate ({savings_rate:.1f}%). Consider reducing expenses.\n")
        insights.append("\n")
        
        # Top spending categories
        if self.expenses:
            category_spending = {}
            for exp in self.expenses:
                cat = exp['category']
                category_spending[cat] = category_spending.get(cat, 0) + exp['amount']
            
            sorted_categories = sorted(category_spending.items(), 
                                      key=lambda x: x[1], reverse=True)
            
            insights.append(f"💸 TOP SPENDING CATEGORIES\n")
            insights.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            for i, (cat, amount) in enumerate(sorted_categories[:3], 1):
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                insights.append(f"{i}. {cat}: ₹{amount:,.0f} ({percentage:.1f}%)\n")
            insights.append("\n")
        
        # Budget warnings
        if self.budget:
            insights.append(f"⚠️ BUDGET ALERTS\n")
            insights.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            warnings_found = False
            
            for category, budget_amount in self.budget.items():
                if budget_amount > 0:
                    spent = sum(e['amount'] for e in self.expenses 
                               if e['category'] == category)
                    percentage = (spent / budget_amount * 100) if budget_amount > 0 else 0
                    
                    if percentage >= 90:
                        insights.append(f"🔴 {category}: {percentage:.0f}% of budget used (₹{spent:,.0f}/₹{budget_amount:,.0f})\n")
                        warnings_found = True
                    elif percentage >= 75:
                        insights.append(f"🟡 {category}: {percentage:.0f}% of budget used (₹{spent:,.0f}/₹{budget_amount:,.0f})\n")
                        warnings_found = True
            
            if not warnings_found:
                insights.append("✅ All categories within budget!\n")
            insights.append("\n")
        
        # AI Recommendations
        insights.append(f"🤖 AI RECOMMENDATIONS\n")
        insights.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        
        if savings_rate < 20:
            insights.append(f"💡 Try the 50/30/20 rule: 50% needs, 30% wants, 20% savings\n")
        
        if self.expenses:
            top_category = max(category_spending.items(), key=lambda x: x[1])[0]
            insights.append(f"💡 Your highest spending is in '{top_category}'. Can you reduce by 10%?\n")
        
        if total_income > 0:
            monthly_savings_target = total_income * 0.2
            current_savings = balance
            if current_savings < monthly_savings_target:
                shortfall = monthly_savings_target - current_savings
                insights.append(f"💡 To reach 20% savings, save ₹{shortfall:,.0f} more this month\n")
        
        insights.append(f"\n💪 Keep tracking! Your financial awareness is improving!")
        
        # Insert all insights
        self.insights_text.insert('1.0', ''.join(insights))
    
    def save_data(self):
        data = {
            'expenses': self.expenses,
            'income': self.income,
            'budget': self.budget
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.expenses = data.get('expenses', [])
                    self.income = data.get('income', [])
                    self.budget = data.get('budget', {})
            except:
                pass

def main():
    root = tk.Tk()
    app = FinanceAIAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()