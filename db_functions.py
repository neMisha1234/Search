from data.favorites import Favorite
from data.users import User
from data.Colleges import Colleges
from data import db_session


db_session.global_init("db/college.db")
db_sess = db_session.create_session()


def add_college_to_fav(college, user_id):
    coll = Colleges()
    user = User()
    coll_id = db_sess.query(Colleges).filter(Colleges.name == str(college['name'])).first()
    db_user_id = db_sess.query(User).filter(User.user_id == str(user_id)).first()
    if not coll_id:
        coll.name = college['name']
        coll.phone = college['Phones']
        coll.site = college['url']
    if not db_user_id:
        user.user_id = str(user_id)
    db_sess.add(coll)
    db_sess.add(user)
    db_sess.commit()

    coll_id = db_sess.query(Colleges).filter(Colleges.name == str(college['name'])).first().id
    db_user_id = db_sess.query(User).filter(User.user_id == str(user_id)).first().id
    fav = Favorite()

    if db_sess.query(Favorite).filter(Favorite.user_id == int(db_user_id)).first() and db_sess.query(Favorite).filter(Favorite.college_id == int(coll_id)).first():
        return
    fav.user_id = db_user_id
    fav.college_id = coll_id
    db_sess.add(fav)
    db_sess.commit()
    return True


def get_favorite(user_id):
    db_user_id = db_sess.query(User).filter(User.user_id == str(user_id)).first()
    if not db_user_id:
        return
    db_user_id = db_user_id.id
    favorites = db_sess.query(Favorite).filter(Favorite.user_id == int(db_user_id)).all()
    print(favorites)
    lst = map(lambda x: db_sess.query(Colleges).filter(Colleges.id == int(x.college_id)).first(), favorites)
    return lst


add_college_to_fav({"name": 'Usa', 'Phones': '111', 'url': "fsfsdfdsf"}, 2)