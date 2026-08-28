from flask_app import app, db, Movie

with app.app_context():
    db.drop_all()
    db.create_all()

    movies_to_add = [
        Movie(
            title="Extraction",
            description="مرتزق في مهمة خطيرة لإنقاذ ابن تاجر مخدرات.",
            watch_link="https://www.youtube.com/embed/Bm11BB97s0s",
            image_url="https://m.media-amazon.com/images/M/MV5BMDJiNzIxYzEtZTllOC00MzZmLWE1ODEtMGYxNmQxY2YwZTUwXkEyXkFqcGdeQXVyMTA4NjE0NjEy._V1_.jpg",
            genre="أكشن",
            rating=8.0
        ),
        Movie(
            title="The Gray Man",
            description="عميل سري يكتشف أسراراً مظلمة ويصبح هدفاً لمطاردة عالمية.",
            watch_link="https://www.youtube.com/embed/Bm11BB97s0s",
            image_url="https://m.media-amazon.com/images/M/MV5BODg3ZjA4MjUtNmEwZS00MWYwLWI2OTQtMDUzMzA1OTc4YTRhXkEyXkFqcGdeQXVyMTA4NjE0NjEy._V1_.jpg",
            genre="أكشن",
            rating=8.2
        ),
        Movie(
            title="Dominique",
            description="امرأة تحاول الهروب من ماضيها في بيئة مليئة بالتشويق.",
            watch_link="https://drive.google.com/file/d/1GzvKaQNfyhrJoTJHHw9kZlNl8jf-V0Ak/preview",
            image_url="https://images.unsplash.com/photo-1485846234645-a62644f84728?w=500&auto=format&fit=crop&q=80",
            genre="أكشن",
            rating=8.5
        )
    ]

    for movie in movies_to_add:
        db.session.add(movie)

    db.session.commit()
    print("تم تحديث الصور والأفلام بنجاح يا أبو سمرة!")
