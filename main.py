import tkinter as tk
from tkinter import messagebox, Listbox, END
import requests
import json

FAVORITES_FILE = "favorites.json"
current_user_data = None

def load_favorites():
    """Загружает список избранных пользователей из файла."""
    try:
        with open(FAVORITES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_favorites(favorites):
    """Сохраняет список избранных пользователей в файл."""
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=2)

def search_user():
    """Обрабатывает поиск пользователя по логину."""
    global current_user_data
    username = entry_search.get().strip()

    if not username:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым!")
        return

    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        response.raise_for_status() # Вызовет исключение для 404 Not Found
        user_data = response.json()
        display_user(user_data)
    except requests.exceptions.HTTPError:
        messagebox.showerror("Ошибка", "Пользователь не найден.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка сети", f"Проверьте подключение к интернету: {e}")

def display_user(user_data):
    """Отображает данные пользователя в интерфейсе."""
    global current_user_data
    listbox_results.delete(0, END)
    
    # Формируем строку для отображения: Логин (Имя)
    display_name = user_data.get('name', 'Нет имени')
    info_line = f"{user_data['login']} ({display_name})"
    listbox_results.insert(END, info_line)
    
    current_user_data = user_data

def add_to_favorites():
    """Добавляет текущего пользователя в избранное."""
    if not current_user_data:
        messagebox.showwarning("Ошибка", "Сначала найдите пользователя!")
        return

    favorites = load_favorites()
    
    # Проверка на дубликаты по логину
    if any(u['login'] == current_user_data['login'] for u in favorites):
        messagebox.showinfo("Информация", "Пользователь уже в избранном!")
        return

    favorites.append(current_user_data)
    save_favorites(favorites)
    messagebox.showinfo("Успех", "Пользователь добавлен в избранное!")


# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("GitHub User Finder")
root.geometry("400x350")
root.resizable(False, False)
root.configure(bg="#f0f0f5")

# Поле ввода и кнопка поиска
frame_search = tk.Frame(root, bg="#f0f0f5")
frame_search.pack(pady=15)

entry_search = tk.Entry(frame_search, width=35, font=('Arial', 12))
entry_search.pack(side=tk.LEFT, padx=5)

btn_search = tk.Button(frame_search, text="Поиск", command=search_user)
btn_search.pack(side=tk.LEFT)

# Список результатов поиска
listbox_results = Listbox(root, width=50, height=6, font=('Arial', 11))
listbox_results.pack(pady=10)

# Кнопка добавления в избранное
btn_fav = tk.Button(root, text="Добавить в избранное", command=add_to_favorites)
btn_fav.pack(pady=5)

root.mainloop()
