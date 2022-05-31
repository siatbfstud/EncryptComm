from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi

from . import appbuilder, db

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""



from flask import render_template
from flask_appbuilder import BaseView, expose, has_access

from . import appbuilder, db

# pylint: disable=R0201
class DemoView(BaseView):
    """
    purpose: demonstrating how to render completely customized view (method1 & method2)
             and view extending the base layout comes with F.A.B
    """
    default_view = "method1"

    @expose('/method1/')
    @has_access
    def page1(self):
        '''API without parameter + customized view'''
        message = 'message #1: Method1'
        return render_template('method1.html', message=message, base_template=appbuilder.base_template, appbuilder=appbuilder)

    @expose('/method2/<message>')
    @has_access
    def page2(self, message):
        '''API with parameter + customized view'''
        message = f'message #2: {message}'
        return render_template('method1.html', message=message)

    @expose('/method3/')
    @has_access
    def page3(self):
        '''API without parameter + view extending the base layout'''
        message = 'message #3: Method3'
        return render_template('method3.html', message=message,
                               base_template=appbuilder.base_template, appbuilder=appbuilder)

appbuilder.add_view(DemoView(), "Message1",
                    category='Demo View', category_icon='fa-envelope',
                    href="/demoview/method1/")

appbuilder.add_link("Message2", category='Demo View',
                    href="/demoview/method2/FAB_Demo_view")

appbuilder.add_link("Message3", category='Demo View',
                    href="/demoview/method3/")

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()
