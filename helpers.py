import requests
from flask import redirect, render_template, request, session
from functools import wraps
from flask import g, request, redirect, url_for

def error(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=code, error=escape(message)), code


def login_required(f):
    """
    Got this Login Required wrap function from the following website
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/ 

    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# list of dictionaries for all the sticks
banana= {
    "black": "/static/black_images/banana2.png",
    "white": "/static/images/banana2.png"
}
blueman = {
    "black": "/static/black_images/blueman.png",
    "white": "/static/images/blueman.png"
}

hi = {
    "black": "/static/black_images/hi.png" ,
    "white": "/static/images/hi.png" 
}

chicken = {
    "black": "/static/black_images/chicken.png",
    "white": "/static/images/chicken.png" 
}

cupcake = {
    "black": "/static/black_images/cupcake.png",
    "white": "/static/images/cupcake.png"
}

whale = {
    "black": "/static/black_images/whale.png",
    "white": "/static/images/whale.png"
}

emoticon = {
    "black": "/static/black_images/emoticon.png",
    "white": "/static/images/emoticon.png"
}

friedEgg = {
    "black": "/static/black_images/fried-egg.png",
    "white": "/static/images/fried-egg.png"
}

gingerbread ={
    "black": "/static/black_images/gingerbread.png",
    "white": "/static/images/gingerbread.png"
}

happy = {
    "black": "/static/black_images/happy.png",
    "white": "/static/images/happy.png" 
}

love = {
    "black": "/static/black_images/love.png",
    "white": "/static/images/love.png"
}




