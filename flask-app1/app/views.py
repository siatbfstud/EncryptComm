from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, CompactCRUDMixin
from app.models import Project, ProjectFiles
from flask_appbuilder import BaseView, expose, has_access
from . import appbuilder, db

class DemoView(BaseView):
    default_view = "method1"

    @expose('/method1/')
    @has_access
    def page1(self):
        return render_template('method1.html', base_template=appbuilder.base_template, appbuilder=appbuilder)

    @expose('/method2/')
    @has_access
    def page2(self):
        return render_template('method2.html', base_template=appbuilder.base_template, appbuilder=appbuilder)

    @expose('/method3/')
    @has_access
    def page3(self):
        return render_template('method3.html', base_template=appbuilder.base_template, appbuilder=appbuilder)

appbuilder.add_view(DemoView(), "Teamet",
                    category='Kontakt', category_icon='fa-envelope',
                    href="/demoview/method1/")

appbuilder.add_link("Message2", category='Kontakt',
                    href="/demoview/method2/")

appbuilder.add_link("Message3", category='Kontakt',
                    href="/demoview/method3/")

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template("404.html", base_template=appbuilder.base_template, appbuilder=appbuilder), 404,)

class ProjectFilesModelView(ModelView):
    datamodel = SQLAInterface(ProjectFiles)

    label_columns = {"file_name": "File Name", "download": "Download"}
    add_columns = ["file", "description", "project"]
    edit_columns = ["file", "description", "project"]
    list_columns = ["file_name", "download"]
    show_columns = ["file_name", "download"]


class ProjectModelView(CompactCRUDMixin, ModelView):
    datamodel = SQLAInterface(Project)
    related_views = [ProjectFilesModelView]

    show_template = "appbuilder/general/model/show_cascade.html"
    edit_template = "appbuilder/general/model/edit_cascade.html"

    add_columns = ["name"]
    edit_columns = ["name"]
    list_columns = ["name", "created_by", "created_on", "changed_by", "changed_on"]
    show_fieldsets = [
        ("Info", {"fields": ["name"]}),
        (
            "Audit",
            {
                "fields": ["created_by", "created_on", "changed_by", "changed_on"],
                "expanded": False,
            },
        ),
    ]

appbuilder.add_view(ProjectModelView, "Projekt filer", icon="fa-table", category="Filer")

appbuilder.add_view_no_menu(ProjectFilesModelView)
db.create_all()