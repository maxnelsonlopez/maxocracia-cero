from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .extensions import db
from .models import FollowUp, Interchange, Participant, User, VHVProduct


class UserView(ModelView):
    column_exclude_list = ["password_hash"]
    form_excluded_columns = ["password_hash", "created_at"]


def init_admin(app):
    admin = Admin(app, name="Maxocracia Admin")

    admin.add_view(UserView(User, db.session))
    admin.add_view(ModelView(Participant, db.session))
    admin.add_view(ModelView(Interchange, db.session))
    admin.add_view(ModelView(FollowUp, db.session))
    admin.add_view(ModelView(VHVProduct, db.session))
