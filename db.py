
import sqlite3
from datetime import datetime
from model import Todo

conn = sqlite3.connect('todos.db')
c = conn.cursor()

def creat_table():
    c.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        task text,
        category text,
        date_added text,
        date_completes text,
        status integer,
        position integer
    )
    
    """)
creat_table()

def insert_todo(todo: Todo):
    c.execute('select count(*) FROM todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        c.execute('INSERT INTO todos VALUES(:task, :category, :date_added, :date_completes, :status, :position)',
        {'task': todo.task,'category': todo.category,'date_added': todo.date_added,'date_completes': todo.date_completes,'status': todo.status,'position': todo.position})

def get_all_todos() -> list[Todo]:
    c.execute('select * from todos')
    results = c.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(*result))
    return todos

def delete_todo(position: int):
    c.execute('select count(*) from todos')
    count = c.fetchone()[0]

    with conn:
        c.execute("DELETE from todos WHERE position=:position", {"position": position})
        for pos in range(position+1, count):
            change_position(pos, pos-1, False)

def change_position(old_position: int, new_position: int, commit=True):
    c.execute("UPDATE todos set position = :position_new WHERE position= :position_old",
                {'position_old':old_position, 'position_new': new_position})
    if commit:
        conn.commit()

def update_todo(position: int, task: str, category: str):
    with conn:
        if task is not None and category is not None:
            c.execute("UPDATE todos set task = :task, category=:category WHERE position= :position",
                {'task':task, 'category': category, 'position': position})
        elif task is not None:
            c.execute("UPDATE todos set task = :task WHERE position= :position",
                {'task':task, 'position': position})
        elif category is not None:
            c.execute("UPDATE todos set  category=:category WHERE position= :position",
                {'category': category, 'position': position})

def complete_todo(position: int):
    with conn:
        c.execute("UPDATE todos set status = 2, date_completes=:date_completes WHERE position= :position",
                {'position': position, 'date_completes': datetime.now().isoformat()})