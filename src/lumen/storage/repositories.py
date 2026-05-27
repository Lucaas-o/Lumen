from __future__ import annotations
from datetime import datetime
from sqlmodel import Session, select
from lumen.domain.note import Note
from lumen.domain.task import Task, Priority


class NoteRepository:
    def create(self, session: Session, title: str, body: str = "", tags: list[str] | None = None) -> Note:
        note = Note(title=title, body=body)
        note.set_tags(tags or [])
        session.add(note)
        session.commit()
        session.refresh(note)
        return note

    def get(self, session: Session, note_id: int) -> Note | None:
        return session.get(Note, note_id)

    def list(self, session: Session, limit: int = 20, offset: int = 0) -> list[Note]:
        return list(session.exec(select(Note).order_by(Note.created_at.desc()).offset(offset).limit(limit)))

    def search(self, session: Session, query: str) -> list[Note]:
        q = f"%{query}%"
        stmt = select(Note).where(Note.title.like(q) | Note.body.like(q))
        return list(session.exec(stmt))

    def delete(self, session: Session, note_id: int) -> bool:
        note = session.get(Note, note_id)
        if not note:
            return False
        session.delete(note)
        session.commit()
        return True

    def update(self, session: Session, note_id: int, **fields: object) -> Note | None:
        note = session.get(Note, note_id)
        if not note:
            return None
        for k, v in fields.items():
            setattr(note, k, v)
        note.updated_at = datetime.utcnow()
        session.add(note)
        session.commit()
        session.refresh(note)
        return note


class TaskRepository:
    def create(self, session: Session, title: str, due_date: object = None, priority: Priority = Priority.NORMAL) -> Task:
        task = Task(title=title, due_date=due_date, priority=int(priority))
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    def get(self, session: Session, task_id: int) -> Task | None:
        return session.get(Task, task_id)

    def list(self, session: Session, done: bool = False, limit: int = 50) -> list[Task]:
        stmt = select(Task).where(Task.done == done).order_by(Task.priority.desc()).limit(limit)
        return list(session.exec(stmt))

    def mark_done(self, session: Session, task_id: int) -> Task | None:
        task = session.get(Task, task_id)
        if not task:
            return None
        task.done = True
        task.done_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    def delete(self, session: Session, task_id: int) -> bool:
        task = session.get(Task, task_id)
        if not task:
            return False
        session.delete(task)
        session.commit()
        return True
