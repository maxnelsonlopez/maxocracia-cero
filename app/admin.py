from flask import redirect, session
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from .extensions import db
from .models import FollowUp, Interchange, Participant, User, VHVProduct


class SecureModelView(ModelView):
    def is_accessible(self):
        user_id = session.get("user_id")
        if not user_id:
            return False
        
        # Check if user is admin in DB
        user = db.session.get(User, user_id)
        return user is not None and user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login page if user doesn't have access
        return redirect("/")


class UserAdminView(SecureModelView):
    column_exclude_list = ["password_hash"]
    form_excluded_columns = ["password_hash", "created_at"]


class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        user_id = session.get("user_id")
        if not user_id:
            return False
        
        user = db.session.get(User, user_id)
        return user is not None and user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect("/")


def init_admin(app):
    admin = Admin(
        app, 
        name="Maxocracia Admin", 
        index_view=SecureAdminIndexView()
    )

    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(SecureModelView(Participant, db.session))
    admin.add_view(SecureModelView(Interchange, db.session))
    admin.add_view(SecureModelView(FollowUp, db.session))
    admin.add_view(SecureModelView(VHVProduct, db.session))
