from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# قاعدة بيانات مؤقتة للأفلام
movies = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        poster = request.form.get('poster')
        if title:
            movies.append({'title': title, 'category': category, 'poster': poster})
        return redirect(url_for('home'))
    
    # دمج وعرض كل المحتويات مترتبة في الصفحة الرئيسية
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
