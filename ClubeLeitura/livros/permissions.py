'''
Permissões do app livros.
'''
from rest_framework import permissions


class EhAdminOuSomenteLeitura(permissions.BasePermission):
    '''
    Libera leitura (GET, HEAD, OPTIONS) para qualquer um e restringe a escrita
    (POST, PUT, DELETE) a administradores (is_staff).
    '''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
