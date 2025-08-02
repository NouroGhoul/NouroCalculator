import tkinter as tk
from tkinter import messagebox
from calculator import CalculatorEngine, CalculationError

class NouroCalculatorUI:
    def __init__(self, root: tk.Tk):
        self.THEMES = {
            'dark': {
                'root_bg': '#121212',
                'mainframe_bg': '#121212',
                'container_bg': '#1e1e1e',
                'container_border': '#333333',
                'display_bg': '#1e1e1e',
                'display_fg': 'white',
                'history_fg': '#aaaaaa',
                'button_bg': '#2d2d2d',
                'button_fg': 'white',
                'button_active': '#3c3c3c',
                'operator_bg': '#ff9500',
                'operator_fg': 'black',
                'operator_active': '#ffaa33',
                'special_bg': '#444444',
                'special_active': '#555555',
                'scientific_bg': '#333333',
                'scientific_active': '#444444',
            },
            'light': {
                'root_bg': '#f0f0f0',
                'mainframe_bg': '#f0f0f0',
                'container_bg': '#ffffff',
                'container_border': '#cccccc',
                'display_bg': '#ffffff',
                'display_fg': 'black',
                'history_fg': '#666666',
                'button_bg': '#e0e0e0',
                'button_fg': 'black',
                'button_active': '#d0d0d0',
                'operator_bg': '#ff9500',
                'operator_fg': 'black',
                'operator_active': '#ffaa33',
                'special_bg': '#c0c0c0',
                'special_active': '#b0b0b0',
                'scientific_bg': '#d0d0d0',
                'scientific_active': '#c0c0c0',
            }
        }
        self.root = root
        self.root.title("Nouro Calculator")
        self.root.geometry("400x500")
        self.root.minsize(300, 400)
        self.current_theme = 'dark'
        self.engine = CalculatorEngine()
        self.scientific_mode = False
        self.history_position = -1
        self._create_widgets()
        self._setup_keybindings()
        self._apply_theme()

    def _create_widgets(self):
        self.mainframe = tk.Frame(self.root, padx=10, pady=10)
        self.mainframe.grid(row=0, column=0, sticky="nsew")
        self.mainframe.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.calc_container = tk.Frame(
            self.mainframe, 
            bd=2, 
            relief="solid"
        )
        self.calc_container.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.calc_container.columnconfigure(0, weight=1)
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(
            self.calc_container,
            textvariable=self.display_var,
            anchor="e",
            font=("Helvetica", 24),
            padx=10,
            pady=10
        )
        self.display.grid(row=0, column=0, sticky="ew")
        self.history_var = tk.StringVar()
        self.history_label = tk.Label(
            self.calc_container,
            textvariable=self.history_var,
            anchor="e",
            font=("Helvetica", 10),
            padx=10
        )
        self.history_label.grid(row=1, column=0, sticky="ew")
        self.button_frame = tk.Frame(self.mainframe)
        self.button_frame.grid(row=1, column=0, sticky="nsew")
        for i in range(5):
            self.button_frame.columnconfigure(i, weight=1, uniform="btn")
        for i in range(7):
            self.button_frame.rowconfigure(i, weight=1, uniform="btn")
        self._create_buttons()
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Scientific Mode", command=self.toggle_scientific_mode, accelerator="Ctrl+M")
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme, accelerator="Ctrl+T")
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        history_menu = tk.Menu(self.menu_bar, tearoff=0)
        history_menu.add_command(label="Show History", command=self.show_history)
        self.menu_bar.add_cascade(label="History", menu=history_menu)
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def _create_buttons(self):
        classic_buttons = [
            ('C', 0, 0, 1, self.clear), 
            ('⌫', 0, 1, 1, self.delete),
            ('(', 0, 2, 1, lambda: self.add_to_expression('(')),
            (')', 0, 3, 1, lambda: self.add_to_expression(')')),
            ('÷', 0, 4, 1, lambda: self.add_to_expression('÷')),
            ('7', 1, 0, 1, lambda: self.add_to_expression('7')),
            ('8', 1, 1, 1, lambda: self.add_to_expression('8')),
            ('9', 1, 2, 1, lambda: self.add_to_expression('9')),
            ('×', 1, 3, 1, lambda: self.add_to_expression('×')),
            ('^', 1, 4, 1, lambda: self.add_to_expression('^')),
            ('4', 2, 0, 1, lambda: self.add_to_expression('4')),
            ('5', 2, 1, 1, lambda: self.add_to_expression('5')),
            ('6', 2, 2, 1, lambda: self.add_to_expression('6')),
            ('-', 2, 3, 1, lambda: self.add_to_expression('-')),
            ('√', 2, 4, 1, lambda: self.add_function('sqrt(')),
            ('1', 3, 0, 1, lambda: self.add_to_expression('1')),
            ('2', 3, 1, 1, lambda: self.add_to_expression('2')),
            ('3', 3, 2, 1, lambda: self.add_to_expression('3')),
            ('+', 3, 3, 1, lambda: self.add_to_expression('+')),
            ('!', 3, 4, 1, lambda: self.add_to_expression('!')),
            ('0', 4, 0, 1, lambda: self.add_to_expression('0')),
            ('.', 4, 1, 1, lambda: self.add_to_expression('.')),
            ('π', 4, 2, 1, lambda: self.add_to_expression('π')),
            ('=', 4, 3, 2, self.calculate),
        ]
        scientific_buttons = [
            ('sin', 5, 0, 1, lambda: self.add_function('sin(')),
            ('cos', 5, 1, 1, lambda: self.add_function('cos(')),
            ('tan', 5, 2, 1, lambda: self.add_function('tan(')),
            ('ln', 5, 3, 1, lambda: self.add_function('ln(')),
            ('log', 5, 4, 1, lambda: self.add_function('log(')),
            ('asin', 6, 0, 1, lambda: self.add_function('asin(')),
            ('acos', 6, 1, 1, lambda: self.add_function('acos(')),
            ('atan', 6, 2, 1, lambda: self.add_function('atan(')),
            ('e', 6, 3, 1, lambda: self.add_to_expression('e')),
            ('exp', 6, 4, 1, lambda: self.add_function('exp(')),
        ]
        self.buttons = {}
        for (text, row, col, colspan, command) in classic_buttons:
            btn = self._create_button(text, row, col, colspan, command)
            self.buttons[text] = btn
        self.scientific_buttons = []
        for (text, row, col, colspan, command) in scientific_buttons:
            btn = self._create_button(text, row, col, colspan, command)
            self.scientific_buttons.append(btn)
            self.buttons[text] = btn
            btn.grid_remove()

    def _create_button(self, text, row, col, colspan, command):
        btn = tk.Button(
            self.button_frame,
            text=text,
            command=command,
            font=("Helvetica", 16),
            relief="flat",
            borderwidth=0
        )
        btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)
        btn.bind("<Enter>", lambda e, b=btn: self._on_button_hover(b, True))
        btn.bind("<Leave>", lambda e, b=btn: self._on_button_hover(b, False))
        return btn

    def _on_button_hover(self, button, hover):
        theme = self.THEMES[self.current_theme]
        text = button['text']
        if text in ['÷', '×', '-', '+', '^', '=']:
            button.config(bg=theme['operator_active'] if hover else theme['operator_bg'])
        elif text in ['C', '⌫']:
            button.config(bg=theme['special_active'] if hover else theme['special_bg'])
        elif text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'ln', 'log', 'exp', '√', '!']:
            button.config(bg=theme['scientific_active'] if hover else theme['scientific_bg'])
        else:
            button.config(bg=theme['button_active'] if hover else theme['button_bg'])

    def _apply_theme(self):
        theme = self.THEMES[self.current_theme]
        self.root.config(bg=theme['root_bg'])
        self.mainframe.config(bg=theme['mainframe_bg'])
        self.calc_container.config(
            bg=theme['container_bg'], 
            highlightbackground=theme['container_border'],
            highlightcolor=theme['container_border']
        )
        self.button_frame.config(bg=theme['mainframe_bg'])
        self.display.config(
            bg=theme['display_bg'],
            fg=theme['display_fg']
        )
        self.history_label.config(
            bg=theme['display_bg'],
            fg=theme['history_fg']
        )
        for text, button in self.buttons.items():
            if text in ['÷', '×', '-', '+', '^', '=']:
                button.config(
                    bg=theme['operator_bg'],
                    fg=theme['operator_fg'],
                    activebackground=theme['operator_active']
                )
            elif text in ['C', '⌫']:
                button.config(
                    bg=theme['special_bg'],
                    activebackground=theme['special_active']
                )
            elif text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'ln', 'log', 'exp', '√', '!']:
                button.config(
                    bg=theme['scientific_bg'],
                    activebackground=theme['scientific_active']
                )
            else:
                button.config(
                    bg=theme['button_bg'],
                    fg=theme['button_fg'],
                    activebackground=theme['button_active']
                )

    def _setup_keybindings(self):
        for digit in "0123456789":
            self.root.bind(digit, lambda e, d=digit: self.add_to_expression(d))
        operators = {
            '+': '+', '-': '-', '*': '×', '/': '÷', '^': '^', '!': '!',
            '(': '(', ')': ')', '.': '.'
        }
        for key, value in operators.items():
            self.root.bind(key, lambda e, v=value: self.add_to_expression(v))
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<Escape>', lambda e: self.clear())
        self.root.bind('<BackSpace>', lambda e: self.delete())
        self.root.bind('<Up>', lambda e: self.navigate_history(-1))
        self.root.bind('<Down>', lambda e: self.navigate_history(1))
        self.root.bind('<Control-m>', lambda e: self.toggle_scientific_mode())
        self.root.bind('<Control-t>', lambda e: self.toggle_theme())

    def add_to_expression(self, value: str):
        expr = self.engine.current_expression
        if value in ['π', 'e'] and expr and expr[-1].isdigit():
            expr += '*'
        expr += value
        self.engine.current_expression = expr
        self._update_display()

    def add_function(self, func: str):
        expr = self.engine.current_expression
        if expr and expr[-1].isdigit():
            expr += '*'
        self.engine.current_expression = expr + func
        self._update_display()

    def clear(self):
        self.engine.clear()
        self.history_position = -1
        self._update_display()

    def delete(self):
        self.engine.delete_last()
        self.history_position = -1
        self._update_display()

    def calculate(self):
        try:
            result = self.engine.evaluate()
            self.display_var.set(str(result))
            self.history_var.set(self.engine.current_expression)
            self.engine.clear()
            self.history_position = -1
        except CalculationError as e:
            messagebox.showerror("Calculation Error", str(e))
            self.clear()

    def navigate_history(self, direction: int):
        history = self.engine.get_history()
        if not history:
            return
        self.history_position = max(-1, min(self.history_position + direction, len(history)-1))
        if self.history_position == -1:
            self.engine.current_expression = ""
            self._update_display()
        else:
            expr, result = history[self.history_position]
            self.engine.current_expression = expr
            self.display_var.set(str(result))
            self.history_var.set(expr)

    def _update_display(self):
        expr = self.engine.current_expression
        self.display_var.set(expr if expr else "0")
        self.history_var.set("")

    def toggle_scientific_mode(self):
        self.scientific_mode = not self.scientific_mode
        for btn in self.scientific_buttons:
            if self.scientific_mode:
                btn.grid()
            else:
                btn.grid_remove()
        height = 600 if self.scientific_mode else 500
        self.root.geometry(f"400x{height}")

    def toggle_theme(self):
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self._apply_theme()

    def show_history(self):
        history = self.engine.get_history()
        if not history:
            messagebox.showinfo("History", "No calculations in history")
            return
        history_text = "\n".join([f"{expr} = {result}" for expr, result in history])
        messagebox.showinfo("Calculation History", history_text)

    def show_shortcuts(self):
        shortcuts = [
            "Digits: 0-9",
            "Operators: + - * / ^ !",
            "Enter: Calculate",
            "Escape: Clear",
            "Backspace: Delete last character",
            "Up/Down: Navigate history",
            "Ctrl+M: Toggle scientific mode",
            "Ctrl+T: Toggle theme",
            "(: Open parenthesis",
            "): Close parenthesis"
        ]
        messagebox.showinfo("Keyboard Shortcuts", "\n".join(shortcuts))

    def show_about(self):
        messagebox.showinfo(
            "About Nouro Calculator",
            "Nouro Calculator - Scientific Calculator\n\n"
            "Version 1.0\n\n"
            "Created by Nouro\n"
            "GitHub: https://github.com/NouroGhoul/NouroGhoul\n\n"
            "Contact me for any questions or feedback!"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = NouroCalculatorUI(root)
    root.mainloop()