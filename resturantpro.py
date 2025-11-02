import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
import json
import os
from collections import defaultdict
import hashlib

class RestaurantSystemWithRoles:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#f0f0f0',
            'bg_secondary': '#f5f5f5',
            'bg_card': '#ffffff',
            'accent': '#00a8cc',
            'accent_secondary': '#ff6b6b',
            'success': '#51cf66',
            'warning': '#ffd43b',
            'danger': '#ff6b6b',
            'text_primary': '#333333',
            'text_secondary': '#a0a0a0'
        }
        
        # Data storage
        self.data_file = "restaurant_data.json"
        self.users_file = "restaurant_users.json"
        self.load_data()
        self.load_users()
        
        # Current session
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.current_user = None
        self.notifications = []
        
        # Apply modern theme
        self.setup_modern_theme()
        
        # Show login screen
        self.show_login()
    
    def setup_modern_theme(self):
        """Setup modern theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), 
                       background=self.colors['bg_primary'], foreground=self.colors['text_primary'])
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), 
                       background=self.colors['bg_secondary'], foreground=self.colors['text_primary'])
        style.configure('Modern.TButton', font=('Segoe UI', 10, 'bold'), 
                       background=self.colors['accent'], foreground=self.colors['bg_primary'],
                       borderwidth=0, focuscolor='none')
        style.map('Modern.TButton',
                 background=[('active', '#00a8cc'), ('pressed', '#0088aa')])
        
        # Configure treeview
        style.configure('Modern.Treeview', background=self.colors['bg_card'], 
                       foreground=self.colors['text_primary'], fieldbackground=self.colors['bg_card'],
                       borderwidth=0, font=('Segoe UI', 10))
        style.configure('Modern.Treeview.Heading', background=self.colors['bg_secondary'], 
                       foreground=self.colors['text_primary'], font=('Segoe UI', 11, 'bold'))
        style.map('Modern.Treeview', background=[('selected', self.colors['accent'])])
    
    def load_users(self):
        """Load user accounts"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            except:
                self.initialize_users()
        else:
            self.initialize_users()
    
    def initialize_users(self):
        """Initialize with three different user roles"""
        self.users = {
            'admin': {
                'password': hashlib.md5('admin123'.encode()).hexdigest(),
                'role': 'Administrator',
                'name': 'System Administrator',
                'permissions': ['all']
            },
            'manager': {
                'password': hashlib.md5('manager123'.encode()).hexdigest(),
                'role': 'Manager',
                'name': 'Restaurant Manager',
                'permissions': ['orders', 'menu', 'inventory', 'kitchen', 'reports', 'settings']
            },
            'cashier': {
                'password': hashlib.md5('cashier123'.encode()).hexdigest(),
                'role': 'Cashier',
                'name': 'Cashier',
                'permissions': ['orders']
            }
        }
        self.save_users()
    
    def save_users(self):
        """Save user accounts"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save users: {e}")
    
    def load_data(self):
        """Load data from file or initialize empty"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            except:
                self.initialize_empty_data()
        else:
            self.initialize_empty_data()
    
    def initialize_empty_data(self):
        """Initialize with empty data"""
        self.data = {
            'menu': {
                'Appetizers': [],
                'Main Courses': [],
                'Desserts': [],
                'Beverages': []
            },
            'inventory': {},
            'orders': [],
            'employees': [],
            'tables': {i: {'status': 'available', 'order_id': None} for i in range(1, 11)},
            'daily_sales': defaultdict(float),
            'expenses': [],
            'customers': [],
            'reservations': [],
            'suppliers': [],
            'coupons': [],
            'tax_settings': {'rate': 0.08, 'name': 'Sales Tax'},
            'kitchen_orders': []
        }
        self.save_data()
    
    def save_data(self):
        """Save data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
    
    def show_notification(self, message, type='info'):
        """Show notification"""
        self.notifications.append({'message': message, 'type': type, 'time': datetime.now()})
        if len(self.notifications) > 10:
            self.notifications.pop(0)
    
    def show_login(self):
        """Show login screen"""
        self.clear_window()
        
        # Login container
        login_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        login_frame.pack(expand=True, fill=tk.BOTH)
        
        # Login card
        card = tk.Frame(login_frame, bg=self.colors['bg_card'], relief=tk.RAISED, bd=2)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=500)
        
        # Logo
        logo_frame = tk.Frame(card, bg=self.colors['bg_card'])
        logo_frame.pack(pady=(30, 10))
        
        tk.Label(logo_frame, text="🍽️", font=('Segoe UI', 36),
                bg=self.colors['bg_card'], fg=self.colors['accent']).pack()
        tk.Label(logo_frame, text="RestaurantOS", font=('Segoe UI', 22, 'bold'),
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack()
        tk.Label(logo_frame, text="Professional", font=('Segoe UI', 10, 'italic'),
                bg=self.colors['bg_card'], fg=self.colors['accent']).pack()
        
        tk.Label(card, text="Modern Restaurant Management", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(pady=(5, 30))
        
        # Login form
        form_frame = tk.Frame(card, bg=self.colors['bg_card'])
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Username:", font=('Segoe UI', 11),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(0, 5))
        
        self.username_entry = tk.Entry(form_frame, font=('Segoe UI', 11), width=25,
                                      bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                      insertbackground=self.colors['text_primary'], relief=tk.FLAT)
        self.username_entry.pack(pady=(0, 15))
        
        tk.Label(form_frame, text="Password:", font=('Segoe UI', 11),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(0, 5))
        
        self.password_entry = tk.Entry(form_frame, font=('Segoe UI', 11), width=25, show="*",
                                      bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                      insertbackground=self.colors['text_primary'], relief=tk.FLAT)
        self.password_entry.pack(pady=(0, 20))
        
        # Login button
        login_btn = tk.Button(form_frame, text="LOGIN", font=('Segoe UI', 12, 'bold'),
                            bg=self.colors['accent'], fg=self.colors['bg_primary'],
                            activebackground='#00a8cc', relief=tk.FLAT, cursor='hand2',
                            command=self.login, width=20, height=2)
        login_btn.pack(pady=10)
        
        # Quick access buttons
        quick_frame = tk.Frame(card, bg=self.colors['bg_card'])
        quick_frame.pack(pady=20)
        
        tk.Label(quick_frame, text="Quick Access:", font=('Segoe UI', 9),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack()
        
        demo_frame = tk.Frame(quick_frame, bg=self.colors['bg_card'])
        demo_frame.pack(pady=5)
        
        tk.Button(demo_frame, text="Admin", font=('Segoe UI', 9),
                 bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=lambda: self.quick_login('admin', 'admin123')).pack(side=tk.LEFT, padx=2)
        tk.Button(demo_frame, text="Manager", font=('Segoe UI', 9),
                 bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=lambda: self.quick_login('manager', 'manager123')).pack(side=tk.LEFT, padx=2)
        tk.Button(demo_frame, text="Cashier", font=('Segoe UI', 9),
                 bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=lambda: self.quick_login('cashier', 'cashier123')).pack(side=tk.LEFT, padx=2)
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()
    
    def quick_login(self, username, password):
        """Quick login for demo"""
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, username)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.login()
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Login Error", "Please enter username and password")
            return
        
        if username in self.users:
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            if self.users[username]['password'] == hashed_password:
                self.current_user = {
                    'username': username,
                    'name': self.users[username]['name'],
                    'role': self.users[username]['role'],
                    'permissions': self.users[username]['permissions']
                }
                self.show_notification(f"Welcome back, {self.current_user['name']}!", 'success')
                self.create_main_interface()
                return
        
        messagebox.showerror("Login Failed", "Invalid username or password")
    
    def create_main_interface(self):
        """Create main dashboard"""
        self.clear_window()
        
        # Header
        self.create_header()
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.create_sidebar(main_container)
        
        # Content area
        self.content_area = tk.Frame(main_container, bg=self.colors['bg_primary'])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Show dashboard
        self.show_dashboard()
    
    def create_header(self):
        """Create modern header"""
        header = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Left side - Logo and title
        left_frame = tk.Frame(header, bg=self.colors['bg_secondary'])
        left_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(left_frame, text="🍽️", font=('Segoe UI', 20),
                bg=self.colors['bg_secondary'], fg=self.colors['accent']).pack(side=tk.LEFT)
        tk.Label(left_frame, text="RestaurantOS", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary']).pack(side=tk.LEFT, padx=8)
        tk.Label(left_frame, text="Professional", font=('Segoe UI', 9, 'italic'),
                bg=self.colors['bg_secondary'], fg=self.colors['accent']).pack(side=tk.LEFT)
        
        # Right side - User info and logout
        right_frame = tk.Frame(header, bg=self.colors['bg_secondary'])
        right_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # User info
        user_frame = tk.Frame(right_frame, bg=self.colors['bg_card'], relief=tk.FLAT)
        user_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(user_frame, text=f"👤 {self.current_user['name']}", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(user_frame, text="Logout", font=('Segoe UI', 9),
                 bg=self.colors['danger'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=self.logout).pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_sidebar(self, parent):
        """Create modern sidebar based on user role"""
        sidebar = tk.Frame(parent, bg=self.colors['bg_secondary'], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Quick stats
        stats_frame = tk.Frame(sidebar, bg=self.colors['bg_card'], relief=tk.FLAT)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(stats_frame, text="Today's Overview", font=('Segoe UI', 11, 'bold'),
                bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=10)
        
        today_orders = len([o for o in self.data['orders'] if o['date'] == self.current_date])
        today_sales = self.data['daily_sales'].get(self.current_date, 0)
        
        stats = [
            ("Orders", str(today_orders), self.colors['accent']),
            ("Revenue", f"${today_sales:.0f}", self.colors['success']),
            ("Tables", "10/10", self.colors['warning'])
        ]
        
        for label, value, color in stats:
            stat_frame = tk.Frame(stats_frame, bg=self.colors['bg_card'])
            stat_frame.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(stat_frame, text=label, font=('Segoe UI', 9),
                    bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)
            tk.Label(stat_frame, text=value, font=('Segoe UI', 10, 'bold'),
                    bg=self.colors['bg_card'], fg=color).pack(side=tk.RIGHT)
        
        # Navigation menu based on user role
        nav_frame = tk.Frame(sidebar, bg=self.colors['bg_secondary'])
        nav_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)
        
        # Define menu items based on user role
        if self.current_user['role'] == 'Administrator':
            menu_items = [
                ("🏠 Dashboard", self.show_dashboard),
                ("📋 Orders", self.open_orders),
                ("🍽️ Menu Management", self.open_menu_management),
                ("📦 Inventory", self.open_inventory),
                ("👥 Customers", self.open_customer_management),
                ("👨‍🍳 Kitchen", self.open_kitchen_display),
                ("💰 Accounting", self.open_accounting),
                ("👥 Employees", self.open_employee_management),
                ("⚙️ Settings", self.open_settings)
            ]
        elif self.current_user['role'] == 'Manager':
            menu_items = [
                ("🏠 Dashboard", self.show_dashboard),
                ("📋 Orders", self.open_orders),
                ("🍽️ Menu Management", self.open_menu_management),
                ("📦 Inventory", self.open_inventory),
                ("👥 Customers", self.open_customer_management),
                ("👨‍🍳 Kitchen", self.open_kitchen_display),
                ("💰 Accounting", self.open_accounting),
                ("📊 Reports", self.open_reports)
            ]
        else:  # Cashier
            menu_items = [
                ("🏠 Dashboard", self.show_dashboard),
                ("📋 Orders", self.open_orders),
                ("👥 Customers", self.open_customer_management)
            ]
        
        for text, command in menu_items:
            btn = tk.Button(nav_frame, text=text, font=('Segoe UI', 10),
                           bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'],
                           relief=tk.FLAT, anchor='w', command=command,
                           activebackground=self.colors['bg_card'], activeforeground=self.colors['accent'])
            btn.pack(fill=tk.X, pady=2, padx=5)
    
    def show_dashboard(self):
        """Show main dashboard"""
        self.clear_content()
        
        # Dashboard title
        title_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="Dashboard", font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        tk.Label(title_frame, text=f"📅 {datetime.now().strftime('%A, %B %d, %Y')}", font=('Segoe UI', 12),
                bg=self.colors['bg_primary'], fg=self.colors['text_secondary']).pack(side=tk.RIGHT)
        
        # Key metrics cards
        metrics_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        metrics_frame.pack(fill=tk.X, pady=10)
        
        # Calculate metrics
        total_revenue = sum(self.data['daily_sales'].values())
        total_orders = len(self.data['orders'])
        avg_order = total_revenue / total_orders if total_orders > 0 else 0
        today_orders = len([o for o in self.data['orders'] if o['date'] == self.current_date])
        today_revenue = self.data['daily_sales'].get(self.current_date, 0)
        
        metrics = [
            ("Today's Revenue", f"${today_revenue:.2f}", self.colors['success'], "📈"),
            ("Today's Orders", str(today_orders), self.colors['accent'], "📋"),
            ("Avg Order Value", f"${avg_order:.2f}", self.colors['warning'], "💰"),
            ("Total Revenue", f"${total_revenue:.2f}", self.colors['success'], "💵"),
            ("Total Orders", str(total_orders), self.colors['accent'], "📊"),
            ("Active Tables", "10/10", self.colors['warning'], "🪑")
        ]
        
        for i, (title, value, color, icon) in enumerate(metrics):
            card = tk.Frame(metrics_frame, bg=self.colors['bg_card'], relief=tk.RAISED, bd=1)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky='nsew')
            
            tk.Label(card, text=icon, font=('Segoe UI', 20),
                    bg=self.colors['bg_card'], fg=color).pack(pady=(15, 5))
            tk.Label(card, text=title, font=('Segoe UI', 10),
                    bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack()
            tk.Label(card, text=value, font=('Segoe UI', 18, 'bold'),
                    bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(pady=(5, 15))
        
        # Configure grid
        for i in range(3):
            metrics_frame.grid_columnconfigure(i, weight=1)
        
        # Quick actions
        bottom_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        actions_frame = tk.LabelFrame(bottom_frame, text="Quick Actions", font=('Segoe UI', 12, 'bold'),
                                     bg=self.colors['bg_card'], fg=self.colors['text_primary'])
        actions_frame.pack(fill=tk.BOTH, expand=True)
        
        # Different quick actions based on user role
        if self.current_user['role'] == 'Administrator':
            actions = [
                ("➕ New Order", self.open_quick_order),
                ("➕ Add Menu Item", self.add_menu_item),
                ("➕ Add Customer", self.add_customer),
                ("➕ Add Expense", self.add_expense),
                ("👥 Add Employee", self.add_employee)
            ]
        elif self.current_user['role'] == 'Manager':
            actions = [
                ("➕ New Order", self.open_quick_order),
                ("➕ Add Menu Item", self.add_menu_item),
                ("➕ Add Customer", self.add_customer),
                ("➕ Add Expense", self.add_expense)
            ]
        else:  # Cashier
            actions = [
                ("➕ New Order", self.open_quick_order),
                ("➕ Add Customer", self.add_customer)
            ]
        
        for text, command in actions:
            btn = tk.Button(actions_frame, text=text, font=('Segoe UI', 10),
                           bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                           relief=tk.FLAT, anchor='w', command=command,
                           activebackground=self.colors['accent'], activeforeground=self.colors['bg_primary'])
            btn.pack(fill=tk.X, padx=15, pady=5)
    
    def open_orders(self):
        """Open orders management"""
        self.clear_content()
        
        # Title
        title_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="Order Management", font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        # Action buttons based on user role
        if self.current_user['role'] in ['Administrator', 'Manager']:
            tk.Button(title_frame, text="➕ New Order", font=('Segoe UI', 10, 'bold'),
                     bg=self.colors['success'], fg=self.colors['text_primary'],
                     relief=tk.FLAT, command=self.open_quick_order).pack(side=tk.RIGHT, padx=5)
        
        # Orders table
        table_frame = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview
        columns = ('ID', 'Table', 'Customer', 'Items', 'Total', 'Status', 'Time')
        self.orders_tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Modern.Treeview')
        
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate orders
        self.update_orders_display()
        
        # Action buttons frame
        action_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        action_frame.pack(fill=tk.X, pady=10)
        
        # Print button (available to all users)
        tk.Button(action_frame, text="🖨️ Print List", font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['warning'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=self.print_order_list).pack(side=tk.LEFT, padx=5)
        
        # Additional buttons based on role
        if self.current_user['role'] in ['Administrator', 'Manager']:
            tk.Button(action_frame, text="📋 View Details", font=('Segoe UI', 10),
                     bg=self.colors['accent'], fg=self.colors['text_primary'],
                     relief=tk.FLAT, command=self.view_order_details).pack(side=tk.LEFT, padx=5)
            tk.Button(action_frame, text="📊 Export Orders", font=('Segoe UI', 10),
                     bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                     relief=tk.FLAT, command=self.export_orders).pack(side=tk.LEFT, padx=5)
    
    def update_orders_display(self):
        """Update orders treeview"""
        # Clear existing items
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        # Add orders
        for order in sorted(self.data['orders'], key=lambda x: x.get('id', 0), reverse=True):
            items_count = len(order['items'])
            status = order.get('status', 'active')
            
            self.orders_tree.insert('', tk.END, values=(
                order['id'], order['table'], order.get('customer', 'Walk-in'),
                items_count, f"${order['total']:.2f}", status.title(),
                order.get('time', 'N/A')
            ))
    
    def print_order_list(self):
        """Print order list"""
        # Create a new window for the print preview
        print_window = tk.Toplevel(self.root)
        print_window.title("Print Order List")
        print_window.geometry("600x500")
        print_window.configure(bg='white')
        
        # Title
        title_frame = tk.Frame(print_window, bg='white')
        title_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(title_frame, text="ORDER LIST", font=('Arial', 16, 'bold'),
                bg='white').pack()
        tk.Label(title_frame, text=f"Date: {self.current_date}", font=('Arial', 10),
                bg='white').pack()
        tk.Label(title_frame, text=f"Printed by: {self.current_user['name']}", font=('Arial', 10),
                bg='white').pack()
        
        # Separator
        separator = tk.Frame(print_window, height=2, bg='black')
        separator.pack(fill=tk.X, pady=5)
        
        # Orders content
        content_frame = tk.Frame(print_window, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create text widget for order list
        order_text = tk.Text(content_frame, font=('Courier', 10), bg='white', wrap=tk.WORD)
        order_text.pack(fill=tk.BOTH, expand=True)
        
        # Generate order list content
        order_content = "ID\tTable\tCustomer\t\tItems\tTotal\tStatus\tTime\n"
        order_content += "-" * 80 + "\n"
        
        for order in sorted(self.data['orders'], key=lambda x: x.get('id', 0), reverse=True):
            items_count = len(order['items'])
            order_content += f"{order['id']}\t{order['table']}\t{order.get('customer', 'Walk-in')}\t\t{items_count}\t${order['total']:.2f}\t{order.get('status', 'active')}\t{order.get('time', 'N/A')}\n"
        
        order_text.insert(tk.END, order_content)
        order_text.config(state=tk.DISABLED)
        
        # Print buttons
        button_frame = tk.Frame(print_window, bg='white')
        button_frame.pack(fill=tk.X, pady=10)
        
        def actual_print():
            # In a real application, this would send to printer
            messagebox.showinfo("Print", "Order list sent to printer!")
            print_window.destroy()
        
        def save_to_file():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"order_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            if filename:
                try:
                    with open(filename, 'w') as f:
                        f.write(f"ORDER LIST\n")
                        f.write(f"Date: {self.current_date}\n")
                        f.write(f"Printed by: {self.current_user['name']}\n")
                        f.write("-" * 80 + "\n")
                        f.write(order_content)
                    messagebox.showinfo("Success", f"Order list saved to {filename}")
                    print_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {e}")
        
        tk.Button(button_frame, text="🖨️ Print", font=('Arial', 10, 'bold'),
                 bg=self.colors['success'], fg='white',
                 command=actual_print).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="💾 Save to File", font=('Arial', 10, 'bold'),
                 bg=self.colors['accent'], fg='white',
                 command=save_to_file).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Cancel", font=('Arial', 10),
                 bg=self.colors['danger'], fg='white',
                 command=print_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def view_order_details(self):
        """View order details"""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an order to view details")
            return
        
        # Get selected order
        item_values = self.orders_tree.item(selection[0])['values']
        order_id = item_values[0]
        
        # Find order in data
        order = next((o for o in self.data['orders'] if o['id'] == order_id), None)
        if not order:
            return
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Order #{order_id} Details")
        details_window.geometry("500x400")
        details_window.configure(bg=self.colors['bg_primary'])
        details_window.transient(self.root)
        details_window.grab_set()
        
        # Order info
        info_frame = tk.Frame(details_window, bg=self.colors['bg_card'])
        info_frame.pack(fill=tk.X, padx=20, pady=20)
        
        info_text = f"""
        Order ID: {order['id']}
        Table: {order['table']}
        Customer: {order.get('customer', 'Walk-in')}
        Date: {order['date']}
        Time: {order.get('time', 'N/A')}
        Status: {order.get('status', 'active')}
        Total: ${order['total']:.2f}
        """
        
        tk.Label(info_frame, text=info_text, font=('Segoe UI', 11),
                bg=self.colors['bg_card'], fg=self.colors['text_primary'],
                justify=tk.LEFT).pack(anchor='w')
        
        # Items
        items_frame = tk.LabelFrame(details_window, text="Order Items", 
                                     font=('Segoe UI', 12, 'bold'),
                                     bg=self.colors['bg_card'], fg=self.colors['text_primary'])
        items_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create treeview for items
        columns = ('Item', 'Price', 'Quantity')
        items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', style='Modern.Treeview')
        
        for col in columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=150)
        
        # Add items
        for item in order['items']:
            items_tree.insert('', tk.END, values=(
                item['name'], f"${item['price']:.2f}", 1
            ))
        
        items_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Close button
        tk.Button(details_window, text="Close", font=('Segoe UI', 10),
                 bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=details_window.destroy).pack(pady=10)
    
    def export_orders(self):
        """Export orders to CSV"""
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['ID', 'Table', 'Customer', 'Total', 'Date', 'Time', 'Status'])
                    for order in self.data['orders']:
                        writer.writerow([order['id'], order['table'], order.get('customer', 'Walk-in'),
                                       order['total'], order['date'], order.get('time', ''), order.get('status', '')])
                self.show_notification("Orders exported successfully", 'success')
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {e}")
    
    def open_menu_management(self):
        """Open menu management"""
        self.clear_content()
        
        # Title
        title_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="Menu Management", font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        # Add button only for admin and manager
        if self.current_user['role'] in ['Administrator', 'Manager']:
            tk.Button(title_frame, text="➕ Add Item", font=('Segoe UI', 10, 'bold'),
                     bg=self.colors['success'], fg=self.colors['text_primary'],
                     relief=tk.FLAT, command=self.add_menu_item).pack(side=tk.RIGHT, padx=5)
        
        # Category tabs
        category_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        category_frame.pack(fill=tk.X, pady=10)
        
        self.selected_category = tk.StringVar(value='Appetizers')
        categories = list(self.data['menu'].keys())
        
        for category in categories:
            tk.Radiobutton(category_frame, text=category, variable=self.selected_category,
                          value=category, command=self.update_menu_display,
                          bg=self.colors['bg_primary'], fg=self.colors['text_primary'],
                          selectcolor=self.colors['bg_secondary'], font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=10)
        
        # Menu items
        items_frame = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview
        columns = ('Name', 'Price', 'Cost', 'Profit')
        self.menu_tree = ttk.Treeview(items_frame, columns=columns, show='headings', style='Modern.Treeview')
        
        for col in columns:
            self.menu_tree.heading(col, text=col)
            self.menu_tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=self.menu_tree.yview)
        self.menu_tree.configure(yscrollcommand=scrollbar.set)
        
        self.menu_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate menu
        self.update_menu_display()
    
    def update_menu_display(self):
        """Update menu treeview"""
        # Clear existing items
        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)
        
        # Add menu items for selected category
        category = self.selected_category.get()
        for item in self.data['menu'].get(category, []):
            profit = item['price'] - item['cost']
            self.menu_tree.insert('', tk.END, values=(
                item['name'], f"${item['price']:.2f}", f"${item['cost']:.2f}",
                f"${profit:.2f}"
            ))
    
    def open_inventory(self):
        """Open inventory management"""
        self.clear_content()
        
        # Title
        title_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="Inventory Management", font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        # Add button only for admin and manager
        if self.current_user['role'] in ['Administrator', 'Manager']:
            tk.Button(title_frame, text="➕ Add Item", font=('Segoe UI', 10, 'bold'),
                     bg=self.colors['success'], fg=self.colors['text_primary'],
                     relief=tk.FLAT, command=self.add_inventory_item).pack(side=tk.RIGHT, padx=5)
        
        # Inventory table
        table_frame = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview
        columns = ('Item', 'Quantity', 'Unit', 'Min Stock', 'Status')
        self.inventory_tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Modern.Treeview')
        
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        
        self.inventory_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate inventory
        self.update_inventory_display()
    
    def update_inventory_display(self):
        """Update inventory treeview"""
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        # Add inventory items
        for item_name, item_data in self.data['inventory'].items():
            quantity = item_data['quantity']
            min_stock = item_data['min_stock']
            
            if quantity <= min_stock:
                status = "Low Stock"
                tag = 'low_stock'
            else:
                status = "Good"
                tag = 'good_stock'
            
            self.inventory_tree.insert('', tk.END, values=(
                item_name, quantity, item_data['unit'], min_stock, status
            ), tags=(tag,))
        
        # Configure tags
        self.inventory_tree.tag_configure('low_stock', background='#ffcccc')
        self.inventory_tree.tag_configure('good_stock', background='#ccffcc')
    
    def open_customer_management(self):
        """Open customer management"""
        self.clear_content()
        
        # Title
        title_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="Customer Management", font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        tk.Button(title_frame, text="➕ Add Customer", font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=self.add_customer).pack(side=tk.RIGHT, padx=5)
        
        # Customer table
        table_frame = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview
        columns = ('Name', 'Phone', 'Email', 'Visits', 'Points')
        self.customer_tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Modern.Treeview')
        
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar.set)
        
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate customers
        self.update_customer_display()
    
    def update_customer_display(self):
        """Update customer treeview"""
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Add customers
        for customer in self.data['customers']:
            self.customer_tree.insert('', tk.END, values=(
                customer['name'], customer['phone'], customer['email'],
                customer['visits'], customer['loyalty_points']
            ))
    
    def open_kitchen_display(self):
        """Open kitchen display system"""
        self.clear_content()
        
        # Title
        title_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="👨‍🍳 Kitchen Display System", font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        # Current time
        self.time_label = tk.Label(title_frame, text="", font=('Segoe UI', 14),
                                  bg=self.colors['bg_primary'], fg=self.colors['accent'])
        self.time_label.pack(side=tk.RIGHT)
        self.update_time()
        
        # Orders in progress
        orders_frame = tk.LabelFrame(self.content_area, text="Orders in Progress", 
                                    font=('Segoe UI', 14, 'bold'),
                                    bg=self.colors['bg_card'], fg=self.colors['text_primary'])
        orders_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create order cards
        self.kitchen_orders_frame = tk.Frame(orders_frame, bg=self.colors['bg_card'])
        self.kitchen_orders_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.update_kitchen_display()
        
        # Auto-refresh
        self.root.after(30000, self.update_kitchen_display)  # Refresh every 30 seconds
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%I:%M %p")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def update_kitchen_display(self):
        """Update kitchen display"""
        # Clear existing orders
        for widget in self.kitchen_orders_frame.winfo_children():
            widget.destroy()
        
        # Get active orders
        active_orders = [o for o in self.data['orders'] if o.get('status') == 'active']
        
        if not active_orders:
            tk.Label(self.kitchen_orders_frame, text="No active orders", font=('Segoe UI', 16),
                    bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(expand=True)
            return
        
        # Display orders
        for order in active_orders[:6]:  # Show max 6 orders
            order_card = tk.Frame(self.kitchen_orders_frame, bg=self.colors['bg_secondary'], 
                                 relief=tk.RAISED, bd=2)
            order_card.pack(fill=tk.X, pady=5)
            
            # Order header
            header_frame = tk.Frame(order_card, bg=self.colors['bg_secondary'])
            header_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(header_frame, text=f"Order #{order['id']} - Table {order['table']}", 
                    font=('Segoe UI', 12, 'bold'),
                    bg=self.colors['bg_secondary'], fg=self.colors['accent']).pack(side=tk.LEFT)
            tk.Label(header_frame, text=order.get('time', ''), font=('Segoe UI', 10),
                    bg=self.colors['bg_secondary'], fg=self.colors['text_secondary']).pack(side=tk.RIGHT)
            
            # Order items
            items_frame = tk.Frame(order_card, bg=self.colors['bg_secondary'])
            items_frame.pack(fill=tk.X, padx=10, pady=5)
            
            for item in order['items']:
                item_frame = tk.Frame(items_frame, bg=self.colors['bg_secondary'])
                item_frame.pack(fill=tk.X, pady=2)
                
                tk.Label(item_frame, text=f"• {item['name']}", font=('Segoe UI', 10),
                        bg=self.colors['bg_secondary'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
            
            # Action button
            tk.Button(order_card, text="Mark Ready", font=('Segoe UI', 10, 'bold'),
                     bg=self.colors['success'], fg=self.colors['text_primary'],
                     relief=tk.FLAT, command=lambda o=order: self.mark_order_ready(o)).pack(pady=5)
    
    def mark_order_ready(self, order):
        """Mark order as ready"""
        order['status'] = 'ready'
        self.show_notification(f"Order #{order['id']} is ready for pickup!", 'success')
        self.update_kitchen_display()
        self.save_data()
    
    def open_accounting(self):
        """Open accounting system"""
        self.clear_content()
        
        # Title
        title_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="Accounting & Finance", font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        # Add expense button only for admin and manager
        if self.current_user['role'] in ['Administrator', 'Manager']:
            tk.Button(title_frame, text="➕ Add Expense", font=('Segoe UI', 10, 'bold'),
                     bg=self.colors['success'], fg=self.colors['text_primary'],
                     relief=tk.FLAT, command=self.add_expense).pack(side=tk.RIGHT, padx=5)
        
        # Financial summary
        summary_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        summary_frame.pack(fill=tk.X, pady=10)
        
        # Calculate metrics
        total_revenue = sum(self.data['daily_sales'].values())
        total_expenses = sum(e['amount'] for e in self.data['expenses'])
        net_profit = total_revenue - total_expenses
        
        metrics = [
            ("Total Revenue", f"${total_revenue:.2f}", self.colors['success']),
            ("Total Expenses", f"${total_expenses:.2f}", self.colors['danger']),
            ("Net Profit", f"${net_profit:.2f}", self.colors['success'] if net_profit > 0 else self.colors['danger'])
        ]
        
        for title, value, color in metrics:
            card = tk.Frame(summary_frame, bg=self.colors['bg_card'], relief=tk.RAISED, bd=1)
            card.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
            
            tk.Label(card, text=title, font=('Segoe UI', 10),
                    bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(pady=10)
            tk.Label(card, text=value, font=('Segoe UI', 16, 'bold'),
                    bg=self.colors['bg_card'], fg=color).pack(pady=(0, 10))
        
        # Expense list
        expense_frame = tk.LabelFrame(self.content_area, text="Recent Expenses", 
                                     font=('Segoe UI', 12, 'bold'),
                                     bg=self.colors['bg_card'], fg=self.colors['text_primary'])
        expense_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview
        columns = ('Date', 'Description', 'Amount')
        expense_tree = ttk.Treeview(expense_frame, columns=columns, show='headings', style='Modern.Treeview')
        
        for col in columns:
            expense_tree.heading(col, text=col)
            expense_tree.column(col, width=120)
        
        # Add expenses
        for expense in reversed(self.data['expenses'][-10:]):
            expense_tree.insert('', tk.END, values=(
                expense['date'], expense['description'],
                f"${expense['amount']:.2f}"
            ))
        
        expense_tree.pack(fill=tk.BOTH, expand=True)
    
    def open_employee_management(self):
        """Open employee management (admin only)"""
        self.clear_content()
        
        # Title
        title_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="Employee Management", font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        tk.Button(title_frame, text="➕ Add Employee", font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=self.add_employee).pack(side=tk.RIGHT, padx=5)
        
        # Employee table
        table_frame = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview
        columns = ('Name', 'Position', 'Email', 'Phone', 'Salary', 'Status')
        self.employee_tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Modern.Treeview')
        
        for col in columns:
            self.employee_tree.heading(col, text=col)
            self.employee_tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.employee_tree.yview)
        self.employee_tree.configure(yscrollcommand=scrollbar.set)
        
        self.employee_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate employees
        self.update_employee_display()
    
    def update_employee_display(self):
        """Update employee treeview"""
        # Clear existing items
        for item in self.employee_tree.get_children():
            self.employee_tree.delete(item)
        
        # Add employees
        for employee in self.data['employees']:
            status_color = 'active' if employee['status'] == 'active' else 'inactive'
            
            self.employee_tree.insert('', tk.END, values=(
                employee['name'], employee['position'], employee['email'],
                employee['phone'], f"${employee['salary']:.2f}", employee['status'].title()
            ), tags=(status_color,))
        
        # Configure tags
        self.employee_tree.tag_configure('active', foreground=self.colors['success'])
        self.employee_tree.tag_configure('inactive', foreground=self.colors['text_secondary'])
    
    def open_reports(self):
        """Open reports (manager only)"""
        self.clear_content()
        
        # Title
        title_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="Reports & Analytics", font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        # Report types
        reports_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        reports_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        report_types = [
            ("📊 Sales Report", self.generate_sales_report),
            ("📦 Inventory Report", self.generate_inventory_report),
            ("👥 Customer Report", self.generate_customer_report),
            ("💰 Financial Report", self.generate_financial_report)
        ]
        
        for i, (title, command) in enumerate(report_types):
            row = i // 2
            col = i % 2
            
            btn_frame = tk.Frame(reports_frame, bg=self.colors['bg_card'], relief=tk.RAISED, bd=1)
            btn_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            tk.Button(btn_frame, text=title, font=('Segoe UI', 12, 'bold'),
                     bg=self.colors['bg_card'], fg=self.colors['text_primary'],
                     relief=tk.FLAT, command=command, width=20, height=5).pack(expand=True)
        
        # Configure grid
        reports_frame.grid_columnconfigure(0, weight=1)
        reports_frame.grid_columnconfigure(1, weight=1)
        reports_frame.grid_rowconfigure(0, weight=1)
        reports_frame.grid_rowconfigure(1, weight=1)
    
    def open_settings(self):
        """Open settings (admin only)"""
        self.clear_content()
        
        # Title
        title_frame = tk.Frame(self.content_area, bg=self.colors['bg_primary'])
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="Settings", font=('Segoe UI', 24, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        
        # Settings content
        settings_frame = tk.Frame(self.content_area, bg=self.colors['bg_card'])
        settings_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Restaurant info
        info_frame = tk.LabelFrame(settings_frame, text="Restaurant Information", 
                                  font=('Segoe UI', 12, 'bold'),
                                  bg=self.colors['bg_card'], fg=self.colors['text_primary'])
        info_frame.pack(fill=tk.X, padx=20, pady=20)
        
        fields = [
            ("Restaurant Name:", ""),
            ("Address:", ""),
            ("Phone:", ""),
            ("Email:", "")
        ]
        
        for label, default in fields:
            field_frame = tk.Frame(info_frame, bg=self.colors['bg_card'])
            field_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(field_frame, text=label, font=('Segoe UI', 10),
                    bg=self.colors['bg_card'], fg=self.colors['text_secondary'], width=15, anchor='w').pack(side=tk.LEFT)
            tk.Entry(field_frame, font=('Segoe UI', 10), bg=self.colors['bg_secondary'],
                    fg=self.colors['text_primary'], insertbackground=self.colors['text_primary'], 
                    relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Tax settings
        tax_frame = tk.LabelFrame(settings_frame, text="Tax Settings", font=('Segoe UI', 12, 'bold'),
                                 bg=self.colors['bg_card'], fg=self.colors['text_primary'])
        tax_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(tax_frame, text="Tax Rate (%):", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=10)
        
        tax_var = tk.StringVar(value=str(self.data['tax_settings']['rate'] * 100))
        tk.Entry(tax_frame, textvariable=tax_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT, width=10).pack(side=tk.LEFT)
        
        # Save button
        tk.Button(settings_frame, text="Save Settings", font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT).pack(pady=20)
    
    # Quick action methods
    def open_quick_order(self):
        """Open quick order dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Quick Order")
        dialog.geometry("600x500")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Quick Order", font=('Segoe UI', 18, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(pady=20)
        
        # Order form
        form_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Customer info
        customer_frame = tk.Frame(form_frame, bg=self.colors['bg_card'])
        customer_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(customer_frame, text="Customer Name:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=5)
        
        customer_var = tk.StringVar()
        tk.Entry(customer_frame, textvariable=customer_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Label(customer_frame, text="Table:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=5)
        
        table_var = tk.StringVar(value="1")
        tk.Spinbox(customer_frame, from_=1, to=10, textvariable=table_var,
                  font=('Segoe UI', 10), bg=self.colors['bg_secondary'],
                  fg=self.colors['text_primary'], relief=tk.FLAT, width=5).pack(side=tk.LEFT, padx=5)
        
        # Menu items
        menu_frame = tk.LabelFrame(form_frame, text="Select Items", font=('Segoe UI', 11, 'bold'),
                                 bg=self.colors['bg_card'], fg=self.colors['text_primary'])
        menu_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Show message if no menu items
        if not any(self.data['menu'].values()):
            tk.Label(menu_frame, text="No menu items available. Please add menu items first.", 
                    font=('Segoe UI', 11), bg=self.colors['bg_card'], fg=self.colors['warning']).pack(pady=20)
        else:
            # Display menu items
            for category, items in self.data['menu'].items():
                if items:
                    cat_frame = tk.Frame(menu_frame, bg=self.colors['bg_card'])
                    cat_frame.pack(fill=tk.X, pady=5)
                    
                    tk.Label(cat_frame, text=category, font=('Segoe UI', 10, 'bold'),
                            bg=self.colors['bg_card'], fg=self.colors['accent']).pack(anchor='w')
                    
                    for item in items:
                        item_frame = tk.Frame(cat_frame, bg=self.colors['bg_secondary'])
                        item_frame.pack(fill=tk.X, pady=2)
                        
                        tk.Label(item_frame, text=f"{item['name']} - ${item['price']:.2f}", 
                                font=('Segoe UI', 9), bg=self.colors['bg_secondary'], 
                                fg=self.colors['text_primary']).pack(side=tk.LEFT, padx=10)
                        
                        self.quick_order_items = []
                        tk.Button(item_frame, text="Add", font=('Segoe UI', 8),
                                 bg=self.colors['accent'], fg=self.colors['text_primary'],
                                 relief=tk.FLAT, 
                                 command=lambda i=item: self.add_quick_order_item(i)).pack(side=tk.RIGHT, padx=5)
        
        # Order summary
        summary_frame = tk.LabelFrame(form_frame, text="Order Summary", font=('Segoe UI', 11, 'bold'),
                                     bg=self.colors['bg_card'], fg=self.colors['text_primary'])
        summary_frame.pack(fill=tk.X, pady=10)
        
        self.quick_order_label = tk.Label(summary_frame, text="No items selected", font=('Segoe UI', 10),
                                        bg=self.colors['bg_card'], fg=self.colors['text_secondary'])
        self.quick_order_label.pack(pady=5)
        
        self.quick_total_label = tk.Label(summary_frame, text="Total: $0.00", font=('Segoe UI', 12, 'bold'),
                                        bg=self.colors['bg_card'], fg=self.colors['success'])
        self.quick_total_label.pack(pady=5)
        
        # Action buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['bg_card'])
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Clear", font=('Segoe UI', 10),
                 bg=self.colors['danger'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=lambda: self.clear_quick_order(dialog)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Confirm Order", font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=lambda: self.confirm_quick_order(dialog, customer_var, table_var)).pack(side=tk.LEFT, padx=5)
    
    def add_quick_order_item(self, item):
        """Add item to quick order"""
        if not hasattr(self, 'quick_order_items'):
            self.quick_order_items = []
        self.quick_order_items.append(item.copy())
        self.update_quick_order_display()
        self.show_notification(f"Added {item['name']} to order", 'success')
    
    def update_quick_order_display(self):
        """Update quick order display"""
        if hasattr(self, 'quick_order_label') and hasattr(self, 'quick_total_label'):
            if not self.quick_order_items:
                self.quick_order_label.config(text="No items selected")
                self.quick_total_label.config(text="Total: $0.00")
                return
            
            # Group items by name
            item_counts = defaultdict(int)
            for item in self.quick_order_items:
                item_counts[item['name']] += 1
            
            # Create display text
            display_text = "\n".join([f"{count}x {name}" for name, count in item_counts.items()])
            self.quick_order_label.config(text=display_text)
            
            # Calculate total
            total = sum(item['price'] for item in self.quick_order_items)
            self.quick_total_label.config(text=f"Total: ${total:.2f}")
    
    def clear_quick_order(self, dialog):
        """Clear quick order"""
        self.quick_order_items = []
        self.update_quick_order_display()
    
    def confirm_quick_order(self, dialog, customer_var, table_var):
        """Confirm quick order"""
        if not self.quick_order_items:
            messagebox.showwarning("No Items", "Please add items to the order")
            return
        
        total = sum(item['price'] for item in self.quick_order_items)
        
        # Create order
        order = {
            'id': len(self.data['orders']) + 1,
            'table': table_var.get(),
            'customer': customer_var.get() or 'Walk-in',
            'items': self.quick_order_items.copy(),
            'total': total,
            'date': self.current_date,
            'time': datetime.now().strftime("%H:%M"),
            'status': 'active'
        }
        
        # Save order
        self.data['orders'].append(order)
        self.data['daily_sales'][self.current_date] += total
        
        # Add to kitchen orders for display
        self.data['kitchen_orders'].append(order)
        
        # Show confirmation
        messagebox.showinfo("Order Confirmed", f"Order #{order['id']} has been confirmed!\nTotal: ${total:.2f}")
        
        # Clear and close
        self.clear_quick_order(dialog)
        dialog.destroy()
        self.save_data()
        self.show_notification(f"New order #{order['id']} created", 'success')
        
        # Refresh displays
        if hasattr(self, 'orders_tree'):
            self.update_orders_display()
        if hasattr(self, 'kitchen_orders_frame'):
            self.update_kitchen_display()
    
    def add_menu_item(self):
        """Add new menu item"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Menu Item")
        dialog.geometry("400x400")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add New Menu Item", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(pady=20)
        
        # Form fields
        form_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Name
        tk.Label(form_frame, text="Item Name:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        name_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=name_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        # Category
        tk.Label(form_frame, text="Category:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        category_var = tk.StringVar(value="Appetizers")
        category_combo = ttk.Combobox(form_frame, textvariable=category_var,
                                     values=list(self.data['menu'].keys()), font=('Segoe UI', 10))
        category_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Price
        tk.Label(form_frame, text="Price (PKR):", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        price_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=price_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        # Cost
        tk.Label(form_frame, text="Cost (PKR):", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        cost_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=cost_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['bg_card'])
        button_frame.pack(pady=20)
        
        def save_item():
            try:
                new_item = {
                    'name': name_var.get(),
                    'price': float(price_var.get()),
                    'cost': float(cost_var.get())
                }
                
                # Add to menu
                self.data['menu'][category_var.get()].append(new_item)
                
                # Add to inventory if not exists
                if new_item['name'] not in self.data['inventory']:
                    self.data['inventory'][new_item['name']] = {
                        'quantity': 50,
                        'unit': 'servings',
                        'min_stock': 10
                    }
                
                self.save_data()
                self.update_menu_display()
                dialog.destroy()
                self.show_notification(f"Menu item '{new_item['name']}' added successfully", 'success')
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price and cost")
        
        tk.Button(button_frame, text="Save Item", font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=save_item).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Cancel", font=('Segoe UI', 10),
                 bg=self.colors['danger'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def add_inventory_item(self):
        """Add new inventory item"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Inventory Item")
        dialog.geometry("400x350")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add New Inventory Item", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(pady=20)
        
        # Form fields
        form_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Item name
        tk.Label(form_frame, text="Item Name:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        name_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=name_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        # Quantity
        tk.Label(form_frame, text="Quantity:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        quantity_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=quantity_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        # Unit
        tk.Label(form_frame, text="Unit:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        unit_var = tk.StringVar(value="servings")
        tk.Entry(form_frame, textvariable=unit_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        # Min stock
        tk.Label(form_frame, text="Min Stock:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        min_stock_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=min_stock_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['bg_card'])
        button_frame.pack(pady=20)
        
        def save_item():
            try:
                self.data['inventory'][name_var.get()] = {
                    'quantity': int(quantity_var.get()),
                    'unit': unit_var.get(),
                    'min_stock': int(min_stock_var.get())
                }
                
                self.save_data()
                self.update_inventory_display()
                dialog.destroy()
                self.show_notification(f"Inventory item '{name_var.get()}' added successfully", 'success')
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
        
        tk.Button(button_frame, text="Save Item", font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=save_item).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Cancel", font=('Segoe UI', 10),
                 bg=self.colors['danger'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def add_customer(self):
        """Add new customer"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Customer")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add New Customer", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(pady=20)
        
        # Form fields
        form_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        fields = [
            ("Name:", ""),
            ("Phone:", ""),
            ("Email:", "")
        ]
        
        entries = {}
        for label, default in fields:
            frame = tk.Frame(form_frame, bg=self.colors['bg_card'])
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=label, font=('Segoe UI', 10),
                    bg=self.colors['bg_card'], fg=self.colors['text_secondary'], width=10, anchor='w').pack(side=tk.LEFT)
            
            var = tk.StringVar(value=default)
            entry = tk.Entry(frame, textvariable=var, font=('Segoe UI', 10),
                           bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                           insertbackground=self.colors['text_primary'], relief=tk.FLAT)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            entries[label] = var
        
        def save_customer():
            new_customer = {
                'name': entries["Name:"].get(),
                'phone': entries["Phone:"].get(),
                'email': entries["Email:"].get(),
                'loyalty_points': 0,
                'visits': 0
            }
            
            self.data['customers'].append(new_customer)
            self.save_data()
            self.update_customer_display()
            dialog.destroy()
            self.show_notification(f"Customer {new_customer['name']} added successfully", 'success')
        
        tk.Button(dialog, text="Save Customer", font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=save_customer).pack(pady=20)
    
    def add_expense(self):
        """Add new expense"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Expense")
        dialog.geometry("400x250")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add Expense", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(pady=20)
        
        # Form fields
        form_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(form_frame, text="Description:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        
        desc_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=desc_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(form_frame, text="Amount:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        
        amount_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=amount_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        def add_expense():
            try:
                expense = {
                    'description': desc_var.get(),
                    'amount': float(amount_var.get()),
                    'date': self.current_date
                }
                self.data['expenses'].append(expense)
                self.save_data()
                dialog.destroy()
                self.show_notification("Expense added successfully", 'success')
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        
        tk.Button(dialog, text="Add Expense", font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=add_expense).pack(pady=20)
    
    def add_employee(self):
        """Add new employee (admin only)"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Employee")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add New Employee", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(pady=20)
        
        # Form fields
        form_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Name
        tk.Label(form_frame, text="Name:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        name_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=name_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        # Position
        tk.Label(form_frame, text="Position:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        position_var = tk.StringVar(value="Waiter")
        position_combo = ttk.Combobox(form_frame, textvariable=position_var,
                                     values=["Waiter", "Chef", "Manager", "Host", "Bartender", "Cleaner"],
                                     font=('Segoe UI', 10))
        position_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Email
        tk.Label(form_frame, text="Email:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        email_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=email_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        # Phone
        tk.Label(form_frame, text="Phone:", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        phone_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=phone_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        # Salary
        tk.Label(form_frame, text="Salary (PKR):", font=('Segoe UI', 10),
                bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(anchor='w', pady=(10, 5))
        salary_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=salary_var, font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'], relief=tk.FLAT).pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['bg_card'])
        button_frame.pack(pady=20)
        
        def save_employee():
            try:
                new_employee = {
                    'id': len(self.data['employees']) + 1,
                    'name': name_var.get(),
                    'position': position_var.get(),
                    'email': email_var.get(),
                    'phone': phone_var.get(),
                    'salary': float(salary_var.get()),
                    'status': 'active'
                }
                
                self.data['employees'].append(new_employee)
                self.save_data()
                self.update_employee_display()
                dialog.destroy()
                self.show_notification(f"Employee {new_employee['name']} added successfully", 'success')
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid salary")
        
        tk.Button(button_frame, text="Save Employee", font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=save_employee).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Cancel", font=('Segoe UI', 10),
                 bg=self.colors['danger'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def generate_sales_report(self):
        """Generate sales report"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Sales Report")
        dialog.geometry("600x500")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Sales Report", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(pady=20)
        
        # Report content
        report_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create text widget for report
        report_text = tk.Text(report_frame, font=('Courier', 10),
                             bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                             wrap=tk.WORD)
        report_text.pack(fill=tk.BOTH, expand=True)
        
        # Generate report content
        report_content = "SALES REPORT\n"
        report_content += "=" * 50 + "\n"
        report_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Calculate metrics
        total_revenue = sum(self.data['daily_sales'].values())
        total_orders = len(self.data['orders'])
        avg_order = total_revenue / total_orders if total_orders > 0 else 0
        
        report_content += f"Total Revenue: ${total_revenue:.2f}\n"
        report_content += f"Total Orders: {total_orders}\n"
        report_content += f"Average Order Value: ${avg_order:.2f}\n\n"
        
        # Today's sales
        today_sales = self.data['daily_sales'].get(self.current_date, 0)
        report_content += f"Today's Sales: ${today_sales:.2f}\n\n"
        
        # Top selling items
        item_sales = defaultdict(int)
        for order in self.data['orders']:
            for item in order['items']:
                item_sales[item['name']] += 1
        
        if item_sales:
            report_content += "TOP SELLING ITEMS:\n"
            for item, count in sorted(item_sales.items(), key=lambda x: x[1], reverse=True)[:10]:
                report_content += f"  {item}: {count} orders\n"
        
        # Insert report
        report_text.insert(tk.END, report_content)
        report_text.config(state=tk.DISABLED)
        
        # Export button
        tk.Button(dialog, text="Export Report", font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=lambda: self.export_report(report_content, "sales_report")).pack(pady=10)
    
    def generate_inventory_report(self):
        """Generate inventory report"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Inventory Report")
        dialog.geometry("600x500")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Inventory Report", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(pady=20)
        
        # Report content
        report_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create text widget for report
        report_text = tk.Text(report_frame, font=('Courier', 10),
                             bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                             wrap=tk.WORD)
        report_text.pack(fill=tk.BOTH, expand=True)
        
        # Generate report content
        report_content = "INVENTORY REPORT\n"
        report_content += "=" * 50 + "\n"
        report_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Total items
        total_items = len(self.data['inventory'])
        report_content += f"Total Items: {total_items}\n\n"
        
        # Low stock items
        low_stock = []
        for item_name, item_data in self.data['inventory'].items():
            if item_data['quantity'] <= item_data['min_stock']:
                low_stock.append(f"{item_name}: {item_data['quantity']} {item_data['unit']}")
        
        if low_stock:
            report_content += f"LOW STOCK ITEMS ({len(low_stock)}):\n"
            for item in low_stock:
                report_content += f"  {item}\n"
        else:
            report_content += "No items are low in stock\n"
        
        # Insert report
        report_text.insert(tk.END, report_content)
        report_text.config(state=tk.DISABLED)
        
        # Export button
        tk.Button(dialog, text="Export Report", font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=lambda: self.export_report(report_content, "inventory_report")).pack(pady=10)
    
    def generate_customer_report(self):
        """Generate customer report"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Customer Report")
        dialog.geometry("600x500")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Customer Report", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(pady=20)
        
        # Report content
        report_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create text widget for report
        report_text = tk.Text(report_frame, font=('Courier', 10),
                             bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                             wrap=tk.WORD)
        report_text.pack(fill=tk.BOTH, expand=True)
        
        # Generate report content
        report_content = "CUSTOMER REPORT\n"
        report_content += "=" * 50 + "\n"
        report_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Total customers
        report_content += f"Total Customers: {len(self.data['customers'])}\n\n"
        
        # Top customers by spending
        customer_spending = defaultdict(float)
        for customer in self.data['customers']:
            total_spent = sum(order['total'] for order in self.data['orders'] 
                            if order.get('customer') == customer['name'])
            customer_spending[customer['name']] = total_spent
        
        if customer_spending:
            report_content += "TOP CUSTOMERS BY SPENDING:\n"
            for name, amount in sorted(customer_spending.items(), key=lambda x: x[1], reverse=True)[:10]:
                report_content += f"  {name}: ${amount:.2f}\n"
        
        # Insert report
        report_text.insert(tk.END, report_content)
        report_text.config(state=tk.DISABLED)
        
        # Export button
        tk.Button(dialog, text="Export Report", font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=lambda: self.export_report(report_content, "customer_report")).pack(pady=10)
    
    def generate_financial_report(self):
        """Generate financial report"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Financial Report")
        dialog.geometry("600x500")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Financial Report", font=('Segoe UI', 16, 'bold'),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(pady=20)
        
        # Report content
        report_frame = tk.Frame(dialog, bg=self.colors['bg_card'])
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create text widget for report
        report_text = tk.Text(report_frame, font=('Courier', 10),
                             bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                             wrap=tk.WORD)
        report_text.pack(fill=tk.BOTH, expand=True)
        
        # Generate report content
        report_content = "FINANCIAL REPORT\n"
        report_content += "=" * 50 + "\n"
        report_content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Calculate metrics
        total_revenue = sum(self.data['daily_sales'].values())
        total_expenses = sum(e['amount'] for e in self.data['expenses'])
        net_profit = total_revenue - total_expenses
        tax_collected = total_revenue * self.data['tax_settings']['rate']
        
        report_content += f"Total Revenue: PKR{total_revenue:.2f}\n"
        report_content += f"Total Expenses: PKR{total_expenses:.2f}\n"
        report_content += f"Net Profit: PKR{net_profit:.2f}\n"
        report_content += f"Tax Collected: PKR{tax_collected:.2f}\n"
        
        # Insert report
        report_text.insert(tk.END, report_content)
        report_text.config(state=tk.DISABLED)
        
        # Export button
        tk.Button(dialog, text="Export Report", font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['success'], fg=self.colors['text_primary'],
                 relief=tk.FLAT, command=lambda: self.export_report(report_content, "financial_report")).pack(pady=10)
    
    def export_report(self, content, filename_prefix):
        """Export report to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(content)
                self.show_notification(f"Report exported to {filename}", 'success')
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {e}")
    
    def logout(self):
        """Logout user"""
        self.current_user = None
        self.show_login()
    
    def clear_content(self):
        """Clear content area"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = RestaurantSystemWithRoles(root)
    root.mainloop()

if __name__ == "__main__":
    main()