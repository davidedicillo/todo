from app import db, Todo

# first_todo = Todo(todo_text = 'Learn flask')
# db.session.add(first_todo)
# db.session.commit()

all_todo = Todo.query.all()
print(all_todo[0].todo_text)