import base64
from rest_framework import HTTP_HEADER_ENCODING, exceptions, response


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    return auth


def get_login_credentials(request):
    """
    @summary: A function to fetch creds from request
    @param request (object): request object with basic auth creds
    @return auth(tuple): A segregated username and password
    """
    auth = get_authorization_header(request).split()

    if not auth or auth[0].lower() != b'basic':
        msg = 'No basic authorization header provided.'
        raise exceptions.AuthenticationFailed(msg)

    if len(auth) == 1:
        msg = 'Invalid basic header. No credentials provided.'
        raise exceptions.AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = 'Invalid basic header. ' \
              'Credentials string should not contain spaces.'
        raise exceptions.AuthenticationFailed(msg)

    try:
        auth_parts = base64.b64decode(auth[1]).decode(
            HTTP_HEADER_ENCODING).partition(':')
    except (TypeError, UnicodeDecodeError):
        msg = 'Invalid basic header. ' \
              'Credentials not correctly base64 encoded.'
        raise exceptions.AuthenticationFailed(msg)

    return auth_parts[0], auth_parts[2]
