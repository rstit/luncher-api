from .views import TokenView


def register_routes(app):
    app.add_url_rule('/auth/token/', view_func=TokenView.as_view('auth:token'))
