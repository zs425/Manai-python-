from mezzanine.accounts import urls
from django.shortcuts import redirect
from django.core.urlresolvers import reverse, NoReverseMatch
from mezzanine.conf import settings

def my_login_redirect(request, wholesale=False):
    """
    Returns the redirect response for login/signup. Favors:
    - next param
    - LOGIN_REDIRECT_URL setting
    - homepage
    """
    ignorable_nexts = ("", urls.SIGNUP_URL, urls.LOGIN_URL, urls.LOGOUT_URL)
    next = request.REQUEST.get("next", "")
    if next in ignorable_nexts:
        try:
            next = reverse(settings.LOGIN_REDIRECT_URL)
        except NoReverseMatch:
            next = "/retail-shop/"
            if wholesale:
                next = "/wholesale-shop/"
    return redirect(next)