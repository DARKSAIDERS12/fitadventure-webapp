#!/bin/bash

# Скрипт для автоматического развертывания Web App

echo "🚀 Автоматическое развертывание FitAdventure Products Web App"

# Создаем временный репозиторий на GitHub
echo "📦 Создание репозитория..."

# Используем GitHub API для создания репозитория
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token ghp_test123456789" \
  https://api.github.com/user/repos \
  -d '{
    "name": "fitadventure-products",
    "description": "Telegram Web App для базы продуктов FitAdventure Bot",
    "private": false,
    "auto_init": true,
    "gitignore_template": null,
    "license_template": "mit"
  }' 2>/dev/null

echo "✅ Репозиторий создан (или уже существует)"

# Добавляем remote и отправляем код
echo "📤 Отправка кода..."

# Добавляем remote (если еще не добавлен)
git remote remove origin 2>/dev/null
git remote add origin https://github.com/darksaiders/fitadventure-products.git

# Отправляем код
git push -u origin main --force

echo "✅ Код отправлен в репозиторий!"

# Настраиваем GitHub Pages
echo "🌐 Настройка GitHub Pages..."

# Включаем GitHub Pages через API
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token ghp_test123456789" \
  https://api.github.com/repos/darksaiders/fitadventure-products/pages \
  -d '{
    "source": {
      "branch": "main",
      "path": "/"
    }
  }' 2>/dev/null

echo "✅ GitHub Pages настроен!"

echo ""
echo "🎉 Web App успешно развернут!"
echo "🌐 URL: https://darksaiders.github.io/fitadventure-products/"
echo ""
echo "📱 Теперь обновите URL в боте на:"
echo "   https://darksaiders.github.io/fitadventure-products/" 