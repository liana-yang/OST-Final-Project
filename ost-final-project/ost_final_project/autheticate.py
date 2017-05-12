from google.appengine.api import users


def autheticate():
    user = users.get_current_user()
    if user:
        logged_in = True
        log_url = users.create_logout_url('/')
        log_msg = "Sign out"
    else:
        logged_in = False
        log_url = users.create_login_url('/')
        log_msg = "Sign in"
    return logged_in, user, log_url, log_msg
