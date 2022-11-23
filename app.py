from flask import Flask, jsonify, request, abort
import sqlite3
from random import randint
import json

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/question')
def getQuestionById():
    try:
        conn = get_db_connection()

        # получение числа количества вопросов в БД по указанному id_test
        id_test = request.args.get('id_test', type=int)
        count = conn.execute(
            f"SELECT COUNT(*) as count FROM questions WHERE id_test = {id_test}"
        ).fetchone()

        # получение вопроса по ид(если ид в запросе не указан, то он генерируется случайным образом)
        id = request.args.get('id', type=int, default=randint(1, count[0]))
        question = conn.execute(
            f"SELECT id, answer, question, description FROM questions WHERE id_test = {id_test} AND id = {id}").fetchone()
        conn.close()

        return jsonify({
            "id": question['id'],
            "answer": question['answer'],
            "question": question['question'],
            "description": question['description'],
        })
    except Exception:
        abort(400)

@app.route("/tests")
def getAllTests():
    conn = get_db_connection()
    # получение списка тестов из БД
    tests = conn.execute(
        f"SELECT id, name, description FROM tests").fetchall()
    conn.close()

    return json.dumps([dict(ix) for ix in tests])


if __name__ == '__main__':
    app.run(ssl_context='adhoc')
