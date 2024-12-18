# t12024

Анализ эффективности и здоровья спринтов на основе данных о состоянии задач

1.Задачи проекта
Создать программу, которая будет анализировать данные о различных спринтах, используя информацию о состоянии задач на таймлайне.

Приложение имеет следующие функции:
- Десктопный интерфейс с загрузкой заданного файла;
- Выбор спринта для анализа;
- Возможность посмотреть метрики здоровья спринта в различном промежутке времени этого спринта с помощью прокрутки таймлайна;
- Визуализация метрик как в цифровом виде, так и столбчатыми диаграммами;  
- Расчет качества спринта по выданным формулам с настраиваемыми параметрами;
- Возможность настройки границ отслеживаемых метрик;

2. Установка и запуск приложения
Приложение протестировано для Python версии 3.12.5.
Для установки зависимостей приложения создайте новое виртуальное окружение Python 3, активируйте его и выполните команду:
pip install -r requirements.txt

После этого приложение можно будет запустить командой:
`python3 main.py`

Или, при работе с *nix, командой:
`./main.py`

3. Работа с приложением

Основная работа с приложением производится через главное окно с четырьмя кнопками: добавление файла с командами, добавление файла с историей изменений, добавление файла со спринтами, анализ данных.

3.1 После добавления всех нужных фалов и дальнейшего нажатия кнопки анализа данных, появляется окно с таймлайном и визуализацией отчетов об эффективности и здоровье спринта.
