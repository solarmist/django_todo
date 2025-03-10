# 🦊 Fox To-Do App

A simple yet fun Django-based to-do app featuring:
- **Categories with icons** 🎨
- **Fortune messages** for completed tasks 🔮
- **Animated toasts** for feedback 🎉

---

## 🚀 **Features**

### 🗂️ Categories with Icons
- Organize tasks using categories with default or custom icons.
- Upload your own category icons or choose from preloaded ones.

### 🔮 Fortune Messages
- Completing tasks reveals **random fortune messages** with animated toasts.
- Fortune examples:
   - “You are 100% more productive than a potato. Keep it up!”
   - “The stapler sees all. Watch your back.”

### 🎉 Animated Toasts
- Feedback for actions using **smooth animations**.
- Toast messages fade out after 3 seconds for a seamless experience.


---

## 🛠 **Setup Instructions**

### 1. Clone the repository
```bash
git clone https://github.com/solarmist/django_todo.git
cd django_todo
```

### 2. Install dependencies
```bash
poetry install
```
### 3. Apply migrations
```bash
python manage.py migrate
```

### 4. Create a superuser
```bash
python manage.py createsuperuser
```

### 5. Run the server
```bash
python manage.py runserver
```

## 📋 Testing

Run tests with:
```bash
python manage.py test
```
