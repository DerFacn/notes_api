from flask import request, jsonify
from app.models import Note
from app.db import session
from app.utils import login_required


@login_required
def get_one(user, note_id):
    note = session.query(Note).filter_by(id=note_id).first()
    if not note:
        return jsonify(message='Note not founded!'), 404
    if note.user_uuid != user.uuid:
        return jsonify(message='Note not founded!'), 404
    return jsonify(id=note.id, text=note.text), 200


@login_required
def get_all(user):
    notes = session.query(Note).filter(Note.user_uuid == user.uuid).all()
    response = [{"id": note.id, "text": note.text} for note in notes]
    return jsonify(response), 200


@login_required
def create(user):
    text = request.json.get('text', None)
    if not text:
        return jsonify(message='Text is required!'), 409
    note = Note(user_uuid=user.uuid, text=text)
    session.add(note)
    session.commit()
    return jsonify(message='Note successfully created!', note={"id": note.id, "text": note.text}), 201


@login_required
def update(user, note_id):
    note = session.query(Note).filter_by(id=note_id).first()
    if not note:
        return jsonify(message='Note not founded!'), 404
    if note.user_uuid != user.uuid:
        return jsonify(message='Note not founded!'), 404
    text = request.json.get('text', None)
    note.text = text
    session.commit()
    return jsonify(message='Note updated!', note={"id": note.id, "text": note.text}), 200


@login_required
def delete(user, note_id):
    note = session.query(Note).filter_by(id=note_id).first()
    if not note:
        return jsonify(message='Note not founded!'), 404
    if note.user_uuid != user.uuid:
        return jsonify(message='Note not founded!'), 404
    session.delete(note)
    session.commit()
    return jsonify(message='Note deleted!'), 200
