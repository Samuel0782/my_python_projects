import sqlite3
from datetime import datetime


def setup_database():
    """Create database and tables if they don't exist"""
    conn = sqlite3.connect('sab_banking.db')
    cursor = conn.cursor()
    
    # Drop existing tables if they exist (clean slate)
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS transactions')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            pin TEXT NOT NULL,
            available_balance REAL DEFAULT 100.00,
            savings REAL DEFAULT 5000.00,
            expenses REAL DEFAULT 750.00,
            car_insurance REAL DEFAULT 120.00,
            income REAL DEFAULT 1000.00,
            medical_bills REAL DEFAULT 0.00
        )
    ''')
    
    # Create transactions table - CORRECT COLUMN NAMES
    cursor.execute('''
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            transaction_type TEXT,
            amount REAL,
            balance_after REAL,
            account_type TEXT,
            description TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default users
    default_users = [
        ('Lucy', '1209', 450.00, 12000.00, 3240.00, 50000.00, 3200.00, 2000.00),
        ('Sandy', '3209', 45000.00, 32000.00, 23000.00, 72000.00, 5400.00, 4300.00),
        ('Dave', '2109', 430.00, 200.00, 250.00, 120.00, 2400.00, 150.00),
        ('Samuel', '5409', 250000.00, 100000.00, 90000.00, 7500.00, 150000.00, 7500.00)
    ]
    
    for username, pin, available_balance, savings, expenses, car_insurance, income, medical_bills in default_users:
        cursor.execute('''
            INSERT INTO users 
            (username, pin, available_balance, savings, expenses, car_insurance, income, medical_bills)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, pin, available_balance, savings, expenses, car_insurance, income, medical_bills))
    
    conn.commit()
    conn.close()
    print("✓ Database setup complete with correct structure!")




def get_user(username):
    conn = sqlite3.connect('SAB_banking.db')
    cursor = conn.cursor()


    cursor.execute('''
    SELECT id, username, pin, available_balance, savings, expenses, car_insurance, income, medical_bills
    
    FROM users WHERE username = ?''', (username,))

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None
    return user

def update_balance(user_id, account_type, amount, transaction_type, description):
    """Update user balance and log transaction"""
    conn = sqlite3.connect('sab_banking.db')
    cursor = conn.cursor()
    
    # Get current balance
    cursor.execute(f'SELECT {account_type} FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result is None:
        conn.close()
        return None
    
    current = result[0]
    available = current + amount
    
    # Update balance
    cursor.execute(f'UPDATE users SET {account_type} = ? WHERE id = ?', (available, user_id))
    
    # Insert transaction
    cursor.execute('''
        INSERT INTO transactions (user_id, transaction_type, amount, balance_after, account_type, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, transaction_type, amount, available, account_type, description))
    
    conn.commit()
    conn.close()
    return available


def log_transaction(user_id, transaction_type, amount, balance_after, account_type, description):
    conn = sqlite3.connect('SAB_banking.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO transactions (user_id,  transaction_type, amount, balance_after, account_type, description)
    VALUES(?,?,?,?,?,?)''',(user_id, transaction_type, amount, balance_after, account_type, description))
    
    conn.commit()
    conn.close()



def get_transaction_history(user_id, limit = 10):
    conn = sqlite3.connect('SAB_Banking.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT transaction_type, amount, balance_after, account_type, description, timestamp
    FROM transactions
    WHERE user_id = ?
    ORDER BY timestamp DESC
    LIMIT ?''', (user_id, limit))

    transactions = cursor.fetchall()
    conn.close()
    return transactions





def login_username():
    
    print('\n' + '='*40)
    print(f'\n=== SAB Digital Banking System ===')
    print('='*40)
    username_input = input('Enter Username: ')
    user = get_user(username_input)

    if not user:
        print('Invalid username, please try again!')
        return False, None


    user_id, username, stored_pin, available_balance, savings, expenses, car_insurance, income, medical_bills = user
    
    password_input = input('Enter PIN: ')


    if not password_input.isdigit():
        print('PIN must be digits only! Try again')
        return False, None

    if len(password_input) != 4:
        print('PIN must be exactly 4 digits!')
        return False, None
    
    if password_input != stored_pin:
        print('Incorrect PIN!')
        return False, None


    print(f"\nHello {username}, you've successfully logged in!")
    print(f"Your current balance: R{available_balance:}")


    user_dict = {
        'id': user_id,
        'username': username,
        'available': available_balance,
        'savings': savings,
        'expenses': expenses, 
        'car_insurance': car_insurance,
        'income': income,
        'medical_bills': medical_bills
    }
    #print("\n DEBUG: Returning from login:")
    #print(user_dict)
    #print("keys:", user_dict.keys())

    
    return True, user_dict 

def interface_app(user_data):
    #print("\n DEBUG: What's in user_data?")
    #print(user_data)
    #print("Key in user_data:", user_data.keys())
    #print("Type:", type(user_data))

    #print("DEBUG - Keys in user_data:", user_data.keys())

    
    user_id = user_data['id']
    username = user_data['username']
    available = user_data['available']
    savings = user_data['savings']
    expenses = user_data['expenses']
    car_insurance = user_data['car_insurance']
    income = user_data['income']
    medical_bills = user_data['medical_bills']
   
    # SAB menu options: 
    while True:
        print(f'{username} please select your service')
        print('option 1: Main_Account')
        print('option 2: Savings')
        print('option 3: Expenses')
        print('option 4: Car_insurance')
        print('option 5: Income')
        print('option 6: Deposit')
        print('option 7: Payment')
        print('option 8: Print Mini statement')
        print('option 9: Exit/Cancel')
       
        choice = input('\n Enter your option to proceed!: ')
        
        if choice == '1':
            print(f'available_balance: R{available}')
            #update balance after transferring fees: 
            #update_balance(user_id, 'available_balance', Payment_amount,'PAYMENT',f'Payment to main_account' )
            #update_balance(user_id,'income', -Payment_amount,'PAYMENT', f'Paymet from income_acount')
        
        elif choice == '2':
            print(f'savings: R{savings}')
        
        elif choice == '3':
            print(f'expenses: R{expenses}')
        
        elif choice == '4':
            print(f'car_insurance: R{car_insurance}') 
        
        elif choice == '5':
            print(f'income: R{income}')
            
        # Transfer from Income to Available Balance
            print(f'\n💰 Current Income Balance: R{income:.2f}')
            print(f'💰 Current Available Balance: R{available:.2f}')
    
            if income <= 0:
                print('❌ No funds in Income account to transfer!')
            else:
                print(f'\nHow much would you like to transfer from Income to Available?')
                transfer_amount = input('Amount: R')
        
            if transfer_amount.isdigit():
                transfer_amount = float(transfer_amount)
            
                if transfer_amount > income:
                    print(f'❌ Insufficient funds in Income! Available: R{income:.2f}')
                else:
                    # Transfer from Income to Available Balance
                    available = update_balance(user_id, 'available_balance', transfer_amount, 'TRANSFER', 'Transfer from Income')
                    income = update_balance(user_id, 'income', -transfer_amount, 'TRANSFER', 'Transfer to Available Balance')
                    print(f'\n✓ R{transfer_amount:.2f} transferred from Income to Available Balance')
                print(f'  Income balance: R{income:.2f}')
                print(f'  Available balance: R{available:.2f}')
            else:
                
                print('❌ Invalid amount!')
            
        
        elif choice == '6':
            deposit = input('Insert cash on the ATM:R')
            if deposit.isdigit():
                deposit_amount = float(deposit)
                #updated balance after deposit
                #income = deposit_amount
                income = update_balance(user_id, 'income', deposit_amount, 'DEPOSIT','Cash deposit')
                
                
                print(f'R{deposit_amount:} was deposited into your account')
                print(f'Income balance: R{income:}')
                print(f'Avialable balance:R{available}')
                #print(f'Use option 7 to transfer from income to Main_balance')

        
            else:    
                print('Cash deposited must be notes only!')
        
        elif choice == '7':
           
            
            #beneficiary database:
            Beneficiary = ['Ivy','Brand','Dave','Quinton']
            
            #payment method options:
            while True:
                print('\n---Make a Payment---')
                print('option 1: Savings')
                print('option 2: Expenses')
                print('option 3: Car_insurance')
                print('option 4: Beneficiary')
                print('option 5: Medical_bills')
                print('option 6: Back')
                
                payment_choice = input('\n Choose an account you want to make payment to (1-5): ')
                
                if payment_choice == '6':
                    print('Returning back to main menu...')
                    break
                    
                if payment_choice not in ['1','2','3','4','5']:
                    print(f'Please select option 1-5, try again!')
                    continue
                
                if payment_choice != '4':
                    payment = input('Enter amount:R')  
                    if not payment.isdigit():
                        print('Payment must be numbers only')
                        continue
                    
                    Payment_amount = float(payment)
                
                    if Payment_amount > available:
                        print(f'Insufficient funds!, Available Balance: R{available}')
                        continue                
                
                if payment_choice == '1':

                    #update balance after transferring fees to savings:
                    update_balance(user_id, 'savings', Payment_amount,'PAYMENT','Transfer to savings')
                    update_balance(user_id,'available_balance', -Payment_amount, 'PAYMENT','Transfer')

                    savings += Payment_amount
                    #available -= Payment_amount
                    print(f'R{Payment_amount:} paid towards savings_account')
                
                elif payment_choice == '2':
                    #update balance after transferring fees to expenses:
                    update_balance(user_id,'expenses', Payment_amount, 'PAYMENT','Transfer to expenses')
                    update_balance(user_id,'available_balance', -Payment_amount,'PAYMENT','Transfer')

                    
                    expenses += Payment_amount
                    available -= Payment_amount
                    print(f'R{Payment_amount:} was paid towards Expenses_account')
               
                elif payment_choice == '3':
                    #update balance aafter transferring fees to car_insurance:
                    update_balance(user_id,'car_insurance', Payment_amount,'PAYMENT','Transfer to car_insurance')
                    update_balance(user_id,'available_balance',-Payment_amount,'PAYMENT','Transfer')
                    
                    car_insurance = Payment_amount
                    available -= Payment_amount
                    print(f'R{car_insurance} was paid to car_insurance_account')
                
                #Beneficiary option:
                elif payment_choice == '4':
                    print('Please select beneficiary from your list!')

                    
                    for i, name in enumerate(Beneficiary, 1):
                        print(f'option {i},{name}')
                    
                    beneficiary_choice = input('select beneficiary(1-4): ')
                    
                    if beneficiary_choice.isdigit() and 1 <= int(beneficiary_choice) <= len(Beneficiary):
                        beneficiary_name = Beneficiary[int(beneficiary_choice) - 1]
                        Payment_input = input(f'Enter amount you want to pay {beneficiary_name}:R')
                        
                        if Payment_input.isdigit():
                            Payment_amount = float(Payment_input)

                            if Payment_amount > available:
                                print(f'Insufficient funds! Available balance: R{available:}')
                            else:
                                #update balance after transferring fees: 
                                available = update_balance(user_id,'available_balance', -Payment_amount,'PAYMENT', f'Beneficiary: {beneficiary_name}')
                                
                                #available -= Payment_amount
                                print(f'R{Payment_amount} was paid to {beneficiary_name}')
                                print(f'  Transaction recorded to {beneficiary_name}')
                    else:
                        print('Invalid beneficiary')
                        continue
                
                elif payment_choice == '5':
                    #update balance after transferring to medical_bills:
                    update_balance(user_id,'medical_bills',Payment_amount,'PAYMENT','Transfer to medical_bills')
                    update_balance(user_id,'available_balance',-Payment_amount,'PAYMENT','Transfer')
                    
                    #medical_bills += Payment_amount
                    available -= Payment_amount
                    print(f'R{Payment_amount} was paid to medical_bills_account ')
               
                #print new balance after using payment proceedure:
            print(f'Current_Available_balance: R{available}')      
                    
        
        elif choice == '8':
            print('\n' + '='*80)
            print('                        TRANSACTION HISTORY')
            print('='*80)
            transactions = get_transaction_history(user_id)
            if not transactions:
                print('                         No transactions yet')
                print('='*80)
            else:
                #FIXED: Adjusted column widths to match data
                print(f"{'Type':<10} {'Amount':>8} {'Balance':>12} {'Account':<20} {'Date':<20}")
                print('-'*80)
            for t in transactions:
                trans_type, amount, balance, account, desc, date = t
                # Format with R and 2 decimals
                amount_str = f"R{amount:}"
                balance_str = f"R{balance:}"
                # Truncate if too long
                account_short = account[:20] if len(account) > 20 else account
                date_short = date[:19] if len(date) > 19 else date
                # Print with exact spacing
                print(f"{trans_type:<10} {amount_str:>8} {balance_str:>12} {account_short:<20} {date_short:<20}")
            print('='*80)
            input('\nPress Enter to continue...')
        
        
        #Exit user interface   
        elif choice == '9':
            print('Thanks for using SAB, Enjoy your lovely day!')
            break

#setup_database()


#Banking interface functions call: 
login_success, username_data = login_username()
if login_success:
    interface_app(username_data)
    
        

        