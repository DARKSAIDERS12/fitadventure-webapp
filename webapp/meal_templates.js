        // Шаблоны питания
        const MEAL_TEMPLATES = {
            "похудение": {
                "1200_калорий": {
                    "название": "Диета 1200 ккал",
                    "калории": 1200,
                    "описание": "Сбалансированная диета для похудения",
                    "продукты": {
                        "завтрак": [
                            { "название": "овсянка", "количество": 50, "категория": "сложные_углеводы" },
                            { "название": "яблоко", "количество": 100, "категория": "простые_углеводы" },
                            { "название": "миндаль", "количество": 10, "категория": "ненасыщенные_жиры" }
                        ],
                        "перекус": [
                            { "название": "творог обезжиренный", "количество": 100, "категория": "белки" },
                            { "название": "клубника", "количество": 50, "категория": "простые_углеводы" }
                        ],
                        "обед": [
                            { "название": "куриная грудка", "количество": 120, "категория": "белки" },
                            { "название": "гречка", "количество": 40, "категория": "сложные_углеводы" },
                            { "название": "брокколи", "количество": 150, "категория": "клетчатка" }
                        ],
                        "полдник": [
                            { "название": "йогурт греческий", "количество": 100, "категория": "белки" }
                        ],
                        "ужин": [
                            { "название": "рыба белая", "количество": 100, "категория": "белки" },
                            { "название": "салат латук", "количество": 100, "категория": "клетчатка" },
                            { "название": "оливковое масло", "количество": 5, "категория": "ненасыщенные_жиры" }
                        ]
                    }
                },
                "1500_калорий": {
                    "название": "Диета 1500 ккал",
                    "калории": 1500,
                    "описание": "Умеренная диета для похудения",
                    "продукты": {
                        "завтрак": [
                            { "название": "овсянка", "количество": 60, "категория": "сложные_углеводы" },
                            { "название": "банан", "количество": 80, "категория": "простые_углеводы" },
                            { "название": "миндаль", "количество": 15, "категория": "ненасыщенные_жиры" }
                        ],
                        "перекус": [
                            { "название": "творог 2%", "количество": 120, "категория": "белки" },
                            { "название": "яблоко", "количество": 100, "категория": "простые_углеводы" }
                        ],
                        "обед": [
                            { "название": "куриная грудка", "количество": 150, "категория": "белки" },
                            { "название": "рис бурый", "количество": 50, "категория": "сложные_углеводы" },
                            { "название": "брокколи", "количество": 200, "категория": "клетчатка" },
                            { "название": "оливковое масло", "количество": 8, "категория": "ненасыщенные_жиры" }
                        ],
                        "полдник": [
                            { "название": "йогурт греческий", "количество": 150, "категория": "белки" },
                            { "название": "орехи грецкие", "количество": 10, "категория": "ненасыщенные_жиры" }
                        ],
                        "ужин": [
                            { "название": "лосось", "количество": 120, "категория": "белки" },
                            { "название": "шпинат", "количество": 100, "категория": "клетчатка" },
                            { "название": "авокадо", "количество": 50, "категория": "ненасыщенные_жиры" }
                        ]
                    }
                }
            },
            "набор_массы": {
                "2500_калорий": {
                    "название": "Набор массы 2500 ккал",
                    "калории": 2500,
                    "описание": "Высококалорийная диета для набора массы",
                    "продукты": {
                        "завтрак": [
                            { "название": "овсянка", "количество": 80, "категория": "сложные_углеводы" },
                            { "название": "банан", "количество": 120, "категория": "простые_углеводы" },
                            { "название": "миндаль", "количество": 30, "категория": "ненасыщенные_жиры" },
                            { "название": "мед", "количество": 20, "категория": "простые_углеводы" }
                        ],
                        "перекус": [
                            { "название": "творог 5%", "количество": 150, "категория": "белки" },
                            { "название": "виноград", "количество": 100, "категория": "простые_углеводы" }
                        ],
                        "обед": [
                            { "название": "говядина постная", "количество": 200, "категория": "белки" },
                            { "название": "рис белый", "количество": 80, "категория": "сложные_углеводы" },
                            { "название": "брокколи", "количество": 150, "категория": "клетчатка" },
                            { "название": "оливковое масло", "количество": 15, "категория": "ненасыщенные_жиры" }
                        ],
                        "полдник": [
                            { "название": "протеин сывороточный", "количество": 30, "категория": "белки" },
                            { "название": "банан", "количество": 100, "категория": "простые_углеводы" }
                        ],
                        "ужин": [
                            { "название": "лосось", "количество": 150, "категория": "белки" },
                            { "название": "картофель", "количество": 200, "категория": "сложные_углеводы" },
                            { "название": "шпинат", "количество": 100, "категория": "клетчатка" }
                        ],
                        "перед_сном": [
                            { "название": "творог 5%", "количество": 100, "категория": "белки" },
                            { "название": "орехи грецкие", "количество": 20, "категория": "ненасыщенные_жиры" }
                        ]
                    }
                }
            },
            "поддержание": {
                "2000_калорий": {
                    "название": "Поддержание 2000 ккал",
                    "калории": 2000,
                    "описание": "Сбалансированная диета для поддержания веса",
                    "продукты": {
                        "завтрак": [
                            { "название": "овсянка", "количество": 60, "категория": "сложные_углеводы" },
                            { "название": "яблоко", "количество": 100, "категория": "простые_углеводы" },
                            { "название": "миндаль", "количество": 20, "категория": "ненасыщенные_жиры" }
                        ],
                        "перекус": [
                            { "название": "творог 5%", "количество": 100, "категория": "белки" },
                            { "название": "груша", "количество": 100, "категория": "простые_углеводы" }
                        ],
                        "обед": [
                            { "название": "куриная грудка", "количество": 150, "категория": "белки" },
                            { "название": "гречка", "количество": 60, "категория": "сложные_углеводы" },
                            { "название": "брокколи", "количество": 150, "категория": "клетчатка" },
                            { "название": "оливковое масло", "количество": 10, "категория": "ненасыщенные_жиры" }
                        ],
                        "полдник": [
                            { "название": "йогурт греческий", "количество": 100, "категория": "белки" },
                            { "название": "орехи грецкие", "количество": 15, "категория": "ненасыщенные_жиры" }
                        ],
                        "ужин": [
                            { "название": "рыба белая", "количество": 120, "категория": "белки" },
                            { "название": "шпинат", "количество": 100, "категория": "клетчатка" },
                            { "название": "авокадо", "количество": 50, "категория": "ненасыщенные_жиры" }
                        ]
                    }
                }
            }
        };

        // Функции для работы с шаблонами
        function getTemplatesByGoal(goal) {
            return MEAL_TEMPLATES[goal] || {};
        }

        function applyTemplateToMealPlanner(templateKey, goal) {
            const templates = getTemplatesByGoal(goal);
            const template = templates[templateKey];
            if (!template) {
                console.error("Шаблон не найден:", templateKey);
                return false;
            }

            // Очищаем текущий план питания
            clearMealPlan();

            // Добавляем продукты из шаблона
            for (const mealType in template.продукты) {
                const products = template.продукты[mealType];
                for (const product of products) {
                    addProductToMealFromTemplate(
                        product.название,
                        product.количество,
                        mealType,
                        goal,
                        product.категория
                    );
                }
            }

            // Обновляем отображение
            updateMealPlanDisplay();
            return true;
        }

        function clearMealPlan() {
            const mealTypes = ["завтрак", "перекус", "обед", "полдник", "ужин", "перед_сном"];
            mealTypes.forEach(mealType => {
                const container = document.getElementById(`${mealType}-products`);
                if (container) {
                    container.innerHTML = "";
                }
            });

            // Очищаем localStorage
            mealTypes.forEach(mealType => {
                localStorage.removeItem(`meal_plan_${mealType}`);
            });
        }

        function addProductToMealFromTemplate(productName, quantity, mealType, goal, category) {
            // Получаем информацию о продукте из базы данных
            const productInfo = getProductInfo(productName, goal, category);
            if (!productInfo) {
                console.error("Продукт не найден:", productName);
                return false;
            }

            // Создаем объект продукта для планировщика
            const product = {
                name: productName,
                quantity: quantity,
                calories: Math.round((productInfo.калории * quantity) / 100),
                proteins: Math.round((productInfo.белки * quantity) / 100 * 10) / 10,
                fats: Math.round((productInfo.жиры * quantity) / 100 * 10) / 10,
                carbs: Math.round((productInfo.углеводы * quantity) / 100 * 10) / 10,
                fiber: Math.round((productInfo.клетчатка * quantity) / 100 * 10) / 10,
                description: productInfo.описание
            };

            // Добавляем в localStorage
            const existingProducts = JSON.parse(localStorage.getItem(`meal_plan_${mealType}`) || "[]");
            existingProducts.push(product);
            localStorage.setItem(`meal_plan_${mealType}`, JSON.stringify(existingProducts));

            return true;
        }

        function getProductInfo(productName, goal, category) {
            if (typeof productsDatabase !== "undefined" && productsDatabase[goal] && productsDatabase[goal][category]) {
                return productsDatabase[goal][category][productName];
            }
            return null;
        }

        function updateMealPlanDisplay() {
            const mealTypes = ["завтрак", "перекус", "обед", "полдник", "ужин", "перед_сном"];
            mealTypes.forEach(mealType => {
                const container = document.getElementById(`${mealType}-products`);
                if (!container) return;

                const products = JSON.parse(localStorage.getItem(`meal_plan_${mealType}`) || "[]");
                container.innerHTML = "";

                products.forEach((product, index) => {
                    const productDiv = document.createElement("div");
                    productDiv.className = "product-item";
                    productDiv.innerHTML = `
                        <div class="product-info">
                            <span class="product-name">${product.name}</span>
                            <span class="product-quantity">${product.quantity}г</span>
                        </div>
                        <div class="product-macros">
                            <span class="calories">${product.calories}ккал</span>
                            <span class="macros">Б:${product.proteins}г | Ж:${product.fats}г | У:${product.carbs}г</span>
                        </div>
                    `;
                    container.appendChild(productDiv);
                });
            });
        }

        function loadMealTemplates() {
            const templates = getTemplatesByGoal(currentGoal);
            const templatesList = document.getElementById('templatesList');
            if (!templatesList) return;

            templatesList.innerHTML = '';
            
            for (const [key, template] of Object.entries(templates)) {
                const templateDiv = document.createElement('div');
                templateDiv.className = 'template-item';
                templateDiv.innerHTML = `
                    <div class="template-info">
                        <h4>${template.название}</h4>
                        <p>${template.описание}</p>
                        <span class="template-calories">${template.калории} ккал</span>
                    </div>
                    <button onclick="applyTemplate('${currentGoal}', '${key}')" class="apply-template-btn">
                        Применить
                    </button>
                `;
                templatesList.appendChild(templateDiv);
            }
        }

        function applyTemplate(goal, templateKey) {
            if (applyTemplateToMealPlanner(templateKey, goal)) {
                alert(`Шаблон "${templateKey}" успешно применен!`);
                closeMealPlanner();
            } else {
                alert('Ошибка при применении шаблона');
            }
        }
