from .views import MealListView


def register_routes(app):
    app.add_url_rule('/meals/', view_func=MealListView.as_view('meals:list'))
