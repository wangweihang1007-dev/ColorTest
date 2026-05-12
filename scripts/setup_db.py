import sqlite3
import re
import os

def parse_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract questions
    # Pattern: \n\d+\.(.*?)\n(A.*?)\n(B.*?)\n(C.*?)\n(D.*?)\n
    questions = []
    # Clean up the content a bit for easier regex matching
    content = content.replace('\\', '') # remove markdown backslashes
    
    q_blocks = re.findall(r'(\d+)\.(.*?)\nA(.*?)\nB(.*?)\nC(.*?)\nD(.*?)\n', content, re.S)
    
    for q_num, q_text, a, b, c, d in q_blocks:
        q_num = int(q_num)
        options = [
            {'label': 'A', 'text': a.strip()},
            {'label': 'B', 'text': b.strip()},
            {'label': 'C', 'text': c.strip()},
            {'label': 'D', 'text': d.strip()}
        ]
        
        # Assign colors based on the rules in the document
        # 1-15: A红, B蓝, C黄, D绿
        # 16-30: A绿, B黄, C蓝, D红
        if 1 <= q_num <= 15:
            options[0]['color'] = '红色'
            options[1]['color'] = '蓝色'
            options[2]['color'] = '黄色'
            options[3]['color'] = '绿色'
        else:
            options[0]['color'] = '绿色'
            options[1]['color'] = '黄色'
            options[2]['color'] = '蓝色'
            options[3]['color'] = '红色'
            
        questions.append({
            'id': q_num,
            'text': q_text.strip(),
            'options': options
        })
    
    return questions

def setup_db(db_path, questions):
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        question_text TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS options (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        label TEXT,
        option_text TEXT,
        color_attribute TEXT,
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )
    ''')
    
    # Insert data
    for q in questions:
        cursor.execute('INSERT INTO questions (id, question_text) VALUES (?, ?)', (q['id'], q['text']))
        for opt in q['options']:
            cursor.execute('''
            INSERT INTO options (question_id, label, option_text, color_attribute)
            VALUES (?, ?, ?, ?)
            ''', (q['id'], opt['label'], opt['text'], opt['color']))
            
    conn.commit()
    conn.close()
    print(f"Database {db_path} has been successfully created and populated with {len(questions)} questions.")

if __name__ == "__main__":
    md_file = "性格色彩测试题.md"
    db_file = "color_test.db"
    
    if os.path.exists(md_file):
        qs = parse_md(md_file)
        if qs:
            setup_db(db_file, qs)
        else:
            print("Failed to parse questions. Please check the markdown format.")
    else:
        print(f"Error: {md_file} not found.")
