from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from .keycloak import decode_token

def keycloak_required(required_roles=None):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({"detail": "Missing or invalid token"}, status=401)

            token = auth_header.split()[1]

            try:
                payload = decode_token(token)
                request.user_info = payload  # Inject user info into request

                if required_roles:
                    user_roles = payload.get("realm_access", {}).get("roles", [])
                    if not any(role in user_roles for role in required_roles):
                        return Response({"detail": "Forbidden: Insufficient role"}, status=403)

            except Exception as e:
                return Response({"detail": f"Token error: {str(e)}"}, status=401)

            return func(request, *args, **kwargs)
        return wrapper
    return decorator
