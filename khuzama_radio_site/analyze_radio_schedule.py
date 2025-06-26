import docx
import re
import json
from collections import defaultdict
from datetime import datetime, timedelta

valid_names = [
    'محمد عبده', 'راشد الماجد', 'عبدالمجيد عبدالله', 'رابح صقر',
    'عبادي الجوهر', 'عبدالله الرويشد', 'طلال مداح', 'أحلام', 'نوال',
    'أنغام', 'أميمة', 'أصالة', 'داليا', 'فؤاد عبدالواحد', 'ماجد المهندس'
]

def extract_data_from_docx(path):
    doc = docx.Document(path)
    rows = []
    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            if len(cells) >= 4 and re.match(r'^\d{1,2}:\d{2}$', cells[0]):
                rows.append({
                    "time": cells[0],
                    "song": cells[1],
                    "duration": cells[2],
                    "artist": cells[3]
                })
    return rows

def is_valid_artist(name):
    return any(valid in name for valid in valid_names)

def analyze(rows):
    correct, incorrect = 0, 0
    parsed_rows = []
    artist_times = defaultdict(list)

    for row in rows:
        artist = row['artist']
        time = row['time']
        valid = is_valid_artist(artist)
        if valid:
            correct += 1
        else:
            incorrect += 1
        parsed_rows.append({**row, 'valid': valid})
        if valid:
            dt = datetime.strptime(time, "%H:%M")
            artist_times[artist].append(dt)

    repeated_in_hour = set()
    for artist, times in artist_times.items():
        times.sort()
        for i in range(1, len(times)):
            if times[i] - times[i - 1] <= timedelta(hours=1):
                repeated_in_hour.add((artist, times[i].strftime("%H:%M")))

    return {
        "correct": correct,
        "incorrect": incorrect,
        "rows": parsed_rows,
        "repeated_in_hour": list(repeated_in_hour)
    }