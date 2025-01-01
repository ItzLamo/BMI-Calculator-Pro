import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dataclasses import dataclass

# ---- Models ----
@dataclass
class BMIRecord:
    weight: float
    height: float
    bmi: float
    category: str
    date: str = None
    
    def __post_init__(self):
        if self.date is None:
            self.date = datetime.now().strftime('%Y-%m-%d %H:%M')
            
    def to_dict(self):
        return {
            'date': self.date,
            'weight': round(self.weight, 1),
            'height': round(self.height, 1),
            'bmi': round(self.bmi, 1),
            'category': self.category
        }

# ---- Utils ----
class BMICalculator:
    @staticmethod
    def calculate(weight: float, height: float, weight_unit: str = 'kg', height_unit: str = 'cm') -> float:
        # Convert to metric if necessary
        if weight_unit == 'lbs':
            weight = weight * 0.453592
        if height_unit == 'inches':
            height = height * 2.54
            
        # Calculate BMI
        height_m = height / 100
        return weight / (height_m * height_m)
    
    @staticmethod
    def get_category(bmi: float) -> tuple[str, list[str], str]:
        if bmi < 16:
            return ("Severe Underweight", [
                "Urgent medical attention required",
                "Consult with healthcare provider immediately",
                "Work with a registered dietitian",
                "Regular health monitoring needed"
            ], "#ff0000")
        elif bmi < 18.5:
            return ("Underweight", [
                "Increase caloric intake with nutrient-rich foods",
                "Consider consulting a nutritionist",
                "Add strength training exercises",
                "Monitor your progress regularly",
                "Focus on protein-rich foods"
            ], "#ff9900")
        elif bmi < 25:
            return ("Normal Weight", [
                "Maintain a balanced diet",
                "Regular exercise (150 minutes/week)",
                "Stay hydrated",
                "Get adequate sleep (7-9 hours)",
                "Regular health check-ups"
            ], "#00cc00")
        elif bmi < 30:
            return ("Overweight", [
                "Monitor portion sizes",
                "Increase physical activity",
                "Reduce processed food intake",
                "Consider keeping a food diary",
                "Aim for gradual weight loss"
            ], "#ff9900")
        elif bmi < 35:
            return ("Obese Class I", [
                "Consult a healthcare provider",
                "Create a sustainable exercise routine",
                "Focus on whole foods",
                "Set realistic weight loss goals",
                "Consider working with a fitness trainer"
            ], "#ff3300")
        else:
            return ("Obese Class II", [
                "Immediate medical consultation required",
                "Supervised weight loss program recommended",
                "Regular health monitoring",
                "Consider professional support",
                "Focus on sustainable lifestyle changes"
            ], "#ff0000")

class DataManager:
    def __init__(self, filename: str = "bmi_history.json"):
        self.filename = filename
        self.history = self.load_history()
        
    def load_history(self) -> list:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_record(self, record: BMIRecord):
        self.history.append(record.to_dict())
        with open(self.filename, 'w') as f:
            json.dump(self.history, f)
    
    def clear_history(self):
        self.history = []
        if os.path.exists(self.filename):
            os.remove(self.filename)

# ---- GUI Components ----
class StatsWindow:
    def __init__(self, parent, history):
        self.window = tk.Toplevel(parent)
        self.window.title("BMI Statistics")
        self.window.geometry("600x400")
        self.history = history
        
        self.create_widgets()
        
    def create_widgets(self):
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text='Summary')
        self.create_summary_tab(summary_frame)
        
        graph_frame = ttk.Frame(notebook)
        notebook.add(graph_frame, text='Trends')
        self.create_graph_tab(graph_frame)
        
    def create_summary_tab(self, parent):
        if not self.history:
            ttk.Label(parent, text="No data available").pack(pady=20)
            return
            
        bmis = [record['bmi'] for record in self.history]
        
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding=10)
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        stats = [
            ("Average BMI:", f"{sum(bmis) / len(bmis):.1f}"),
            ("Lowest BMI:", f"{min(bmis):.1f}"),
            ("Highest BMI:", f"{max(bmis):.1f}"),
            ("Total Records:", str(len(bmis)))
        ]
        
        for i, (label, value) in enumerate(stats):
            ttk.Label(stats_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky='w')
            ttk.Label(stats_frame, text=value).grid(row=i, column=1, padx=5, pady=2, sticky='w')
            
    def create_graph_tab(self, parent):
        if not self.history:
            ttk.Label(parent, text="No data available").pack(pady=20)
            return
            
        fig, ax = plt.subplots(figsize=(6, 4))
        
        dates = [datetime.strptime(record['date'], '%Y-%m-%d %H:%M') for record in self.history]
        bmis = [record['bmi'] for record in self.history]
        
        ax.plot(dates, bmis, marker='o')
        ax.set_title('BMI Trend Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('BMI')
        fig.autofmt_xdate()
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator Pro")
        self.root.geometry("650x600")
        self.root.configure(bg="#f0f2f5")
        
        self.data_manager = DataManager()
        
        self.create_widgets()
        self.create_menu()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear History", command=self.clear_history)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="History", command=self.show_history)
        view_menu.add_command(label="Statistics", command=self.show_statistics)
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 24, "bold"))
        style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))
        style.configure("Result.TLabel", font=("Helvetica", 16))
        
        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Label(title_frame, text="BMI Calculator Pro", style="Title.TLabel").pack()
        ttk.Label(title_frame, text="by Hassan Ahmed for The Hack Club", font=("Helvetica", 10)).pack()
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Personal Information", padding="10")
        input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Weight input
        ttk.Label(input_frame, text="Weight:").grid(row=0, column=0, padx=5, pady=5)
        self.weight_var = tk.StringVar()
        self.weight_entry = ttk.Entry(input_frame, textvariable=self.weight_var)
        self.weight_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.weight_unit = tk.StringVar(value="kg")
        ttk.Radiobutton(input_frame, text="kg", variable=self.weight_unit, value="kg").grid(row=0, column=2)
        ttk.Radiobutton(input_frame, text="lbs", variable=self.weight_unit, value="lbs").grid(row=0, column=3)
        
        # Height input
        ttk.Label(input_frame, text="Height:").grid(row=1, column=0, padx=5, pady=5)
        self.height_var = tk.StringVar()
        self.height_entry = ttk.Entry(input_frame, textvariable=self.height_var)
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.height_unit = tk.StringVar(value="cm")
        ttk.Radiobutton(input_frame, text="cm", variable=self.height_unit, value="cm").grid(row=1, column=2)
        ttk.Radiobutton(input_frame, text="inches", variable=self.height_unit, value="inches").grid(row=1, column=3)
        
        # Calculate button
        calculate_btn = ttk.Button(input_frame, text="Calculate BMI", command=self.calculate_bmi)
        calculate_btn.grid(row=2, column=0, columnspan=4, pady=20)
        
        # Results frame
        self.result_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        self.result_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.bmi_label = ttk.Label(self.result_frame, text="", style="Result.TLabel")
        self.bmi_label.grid(row=0, column=0, pady=10)
        
        self.category_label = ttk.Label(self.result_frame, text="", style="Result.TLabel")
        self.category_label.grid(row=1, column=0, pady=10)
        
        # Progress bar
        self.progress_frame = ttk.Frame(self.result_frame)
        self.progress_frame.grid(row=2, column=0, pady=10)
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=200, mode='determinate')
        self.progress_bar.grid(row=0, column=0, pady=5)
        
        # Recommendations frame
        self.recommendations_frame = ttk.LabelFrame(main_frame, text="Health Recommendations", padding="10")
        self.recommendations_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
    def calculate_bmi(self):
        try:
            weight = float(self.weight_var.get())
            height = float(self.height_var.get())
            
            bmi = BMICalculator.calculate(
                weight, height,
                self.weight_unit.get(),
                self.height_unit.get()
            )
            
            category, recommendations, color = BMICalculator.get_category(bmi)
            
            record = BMIRecord(weight, height, bmi, category)
            self.data_manager.save_record(record)
            
            self.bmi_label.configure(text=f"BMI: {bmi:.1f}")
            self.category_label.configure(text=f"Category: {category}")
            
            progress = min(100, (bmi / 50) * 100)
            self.progress_bar['value'] = progress
            
            for widget in self.recommendations_frame.winfo_children():
                widget.destroy()
                
            for i, rec in enumerate(recommendations):
                ttk.Label(
                    self.recommendations_frame,
                    text=f"• {rec}",
                    foreground=color
                ).grid(row=i, column=0, sticky="w", pady=2)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for weight and height")
            
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("BMI History")
        history_window.geometry("600x400")
        
        columns = ('Date', 'Weight', 'Height', 'BMI', 'Category')
        tree = ttk.Treeview(history_window, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
            
        for entry in self.data_manager.history:
            tree.insert('', 'end', values=(
                entry['date'],
                f"{entry['weight']} kg",
                f"{entry['height']} cm",
                entry['bmi'],
                entry['category']
            ))
            
        tree.pack(padx=10, pady=10, fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(history_window, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
    def show_statistics(self):
        StatsWindow(self.root, self.data_manager.history)
        
    def clear_history(self):
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all history?"):
            self.data_manager.clear_history()
            messagebox.showinfo("Success", "History cleared successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()