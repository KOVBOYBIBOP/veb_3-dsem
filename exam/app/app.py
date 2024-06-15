import math
from flask import Flask, flash, make_response, redirect, render_template, request, send_from_directory, url_for
from sqlalchemy import MetaData, desc, func
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
import bleach
import markdown
from datetime import datetime
import os

app = Flask(__name__, static_url_path='/static')
application = app

# Конфигурация приложения
app.config.from_pyfile('config.py')

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

PERMITTED_FIELDS = ["title", "description", "publication_year", "publisher", "writer", "pages", "cover_image"]

from auth import auth_blueprint, init_auth_manager, authorize_user
from comments import comments_blueprint
from tools import FileSaver
from models import File, Book, Category, Feedback

app.register_blueprint(auth_blueprint)
app.register_blueprint(comments_blueprint)

init_auth_manager(app)

@app.route('/')
def home():
    current_page = request.args.get('page', 1, type=int)
    per_page = app.config['PER_PAGE']
    book_info = []
    query = db.session.query(Book)

    # Параметры поиска
    search_title = request.args.get('title')
    search_genres = request.args.getlist('genre')
    search_years = request.args.getlist('year')
    search_author = request.args.get('author')
    search_volume_from = request.args.get('volume_from')
    search_volume_to = request.args.get('volume_to')

    if search_title:
        query = query.filter(Book.title.ilike(f'%{search_title}%'))
    if search_genres:
        query = query.join(Book.categories).filter(Category.id.in_(search_genres))
    if search_years:
        query = query.filter(Book.publication_year.in_(search_years))
    if search_author:
        query = query.filter(Book.writer.ilike(f'%{search_author}%'))
    if search_volume_from:
        query = query.filter(Book.pages >= int(search_volume_from))
    if search_volume_to:
        query = query.filter(Book.pages <= int(search_volume_to))

    total_books = query.count()
    books = query.order_by(desc(Book.publication_year)).limit(per_page).offset(per_page * (current_page - 1)).all()
    
    for book in books:
        book_details = {
            'book': book,
            'categories': book.categories,
        }
        book_info.append(book)

    total_pages = math.ceil(total_books / per_page)
    
    all_categories = db.session.query(Category).all()
    all_years = db.session.query(Book.publication_year).distinct().all()

    return render_template(
        'index.html',
        books=book_info,
        page=current_page,
        total_pages=total_pages,
        categories=all_categories,
        years=[year[0] for year in all_years],
        search_params=request.args
    )

@app.route('/media/images/<image_id>')
def serve_image(image_id):
    image_file = db.session.query(File).filter_by(id=image_id).first_or_404()
    return send_from_directory(app.config['UPLOAD_FOLDER'], image_file.storage_filename)

def extract_params(field_list):
    parameters = {}
    for field in field_list:
        parameters[field] = request.form.get(field) or None
    return parameters

@app.route('/books/new')
@login_required
@authorize_user("create")
def new_book_form():
    all_categories = db.session.query(Category).all()
    return render_template('books/new.html', categories=all_categories, book={}, new_genres=[], is_edit=False)

@app.route('/books/new', methods=['POST'])
@login_required
@authorize_user("create")
def create_book():
    all_categories = db.session.query(Category).all()
    
    if request.method == 'POST':
        if not current_user.can("create"):
            flash("Недостаточно прав для доступа к странице", "warning")
            return redirect(url_for("home"))
        
        cleaned_params = request.form.to_dict()
        for param in cleaned_params:
            cleaned_params[param] = bleach.clean(cleaned_params[param])
        
        selected_genres = request.form.getlist('category_ids')
        
        try:
            uploaded_file = request.files.get('cover_img')
            if uploaded_file and uploaded_file.filename:
                img_saver = FileSaver(uploaded_file)
                saved_file = img_saver.save_to_db()
            else:
                saved_file = None

            new_book = Book(
                title=cleaned_params.get('title'),
                description=cleaned_params.get('description'),
                publication_year=cleaned_params.get('publication_year'),
                publisher=cleaned_params.get('publisher'),
                writer=cleaned_params.get('writer'),
                pages=cleaned_params.get('pages'),
                cover_image=saved_file.id if saved_file else None
            )

            for category_id in selected_genres:
                category = db.session.query(Category).filter_by(id=category_id).first()
                if category:
                    new_book.categories.append(category)
            
            db.session.add(new_book)
            db.session.commit()
            
            if saved_file:
                img_saver.save_to_system()
            
            flash(f"Книга '{new_book.title}' успешно добавлена", "success")
            return redirect(url_for('show_book', book_id=new_book.id))
        except Exception as e:
            db.session.rollback()
            flash(f"При сохранении возникла ошибка: {str(e)}", "danger")
            return render_template("books/new.html", categories=all_categories, book=cleaned_params, new_genres=selected_genres, is_edit=False)
    
    return render_template('books/new.html', categories=all_categories, book={}, new_genres=[], is_edit=False)

@app.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
@authorize_user("edit")
def edit_book_form(book_id):
    selected_book = db.session.query(Book).filter(Book.id == book_id).first()
    all_categories = db.session.query(Category).all()
    selected_genres = [str(category.id) for category in selected_book.categories]

    if request.method == 'POST':
        if not current_user.can("edit"):
            flash("Недостаточно прав для доступа к странице", "warning")
            return redirect(url_for("home"))
        updated_params = extract_params(PERMITTED_FIELDS)
        for param in updated_params:
            if updated_params[param] is not None:
                updated_params[param] = bleach.clean(updated_params[param])
        selected_genres = request.form.getlist('category_ids')
        try:
            updated_categories = []
            for category_id in selected_genres:
                if int(category_id) != 0:
                    category = db.session.query(Category).filter_by(id=category_id).first()
                    updated_categories.append(category)
            selected_book.categories = updated_categories
            selected_book.title = updated_params['title']
            selected_book.description = updated_params['description']
            selected_book.publication_year = updated_params['publication_year']
            selected_book.publisher = updated_params['publisher']
            selected_book.writer = updated_params['writer']
            selected_book.pages = updated_params['pages']
            selected_book.cover_image = updated_params['cover_image']
            db.session.commit()
            flash(f"Книга '{selected_book.title}' успешно обновлена", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"При сохранении возникла ошибка: {str(e)}", "danger")
            return render_template("books/edit.html", categories=all_categories, book=selected_book, new_genres=selected_genres, is_edit=True)
        return redirect(url_for('show_book', book_id=selected_book.id))

    return render_template("books/edit.html", categories=all_categories, book=selected_book, new_genres=selected_genres, is_edit=True)

@app.route('/delete_post/<int:book_id>', methods=['POST'])
@login_required
@authorize_user('delete')
def delete_book(book_id):
    try:
        book_to_delete = db.session.query(Book).filter(Book.id == book_id).first()
        if book_to_delete:
            book_to_delete.categories = []
            db.session.commit()
            
            db.session.query(Feedback).filter(Feedback.book_id == book_id).delete()
            
            image_usage_count = db.session.query(Book).filter(Book.cover_image == book_to_delete.cover_image).count()
            
            db.session.delete(book_to_delete)
            db.session.commit()
            
            if image_usage_count == 1:
                image_to_delete = db.session.query(File).filter(File.id == book_to_delete.cover_image).first()
                if image_to_delete:
                    db.session.delete(image_to_delete)
                    db.session.commit()
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_to_delete.storage_filename))

            response = make_response(redirect(url_for('home')))
            flash('Запись успешно удалена', 'success')
            return response
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении: {e}', 'danger')
    return redirect(url_for('home'))

@app.route('/books/<int:book_id>')
def show_book(book_id):
    try:
        selected_book = db.session.query(Book).filter(Book.id == book_id).first()
        selected_book.description = markdown.markdown(selected_book.description)
        user_feedback = None
        all_feedback = None
        if current_user.is_authenticated:
            user_feedback = db.session.query(Feedback).filter(Feedback.book_id == book_id, Feedback.user_id == current_user.id).first()
            if user_feedback:
                user_feedback.comment = markdown.markdown(user_feedback.comment)
            all_feedback = db.session.query(Feedback).filter(Feedback.book_id == book_id, Feedback.user_id != current_user.id).all()
        else:
            all_feedback = db.session.query(Feedback).filter(Feedback.book_id == book_id).all()
        
        feedback_comments = []
        for feedback in all_feedback:
            feedback_comments.append({
                'user_id': feedback.user_id,
                'score': feedback.score,
                'comment': markdown.markdown(feedback.comment),
                'date_posted': feedback.date_posted
            })
        
        book_categories = selected_book.categories
        
        response = make_response(render_template('books/show.html', book=selected_book, categories=book_categories, comment=user_feedback, all_comments=feedback_comments))
        
        return response
    except Exception as e:
        flash(f'Ошибка при загрузке данных: {e}', 'danger')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
