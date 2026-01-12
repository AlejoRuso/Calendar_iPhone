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



Сохраненные стили:

Оформление:
{
  "display": {
    "width": 1320,
    "height": 2868
  },
  "layout": {
    "top_offset": 900,
    "day_radius": 13,
    
  
    "month_spacing_x": 40,
    "month_spacing_y": 0,
    
 
    "month_margin_x": 100,
    "month_margin_y": 250,
    

    "day_spacing_x": 50,
    "day_spacing_y": 40,
    

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
    "progress_text": "#918E8EFF"
  },
  "calendar": {
    "months": [
      " Янв", " Фев", " Мар", " Апр",
      " Май", " Июн", " Июл", " Авг",
      " Сен", " Окт", " Ноя", " Дек"
    ],
    "week_start": 0,
    "show_numbers": false,
    "month_text_align": "left"
  },
  "fonts": {
    "month_size": 46,
    "day_size": 20,
    "progress_size": 36
  },
  "progress": {
    "width_percent": 30,
    "height": 50,
    "margin": 100,
    "position": "center"
  },
  "highlighted_ranges": [
    {
      "date": "2026-01-13",
      "color": "#915803"
    }
  ],
  "output": "calendar.png"
}



"quote": {
  "enabled": true,
  "text": "Сегодня — идеальный день, чтобы сделать шаг к мечте",
  "quotes": [
    "Маленькие шаги каждый день приводят к большим результатам",
    "Успех — это сумма маленьких усилий, повторяющихся изо дня в день"
  ],
  "font_size": 42,
  "color": "#FFFFFF",
  "align": "center",
  
  // ПОЗИЦИОНИРОВАНИЕ ФРАЗЫ
  "position": "above_calendar",  // above_calendar, top_left, top_center, top_right
  
  // ВЕРТИКАЛЬНЫЕ НАСТРОЙКИ
  "margin_top": 40,       // Отступ от верха экрана до фразы
  "margin_bottom": 20,    // Минимальный зазор между фразой и месяцами
  
  // ГОРИЗОНТАЛЬНЫЕ НАСТРОЙКИ (ограничение текста)
  "margin_left": 60,      // Отступ текста от левого края экрана
  "margin_right": 60,     // Отступ текста от правого края экрана
  
  // АВТОМАТИЧЕСКИЕ НАСТРОЙКИ (рассчитываются автоматически)
  "max_width": 1200,      // Максимальная ширина текста (авто: ширина экрана - margin_left - margin_right)
  "line_height": 1.2      // Межстрочный интервал
  
  // ДОПОЛНИТЕЛЬНО
  "show_number": false    // Показывать номер фразы (например: "15/100")
}