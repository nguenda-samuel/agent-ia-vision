import io
import math
import os
import random
import re
import sys
import threading
import time
import tkinter as tk

import customtkinter as ctk
from google import genai
from gtts import gTTS
import mss
from PIL import Image, ImageChops, ImageStat, ImageTk
import pygame
from pynput import keyboard, mouse
import speech_recognition as sr

from ai_engine import AIEngine

# Configuration de l'esthétique globale
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BG_COLOR = "#1e1e2e"
FRAME_BG = "#2a2b3d"
USER_BUBBLE = "#6c5ce7"
AI_BUBBLE = "#34495e"
ACCENT_COLOR = "#00cec9"
TEXT_COLOR = "#c8d3f5"


# ==================== POINTEUR VISUEL AVEC MAIN VECTORIELLE (SANS PNG) ====================


class AnimatedPointerWindow(tk.Toplevel):

    def __init__(self, root, on_valid_click_callback):
        super().__init__(root)
        self.root = root
        self.on_valid_click_callback = on_valid_click_callback

        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.trans_color = "#000001"
        self.config(bg=self.trans_color)
        try:
            self.wm_attributes("-transparentcolor", self.trans_color)
        except Exception:
            pass

        self.size = 120
        self.geometry(f"{self.size}x{self.size}+-300+-300")

        self.canvas = tk.Canvas(
            self,
            width=self.size,
            height=self.size,
            bg=self.trans_color,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.ripple_phase = 0.0
        self.current_x, self.current_y = -300, -300
        self.exact_target_x, self.exact_target_y = 0, 0
        self.tolerance_radius = 75

        self.virtual_mouse = mouse.Controller()
        self.active_listener = False
        self.mouse_listener = mouse.Listener(on_click=self.on_global_click)
        self.mouse_listener.start()

        self.animate_ripples()

    def draw_vector_hand(self, cx, cy):
        """Dessine un avatar de main/index en vectoriel pur (sans aucun bord d'image)."""
        hand_color = "#ffffff"
        border_color = "#00cec9"

        # 1. Poing / Paume
        self.canvas.create_oval(
            cx - 11,
            cy - 2,
            cx + 11,
            cy + 18,
            fill=hand_color,
            outline=border_color,
            width=2,
        )

        # 2. Index qui pointe vers le haut
        self.canvas.create_polygon(
            cx - 5,
            cy - 22,
            cx + 5,
            cy - 22,
            cx + 6,
            cy + 2,
            cx - 6,
            cy + 2,
            fill=hand_color,
            outline=border_color,
            width=2,
        )

        # 3. Pouce sur le côté
        self.canvas.create_polygon(
            cx - 10,
            cy + 2,
            cx - 16,
            cy - 4,
            cx - 12,
            cy - 8,
            cx - 6,
            cy + 2,
            fill=hand_color,
            outline=border_color,
            width=2,
        )

        # 4. Point d'impact lumineux au bout du doigt
        self.canvas.create_oval(
            cx - 3, cy - 25, cx + 3, cy - 19, fill="#ff7675", outline=""
        )

    def animate_ripples(self):
        self.canvas.delete("all")
        cx, cy = self.size // 2, self.size // 2

        # Vagues d'ondes
        self.ripple_phase = (self.ripple_phase + 0.06) % 1.0
        for i in range(2):
            phase = (self.ripple_phase + i * 0.5) % 1.0
            r = 18 + phase * 36
            width = max(1, int(3.5 - phase * 2.5))
            color = "#00cec9" if phase < 0.65 else "#007a78"

            self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r, outline=color, width=width
            )

        # Dessin de la main vectorielle
        self.draw_vector_hand(cx, cy)

        self.after(30, self.animate_ripples)

    def on_global_click(self, x, y, button, pressed):
        if pressed and self.active_listener and button == mouse.Button.left:
            pointer_center_x = self.current_x + (self.size / 2)
            pointer_center_y = self.current_y + (self.size / 2)

            dist_target = math.hypot(
                x - self.exact_target_x, y - self.exact_target_y
            )
            dist_pointer = math.hypot(
                x - pointer_center_x, y - pointer_center_y
            )

            if (
                dist_target <= self.tolerance_radius
                or dist_pointer <= self.tolerance_radius
            ):
                self.active_listener = False
                clicked_on_finger = (dist_pointer < dist_target) and (
                    dist_target > 25
                )

                if clicked_on_finger:

                    def _auto_click():
                        time.sleep(0.05)
                        self.virtual_mouse.position = (
                            int(self.exact_target_x),
                            int(self.exact_target_y),
                        )
                        time.sleep(0.05)
                        self.virtual_mouse.click(mouse.Button.left)

                    threading.Thread(target=_auto_click, daemon=True).start()
                    self.root.after(200, self.on_valid_click_callback)
                else:
                    self.hide()
                    self.root.after(150, self.on_valid_click_callback)

    def animate_to(self, target_x, target_y):
        self.exact_target_x, self.exact_target_y = target_x, target_y
        dest_x, dest_y = int(target_x - (self.size / 2)), int(
            target_y - (self.size / 2)
        )

        if self.current_x < 0:
            self.current_x, self.current_y = dest_x, dest_y - 150

        steps = 12
        dx = (dest_x - self.current_x) / steps
        dy = (dest_y - self.current_y) / steps

        def step(i):
            if i < steps:
                self.current_x += dx
                self.current_y += dy
                self.geometry(f"+{int(self.current_x)}+{int(self.current_y)}")
                self.root.after(12, lambda: step(i + 1))
            else:
                self.current_x, self.current_y = dest_x, dest_y
                self.geometry(f"+{dest_x}+{dest_y}")
                self.active_listener = True

        step(0)

    def hide(self):
        self.active_listener = False
        self.current_x, self.current_y = -300, -300
        self.geometry("+-300+-300")


# ==================== MINI-FENÊTRE DE SAISIE RAPIDE ====================


class QuickInputWindow(ctk.CTkToplevel):

    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.title("✍️ Saisie Rapide")
        self.geometry("480x130")
        self.wm_attributes("-topmost", True)
        self.resizable(False, False)
        self.configure(fg_color=BG_COLOR)

        self.protocol("WM_DELETE_WINDOW", self.withdraw)

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - 480) // 2
        y = (screen_h - 130) // 2
        self.geometry(f"480x130+{x}+{y}")

        self.frame = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color=FRAME_BG,
            border_width=1,
            border_color=USER_BUBBLE,
        )
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.lbl_title = ctk.CTkLabel(
            self.frame,
            text="Tapez votre instruction pour l'agent :",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR,
        )
        self.lbl_title.pack(anchor="w", padx=12, pady=(10, 5))

        self.input_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=10, pady=5)

        self.entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Ex: Clique sur le bouton Valider...",
            height=42,
            font=ctk.CTkFont(size=13),
            corner_radius=8,
            border_color=USER_BUBBLE,
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.entry.bind(
            "<Return>", lambda event: self.send_prompt(use_vision=True)
        )
        self.entry.bind("<Escape>", lambda event: self.withdraw())

        self.btn_vision = ctk.CTkButton(
            self.input_frame,
            text="📸 Écran",
            width=85,
            height=42,
            fg_color=USER_BUBBLE,
            hover_color="#5f27cd",
            font=ctk.CTkFont(weight="bold"),
            command=lambda: self.send_prompt(use_vision=True),
        )
        self.btn_vision.pack(side="right", padx=(0, 6))

        self.btn_send = ctk.CTkButton(
            self.input_frame,
            text="🚀",
            width=45,
            height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=lambda: self.send_prompt(use_vision=True),
        )
        self.btn_send.pack(side="right")

        self.withdraw()

    def show_and_focus(self):
        self.deiconify()
        self.lift()
        self.focus_force()
        self.entry.focus_set()

    def send_prompt(self, use_vision=True):
        text = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        self.withdraw()
        if text:
            self.app.append_to_chat(text, is_user=True)
            self.app.process_custom_prompt(text, use_vision=use_vision)


# ==================== SOUS-TITRES ET VISUALISEUR AUDIO ====================


class SubtitleWindow(tk.Toplevel):

    def __init__(self, root):
        super().__init__(root)
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.config(bg="#000001")
        try:
            self.wm_attributes("-transparentcolor", "#000001")
        except Exception:
            pass
        self.geometry("-2000-2000")

        self.frame = tk.Frame(
            self,
            bg=FRAME_BG,
            bd=0,
            highlightbackground=ACCENT_COLOR,
            highlightthickness=1,
        )
        self.frame.pack(padx=10, pady=10)

        self.bar_canvas = tk.Canvas(
            self.frame, width=30, height=30, bg=FRAME_BG, highlightthickness=0
        )
        self.bar_canvas.pack(side="left", padx=(10, 0), pady=5)

        self.label = tk.Label(
            self.frame,
            text="",
            fg="white",
            bg=FRAME_BG,
            font=("Segoe UI", 12, "bold"),
            wraplength=350,
            justify="left",
        )
        self.label.pack(side="left", padx=10, pady=5)

        self.hide_timer = None
        self.is_speaking = False
        self.animate_bars()

    def show(self, text, x, y):
        self.attributes("-alpha", 0.0)
        self.label.config(text=text)
        self.update_idletasks()
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        self.geometry(f"{w}x{h}+{int(x)}+{int(y)}")

        self.is_speaking = True
        self.fade_in()

        if self.hide_timer:
            self.after_cancel(self.hide_timer)
        self.hide_timer = self.after(6000, self.hide)

    def fade_in(self, alpha=0.0):
        if alpha < 1.0:
            alpha += 0.15
            self.attributes("-alpha", alpha)
            self.after(20, lambda: self.fade_in(alpha))

    def hide(self):
        self.is_speaking = False
        self.geometry("-2000-2000")

    def animate_bars(self):
        self.bar_canvas.delete("bar")
        if self.is_speaking:
            for i in range(4):
                h = random.randint(5, 20)
                x = i * 6 + 4
                self.bar_canvas.create_rectangle(
                    x, 25 - h, x + 4, 25, fill=ACCENT_COLOR, tags="bar"
                )
        else:
            for i in range(4):
                x = i * 6 + 4
                self.bar_canvas.create_rectangle(
                    x, 23, x + 4, 25, fill="#7f8fa6", tags="bar"
                )
        self.after(100, self.animate_bars)


# ==================== AVATAR (LÉVITATION & HALO NÉON) ====================


class AvatarWindow(tk.Toplevel):

    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.trans_color = "#000001"
        self.config(bg=self.trans_color)
        try:
            self.wm_attributes("-transparentcolor", self.trans_color)
        except Exception:
            pass

        self.size = 110
        self.geometry(f"{self.size}x{self.size}+100+100")

        self.canvas = tk.Canvas(
            self,
            width=self.size,
            height=self.size,
            bg=self.trans_color,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.state = "idle"
        self.angle = 0

        try:
            pil_img = Image.open("avatar.png").convert("RGBA")
            pil_img = pil_img.resize((65, 65), Image.Resampling.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(pil_img)
            self.img_id = self.canvas.create_image(
                self.size // 2, self.size // 2, image=self.tk_img
            )
        except Exception:
            self.img_id = self.canvas.create_oval(
                25,
                25,
                self.size - 25,
                self.size - 25,
                fill="#2c3e50",
                outline="",
            )
            self.canvas.create_text(
                self.size // 2, self.size // 2, text="🤖", font=("Arial", 30)
            )

        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind(
            "<Double-Button-1>",
            lambda e: self.app.quick_input.show_and_focus(),
        )

        self.canvas.bind("<Button-3>", self.show_context_menu)
        self.menu = tk.Menu(
            self, tearoff=0, bg=FRAME_BG, fg="white", font=("Segoe UI", 11)
        )
        self.menu.add_command(
            label="✍️ Saisie Rapide (Prompt)",
            command=lambda: self.app.quick_input.show_and_focus(),
        )
        self.menu.add_command(
            label="💬 Ouvrir Chat Complet", command=self.app.toggle_main_window
        )
        self.menu.add_command(
            label="📸 Analyser l'écran (F9)",
            command=lambda: self.app.process_request(use_vision=True),
        )
        self.menu.add_command(
            label="🎙️ Commande Vocale", command=self.app.listen_microphone
        )
        self.menu.add_separator()
        self.menu.add_command(
            label="🛑 Stopper l'Agent", command=self.app.stop_agent_workflow
        )
        self.menu.add_command(label="❌ Quitter", command=self.app.on_closing)

        self.animate_ring_and_levitate()

    def start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def do_drag(self, event):
        x = self.winfo_pointerx() - self.drag_x
        y = self.winfo_pointery() - self.drag_y
        self.geometry(f"+{x}+{y}")

    def show_context_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def set_state(self, new_state):
        self.state = new_state
        self.canvas.delete("ring")

    def animate_ring_and_levitate(self):
        self.canvas.delete("ring")
        offset_y = math.sin(time.time() * 2.5) * 6
        if self.canvas.type(self.img_id) == "image":
            self.canvas.coords(
                self.img_id, self.size // 2, (self.size // 2) + offset_y
            )
        else:
            self.canvas.coords(
                self.img_id,
                25,
                25 + offset_y,
                self.size - 25,
                self.size - 25 + offset_y,
            )

        cx, cy, r = self.size // 2, (self.size // 2) + offset_y, 35

        if self.state == "idle":
            width = 2 + math.sin(time.time() * 3) * 1.5
            self.canvas.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                outline="#3498db",
                width=width,
                tags="ring",
            )

        elif self.state == "scan":
            self.angle = (self.angle + 12) % 360
            self.canvas.create_arc(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                start=self.angle,
                extent=100,
                outline="#a29bfe",
                width=5,
                style=tk.ARC,
                tags="ring",
            )
            self.canvas.create_arc(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                start=self.angle + 180,
                extent=100,
                outline="#e056fd",
                width=5,
                style=tk.ARC,
                tags="ring",
            )

        elif self.state == "speak":
            scale = abs(math.sin(time.time() * 8)) * 6
            self.canvas.create_oval(
                cx - r - scale,
                cy - r - scale,
                cx + r + scale,
                cy + r + scale,
                outline="#55efc4",
                width=2,
                tags="ring",
            )
            self.canvas.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                outline="#00cec9",
                width=4,
                tags="ring",
            )

        self.after(30, self.animate_ring_and_levitate)

    def dodge_if_needed(self, target_x, target_y):
        curr_x = self.winfo_rootx()
        curr_y = self.winfo_rooty()
        center_x = curr_x + self.size / 2
        center_y = curr_y + self.size / 2

        dist = math.hypot(center_x - target_x, center_y - target_y)
        if dist < 180:
            safe_y = curr_y - 200 if curr_y > 250 else curr_y + 200
            safe_x = curr_x + 200 if curr_x < 500 else curr_x - 200
            self.smooth_move(safe_x, safe_y)

    def smooth_move(self, dest_x, dest_y, step=0):
        if step < 20:
            curr_x, curr_y = self.winfo_rootx(), self.winfo_rooty()
            nx = curr_x + (dest_x - curr_x) * 0.2
            ny = curr_y + (dest_y - curr_y) * 0.2
            self.geometry(f"+{int(nx)}+{int(ny)}")
            self.after(16, lambda: self.smooth_move(dest_x, dest_y, step + 1))


# ==================== APPLICATION PRINCIPALE ====================


class VisionAssistantApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("IA Vision Pro Agent")
        self.geometry("520x620+60+40")
        self.wm_attributes("-topmost", True)
        self.configure(fg_color=BG_COLOR)

        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.ai_engine = AIEngine(gemini_client=self.client)

        self.current_workflow_goal = None
        self.workflow_active = False
        self.is_processing = False  # Garde-fou : empêche deux analyses simultanées
        self.wait_retry_count = 0
        self.max_wait_retries = 6  # Nombre d'attentes consécutives tolérées avant d'abandonner
        self.current_sequence = []
        self.current_step_index = 0
        self.current_monitor = None
        self.last_click_coords = (-100, -100)

        self.pointer = AnimatedPointerWindow(
            self, on_valid_click_callback=self.next_sequence_step
        )
        pygame.mixer.init()

        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color=FRAME_BG,
            border_width=1,
            border_color=ACCENT_COLOR,
        )
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.header_frame = ctk.CTkFrame(
            self.main_frame, fg_color="transparent"
        )
        self.header_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))

        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="👁️ Vision Pro Agent",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_COLOR,
        )
        self.header_label.pack(side="left", padx=5)

        self.btn_quick = ctk.CTkButton(
            self.header_frame,
            text="✍️ Saisie",
            width=70,
            height=28,
            fg_color=USER_BUBBLE,
            command=lambda: self.quick_input.show_and_focus(),
        )
        self.btn_quick.pack(side="right", padx=3)

        self.btn_hide = ctk.CTkButton(
            self.header_frame,
            text="↙️ Masquer",
            width=65,
            height=28,
            fg_color="#4b6584",
            command=self.toggle_main_window,
        )
        self.btn_hide.pack(side="right", padx=3)

        self.lbl_status = ctk.CTkLabel(
            self.main_frame,
            text="🟢 Prêt",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#55efc4",
        )
        self.lbl_status.pack(side="top", anchor="w", padx=15, pady=(2, 5))

        self.input_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=BG_COLOR,
            corner_radius=10,
            border_width=1,
            border_color="#3d3f54",
        )
        self.input_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        self.entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Écrivez votre demande ici...",
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            border_width=0,
        )
        self.entry.pack(
            side="left", fill="x", expand=True, padx=(8, 6), pady=8
        )
        self.entry.bind(
            "<Return>", lambda event: self.process_request(use_vision=True)
        )

        self.btn_vision = ctk.CTkButton(
            self.input_frame,
            text="📸",
            width=45,
            height=40,
            fg_color=USER_BUBBLE,
            hover_color="#5f27cd",
            font=ctk.CTkFont(size=16),
            command=lambda: self.process_request(use_vision=True),
        )
        self.btn_vision.pack(side="right", padx=(0, 6), pady=8)

        self.btn_send = ctk.CTkButton(
            self.input_frame,
            text="🚀",
            width=45,
            height=40,
            font=ctk.CTkFont(size=15),
            fg_color="#0984e3",
            command=lambda: self.process_request(use_vision=True),
        )
        self.btn_send.pack(side="right", padx=(0, 8), pady=8)

        self.chat_history = ctk.CTkScrollableFrame(
            self.main_frame, fg_color="transparent"
        )
        self.chat_history.pack(
            side="top", fill="both", expand=True, padx=5, pady=5
        )

        self.append_to_chat(
            "🤖 Agent Prêt !\n👉 Cliquez sur 📸 pour analyser l'écran ou entrez votre prompt.",
            is_user=False,
        )

        self.avatar = AvatarWindow(self)
        self.subtitle = SubtitleWindow(self)
        self.quick_input = QuickInputWindow(self)

        self.withdraw()
        self.main_window_visible = False

        self.hotkey_listener = keyboard.GlobalHotKeys(
            {"<f9>": self.on_f9_pressed}
        )
        self.hotkey_listener.start()

        self.protocol("WM_DELETE_WINDOW", self.toggle_main_window)

    def toggle_main_window(self):
        if self.main_window_visible:
            self.withdraw()
            self.main_window_visible = False
        else:
            self.deiconify()
            self.main_window_visible = True

    def process_custom_prompt(self, text, use_vision=True):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.process_request(use_vision=use_vision)

    def set_status(self, text, color="#55efc4", avatar_state="idle"):
        self.lbl_status.configure(text=text, text_color=color)
        self.avatar.set_state(avatar_state)

    def _set_input_buttons_state(self, state):
        self.btn_send.configure(state=state)
        self.btn_vision.configure(state=state)
        if hasattr(self, "quick_input") and hasattr(self.quick_input, "btn_send"):
            self.quick_input.btn_send.configure(state=state)
            self.quick_input.btn_vision.configure(state=state)

    def stop_agent_workflow(self):
        self.workflow_active = False
        self.current_workflow_goal = None
        self.current_sequence = []
        self.last_click_coords = (-100, -100)
        self.pointer.hide()
        self.stop_audio()
        self._set_input_buttons_state("normal")
        self.set_status("🟢 Prêt", "#55efc4", "idle")

    def process_request(self, use_vision):
        # Garde-fou anti-concurrence : si une analyse tourne déjà, on ignore
        # cette nouvelle demande au lieu de lancer un 2e appel API en parallèle.
        if self.is_processing:
            print("⏳ [Garde-fou] Analyse déjà en cours, requête ignorée.")
            return

        prompt = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        if prompt:
            self.append_to_chat(prompt, is_user=True)
            self.current_workflow_goal = prompt
        elif not self.current_workflow_goal:
            self.current_workflow_goal = "Assistance et guidage sur l'écran"

        self.workflow_active = True
        self.is_processing = True
        self._set_input_buttons_state("disabled")
        self.current_sequence = []

        self.set_status("⚡ Analyse de l'écran...", "#f1c40f", "scan")
        threading.Thread(
            target=self.autonomous_agent_step,
            args=(use_vision,),
            daemon=True,
        ).start()

    def autonomous_agent_step(self, use_vision):
        try:
            if not self.workflow_active:
                return
            if use_vision:
                self.avatar.withdraw()
                # Le pointeur est déjà masqué avant qu'on revienne ici (voir
                # execute_sequence_step) : pas besoin de le refaire, et surtout
                # pas depuis ce thread (voir explication ci-dessous).
                time.sleep(0.1)

                monitor = self.get_active_monitor()
                self.current_monitor = monitor

                def _capture_monitor():
                    with mss.MSS() as sct:
                        shot = sct.grab(monitor)
                        return Image.frombytes(
                            "RGB", shot.size, shot.bgra, "raw", "BGRX"
                        )

                self.after(
                    0,
                    lambda: self.set_status(
                        "🔎 Attente de stabilité de l'écran...", "#f1c40f", "scan"
                    ),
                )
                # 100% local : aucune requête API n'est faite tant que l'écran bouge.
                img = self.ai_engine.stream.wait_until_stable(_capture_monitor)
                img.thumbnail((768, 768))

                self.avatar.deiconify()

                decision = self.ai_engine.process_screen_and_intent(
                    img, self.current_workflow_goal
                )

                if isinstance(decision, dict):
                    action = decision.get("action", "none")
                    response_text = decision.get(
                        "text", "Je ne trouve pas d'action claire à faire."
                    )
                    x = decision.get("x")
                    y = decision.get("y")

                    self.append_to_chat(response_text, is_user=False)

                    if action == "click" and x is not None and y is not None:
                        self.wait_retry_count = 0
                        self.current_sequence = [
                            {
                                "x": int(x),
                                "y": int(y),
                                "text": response_text,
                            }
                        ]
                        self.current_step_index = 0
                        self.after(
                            0,
                            lambda: self.execute_sequence_step(
                                self.current_step_index
                            ),
                        )
                    elif action == "wait":
                        self.speak(response_text)
                        self.wait_retry_count += 1
                        if self.wait_retry_count <= self.max_wait_retries:
                            # On relance une analyse un peu plus tard. La vraie
                            # attente "intelligente" se fait toute seule au
                            # prochain appel via wait_until_stable — en local,
                            # sans consommer de quota API pendant l'attente.
                            self.after(
                                900,
                                lambda: self.process_request(use_vision=True),
                            )
                        else:
                            self.wait_retry_count = 0
                            self.append_to_chat(
                                "⚠️ Toujours en attente après plusieurs essais, "
                                "j'arrête pour ne pas gaspiller ton quota API. "
                                "Réappuie sur F9 quand la page sera prête.",
                                is_user=False,
                            )
                            self.after(0, self.stop_agent_workflow)
                    else:
                        self.wait_retry_count = 0
                        self.speak(response_text)
                        self.after(0, self.stop_agent_workflow)

                else:
                    response_text = str(decision)
                    self.append_to_chat(f"{response_text}", is_user=False)
                    self.speak(response_text)
                    self.after(0, self.stop_agent_workflow)

            else:
                response = self.client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=[self.current_workflow_goal],
                )
                response_text = response.text.strip()
                self.append_to_chat(f"{response_text}", is_user=False)
                self.speak(response_text)
                self.after(0, self.stop_agent_workflow)

        except Exception as e:
            err_msg = str(e)
            if (
                "429" in err_msg
                or "RESOURCE_EXHAUSTED" in err_msg
                or "Quota" in err_msg
            ):
                self.append_to_chat(
                    "⚠️ Quota API temporairement atteint.\nL'IA fait une pause. Patiente ~1 min puis réappuie sur F9.",
                    is_user=False,
                )
                self.after(0, self.stop_agent_workflow)
            else:
                self.append_to_chat(f"❌ Erreur : {err_msg}", is_user=False)
                self.after(
                    0, lambda: self.set_status("❌ Erreur", "#e74c3c", "idle")
                )
                self.after(0, self.stop_agent_workflow)
        finally:
            # Quoi qu'il arrive (succès, erreur, ou sortie anticipée), on
            # relâche le verrou pour qu'une nouvelle analyse puisse démarrer.
            self.is_processing = False
            self.after(0, lambda: self._set_input_buttons_state("normal"))

    def execute_sequence_step(self, index):
        if not self.workflow_active:
            return

        if index >= len(self.current_sequence):
            self.pointer.hide()

            def _wait_and_reprocess():
                self.set_status(
                    "⚡ Analyse de la suite...", "#00cec9", "scan"
                )
                self.process_request(use_vision=True)

            threading.Thread(target=_wait_and_reprocess, daemon=True).start()
            return

        step = self.current_sequence[index]

        dist = math.hypot(
            step["x"] - self.last_click_coords[0],
            step["y"] - self.last_click_coords[1],
        )
        if dist < 20:
            self.pointer.hide()
            self.set_status("⏳ Transition...", "#f39c12", "scan")
            self.speak("Je patiente pour laisser la page réagir.")
            self.last_click_coords = (-100, -100)
            self.after(1000, lambda: self.process_request(use_vision=True))
            return

        self.last_click_coords = (step["x"], step["y"])

        monitor = self.current_monitor
        click_x = monitor["left"] + int(
            (step["x"] / 1000.0) * monitor["width"]
        )
        click_y = monitor["top"] + int(
            (step["y"] / 1000.0) * monitor["height"]
        )

        self.avatar.dodge_if_needed(click_x, click_y)
        self.pointer.animate_to(click_x, click_y)
        self.set_status(
            f"👆 Étape {index+1}/{len(self.current_sequence)}",
            "#00cec9",
            "speak",
        )

        self.speak(step["text"])

    def next_sequence_step(self):
        if self.current_sequence:
            self.current_step_index += 1
            self.stop_audio()
            self.execute_sequence_step(self.current_step_index)

    def get_active_monitor(self):
        x, y = self.winfo_pointerx(), self.winfo_pointery()
        with mss.MSS() as sct:
            monitors = (
                sct.monitors[1:] if len(sct.monitors) > 1 else sct.monitors
            )
            for mon in monitors:
                if (
                    mon["left"] <= x <= mon["left"] + mon["width"]
                    and mon["top"] <= y <= mon["top"] + mon["height"]
                ):
                    return mon
            return monitors[0]

    def listen_microphone(self):

        def _listen():
            recognizer = sr.Recognizer()
            try:
                self.after(
                    0,
                    lambda: self.set_status("🎙️ Écoute...", "#ff7675", "speak"),
                )
                self.after(
                    0,
                    lambda: self.subtitle.show(
                        "Écoute en cours...",
                        self.avatar.winfo_rootx() + 120,
                        self.avatar.winfo_rooty(),
                    ),
                )
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.4)
                    audio = recognizer.listen(
                        source, timeout=4, phrase_time_limit=6
                    )
                text = recognizer.recognize_google(audio, language="fr-FR")
                self.after(0, lambda: self.append_to_chat(text, is_user=True))
                self.after(
                    0,
                    lambda: self.process_custom_prompt(text, use_vision=True),
                )
            except Exception:
                self.after(
                    0, lambda: self.set_status("🟢 Prêt", "#55efc4", "idle")
                )
                self.after(0, self.subtitle.hide)

        threading.Thread(target=_listen, daemon=True).start()

    def stop_audio(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def speak(self, text):

        def _speak_thread():
            try:
                if not text.strip():
                    return
                self.stop_audio()

                self.after(
                    0,
                    lambda: self.subtitle.show(
                        text,
                        self.avatar.winfo_rootx() + 120,
                        self.avatar.winfo_rooty(),
                    ),
                )
                self.after(0, lambda: self.avatar.set_state("speak"))

                tts = gTTS(text=text, lang="fr")
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                pygame.mixer.music.load(fp)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

                self.after(0, lambda: self.avatar.set_state("idle"))
            except Exception:
                pass

        threading.Thread(target=_speak_thread, daemon=True).start()

    def on_f9_pressed(self):
        self.after(0, lambda: self.process_request(use_vision=True))

    def on_closing(self):
        self.hotkey_listener.stop()
        self.pointer.mouse_listener.stop()
        self.workflow_active = False
        self.stop_audio()
        self.destroy()

    def append_to_chat(self, text, is_user=False):
        bubble_color = USER_BUBBLE if is_user else AI_BUBBLE
        align = "e" if is_user else "w"

        bubble_frame = ctk.CTkFrame(self.chat_history, fg_color="transparent")
        bubble_frame.pack(fill="x", pady=4, anchor=align)

        lbl = ctk.CTkLabel(
            bubble_frame,
            text=text,
            fg_color=bubble_color,
            text_color="white",
            corner_radius=12,
            wraplength=340,
            justify="left",
            font=ctk.CTkFont(size=12),
        )
        lbl.pack(
            side="right" if is_user else "left",
            padx=10,
            pady=2,
            ipadx=12,
            ipady=8,
        )

        self.after(
            50, lambda: self.chat_history._parent_canvas.yview_moveto(1.0)
        )


if __name__ == "__main__":
    app = VisionAssistantApp()
    app.mainloop()

