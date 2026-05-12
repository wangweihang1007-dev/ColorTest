import sqlite3
import re
import os
import json
from datetime import datetime

def parse_md_full(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean up content
    content = content.replace('\\', '')
    
    # 1. Parse Questions
    questions = []
    q_blocks = re.findall(r'(\d+)\.(.*?)\nA(.*?)\nB(.*?)\nC(.*?)\nD(.*?)\n', content, re.S)
    
    color_map = {
        '红色': 'red', '蓝色': 'blue', '黄色': 'yellow', '绿色': 'green'
    }
    
    for q_num, q_text, a, b, c, d in q_blocks:
        q_num = int(q_num)
        options = [
            {'label': 'A', 'text': a.strip()},
            {'label': 'B', 'text': b.strip()},
            {'label': 'C', 'text': c.strip()},
            {'label': 'D', 'text': d.strip()}
        ]
        
        # 1-15: A red, B blue, C yellow, D green
        # 16-30: A green, B yellow, C blue, D red
        if 1 <= q_num <= 15:
            mapping = ['red', 'blue', 'yellow', 'green']
        else:
            mapping = ['green', 'yellow', 'blue', 'red']
            
        for i in range(4):
            options[i]['color'] = mapping[i]
            
        questions.append({
            'id': q_num,
            'text': q_text.strip(),
            'options': options
        })
    
    # 2. Parse Personality Config
    configs = []
    # Pattern for color descriptions
    # Using a simpler split-based approach for the four colors
    color_sections = re.split(r'(红色|蓝色|黄色|绿色):', content)
    # color_sections[0] is intro, then [1]=color name, [2]=content, etc.
    for i in range(1, len(color_sections), 2):
        c_name = color_sections[i]
        c_text = color_sections[i+1].strip()
        
        # Extract title and description
        # Title is the color name + "人格"
        title = f"{c_name}人格"
        
        # Split advantages and disadvantages
        # This is a bit manual but based on the MD structure
        subtitle = ""
        if "优势" in c_text or "魅力" in c_text or "天赋" in c_text or "好处" in c_text:
            # Try to grab the first few descriptive words as subtitle
            subtitle_match = re.search(r'优势是：\n(.*?)\n', c_text)
            if not subtitle_match: subtitle_match = re.search(r'魅力在于：\n(.*?)\n', c_text)
            if not subtitle_match: subtitle_match = re.search(r'天赋：\n(.*?)\n', c_text)
            if not subtitle_match: subtitle_match = re.search(r'好处是：\n(.*?)\n', c_text)
            
            if subtitle_match:
                subtitle = subtitle_match.group(1).strip()
        
        configs.append({
            'color_type': color_map[c_name],
            'title': title,
            'subtitle': subtitle,
            'description': c_text
        })
        
    return questions, configs

def setup_db_v2(db_path, questions, configs):
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. question
    cursor.execute('''
    CREATE TABLE question (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        sort_order INTEGER DEFAULT 0,
        status INTEGER DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 2. question_option
    cursor.execute('''
    CREATE TABLE question_option (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        label TEXT NOT NULL,
        content TEXT NOT NULL,
        color_type TEXT NOT NULL,
        score_value INTEGER DEFAULT 1,
        sort_order INTEGER DEFAULT 0,
        FOREIGN KEY (question_id) REFERENCES question (id)
    )
    ''')
    cursor.execute('CREATE INDEX idx_option_question ON question_option(question_id)')
    
    # 3. personality_config
    cursor.execute('''
    CREATE TABLE personality_config (
        color_type TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        subtitle TEXT,
        description TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 4. user
    cursor.execute('''
    CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        openid TEXT UNIQUE NOT NULL,
        nickname TEXT,
        avatar_url TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 5. test_record
    cursor.execute('''
    CREATE TABLE test_record (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        answers_json TEXT,
        score_detail TEXT,
        final_color TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user (id)
    )
    ''')
    cursor.execute('CREATE INDEX idx_record_user ON test_record(user_id)')
    cursor.execute('CREATE INDEX idx_record_color ON test_record(final_color)')
    
    # Insert Data
    for q in questions:
        cursor.execute('INSERT INTO question (id, content, sort_order) VALUES (?, ?, ?)', 
                       (q['id'], q['text'], q['id']))
        for i, opt in enumerate(q['options']):
            cursor.execute('''
            INSERT INTO question_option (question_id, label, content, color_type, sort_order)
            VALUES (?, ?, ?, ?, ?)
            ''', (q['id'], opt['label'], opt['text'], opt['color'], i))
            
    for c in configs:
        cursor.execute('''
        INSERT INTO personality_config (color_type, title, subtitle, description)
        VALUES (?, ?, ?, ?)
        ''', (c['color_type'], c['title'], c['subtitle'], c['description']))
            
    conn.commit()
    conn.close()
    print(f"Database {db_path} has been successfully created with the new professional schema.")

if __name__ == "__main__":
    md_file = "docs/性格色彩测试题.md"
    db_file = "backend/color_test.db"
    
    if os.path.exists(md_file):
        qs, _ = parse_md_full(md_file)
        
        # Override with detailed, professional analysis
        cfgs = [
            {
                "color_type": "red",
                "title": "元气红色 - 快乐的带动者",
                "subtitle": "核心动机：快乐、表达、被认可",
                "description": "【性格概述】\n红色性格的人像阳光一样灿烂。你极具感染力，天生乐天派，总是能给周围的人带来欢乐。你擅长用生动的语言表达情感，是天生的外交家。\n\n【核心优势】\n1. 极强的社交能力：能快速与陌生人建立联系，打破僵局。\n2. 创造力丰富：思维跳跃，总能提出令人惊喜的创意。\n3. 乐观主义：面对困难时总能看到积极的一面。\n\n【性格局限】\n1. 情绪化严重：容易激动，也容易因琐事感到沮丧。\n2. 缺乏条理：在细节和长期规划上有所欠缺。\n3. 渴望赞美：过度依赖他人的认可。\n\n【发展建议】\n适合市场、公关、演艺等岗位。学会‘静心’和‘深度思考’是你成长的关键。"
            },
            {
                "color_type": "blue",
                "title": "睿智蓝色 - 完美的思想家",
                "subtitle": "核心动机：完美、秩序、深度",
                "description": "【性格概述】\n蓝色性格的人深邃如大海。你严谨、细腻、追求完美。你更喜欢独自思考而非在喧闹中社交，对真相有近乎执着的追求。\n\n【核心优势】\n1. 极致的严谨：计划无懈可击，细节处理极其到位。\n2. 忠诚可靠：一旦承诺，不计代价地去实现。\n3. 深度洞察：能看到现象背后的本质。\n\n【性格局限】\n1. 完美主义陷阱：过分纠结细节可能导致效率降低。\n2. 社交距离感：初次接触时常给人以冷漠、难接近的印象。\n3. 批判性过强：对自己和他人都有极高的标准。\n\n【发展建议】\n适合研发、法律、财会等精密领域。学会接受‘遗憾’和‘不完美’是人生的重要功课。"
            },
            {
                "color_type": "yellow",
                "title": "霸气黄色 - 强力的引领者",
                "subtitle": "核心动机：目标、控制、效率",
                "description": "【性格概述】\n黄色性格的人如同火焰。你目标明确，行动迅速，天生具备领导者气质。你不在乎他人的评价，只关注事情是否完成。\n\n【核心优势】\n1. 极强的执行力：行动派，从不拖泥带水。\n2. 决策果断：在混乱局面下能迅速做出决定。\n3. 意志坚定：不畏困难，越挫越勇。\n\n【性格局限】\n1. 攻击性较强：过于直接的表达方式有时会伤害他人。\n2. 固执己见：一旦认定目标，很难听进反对意见。\n3. 忽视情感：为了效率，可能会牺牲团队的情感需求。\n\n【发展建议】\n天生的管理人才和创业者。建议加强‘同理心’练习，平衡‘目标’与‘人心’。"
            },
            {
                "color_type": "green",
                "title": "平和绿色 - 稳定的和平鸽",
                "subtitle": "核心动机：平和、稳定、接纳",
                "description": "【性格概述】\n绿色性格的人像大地一样包容。你性格温和，是绝佳的倾听者。你追求生活的平衡与和谐，能给身边的人带来安全感。\n\n【核心优势】\n1. 情绪稳定：团队的润滑剂，能化解尴尬与冲突。\n2. 极强的包容心：能接纳不同性格的人，从不轻易评判。\n3. 可靠的后盾：在压力下依然能保持镇定。\n\n【性格局限】\n1. 优柔寡断：害怕做决定，担心引发不和谐。\n2. 缺乏主动性：倾向于维持现状，有时会错失良机。\n3. 压抑自我：为了迎合他人而牺牲自己的需求。\n\n【发展建议】\n适合人力资源、心理咨询、行政等领域。学会‘说不’和表达真实需求是你获得自由的第一步。"
            }
        ]
        
        setup_db_v2(db_file, qs, cfgs)
    else:
        print(f"Error: {md_file} not found.")
