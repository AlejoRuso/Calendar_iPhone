{
  "display": {
    "width": 1320,
    "height": 2868
  },
  "layout": {
    "top_offset": 300,
    "day_radius": 22,
    
    // ОТСТУПЫ МЕЖДУ МЕСЯЦАМИ
    "month_spacing_x": 30,  // Горизонтальное расстояние между месяцами
    "month_spacing_y": 40,  // Вертикальное расстояние между месяцами
    
    // ОТСТУПЫ ОТ КРАЕВ ЭКРАНА ДО СЕТКИ МЕСЯЦЕВ
    "month_margin_x": 40,   // Горизонтальный отступ от краев экрана
    "month_margin_y": 20,   // Вертикальный отступ от верха календаря (после top_offset)
    
    // РАССТОЯНИЯ МЕЖДУ КРУЖКАМИ
    "day_spacing_x": 50,    // Горизонтальное расстояние между центрами кружков
    "day_spacing_y": 50,    // Вертикальное расстояние между центрами кружков
    
    // ОТСТУПЫ СЕТКИ КРУЖКОВ ВНУТРИ МЕСЯЦА
    "day_grid_padding_x": 20,  // Горизонтальный отступ кружков от краев месяца
    "day_grid_padding_y": 80   // Вертикальный отступ кружков от названия месяца
  },
  "colors": {
    "background": "#000000",
    "month_text": "#FFFFFF",
    "future_day": "#333333",
    "past_day": "#FFFFFF",
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
    "show_numbers": false,
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