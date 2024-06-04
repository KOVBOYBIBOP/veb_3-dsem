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



app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

PERMITTED_PARAMS = ["title", "description", "publication_year", "publisher", "writer", "pages", "cover_image"]

from auth import auth_bp, init_login_manager, check_rights
from comments import comments_bp
from tools import ImageSaver
from models import File, Book, Category, Feedback

app.register_blueprint(auth_bp)
app.register_blueprint(comments_bp)

init_login_manager(app)

def get_viewed_books():
    viewed_books = []
    if request.cookies.get('viewed_books'):
        books = request.cookies.get('viewed_books').split(',')
        for book in books:
            viewed_book = db.session.query(Book).filter(Book.id == int(book)).scalar()
            if viewed_book:
                viewed_books.append(viewed_book)
    return viewed_books

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = app.config['PER_PAGE']
    viewed_books = get_viewed_books()
    info_about_books = []
    books_query = db.session.query(Book)

    # Получение параметров поиска
    title = request.args.get('title')
    genre_ids = request.args.getlist('genre')
    years = request.args.getlist('year')
    author = request.args.get('author')
    volume_from = request.args.get('volume_from')
    volume_to = request.args.get('volume_to')

    if title:
        books_query = books_query.filter(Book.title.ilike(f'%{title}%'))
    if genre_ids:
        books_query = books_query.join(Book.categories).filter(Category.id.in_(genre_ids))
    if years:
        books_query = books_query.filter(Book.publication_year.in_(years))
    if author:
        books_query = books_query.filter(Book.writer.ilike(f'%{author}%'))
    if volume_from:
        books_query = books_query.filter(Book.pages >= int(volume_from))
    if volume_to:
        books_query = books_query.filter(Book.pages <= int(volume_to))

    books_counter = books_query.count()
    books = books_query.order_by(desc(Book.publication_year)).limit(per_page).offset(per_page * (page - 1)).all()
    
    for book in books:
        info = {
            'book': book,
            'categories': book.categories,
        }
        info_about_books.append(info)
        # Вывод данных о книге в консоль
        print(f"Book ID: {book.id}")
        print(f"Title: {book.title}")
        print(f"Description: {book.description}")
        print(f"Publication Year: {book.publication_year}")
        print(f"Publisher: {book.publisher}")
        print(f"Writer: {book.writer}")
        print(f"Pages: {book.pages}")
        print(f"Total Ratings: {book.total_ratings}")
        print(f"Ratings Count: {book.ratings_count}")
        print(f"Cover Image ID: {book.cover_image}")
        print("Categories:")
        for category in book.categories:
            print(f" - {category.category_name}")
        print("\n")

    page_count = math.ceil(books_counter / per_page)
    
    # Получение всех категорий и годов для формы поиска
    categories = db.session.query(Category).all()
    years = db.session.query(Book.publication_year).distinct().all()

    return render_template(
        'index.html',
        books=info_about_books,
        page=page,
        page_count=page_count,
        viewed_books=viewed_books,
        categories=categories,
        years=[year[0] for year in years],  # Преобразуем список кортежей в список значений
        search_params=request.args  # Передаем текущие параметры поиска для сохранения состояния формы
    )






@app.route('/media/images/<image_id>')
def image(image_id):
    img = db.session.query(File).filter_by(id=image_id).first_or_404()
    return send_from_directory(app.config['UPLOAD_FOLDER'], img.storage_filename)

def params(names_list):
    result = {}
    for name in names_list:
        result[name] = request.form.get(name) or None
    return result

@app.route('/books/new')
@login_required
@check_rights("create")
def new_book():
    categories = db.session.query(Category).all()
    # Вывод жанров в консоль
    print("Полученные жанры:")
    for category in categories:
        print(f"ID: {category.id}, Name: {category.category_name}")
    return render_template('books/new.html', categories=categories, book={}, new_genres=[], is_edit=False)

@app.route('/books/new', methods=['POST'])
@login_required
@check_rights("create")
def new_book_route():
    categories = db.session.query(Category).all()
    # Вывод жанров в консоль
    print("Полученные жанры:")
    for category in categories:
        print(f"ID: {category.id}, Name: {category.category_name}")
    
    if request.method == 'POST':
        if not current_user.can("create"):
            flash("Недостаточно прав для доступа к странице", "warning")
            return redirect(url_for("index"))
        
        cur_params = request.form.to_dict()
        for param in cur_params:
            cur_params[param] = bleach.clean(cur_params[param])
        
        new_genres = request.form.getlist('category_ids')
        
        try:
            f = request.files.get('cover_img')
            if f and f.filename:
                img = ImageSaver(f)
                db_img = img.save_to_db()
            else:
                db_img = None

            book = Book(
                title=cur_params.get('title'),
                description=cur_params.get('description'),
                publication_year=cur_params.get('publication_year'),
                publisher=cur_params.get('publisher'),
                writer=cur_params.get('writer'),
                pages=cur_params.get('pages'),
                cover_image=db_img.id if db_img else None
            )

            for category_id in new_genres:
                category = db.session.query(Category).filter_by(id=category_id).first()
                if category:
                    book.categories.append(category)
            
            db.session.add(book)
            db.session.commit()
            
            if db_img:
                img.save_to_system()
            
            flash(f"Книга '{book.title}' успешно добавлена", "success")
            return redirect(url_for('show', book_id=book.id))
        except Exception as e:
            db.session.rollback()
            flash(f"При сохранении возникла ошибка: {str(e)}", "danger")
            return render_template("books/new.html", categories=categories, book=cur_params, new_genres=new_genres, is_edit=False)
    
    return render_template('books/new.html', categories=categories, book={}, new_genres=[], is_edit=False)


@app.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
@check_rights("edit")
def edit_book(book_id):
    book = db.session.query(Book).filter(Book.id == book_id).scalar()
    categories = db.session.query(Category).all()
    edited_genres = [str(category.id) for category in book.categories]

    # Вывод жанров в консоль
    print("Полученные жанры:")
    for category in categories:
        print(f"ID: {category.id}, Name: {category.category_name}")

    if request.method == 'POST':
        if not current_user.can("edit"):
            flash("Недостаточно прав для доступа к странице", "warning")
            return redirect(url_for("index"))
        cur_params = params(PERMITTED_PARAMS)
        for param in cur_params:
            if cur_params[param] is not None:
                cur_params[param] = bleach.clean(cur_params[param])
        new_genres = request.form.getlist('category_ids')
        try:
            categories_list = []
            for category in new_genres:
                if int(category) != 0:
                    new_category = db.session.query(Category).filter_by(id=category).scalar()
                    categories_list.append(new_category)
            book.categories = categories_list
            book.title = cur_params['title']
            book.description = cur_params['description']
            book.publication_year = cur_params['publication_year']
            book.publisher = cur_params['publisher']
            book.writer = cur_params['writer']
            book.pages = cur_params['pages']
            book.cover_image = cur_params['cover_image']
            db.session.commit()
            flash(f"Книга '{book.title}' успешно обновлена", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"При сохранении возникла ошибка: {str(e)}", "danger")
            return render_template("books/edit.html", categories=categories, book=book, new_genres=new_genres, is_edit=True)
        return redirect(url_for('show', book_id=book.id))

    return render_template("books/edit.html", categories=categories, book=book, new_genres=edited_genres, is_edit=True)


@app.route('/delete_post/<int:book_id>', methods=['POST'])
@login_required
@check_rights('delete')
def delete_post(book_id):
    try:
        book = db.session.query(Book).filter(Book.id == book_id).scalar()
        if book:
            # Удаляем связанные категории
            book.categories = []
            db.session.commit()
            
            # Удаляем связанные отзывы
            db.session.query(Feedback).filter(Feedback.book_id == book_id).delete()
            
            # Проверяем, используется ли изображение в других книгах
            count_of_images = db.session.query(Book).filter(Book.cover_image == book.cover_image).count()
            
            # Удаляем саму книгу
            db.session.delete(book)
            db.session.commit()
            
            # Удаляем изображение, если оно не используется в других книгах
            if count_of_images == 1:
                image = db.session.query(File).filter(File.id == book.cover_image).scalar()
                if image:
                    db.session.delete(image)
                    db.session.commit()
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.storage_filename))

            # Обновляем куки с просмотренными книгами
            res = make_response(redirect(url_for('index')))
            if request.cookies.get('viewed_books'):
                viewed_books = []
                book_ids = request.cookies.get('viewed_books').split(',')
                for id in book_ids:
                    if id != str(book_id):
                        viewed_books.append(id)
                res.set_cookie('viewed_books', ','.join(viewed_books), max_age=60*60*24*365*2)
            flash('Запись успешно удалена', 'success')
            return res
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении: {e}', 'danger')
    return redirect(url_for('index'))


@app.route('/books/<int:book_id>/update', methods=['POST'])
@login_required
@check_rights("edit")
def update_book(book_id):
    if not current_user.can("edit"):
        flash("Недостаточно прав для доступа к странице", "warning")
        return redirect(url_for("index"))
    cur_params = params(PERMITTED_PARAMS)
    for param in cur_params:
        cur_params[param] = bleach.clean(cur_params[param])
    new_categories = request.form.getlist('category_id[]')
    categories = db.session.query(Category).all()
    book = db.session.query(Book).filter(Book.id == book_id).scalar()
    try:
        categories_list = []
        for category in new_categories:
            if int(category) != 0:
                new_category = db.session.query(Category).filter_by(id=category).scalar()
                categories_list.append(new_category)
        book.categories = categories_list
        book.title = cur_params['title']
        book.description = cur_params['description']
        book.publication_year = cur_params['publication_year']
        book.publisher = cur_params['publisher']
        book.writer = cur_params['writer']
        book.pages = cur_params['pages']
        book.cover_image = cur_params['cover_image']
        db.session.commit()
        flash(f"Книга '{book.title}' успешно обновлена", "success")
    except:
        db.session.rollback()
        flash("При сохранении возникла ошибка", "danger")
        return render_template("books/edit.html", categories=categories, book=book, new_categories=new_categories)
    return redirect(url_for('show', book_id=book.id))

@app.route('/books/<int:book_id>')
def show(book_id):
    try:
        book = db.session.query(Book).filter(Book.id == book_id).scalar()
        book.description = markdown.markdown(book.description)
        user_comment = None
        all_comments = None
        if current_user.is_authenticated:
            user_comment = db.session.query(Feedback).filter(Feedback.book_id == book_id, Feedback.user_id == current_user.id).scalar()
            if user_comment:
                user_comment.comment = markdown.markdown(user_comment.comment)
            all_comments = db.session.query(Feedback).filter(Feedback.book_id == book_id, Feedback.user_id != current_user.id).all()
        else:
            all_comments = db.session.query(Feedback).filter(Feedback.book_id == book_id).all()
        
        markdown_all_comments = []
        for comment in all_comments:
            markdown_all_comments.append({
                'user_id': comment.user_id,
                'score': comment.score,
                'comment': markdown.markdown(comment.comment),
                'date_posted': comment.date_posted
            })
        
        categories = book.categories

        # Добавим отладочные выводы
        print(f"Book ID: {book.id}")
        print(f"User Comment: {user_comment}")
        print(f"All Comments: {markdown_all_comments}")
        
        res = make_response(render_template('books/show.html', book=book, categories=categories, comment=user_comment, all_comments=markdown_all_comments))
        
        viewed_books = request.cookies.get('viewed_books')
        if not viewed_books:
            viewed_books = []
        else:
            viewed_books = viewed_books.split(',')
        
        if str(book_id) not in viewed_books:
            viewed_books.append(str(book_id))
        
        if len(viewed_books) > 5:
            viewed_books = viewed_books[-5:]
        
        res.set_cookie('viewed_books', ','.join(viewed_books), max_age=60*60*24*365*2)
        
        return res
    except Exception as e:
        flash(f'Ошибка при загрузке данных: {e}', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
