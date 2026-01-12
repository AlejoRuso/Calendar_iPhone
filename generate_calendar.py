#!/usr/bin/env python3
"""
Генератор прогрессивного календаря для iPhone
Конфигурация в файле config.json
"""

import json
import os
from datetime import datetime, date, timedelta
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Tuple, Optional
import math

class CalendarGenerator:
    def __init__(self, config_path: str = "config.json"):
        """Инициализация с конфигурационным файлом"""
        if not os.path.exists(config_path):
            print("⚠ Конфиг не найден, создаю файл config.json")
            self.create_default_config()
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.validate_and_apply_config()
        self.today = date.today()
        self.year = self.config.get('year', self.today.year)
        self.calculate_progress()
        
        print(f"✓ Загружен конфиг из {config_path}")
        print(f"✓ Отступы месяцев: {self.month_spacing_x}px по горизонтали, {self.month_spacing_y}px по вертикали")
        print(f"✓ Расстояние между кружками: {self.day_spacing_x}px по горизонтали, {self.day_spacing_y}px по вертикали")
    
    def validate_and_apply_config(self):
        """Валидация и применение конфига"""
        self.width = self.config['display']['width']
        self.height = self.config['display']['height']
        self.top_offset = self.config['layout']['top_offset']
        
        # Отступы между месяцами
        self.month_spacing_x = self.config['layout'].get('month_spacing_x', 30)
        self.month_spacing_y = self.config['layout'].get('month_spacing_y', 40)
        
        # Отступы от краев экрана до сетки месяцев
        self.month_margin_x = self.config['layout'].get('month_margin_x', 40)
        self.month_margin_y = self.config['layout'].get('month_margin_y', 20)
        
        # Параметры расположения кружков
        self.day_radius = self.config['layout']['day_radius']
        
        # Расстояния между кружками (между центрами)
        self.day_spacing_x = self.config['layout'].get('day_spacing_x', 50)
        self.day_spacing_y = self.config['layout'].get('day_spacing_y', 50)
        
        # Отступы сетки кружков внутри месяца
        self.day_grid_padding_x = self.config['layout'].get('day_grid_padding_x', 20)
        self.day_grid_padding_y = self.config['layout'].get('day_grid_padding_y', 80)
        
        # Цвета
        self.colors = self.config['colors']
        
        # Настройки календаря
        self.months = self.config['calendar']['months']
        self.week_start = self.config['calendar']['week_start']
        self.show_numbers = self.config['calendar'].get('show_numbers', False)
        self.month_text_align = self.config['calendar'].get('month_text_align', 'left')
        
        # Настройки прогресс-бара
        self.progress_width_percent = self.config['progress'].get('width_percent', 30)
        self.progress_height = self.config['progress'].get('height', 40)
        self.progress_margin = self.config['progress'].get('margin', 20)
        self.progress_position = self.config['progress'].get('position', 'center')
        
        # Дни для выделения
        self.highlighted_dates = []
        for date_range in self.config.get('highlighted_ranges', []):
            if 'date' in date_range:
                d = datetime.strptime(date_range['date'], '%Y-%m-%d').date()
                self.highlighted_dates.append({
                    'start': d, 'end': d, 'color': date_range['color']
                })
            else:
                start = datetime.strptime(date_range['start'], '%Y-%m-%d').date()
                end = datetime.strptime(date_range['end'], '%Y-%m-%d').date()
                self.highlighted_dates.append({
                    'start': start, 'end': end, 'color': date_range['color']
                })
    
    def calculate_progress(self):
        """Расчет прогресса года"""
        start_of_year = date(self.year, 1, 1)
        end_of_year = date(self.year, 12, 31)
        
        self.total_days = (end_of_year - start_of_year).days + 1
        
        if self.today.year == self.year:
            days_passed = (self.today - start_of_year).days + 1
        elif self.today.year > self.year:
            days_passed = self.total_days  # Год завершен
        else:
            days_passed = 0  # Год еще не начался
        
        self.progress_percent = round((days_passed / self.total_days) * 100, 1)
        self.days_passed = days_passed
    
    def get_day_color(self, day_date: date) -> str:
        """Определение цвета для конкретного дня"""
        # Проверяем выделенные диапазоны
        for date_range in self.highlighted_dates:
            if date_range['start'] <= day_date <= date_range['end']:
                return date_range['color']
        
        # Текущий день
        if day_date == self.today:
            return self.colors['current_day']
        
        # Прошедшие дни
        if day_date < self.today:
            return self.colors['past_day']
        
        # Будущие дни
        return self.colors['future_day']
    
    def draw_month(self, draw: ImageDraw, month_idx: int, 
                   x0: int, y0: int, width: int, height: int):
        """Отрисовка одного месяца с настраиваемыми расстояниями"""
        # Название месяца
        month_name = self.months[month_idx]
        try:
            font = ImageFont.truetype("arial.ttf", 
                                     self.config['fonts']['month_size'])
        except:
            font = ImageFont.load_default()
        
        # Выравнивание названия месяца
        if self.month_text_align == 'center':
            text_x = x0 + width // 2
            anchor = "mm"
        elif self.month_text_align == 'right':
            text_x = x0 + width - 20
            anchor = "rm"
        else:  # left (default)
            text_x = x0 + 20
            anchor = "lm"
        
        draw.text(
            (text_x, y0 + 40),
            month_name,
            fill=self.colors['month_text'],
            font=font,
            anchor=anchor
        )
        
        # Параметры сетки дней
        cols = 7  # дней в неделе
        rows = 6  # максимальное количество недель в месяце
        
        # Вычисляем начальную позицию сетки кружков
        grid_start_x = x0 + self.day_grid_padding_x
        grid_start_y = y0 + self.day_grid_padding_y
        
        # Рассчитываем общую ширину и высоту сетки
        total_grid_width = (cols - 1) * self.day_spacing_x + 2 * self.day_radius
        total_grid_height = (rows - 1) * self.day_spacing_y + 2 * self.day_radius
        
        # Центрируем сетку, если она меньше ширины месяца
        if total_grid_width < (width - 2 * self.day_grid_padding_x):
            grid_start_x = x0 + (width - total_grid_width) // 2
        
        # Первый день месяца
        try:
            month_date = date(self.year, month_idx + 1, 1)
        except ValueError:
            return
        
        # Количество дней в месяце
        if month_idx == 11:
            next_month = date(self.year + 1, 1, 1)
        else:
            next_month = date(self.year, month_idx + 2, 1)
        
        days_in_month = (next_month - month_date).days
        
        # День недели первого дня месяца (0-понедельник)
        first_weekday = month_date.weekday()
        
        # Корректировка для начала недели
        if self.week_start > 0:
            first_weekday = (first_weekday - self.week_start) % 7
        
        # Рисуем дни
        for day in range(1, days_in_month + 1):
            current_date = date(self.year, month_idx + 1, day)
            
            # Определяем позицию в сетке
            day_of_month = day - 1
            adjusted_day = day_of_month + first_weekday
            
            col = adjusted_day % cols
            row = adjusted_day // cols
            
            # Центр кружка
            center_x = grid_start_x + self.day_radius + col * self.day_spacing_x
            center_y = grid_start_y + self.day_radius + row * self.day_spacing_y
            
            # Получаем цвет дня
            color = self.get_day_color(current_date)
            
            # Рисуем кружок
            draw.ellipse(
                [
                    center_x - self.day_radius,
                    center_y - self.day_radius,
                    center_x + self.day_radius,
                    center_y + self.day_radius
                ],
                fill=color
            )
            
            # Рисуем числа (если включено)
            if self.show_numbers:
                try:
                    day_font = ImageFont.truetype("arial.ttf", 
                                                self.config['fonts']['day_size'])
                except:
                    day_font = ImageFont.load_default()
                
                # Определяем цвет текста в зависимости от фона
                if color in ['#90EE90', '#4CAF50', "#915803", '#2196F3', '#F44336']:
                    text_color = 'white'
                else:
                    text_color = 'black'
                
                draw.text(
                    (center_x, center_y),
                    str(day),
                    fill=text_color,
                    font=day_font,
                    anchor="mm"
                )
    
    def draw_progress(self, draw: ImageDraw, y_position: int):
        """Отрисовка прогресс-бара"""
        # Рассчитываем ширину прогресс-бара (30% от ширины экрана)
        bar_width = int(self.width * (self.progress_width_percent / 100))
        
        # Определяем позицию по горизонтали
        if self.progress_position == 'left':
            bar_x = self.progress_margin
        elif self.progress_position == 'right':
            bar_x = self.width - bar_width - self.progress_margin
        else:  # center (default)
            bar_x = (self.width - bar_width) // 2
        
        bar_y = y_position
        
        # Фон прогресс-бара
        draw.rectangle(
            [bar_x, bar_y, bar_x + bar_width, bar_y + self.progress_height],
            fill=self.colors['progress_background']
        )
        
        # Заполненная часть
        filled_width = int(bar_width * (self.progress_percent / 100))
        draw.rectangle(
            [bar_x, bar_y, bar_x + filled_width, bar_y + self.progress_height],
            fill=self.colors['progress_fill']
        )
        
        # Текст прогресса
        try:
            font = ImageFont.truetype("arial.ttf", 
                                     self.config['fonts']['progress_size'])
        except:
            font = ImageFont.load_default()
        
        progress_text = f"{self.progress_percent}%"
        text_bbox = draw.textbbox((0, 0), progress_text, font=font)
        text_height = text_bbox[3] - text_bbox[1]
        
        # Позиция текста справа от прогресс-бара
        text_x = bar_x + bar_width + 10
        text_y = bar_y + (self.progress_height - text_height) // 2
        
        draw.text(
            (text_x, text_y),
            progress_text,
            fill=self.colors['progress_text'],
            font=font
        )
    
    def calculate_month_dimensions(self):
        """Расчет размеров и положения месяцев с учетом отступов"""
        cols = 3
        rows = 4
        
        # Высота календаря (без прогресс-бара)
        calendar_height = self.height - self.top_offset - 150
        
        # Доступная ширина после отступов
        available_width = self.width - 2 * self.month_margin_x - (cols - 1) * self.month_spacing_x
        available_height = calendar_height - 2 * self.month_margin_y - (rows - 1) * self.month_spacing_y
        
        # Ширина и высота одного месяца
        month_width = available_width // cols
        month_height = available_height // rows
        
        return cols, rows, month_width, month_height
    
    def generate(self) -> str:
        """Генерация полного изображения календаря"""
        # Создаем изображение
        image = Image.new('RGB', (self.width, self.height), 
                         color=self.colors['background'])
        draw = ImageDraw.Draw(image)
        
        # Рассчитываем размеры месяцев
        cols, rows, month_width, month_height = self.calculate_month_dimensions()
        
        # Рисуем месяцы
        for i in range(12):
            col = i % cols
            row = i // cols
            
            # Позиция месяца с учетом отступов
            x0 = self.month_margin_x + col * (month_width + self.month_spacing_x)
            y0 = self.top_offset + self.month_margin_y + row * (month_height + self.month_spacing_y)
            
            self.draw_month(draw, i, x0, y0, month_width, month_height)
        
        # Рисуем прогресс-бар
        progress_y = self.height - 120
        self.draw_progress(draw, progress_y)
        
        # Сохраняем изображение
        output_path = self.config.get('output', 'calendar.png')
        image.save(output_path, "PNG")
        
        print(f"✓ Изображение сохранено: {output_path}")
        print(f"✓ Прогресс: {self.days_passed}/{self.total_days} дней ({self.progress_percent}%)")
        print(f"✓ Размер месяца: {month_width}x{month_height} пикселей")
        
        return output_path
    
    def create_default_config(self):
        """Создание конфигурационного файла по умолчанию"""
        config = {
            "display": {
                "width": 1320,
                "height": 2868
            },
            "layout": {
                "top_offset": 300,
                "day_radius": 22,
                # Отступы между месяцами
                "month_spacing_x": 30,
                "month_spacing_y": 40,
                # Отступы от краев экрана до сетки месяцев
                "month_margin_x": 40,
                "month_margin_y": 20,
                # Расстояния между кружками
                "day_spacing_x": 50,
                "day_spacing_y": 50,
                # Отступы сетки кружков внутри месяца
                "day_grid_padding_x": 20,
                "day_grid_padding_y": 80
            },
            "colors": {
                "background": "#000000",
                "month_text": "#918E8EFF",
                "future_day": "#333333",
                "past_day": "#918E8EFF",
                "current_day": "#90EE90",
                "progress_background": "#333333",
                "progress_fill": "#4CAF50",
                "progress_text": "#FFFFFF"
            },
            "calendar": {
                "months": [
                    "Январь", "Февраль", "Март", "Апрель",
                    "Май", "Июнь", "Июль", "Август",
                    "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
                ],
                "week_start": 0,
                "show_numbers": False,
                "month_text_align": "left"
            },
            "fonts": {
                "month_size": 48,
                "day_size": 20,
                "progress_size": 36
            },
            "progress": {
                "width_percent": 30,
                "height": 40,
                "margin": 20,
                "position": "center"
            },
            "highlighted_ranges": [],
            "output": "calendar.png"
        }
        
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✓ Создан config.json с настройками по умолчанию")
        return config

def main():
    """Основная функция"""
    generator = CalendarGenerator()
    output_file = generator.generate()
    
    # Для GitHub Pages: создаем редирект на изображение
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url={output_file}">
    <title>Calendar</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #000;
        }}
        img {{
            display: block;
            margin: 0 auto;
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    <img src="{output_file}" alt="Calendar Progress">
</body>
</html>""")
    
    print(f"✓ HTML страница создана: index.html")
    print(f"✓ Для использования в автоматизации: https://alejoruso.github.io/Calendar_iPhone/calendar.png")

if __name__ == "__main__":
    main()