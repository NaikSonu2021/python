# 🐍 Complete Python Mastery Platform

**From Zero to Hero - Master Python with 50+ Interactive Lessons!**

## ✨ Features

### 📚 **Comprehensive Curriculum**
- **15 Beginner Lessons**: Start from absolute basics
- **20 Intermediate Lessons**: Advanced concepts and techniques
- **15 Advanced Lessons**: Expert-level Python mastery
- **50+ Total Lessons** with full content and examples

### 💻 **Real Python Execution**
- Backend-powered Python execution
- Full `input()` function support
- Real error messages and output
- Execute any Python code

### 🎯 **Interactive Learning**
- Interactive quizzes after each lesson
- Practice exercises with test cases
- Real-world projects
- Code examples you can try

### 🏆 **Gamification**
- XP system for motivation
- 12+ Unlockable achievements
- Daily streak tracking
- Progress bars for each level

### 🎮 **Engaging Content**
- Beautiful, modern UI
- Syntax-highlighted code editor
- Terminal-style output
- Responsive design

## 🚀 Quick Start

### Option 1: Local Setup

1. **Install Python 3.11+**

2. **Clone or download files**

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the app:**
```bash
python app.py
```

5. **Open browser:**
```
http://localhost:5000
```

### Option 2: Deploy to Koyeb (Free)

1. **Sign up at [Koyeb.com](https://koyeb.com)**

2. **Create New App** → **Deploy from GitHub**

3. **Connect your repository**

4. **Configure:**
   - Build command: (leave empty)
   - Run command: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Port: 5000

5. **Deploy!**

6. **Update API_URL in index.html:**
   - Change `const API_URL = 'http://localhost:5000';`
   - To your Koyeb URL: `const API_URL = 'https://your-app.koyeb.app';`

### Option 3: Deploy to PythonAnywhere (Free)

1. **Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com)**

2. **Upload files** to your account

3. **Open Bash console:**
```bash
pip install --user flask flask-cors gunicorn
```

4. **Create Web App:**
   - Go to Web tab
   - Add new web app
   - Choose Flask
   - Python 3.11
   - Set path to your app.py

5. **Configure static files:**
   - URL: `/`
   - Directory: `/home/yourusername/templates`

6. **Reload web app**

7. **Update API_URL** to your PythonAnywhere URL

## 📁 Project Structure

```
python-mastery/
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
├── Procfile               # Deployment config
├── runtime.txt            # Python version
├── templates/
│   └── index.html         # Main frontend
└── README.md              # This file
```

## 🎓 Lesson Topics

### 🌱 Beginner (15 Lessons)
1. Python Basics & Installation
2. Variables & Data Types
3. Basic Operations & Math
4. Strings & String Methods
5. Lists & List Methods
6. Conditional Statements (if/else)
7. Loops (for & while)
8. Functions & Parameters
9. Dictionaries & Sets
10. Tuples & Comprehensions
...and more!

### 🚀 Intermediate (20 Lessons)
1. Object-Oriented Programming
2. File Handling & I/O
3. Exception Handling
4. Modules & Packages
5. Regular Expressions
6. Lambda & Functional Programming
7. Decorators
8. Generators & Iterators
9. Context Managers
10. Working with JSON & APIs
...and more!

### ⚡ Advanced (15 Lessons)
1. Advanced OOP - Inheritance & Polymorphism
2. Multithreading & Multiprocessing
3. Asyncio & Async Programming
4. Database Operations
5. Web Scraping
6. Testing & Debugging
7. Design Patterns
8. Performance Optimization
9. Data Science with Pandas & NumPy
10. Machine Learning Basics
...and more!

## 🎮 Features

### Code Editor
- Syntax highlighting
- Real Python execution via backend
- Multiple input support
- Copy code functionality
- Format code option

### Terminal Output
- Live execution results
- Error messages with stack traces
- Input/output display
- Scrollable history

### Progress Tracking
- Lesson completion tracking
- XP system
- Daily streak counter
- Level progress bars
- Achievement system

### Achievements
- 🎯 First Steps - Complete first lesson
- 🔥 5 Day Streak - Learn for 5 days
- 💯 Perfect Score - Get 100% on quiz
- 🚀 Code Runner - Execute 50 programs
- 📚 Beginner Master - Complete all beginner lessons
- ⚡ Intermediate Pro - Complete all intermediate lessons
- 👑 Advanced Expert - Complete all advanced lessons
- 🏆 Python Master - Complete all 50 lessons
- 💪 Practice Makes Perfect - Complete 25 exercises
- 🎮 Project Builder - Complete 5 projects
- ⭐ XP Hunter - Earn 5000 XP
- 🧠 Quick Learner - Complete lesson in under 10 min

## 💡 Usage Tips

### For Students
1. Start from Beginner level
2. Complete lessons in order
3. Try all code examples
4. Take quizzes to test knowledge
5. Practice with exercises
6. Build projects to apply skills

### For Teachers
1. Use as course material
2. Assign specific lessons
3. Track student progress
4. Create custom exercises
5. Add your own projects

## 🔧 Customization

### Add New Lessons
Edit `templates/index.html`:
```javascript
lessonsData.beginner.push({
    id: 'b11',
    title: 'Your Lesson Title',
    description: 'Lesson description',
    xp: 100,
    time: '30 min',
    difficulty: 'Easy',
    content: `Your lesson HTML content`,
    quiz: [...]
});
```

### Modify Achievements
```javascript
achievementsData.push({
    id: 13,
    icon: '🌟',
    title: 'Your Achievement',
    description: 'Description',
    unlocked: false
});
```

### Change Theme Colors
Edit CSS variables in `<style>`:
```css
:root {
    --primary: #667eea;
    --secondary: #764ba2;
    --success: #28a745;
    --danger: #dc3545;
}
```

## 🐛 Troubleshooting

### Backend not connecting
- Check if Flask server is running
- Verify `API_URL` in index.html matches your backend
- Check CORS settings in app.py

### Code execution failing
- Ensure Python 3.11+ is installed
- Check backend logs for errors
- Verify input format for `input()` functions

### Progress not saving
- Check browser localStorage is enabled
- Clear cache and try again
- Progress is saved locally per browser

## 📝 License

Free to use for educational purposes!

## 🤝 Contributing

Feel free to:
- Add more lessons
- Improve existing content
- Fix bugs
- Add new features
- Translate to other languages

## 🎯 Roadmap

- [ ] Add video tutorials
- [ ] More interactive exercises
- [ ] Code challenges with leaderboard
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] AI-powered code assistant
- [ ] Certificate generation
- [ ] Social features

## 📧 Support

Need help? Check:
- README.md (this file)
- Code comments
- Flask documentation
- Python documentation

## 🌟 Made with ❤️ for Python Learners

Happy Coding! 🐍✨
