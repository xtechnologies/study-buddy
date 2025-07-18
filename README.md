# 📚 Study-Bud

**Study-Bud** is your intelligent study companion — a web-based platform built with Django, HTML, and CSS. It includes an AI-powered chatbot that helps students with their academic questions, provides study support, and keeps them motivated through personalized interaction.

---

## 🚀 Features

- 🤖 **AI Study Assistant** – Chatbot capable of answering academic questions and providing helpful tips.
- 📸 **User Profile Images** – Upload and manage your own profile picture.
- 🎨 **Responsive UI** – Clean frontend built with HTML and CSS.
- ⚙️ **Django Framework** – Robust backend architecture using Python and Django.
- 📁 **Structured Project** – Modular and scalable project layout for easy development and collaboration.

---

## 🛠 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3
- **AI:** NLP-powered chatbot (can be extended with OpenAI or similar)
- **Database:** SQLite (default, can be configured)

---

## 📁 Project Structure

```
study-buddy/
├── base/                  # Base configuration and utilities
├── chatbot/               # AI chatbot logic and views
├── media/profile_images/  # Uploaded profile pictures
├── static/                # Static files (CSS, JS, images)
├── studybuddy/            # Main Django project configuration
├── templates/             # HTML templates for the frontend
├── .gitignore             # Files and folders to ignore in Git
├── README.md              # You're reading it!
```

---

## 🔧 Installation & Setup

Follow these steps to get the project running locally:

1. **Clone the repository**
   ```bash
   git clone https://github.com/xtechnologies/study-buddy.git
   cd study-buddy
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Visit the app in your browser**
   ```
   http://127.0.0.1:8000/
   ```

---

## 🤖 About the Chatbot

The chatbot is designed to:
- Answer student queries
- Provide study advice
- Offer definitions and summaries
- Encourage positive study habits

The AI logic can be extended using:
- OpenAI GPT API
- Hugging Face Transformers
- Custom-trained models

---

## ✨ Future Improvements

- Add subject-specific tutoring modules
- Gamify the study process (e.g. flashcards, quizzes)
- Add user authentication and dashboards
- Integrate reminders and to-do lists

---

## 🙌 Contributing

Contributions are welcome! If you'd like to improve Study-Bud:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🌐 Live Demo

(Coming soon...)

---

Happy studying with **Study-Bud**! 🎓🤝
