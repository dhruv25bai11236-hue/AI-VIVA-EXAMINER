# AI Viva Examiner

## Overview
AI Viva Examiner is a desktop-based AI-powered viva examination simulator built with Python and CustomTkinter. It generates subject-specific viva questions, provides preparation time, captures spoken answers through a microphone, converts speech to text, and evaluates responses using a keyword-based scoring system.

The application is designed for high-school level academic subjects and offers an interactive user interface with automated assessment and performance reporting.

---

## Features

### Smart Viva Question Generation
- Generates random viva questions from a predefined academic database.
- Supports:
  - Class 10 Subjects
    - Science
    - Social Science
    - English
  - Class 12 Subjects
    - Physics
    - Chemistry
    - Biology
    - English

### Automated Viva Workflow
1. Select class and subject.
2. Generate a viva question.
3. Get 30 seconds of preparation time.
4. Automatic voice recording starts.
5. Speech is converted to text.
6. Answer is evaluated automatically.
7. Score and performance report are displayed.

### Speech Recognition
- Uses Google Speech Recognition through the `speech_recognition` library.
- Captures answers directly from the microphone.

### Performance Evaluation
- Keyword-based answer analysis.
- Accuracy percentage calculation.
- Final score out of 10.
- Performance grading:
  - Expert Mastery
  - Good Standard
  - Needs Work

### Modern User Interface
- Built using CustomTkinter.
- Dark theme dashboard.
- Animated audio wave visualization.
- Real-time countdown timer.
- Performance report panel.

---

## Project Structure

```text
.
├── main.py              # Main application and UI
├── question_bank.py     # Academic database and question patterns
└── README.md            # Project documentation
```

---

## Technologies Used

- Python 3.x
- CustomTkinter
- Tkinter Canvas
- SpeechRecognition
- Threading
- Regular Expressions (re)
- Math Module

---

## Installation

### 1. Clone the Repository

```bash
[git clone https://github.com/your-username/ai-viva-examiner.git
cd ai-viva-examiner](https://github.com/dhruv25bai11236-hue/AI-VIVA-EXAMINER)
```

### 2. Install Dependencies

```bash
pip install customtkinter SpeechRecognition pyaudio
```

If PyAudio installation fails:

```bash
pip install pipwin
pipwin install pyaudio
```

---

## Running the Project

```bash
python main.py
```

---

## How It Works

### Question Generation
The system randomly selects:
- A subject
- A topic from the academic database
- A question pattern

and generates a viva question.

### Preparation Phase
A 30-second countdown timer allows students to prepare.

### Voice Capture
After the timer reaches zero:
- Microphone recording starts automatically.
- Speech is converted into text.

### Evaluation
The system:
- Extracts keywords from the reference answer.
- Compares them with the student's response.
- Calculates:
  - Accuracy percentage
  - Word count score
  - Final marks out of 10

---

## Sample Workflow

```text
Select Subject
      ↓
Generate Question
      ↓
30s Preparation Timer
      ↓
Voice Recording
      ↓
Speech-to-Text
      ↓
Evaluation
      ↓
Performance Report
```

---

## Future Improvements

- AI-powered semantic answer evaluation using NLP.
- GPT-based viva conversations.
- Database integration for student records.
- Export reports to PDF.
- Multi-language support.
- Teacher dashboard.
- Online viva mode.

---

## Educational Use Cases

- School viva practice
- Oral examination preparation
- Self-assessment
- Classroom demonstrations
- Subject revision sessions

---

## Author
Dhruv Shrivastava
Developed as an AI-assisted Viva Examination System using Python, CustomTkinter, and Speech Recognition.
