from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Feedback, Book
from app import db
import bleach

comments_bp = Blueprint('comments', __name__, url_prefix='/comments')

@comments_bp.route('/<int:book_id>', methods=['GET', 'POST'])
@login_required
def comment_post(book_id):
    comment = db.session.query(Feedback).filter(Feedback.book_id == book_id, Feedback.user_id == current_user.id).scalar()
    book = db.session.query(Book).filter(Book.id == book_id).scalar()
    
    if comment:
        flash("Можно добавить только одну рецензию", "warning")
        return redirect(url_for('show', book_id=book_id))
    
    if request.method == 'POST':
        mark = request.form.get('mark')
        short_desc = request.form.get('short_desc')
        
        # Проверяем, чтобы все необходимые данные были переданы
        if mark is None or short_desc is None:
            flash('Все поля должны быть заполнены.', 'danger')
            return redirect(url_for('comments.comment_post', book_id=book_id))
        
        try:
            score = int(mark)
        except ValueError:
            flash('Некорректное значение для оценки.', 'danger')
            return redirect(url_for('comments.comment_post', book_id=book_id))
        
        params = {
            "score": score,
            "comment": bleach.clean(short_desc),
            "user_id": current_user.id,
            "book_id": book_id
        }
        
        try:
            comment = Feedback(**params)
            db.session.add(comment)
            book.total_ratings = book.total_ratings + score
            book.ratings_count = book.ratings_count + 1
            db.session.commit()
            flash("Рецензия успешно добавлена", "success")
            return redirect(url_for('show', book_id=book_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении рецензии: {str(e)}', "danger")
            return redirect(url_for('comments.comment_post', book_id=book_id))
    
    return render_template('comment_post.html', book_id=book_id)
