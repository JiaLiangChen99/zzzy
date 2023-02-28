from server import app
from dash import Input, Output

@app.callback(
    Output('article_main','children'),
    Input('article_page_store','data'),
)
def show_article(hash):
    return f'当前文章:{hash}'