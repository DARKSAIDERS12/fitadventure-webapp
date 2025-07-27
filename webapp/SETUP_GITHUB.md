# 🚀 Настройка GitHub репозитория

## 📋 Шаги для создания репозитория:

1. **Откройте GitHub.com**
2. **Нажмите "+" → "New repository"**
3. **Настройки репозитория:**
   - Repository name: `fitadventure-products`
   - Description: `Telegram Web App для базы продуктов FitAdventure Bot`
   - Public (публичный)
   - ✅ Add a README file
   - ✅ Add .gitignore: None
   - ✅ Choose a license: MIT License

4. **Нажмите "Create repository"**

## 🔗 После создания репозитория:

```bash
# Добавьте удаленный репозиторий
git remote add origin https://github.com/darksaiders/fitadventure-products.git

# Отправьте код
git push -u origin main
```

## ⚙️ Настройка GitHub Pages:

1. **Перейдите в Settings репозитория**
2. **Найдите раздел "Pages"**
3. **Source: Deploy from a branch**
4. **Branch: main**
5. **Folder: / (root)**
6. **Нажмите "Save"**

## 🌐 Результат:

После настройки Web App будет доступен по адресу:
`https://darksaiders.github.io/fitadventure-products/`

## 🔧 Обновление бота:

После получения URL обновите `main.py`:

```python
web_app_url = "https://darksaiders.github.io/fitadventure-products/"
``` 