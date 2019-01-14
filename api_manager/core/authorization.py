import base64
from rest_framework import HTTP_HEADER_ENCODING, exceptions, response, status
from rest_framework.authtoken.models import Token


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


def get_token_from_request(request):
    """
    @summary: Returns the token from requests
    @param request: request object
    @return token (string): user token
    """
    return request.META.get("HTTP_AUTHORIZATION").split()[1] \
        if request.META.get("HTTP_AUTHORIZATION") else None


def delete_token(request):
    """
    @summary: A function to delete token from request
    @param request: http request object
    @return response : http response object
    """
    try:
        token = get_token_from_request(request)
        if not token:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        Token.objects.get(pk=token).delete()
    except Exception as e:
        msg = str(e)
        return response.Response(
            data=msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response.Response(status=status.HTTP_204_NO_CONTENT)