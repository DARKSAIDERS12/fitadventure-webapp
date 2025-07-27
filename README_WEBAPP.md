# 🍎 База продуктов FitAdventure - Web App

## 📱 Как разместить Web App

### Вариант 1: GitHub Pages (Рекомендуется)

1. **Создайте новый репозиторий на GitHub:**
   - Название: `fitadventure-products`
   - Публичный репозиторий

2. **Загрузите файлы:**
   - Скопируйте `index.html` в корень репозитория
   - Переименуйте в `index.html`

3. **Включите GitHub Pages:**
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: main
   - Folder: / (root)

4. **URL будет:** `https://ваш-username.github.io/fitadventure-products/`

### Вариант 2: Vercel

1. **Создайте аккаунт на Vercel**
2. **Создайте новый проект**
3. **Загрузите `index.html`**
4. **Получите URL вида:** `https://fitadventure-products.vercel.app`

### Вариант 3: Netlify

1. **Создайте аккаунт на Netlify**
2. **Drag & Drop `index.html`**
3. **Получите URL вида:** `https://fitadventure-products.netlify.app`

## 🔧 Обновление URL в боте

После размещения Web App обновите URL в `main.py`:

```python
web_app_url = "https://ваш-username.github.io/fitadventure-products/"
```

## 📋 Функции Web App

- ✅ **Категории продуктов:**
  - 🌾 Сложные углеводы
  - ⚡ Простые углеводы
  - 🥩 Белки
  - 🫒 Ненасыщенные жиры
  - 🧈 Насыщенные жиры
  - 🌿 Клетчатка

- ✅ **Фильтрация по целям:**
  - Похудение
  - Набор массы
  - Поддержание

- ✅ **Поиск продуктов**
- ✅ **Детальная информация о БЖУ**
- ✅ **Интеграция с Telegram**

## 🚀 Быстрый старт

1. Создайте репозиторий на GitHub
2. Загрузите `index.html`
3. Включите GitHub Pages
4. Обновите URL в боте
5. Перезапустите бота

## 📞 Поддержка

Если возникли проблемы с размещением Web App, используйте обычную версию с кнопками (уже реализована в боте). 