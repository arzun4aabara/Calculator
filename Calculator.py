import tkinter as tk
from tkinter import font
import math

class BeautifulCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("380x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#1C1C1E")
        
        # --- State Variables ---
        self.expression = ""
        self.current_input = "0"
        self.result_shown = False
        
        # --- Colors ---
        self.colors = {
            "bg":           "#1C1C1E",
            "display_bg":   "#1C1C1E",
            "display_fg":   "#FFFFFF",
            "sub_display":  "#8E8E93",
            "num_bg":       "#2C2C2E",
            "num_fg":       "#FFFFFF",
            "num_hover":    "#3A3A3C",
            "op_bg":        "#FF9F0A",
            "op_fg":        "#FFFFFF",
            "op_hover":     "#FFB340",
            "func_bg":      "#3A3A3C",
            "func_fg":      "#FFFFFF",
            "func_hover":   "#48484A",
            "equal_bg":     "#30D158",
            "equal_fg":     "#FFFFFF",
            "equal_hover":  "#4AE371",
            "clear_bg":     "#FF453A",
            "clear_fg":     "#FFFFFF",
            "clear_hover":  "#FF6961",
        }
        
        self._build_display()
        self._build_buttons()
        self._bind_keyboard()

    # ─────────────────────────── DISPLAY ───────────────────────────
    def _build_display(self):
        display_frame = tk.Frame(self.root, bg=self.colors["display_bg"], height=160)
        display_frame.pack(fill="x", padx=20, pady=(30, 10))
        display_frame.pack_propagate(False)

        self.sub_display = tk.Label(
            display_frame,
            text="",
            font=("SF Pro Display", 16),
            fg=self.colors["sub_display"],
            bg=self.colors["display_bg"],
            anchor="e"
        )
        self.sub_display.pack(fill="x", padx=10, pady=(15, 0))

        self.main_display = tk.Label(
            display_frame,
            text="0",
            font=("SF Pro Display", 48, "bold"),
            fg=self.colors["display_fg"],
            bg=self.colors["display_bg"],
            anchor="e"
        )
        self.main_display.pack(fill="x", padx=10, pady=(0, 10))

    # ─────────────────────────── BUTTONS ───────────────────────────
    def _build_buttons(self):
        btn_frame = tk.Frame(self.root, bg=self.colors["bg"])
        btn_frame.pack(fill="both", expand=True, padx=15, pady=(0, 20))

        # Button layout: (text, type)
        layout = [
            [("C", "clear"),  ("⌫", "func"),  ("%", "func"),  ("÷", "op")],
            [("7", "num"),    ("8", "num"),    ("9", "num"),   ("×", "op")],
            [("4", "num"),    ("5", "num"),    ("6", "num"),   ("−", "op")],
            [("1", "num"),    ("2", "num"),    ("3", "num"),   ("+", "op")],
            [("±", "func"),   ("0", "num"),    (".", "num"),   ("=", "equal")],
        ]

        for r, row in enumerate(layout):
            btn_frame.rowconfigure(r, weight=1)
            for c, (text, btn_type) in enumerate(row):
                btn_frame.columnconfigure(c, weight=1)

                bg, fg, hover = self._get_btn_colors(btn_type)

                btn = tk.Canvas(
                    btn_frame,
                    bg=self.colors["bg"],
                    highlightthickness=0,
                    cursor="hand2"
                )
                btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

                # Store info on canvas
                btn.btn_text = text
                btn.btn_type = btn_type
                btn.bg_color = bg
                btn.fg_color = fg
                btn.hover_color = hover
                btn.rect_id = None
                btn.text_id = None

                btn.bind("<Configure>", lambda e, b=btn: self._draw_round_btn(b))
                btn.bind("<Enter>", lambda e, b=btn: self._on_hover(b, True))
                btn.bind("<Leave>", lambda e, b=btn: self._on_hover(b, False))
                btn.bind("<Button-1>", lambda e, b=btn: self._on_click(b))

    def _get_btn_colors(self, btn_type):
        c = self.colors
        if btn_type == "num":
            return c["num_bg"], c["num_fg"], c["num_hover"]
        elif btn_type == "op":
            return c["op_bg"], c["op_fg"], c["op_hover"]
        elif btn_type == "func":
            return c["func_bg"], c["func_fg"], c["func_hover"]
        elif btn_type == "equal":
            return c["equal_bg"], c["equal_fg"], c["equal_hover"]
        elif btn_type == "clear":
            return c["clear_bg"], c["clear_fg"], c["clear_hover"]
        return c["num_bg"], c["num_fg"], c["num_hover"]

    def _draw_round_btn(self, btn):
        btn.delete("all")
        w = btn.winfo_width()
        h = btn.winfo_height()
        r = 18  # corner radius

        # Draw rounded rectangle
        btn.rect_id = self._round_rect(btn, 2, 2, w - 2, h - 2, r, fill=btn.bg_color, outline="")

        # Draw text
        font_size = 22 if btn.btn_type in ("op", "equal", "clear") else 20
        btn.text_id = btn.create_text(
            w / 2, h / 2,
            text=btn.btn_text,
            fill=btn.fg_color,
            font=("SF Pro Display", font_size, "bold")
        )

    def _round_rect(self, canvas, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1,
            x1 + r, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    # ─────────────────────── HOVER EFFECT ──────────────────────────
    def _on_hover(self, btn, entering):
        color = btn.hover_color if entering else btn.bg_color
        btn.delete("all")
        w = btn.winfo_width()
        h = btn.winfo_height()
        r = 18
        self._round_rect(btn, 2, 2, w - 2, h - 2, r, fill=color, outline="")
        font_size = 22 if btn.btn_type in ("op", "equal", "clear") else 20
        btn.create_text(
            w / 2, h / 2,
            text=btn.btn_text,
            fill=btn.fg_color,
            font=("SF Pro Display", font_size, "bold")
        )

    # ─────────────────────── CLICK LOGIC ───────────────────────────
    def _on_click(self, btn):
        text = btn.btn_text

        # Flash animation
        self._flash(btn)

        if text == "C":
            self._clear()
        elif text == "⌫":
            self._backspace()
        elif text == "±":
            self._negate()
        elif text == "%":
            self._percent()
        elif text == "=":
            self._evaluate()
        elif text in ("+", "−", "×", "÷"):
            self._add_operator(text)
        else:
            self._add_digit(text)

    def _flash(self, btn):
        """Quick brightness flash on click."""
        w = btn.winfo_width()
        h = btn.winfo_height()
        btn.delete("all")
        self._round_rect(btn, 2, 2, w - 2, h - 2, 18, fill="#FFFFFF", outline="")
        font_size = 22 if btn.btn_type in ("op", "equal", "clear") else 20
        btn.create_text(
            w / 2, h / 2,
            text=btn.btn_text,
            fill="#000000",
            font=("SF Pro Display", font_size, "bold")
        )
        btn.after(80, lambda: self._draw_round_btn(btn))

    # ─────────────────── CALCULATOR FUNCTIONS ──────────────────────
    def _clear(self):
        self.expression = ""
        self.current_input = "0"
        self.result_shown = False
        self._update_display()

    def _backspace(self):
        if self.result_shown:
            return
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
            if self.current_input == "-":
                self.current_input = "0"
        else:
            self.current_input = "0"
        self._update_display()

    def _negate(self):
        if self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self._update_display()

    def _percent(self):
        try:
            val = float(self.current_input) / 100
            self.current_input = self._format_number(val)
            self._update_display()
        except ValueError:
            pass

    def _add_digit(self, digit):
        if self.result_shown:
            self.current_input = "0"
            self.expression = ""
            self.result_shown = False

        if digit == ".":
            if "." in self.current_input:
                return
            self.current_input += "."
        else:
            if self.current_input == "0":
                self.current_input = digit
            else:
                if len(self.current_input.replace("-", "").replace(".", "")) < 12:
                    self.current_input += digit

        self._update_display()

    def _add_operator(self, op):
        self.result_shown = False
        op_map = {"÷": "/", "×": "*", "−": "-", "+": "+"}
        self.expression += self.current_input + " " + op_map[op] + " "
        self.current_input = "0"
        self._update_display()

    def _evaluate(self):
        try:
            full_expr = self.expression + self.current_input
            # Safety: only allow numbers and basic ops
            allowed = set("0123456789.+-*/ ()")
            if not all(ch in allowed for ch in full_expr.replace(" ", "")):
                raise ValueError("Invalid chars")

            result = eval(full_expr)

            display_expr = self.expression + self.current_input + " ="
            display_expr = display_expr.replace("*", "×").replace("/", "÷").replace("-", "−")

            self.expression = ""
            self.current_input = self._format_number(result)
            self.result_shown = True

            self.sub_display.config(text=display_expr)
            self.main_display.config(text=self.current_input)
            self._auto_resize()
        except ZeroDivisionError:
            self.sub_display.config(text="")
            self.main_display.config(text="Can't divide by 0")
            self.expression = ""
            self.current_input = "0"
            self.result_shown = True
        except Exception:
            self.sub_display.config(text="")
            self.main_display.config(text="Error")
            self.expression = ""
            self.current_input = "0"
            self.result_shown = True

    def _format_number(self, value):
        if isinstance(value, float):
            if value == int(value) and abs(value) < 1e15:
                return str(int(value))
            else:
                formatted = f"{value:.10g}"
                return formatted
        return str(value)

    # ──────────────────── DISPLAY UPDATE ───────────────────────────
    def _update_display(self):
        expr_display = self.expression.replace("*", "×").replace("/", "÷").replace("-", "−")
        self.sub_display.config(text=expr_display)
        self.main_display.config(text=self.current_input)
        self._auto_resize()

    def _auto_resize(self):
        text = self.current_input
        length = len(text)
        if length <= 9:
            size = 48
        elif length <= 12:
            size = 38
        elif length <= 16:
            size = 30
        else:
            size = 24
        self.main_display.config(font=("SF Pro Display", size, "bold"))

    # ──────────────────── KEYBOARD BINDINGS ────────────────────────
    def _bind_keyboard(self):
        self.root.bind("<Key>", self._key_press)

    def _key_press(self, event):
        key = event.char
        keysym = event.keysym

        if key in "0123456789":
            self._add_digit(key)
        elif key == ".":
            self._add_digit(".")
        elif key == "+":
            self._add_operator("+")
        elif key == "-":
            self._add_operator("−")
        elif key == "*":
            self._add_operator("×")
        elif key == "/":
            self._add_operator("÷")
        elif key == "%" :
            self._percent()
        elif keysym == "Return" or key == "=":
            self._evaluate()
        elif keysym == "BackSpace":
            self._backspace()
        elif keysym == "Escape" or key.lower() == "c":
            self._clear()


# ═══════════════════════════ RUN ═══════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()

    # Center window on screen
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w - 380) // 2
    y = (screen_h - 620) // 2
    root.geometry(f"380x620+{x}+{y}")

    app = BeautifulCalculator(root)
    root.mainloop()