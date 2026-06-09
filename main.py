# main.py
import sys
import time
import threading
import random
import re
import math
import customtkinter as ctk
from tkinter import Canvas
import speech_recognition as sr

# Import the standalone question bank dataset safely
from question_bank import ACADEMIC_DATABASE, QUESTION_PATTERNS

ctk.set_appearance_mode("Dark")

class AIVivaExaminerUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Core System Logic Setup
        self.academic_database = ACADEMIC_DATABASE
        self.question_patterns = QUESTION_PATTERNS
        self.covered_topics = {}
        
        # Runtime States
        self.selected_subject = None
        self.current_question = ""
        self.current_reference = ""
        self.current_topic = ""
        
        # Premium Geometry & Base Config
        self.title("AI Viva Examiner - Analyze. Evaluate. Accelerate.")
        self.geometry("1200x780")
        self.minsize(1050, 700)
        
        # Layout weights
        self.grid_columnconfigure(0, weight=0) # Sidebar fixed
        self.grid_columnconfigure(1, weight=1) # Main View dynamic
        self.grid_rowconfigure(0, weight=1)
        
        # Audio Animation States
        self.wave_animation_active = False
        self.wave_time = 0
        
        self.create_premium_layout()
        
    def create_premium_layout(self):
        # ----------------- SIDEBAR (NEO-DARK) -----------------
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#090d16")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # App Title Typography
        self.logo_label = ctk.CTkLabel(self.sidebar, text="AI VIVA EXAMINER", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=25, pady=(35, 5), sticky="w")
        
        self.sub_logo = ctk.CTkLabel(self.sidebar, text="AUTOMATED EVALUATION ENGINE", text_color="#4a5568", font=ctk.CTkFont(size=10, weight="bold"))
        self.sub_logo.grid(row=1, column=0, padx=25, pady=(0, 30), sticky="w")
        
        # Form Controls
        self.class_label = ctk.CTkLabel(self.sidebar, text="ACADEMIC CLASS LEVEL", text_color="#718096", font=ctk.CTkFont(size=11, weight="bold"))
        self.class_label.grid(row=2, column=0, padx=25, pady=(10, 5), sticky="w")
        
        self.class_combo = ctk.CTkComboBox(self.sidebar, values=["10th Standard", "12th Standard"], command=self.update_subject_options, fg_color="#111625", border_color="#1f293d")
        self.class_combo.grid(row=3, column=0, padx=25, pady=(0, 20), sticky="ew")
        
        self.sub_label = ctk.CTkLabel(self.sidebar, text="TARGET SYLLABUS DISCIPLINE", text_color="#718096", font=ctk.CTkFont(size=11, weight="bold"))
        self.sub_label.grid(row=4, column=0, padx=25, pady=(10, 5), sticky="w")
        
        self.sub_combo = ctk.CTkComboBox(self.sidebar, values=[], fg_color="#111625", border_color="#1f293d")
        self.sub_combo.grid(row=5, column=0, padx=25, pady=(0, 40), sticky="ew")
        
        # Core Launcher Action Buttons (Vibrant Violet / Cyberpunk theme)
        self.start_btn = ctk.CTkButton(self.sidebar, text="Start Viva", command=self.trigger_question_generation, fg_color="#7928CA", hover_color="#ff0080", height=45, font=ctk.CTkFont(weight="bold", size=13))
        self.start_btn.grid(row=6, column=0, padx=25, pady=10, sticky="ew")
        
        self.reset_btn = ctk.CTkButton(self.sidebar, text="Restart Viva", command=self.clear_dashboard_fields, fg_color="transparent", border_width=1, border_color="#2d3748", text_color="#e2e8f0", hover_color="#111625", height=35)
        self.reset_btn.grid(row=7, column=0, padx=25, pady=10, sticky="ew")
        
        self.update_subject_options("10th Standard")

        # ----------------- MAIN DISPLAY CENTERSTAGE -----------------
        self.main_content = ctk.CTkFrame(self, fg_color="#05070c", corner_radius=0)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(2, weight=1) 
        
        # --- HEADERS & DIGITAL HUD CLOCK ---
        self.header_panel = ctk.CTkFrame(self.main_content, fg_color="#0c101b", corner_radius=12, height=90, border_width=1, border_color="#111625")
        self.header_panel.grid(row=0, column=0, sticky="ew", padx=30, pady=(35, 15))
        self.header_panel.grid_propagate(False)
        
        self.banner_text = ctk.CTkLabel(self.header_panel, text="System Core Idle Status • Configuration Required", font=ctk.CTkFont(size=14, weight="normal"), text_color="#a0aec0")
        self.banner_text.pack(side="left", padx=25, pady=20)
        
        self.clock_frame = ctk.CTkFrame(self.header_panel, fg_color="#111625", corner_radius=8, border_width=1, border_color="#1f293d")
        self.clock_frame.pack(side="right", padx=20, pady=15, fill="y")
        
        self.clock_label = ctk.CTkLabel(self.clock_frame, text="00:30", font=ctk.CTkFont(family="Consolas", size=30, weight="bold"), text_color="#00f5d4")
        self.clock_label.pack(padx=20, pady=5)
        
        # --- AUDIO ANIMATION CANVAS HUD (Glowing Wave Strip) ---
        self.wave_canvas = Canvas(self.main_content, height=20, bg="#05070c", highlightthickness=0)
        self.wave_canvas.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 15))

        # --- PANELS (ADJUSTED SIZE: Main Area is 75% wide, Report is 25% wide) ---
        self.notebook_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.notebook_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 30))
        self.notebook_frame.grid_columnconfigure(0, weight=3) # Main Text View (Takes 3x space)
        self.notebook_frame.grid_columnconfigure(1, weight=1) # Score Panel (Takes 1x space - made smaller!)
        self.notebook_frame.grid_rowconfigure(0, weight=1)

        # Main Text Readout Log (Bigger Workspace)
        self.display_box = ctk.CTkTextbox(self.notebook_frame, font=ctk.CTkFont(family="Consolas", size=13), fg_color="#0c101b", border_color="#171f30", border_width=1, text_color="#e2e8f0", corner_radius=12)
        self.display_box.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0)
        
        # SCORECARD PANEL (Compact and Minimalistic Redesign)
        self.report_card = ctk.CTkFrame(self.notebook_frame, fg_color="#0c101b", border_width=1, border_color="#171f30", corner_radius=12)
        self.report_card.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.setup_report_card_scaffolding()

        self.append_terminal_text("Welcome to AI Viva Examiner.\n\n"
                                  "Viva Instructions:\n"
                                  "1. Select academic credentials via parameters in the Left Panel.\n"
                                  "2. Start Viva: Question generates instantly and your viva will start.\n"
                                  "3. Digital Clock gives you 30 seconds prepration time.\n"
                                  "4. CRITICAL CRITERIA: Audio Capture fires automatically at 00:00! Speak promptly.", clear=True)

    def setup_report_card_scaffolding(self):
        for widget in self.report_card.winfo_children():
            widget.destroy()
            
        lbl = ctk.CTkLabel(self.report_card, text="Performance Report", font=ctk.CTkFont(size=12, weight="bold"), text_color="#90cdf4")
        lbl.pack(pady=(20, 15), padx=15, anchor="w")
        
        self.score_badge = ctk.CTkLabel(self.report_card, text="--.-", font=ctk.CTkFont(family="Segoe UI", size=56, weight="bold"), text_color="#2d3748")
        self.score_badge.pack(pady=5)
        
        self.score_lbl = ctk.CTkLabel(self.report_card, text="FINAL SCORE OUT OF 10.0", font=ctk.CTkFont(size=9, weight="bold"), text_color="#4a5568")
        self.score_lbl.pack(pady=(0, 20))
        
        self.metric_group = ctk.CTkFrame(self.report_card, fg_color="#111625", corner_radius=8, border_width=1, border_color="#171f30")
        self.metric_group.pack(fill="x", padx=15, pady=5)
        
        self.meta_subject = self.create_metric_row(self.metric_group, "Subject:", "Not Loaded")
        self.meta_topic = self.create_metric_row(self.metric_group, "Topic:", "Idle")
        self.meta_accuracy = self.create_metric_row(self.metric_group, "Accuracy:", "0.0%")
        self.meta_grade = self.create_metric_row(self.metric_group, "Grade:", "Unclassified")

    def create_metric_row(self, parent, label_text, default_val):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=6)
        
        l_lbl = ctk.CTkLabel(row, text=label_text, font=ctk.CTkFont(size=11), text_color="#a0aec0")
        l_lbl.pack(side="left")
        
        r_lbl = ctk.CTkLabel(row, text=default_val, font=ctk.CTkFont(size=11, weight="bold"), text_color="#edf2f7")
        r_lbl.pack(side="right")
        return r_lbl

    def update_subject_options(self, selected_class):
        if "12" in selected_class:
            subjects = ["Physics", "Chemistry", "Biology", "English"]
        else:
            subjects = ["Science", "Social science", "English"]
        self.sub_combo.configure(values=subjects)
        self.sub_combo.set(subjects[0])

    def append_terminal_text(self, text, clear=False):
        self.display_box.configure(state="normal")
        if clear:
            self.display_box.delete("1.0", ctk.END)
        self.display_box.insert(ctk.END, text + "\n")
        self.display_box.see(ctk.END)
        self.display_box.configure(state="disabled")

    def trigger_question_generation(self):
        self.selected_subject = self.sub_combo.get()
        self.start_btn.configure(state="disabled")
        self.class_combo.configure(state="disabled")
        self.sub_combo.configure(state="disabled")
        self.clock_label.configure(text_color="#ff0080") 
        
        threading.Thread(target=self.async_process_question, daemon=True).start()

    def async_process_question(self):
        sub = self.selected_subject
        subject_data = self.academic_database.get(sub, {})
        topics = list(subject_data.keys()) if subject_data else ["General Science"]
        
        if sub not in self.covered_topics:
            self.covered_topics[sub] = []
        remaining = list(set(topics) - set(self.covered_topics[sub]))
        if not remaining:
            self.covered_topics[sub].clear()
            remaining = topics
            
        self.current_topic = random.choice(remaining)
        self.covered_topics[sub].append(self.current_topic)
        
        pattern = random.choice(self.question_patterns)
        self.current_question = pattern.format(topic=self.current_topic, subject=sub)
        
        data = subject_data.get(self.current_topic, {
            "definition": f"{self.current_topic} framework analysis.",
            "explanation": "No comprehensive database explanation maps loaded.",
            "keywords": ["Academic Standards"]
        })
        key_points = "\n- ".join(data["keywords"])
        self.current_reference = f"Core Definition:\n{data['definition']}\n\nTechnical Breakdown:\n{data['explanation']}\n\nTarget Scoring Vocabulary Terms:\n- {key_points}"
        
        self.append_terminal_text("", clear=True)
        self.append_terminal_text(f"📝 VIVA QUESTION MATRIX INITIALIZED:\n{'-'*65}\n👉 {self.current_question}\n{'-'*65}\n")
        self.append_terminal_text("System Clock Alert: Study clock active. Formulate conceptual outlines immediately...\n")
        
        # Clock countdown
        for i in range(30, -1, -1):
            self.clock_label.configure(text=f"00:{i:02d}")
            self.banner_text.configure(text=f"Phase Matrix: Preparation Phase Active. Speak your answer in {i}s...")
            time.sleep(1)
            
        # Trigger Automated Recording
        self.clock_label.configure(text="00:00", text_color="#00f5d4")
        self.banner_text.configure(text="Clock Expired! Capture Mode Live: Initialize Mic Feed Pipeline...")
        self.async_automated_voice_capture_pipeline()

    # ----------------- AUDIO ANIMATION ENGINE -----------------
    def animate_wave_hud(self):
        if not self.wave_animation_active:
            self.wave_canvas.delete("all")
            return

        self.wave_canvas.delete("wave_path")
        self.wave_time += 0.2
        
        width = self.wave_canvas.winfo_width()
        height = self.wave_canvas.winfo_height()
        mid_y = height / 2
        points = []
        
        glow_color = "#00f5d4"

        for x in range(0, width + 5, 5):
            y = mid_y + (7 * math.sin((x * 0.03) + self.wave_time))
            points.append(x)
            points.append(y)
            
        if len(points) >= 4:
            self.wave_canvas.create_line(points, smooth=True, fill=glow_color, width=2.5, capstyle="round", tags="wave_path")

        self.after(30, self.animate_wave_hud)

    def async_automated_voice_capture_pipeline(self):
        self.append_terminal_text(f"\n{'*'*25} 🎙️ MIC RECORDING ENGINE ACTIVE — RESPOND NOW {'*'*25}\n")
        
        # ACTIVATE WAVE ANIMATION
        self.wave_animation_active = True
        self.wave_time = 0
        self.after(0, self.animate_wave_hud)

        recognizer = sr.Recognizer()
        spoken_response = None
        
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
            spoken_response = recognizer.recognize_google(audio)
        except Exception:
            spoken_response = None
        finally:
            # STOP WAVE ANIMATION
            self.wave_animation_active = False

        if not spoken_response:
            self.append_terminal_text("[!] Evaluation Cancelled: Zero audio input processed.")
            self.banner_text.configure(text="Capture Failed. Ready for safe system restart.")
            self.restore_action_buttons()
            return

        # Metrics Analytics Mapping
        self.append_terminal_text(f"Processed Voice Transcription Log:\n\" {spoken_response} \"\n")
        
        keywords = set(re.findall(r'\b[a-zA-Z]{5,}\b', self.current_reference.lower()))
        user_words = set(re.findall(r'\b[a-zA-Z]{5,}\b', spoken_response.lower()))
        
        accuracy_pct = 0.0
        if keywords:
            matches = sum(1 for word in keywords if word in user_words)
            accuracy_pct = round((matches / len(keywords)) * 100, 2)
            
        word_count = len(spoken_response.split())
        base_marks = (accuracy_pct * 0.07) + (min(word_count, 60) * 0.05)
        final_marks = min(round(base_marks, 1), 10.0)
        
        level = "Needs Work"
        theme_glow = "#ff0080" # Crimson Neon
        if final_marks >= 8.5: 
            level = "Expert Mastery"
            theme_glow = "#00f5d4" # Cyan Teal Neon
        elif final_marks >= 6.5: 
            level = "Good Standard"
            theme_glow = "#ffb703" # Amber Yellow
            
        # DYNAMIC SCORE UPDATE
        self.score_badge.configure(text=f"{final_marks:04.1f}", text_color=theme_glow)
        self.meta_subject.configure(text=self.selected_subject)
        self.meta_topic.configure(text=self.current_topic if len(self.current_topic) < 14 else self.current_topic[:11]+"...")
        self.meta_accuracy.configure(text=f"{accuracy_pct}%", text_color=theme_glow)
        self.meta_grade.configure(text=level, text_color=theme_glow)
        
        self.append_terminal_text(f"{'-'*65}\n📋 EVALUATION REFERENCE PROFILE GUIDELINES:\n{'-'*65}")
        self.append_terminal_text(self.current_reference)
        
        self.banner_text.configure(text="Assessment processing complete. Score scorecard data values locked.")
        self.restore_action_buttons()

    def restore_action_buttons(self):
        self.start_btn.configure(state="normal")
        self.class_combo.configure(state="normal")
        self.sub_combo.configure(state="normal")

    def clear_dashboard_fields(self):
        self.append_terminal_text("", clear=True)
        self.append_terminal_text("System normalized. Select branch to resume.")
        self.banner_text.configure(text="System Core Idle Status • Configuration Required")
        self.clock_label.configure(text="00:30", text_color="#00f5d4")
        self.setup_report_card_scaffolding()
        self.restore_action_buttons()

if __name__ == "__main__":
    app = AIVivaExaminerUI()
    app.mainloop()