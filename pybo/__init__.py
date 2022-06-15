from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def page_not_found(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models

    # 블루프린트
<<<<<<< HEAD
    from .views import main_views, question_views, answer_views, auth_views, exercise_views, \
        calculator_views,form_sending_views, apply_views, complete_views, mypage_views, \
        hconnect_views, photo_views
    # form_sending_views, apply_views, complete_views, certify_views, mypage_views, hconnect_views, test_views,
    #     test2_views, test3_views, test4_views, photo_views, hongtest,



=======
    from .views import main_views, question_views, answer_views, auth_views, exercise_views, calculator_views, \
        form_sending_views, apply_views, complete_views, mypage_views, hconnect_views, \
        photo_views, hongtest, form_sending_views, apply_views, complete_views, mypage_views, hconnect_views
>>>>>>> 817cd5959d0d6dfce9ba967420741d5d3a4bbbdf
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(exercise_views.bp)
    app.register_blueprint(calculator_views.bp)
    app.register_blueprint(form_sending_views.bp)
    app.register_blueprint(apply_views.bp)
    app.register_blueprint(complete_views.bp)
    app.register_blueprint(mypage_views.bp)
    app.register_blueprint(hconnect_views.bp)
    app.register_blueprint(photo_views.bp)



    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    # 오류페이지
    app.register_error_handler(404, page_not_found)

    return app

