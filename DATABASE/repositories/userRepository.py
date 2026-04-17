from typing import List, Optional, Tuple
from datetime import datetime, date
from sqlalchemy import func, or_

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.models.user import User
from DATABASE import db

class UserRepository:

    @staticmethod
    def create(email: str, password: str, name: str, 
               last_name: str, second_last_name: str) -> Tuple[Optional[User], Optional[str]]:
        """
        Crea un nuevo usuario.
        
        Args:
            email: Email del usuario
            password: Contraseña en texto plano (se hasheará)
            name: Nombre
            last_name: Apellido paterno
            second_last_name: Apellido materno
        
        Returns:
            (user, error_message)
            - Si exitoso: (User, None)
            - Si error: (None, mensaje_de_error)
        """        
        # Validar email
        is_valid, error_msg = User.validate_email(email)
        if not is_valid:
            return None, error_msg
        
        # Validar contraseña
        is_valid, error_msg = User.validate_password(password)
        if not is_valid:
            return None, error_msg
        
        # Validar nombre
        is_valid, error_msg = User.validate_name(name, "Nombre")
        if not is_valid:
            return None, error_msg
        
        # Validar apellido paterno
        is_valid, error_msg = User.validate_name(last_name, "Apellido Paterno")
        if not is_valid:
            return None, error_msg
        
        # Validar apellido materno
        is_valid, error_msg = User.validate_name(second_last_name, "Apellido Materno")
        if not is_valid:
            return None, error_msg
        
        # Verificar si el email ya existe
        existing_user = UserRepository.get_by_email(email)
        if existing_user:
            return None, f"El email '{email}' ya está registrado"
        
        try:
            # Crear usuario
            user = User(
                Email=email.lower().strip(),
                Name=name.strip(),
                LastName=last_name.strip(),
                SecondLastName=second_last_name.strip(),
                CreateDate=date.today(),
                Active=True
            )
            
            # Hashear contraseña
            user.set_password(password)
            
            # Guardar en base de datos
            db.db.session.add(user)
            db.db.session.commit()
            
            return user, None
            
        except Exception as e:
            db.db.session.rollback()
            return None, f"Error al crear usuario: {str(e)}"
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por ID.
        
        Args:
            user_id: ID del usuario
        
        Returns:
            User o None si no existe
        """
        return User.query.filter_by(Id=user_id).first()
    
    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """
        Obtiene un usuario por email (case-insensitive).
        
        Args:
            email: Email del usuario
        
        Returns:
            User o None si no existe
        """
        return User.query.filter(
            func.lower(User.Email) == email.lower()
        ).first()
    
    @staticmethod
    def authenticate(email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """
        Autentica un usuario con email y contraseña.
        
        Args:
            email: Email del usuario
            password: Contraseña en texto plano
        
        Returns:
            (user, error_message)
            - Si exitoso: (User, None)
            - Si error: (None, mensaje_de_error)
        """
        # Buscar usuario por email
        user = UserRepository.get_by_email(email)
        
        if not user:
            return None, "Credenciales inválidas"
        
        # Verificar si está activo
        if not user.Active:
            return None, "Usuario desactivado. Contacte al administrador."
        
        # Verificar contraseña
        if not user.check_password(password):
            return None, "Credenciales inválidas"
        
        return user, None
    
    @staticmethod
    def update(user_id: int, **kwargs) -> Tuple[Optional[User], Optional[str]]:
        """
        Actualiza información de un usuario.
        
        Args:
            user_id: ID del usuario
            **kwargs: Campos a actualizar (Email, Name, LastName, SecondLastName, Password, Active)
        
        Returns:
            (user, error_message)
        """
        user = UserRepository.get_by_id(user_id)
        
        if not user:
            return None, "Usuario no encontrado"
        
        try:
            # Actualizar contraseña si se proporciona
            if 'Password' in kwargs or 'password' in kwargs:
                password = kwargs.pop('Password', None) or kwargs.pop('password', None)
                if password:
                    is_valid, error_msg = User.validate_password(password)
                    if not is_valid:
                        return None, error_msg
                    user.set_password(password)
            
            # Validar email si se actualiza
            if 'Email' in kwargs:
                is_valid, error_msg = User.validate_email(kwargs['Email'])
                if not is_valid:
                    return None, error_msg
                
                # Verificar que no exista otro usuario con ese email
                existing = UserRepository.get_by_email(kwargs['Email'])
                if existing and existing.Id != user_id:
                    return None, "El email ya está en uso"
                
                user.Email = kwargs['Email'].lower().strip()
            
            # Validar y actualizar nombre
            if 'Name' in kwargs:
                is_valid, error_msg = User.validate_name(kwargs['Name'], "Nombre")
                if not is_valid:
                    return None, error_msg
                user.Name = kwargs['Name'].strip()
            
            # Validar y actualizar apellido paterno
            if 'LastName' in kwargs:
                is_valid, error_msg = User.validate_name(kwargs['LastName'], "Apellido Paterno")
                if not is_valid:
                    return None, error_msg
                user.LastName = kwargs['LastName'].strip()
            
            # Validar y actualizar apellido materno
            if 'SecondLastName' in kwargs:
                is_valid, error_msg = User.validate_name(kwargs['SecondLastName'], "Apellido Materno")
                if not is_valid:
                    return None, error_msg
                user.SecondLastName = kwargs['SecondLastName'].strip()
            
            # Actualizar estado activo
            if 'Active' in kwargs:
                user.Active = bool(kwargs['Active'])
            
            db.db.session.commit()
            
            return user, None
            
        except Exception as e:
            db.db.session.rollback()
            return None, f"Error al actualizar usuario: {str(e)}"
    
    @staticmethod
    def change_password(user_id: int, old_password: str, new_password: str) -> Tuple[bool, Optional[str]]:
        """
        Cambia la contraseña de un usuario verificando la contraseña anterior.
        
        Args:
            user_id: ID del usuario
            old_password: Contraseña actual
            new_password: Nueva contraseña
        
        Returns:
            (success, error_message)
        """
        user = UserRepository.get_by_id(user_id)
        
        if not user:
            return False, "Usuario no encontrado"
        
        # Verificar contraseña actual
        if not user.check_password(old_password):
            return False, "La contraseña actual es incorrecta"
        
        # Validar nueva contraseña
        is_valid, error_msg = User.validate_password(new_password)
        if not is_valid:
            return False, error_msg
        
        try:
            # Establecer nueva contraseña
            user.set_password(new_password)
            db.db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.db.session.rollback()
            return False, f"Error al cambiar contraseña: {str(e)}"
    
    @staticmethod
    def deactivate(user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Desactiva un usuario (soft delete).
        
        Args:
            user_id: ID del usuario
        
        Returns:
            (success, error_message)
        """
        user = UserRepository.get_by_id(user_id)
        
        if not user:
            return False, "Usuario no encontrado"
        
        try:
            user.Active = False
            db.db.session.commit()
            return True, None
            
        except Exception as e:
            db.db.session.rollback()
            return False, f"Error al desactivar usuario: {str(e)}"
    
    @staticmethod
    def activate(user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Activa un usuario desactivado.
        
        Args:
            user_id: ID del usuario
        
        Returns:
            (success, error_message)
        """
        user = UserRepository.get_by_id(user_id)
        
        if not user:
            return False, "Usuario no encontrado"
        
        try:
            user.Active = True
            db.db.session.commit()
            return True, None
            
        except Exception as e:
            db.db.session.rollback()
            return False, f"Error al activar usuario: {str(e)}"
    
    @staticmethod
    def delete(user_id: int) -> Tuple[bool, Optional[str]]:
        """
        Elimina un usuario permanentemente (soft delete).        
        
        Args:
            user_id: ID del usuario
        
        Returns:
            (success, error_message)    
        """
        user = UserRepository.get_by_id(user_id)
        
        if not user:
            return False, "Usuario no encontrado"
        
        try:
            user.Active = False  # Soft delete
            db.db.session.commit()
            return True, None
            
        except Exception as e:
            db.db.session.rollback()
            return False, f"Error al eliminar usuario: {str(e)}"
    
    @staticmethod
    def get_all(active_only: bool = True, limit: int = 100, offset: int = 0) -> List[User]:
        """
        Obtiene todos los usuarios con paginación.
        
        Args:
            active_only: Si True, solo usuarios activos
            limit: Número máximo de resultados
            offset: Número de resultados a saltar
        
        Returns:
            Lista de usuarios
        """
        query = User.query
        
        if active_only:
            query = query.filter_by(Active=True)
        
        return query.order_by(User.CreateDate.desc()).limit(limit).offset(offset).all()
    
    @staticmethod
    def search(query_str: str, active_only: bool = True, limit: int = 50) -> List[User]:
        """
        Busca usuarios por email, nombre o apellidos.
        
        Args:
            query_str: Texto a buscar
            active_only: Si True, solo usuarios activos
            limit: Número máximo de resultados
        
        Returns:
            Lista de usuarios que coinciden
        """
        search_pattern = f"%{query_str}%"
        
        query = User.query.filter(
            or_(
                User.Email.ilike(search_pattern),
                User.Name.ilike(search_pattern),
                User.LastName.ilike(search_pattern),
                User.SecondLastName.ilike(search_pattern)
            )
        )
        
        if active_only:
            query = query.filter_by(Active=True)
        
        return query.limit(limit).all()
    
    @staticmethod
    def count_users(active_only: bool = False) -> int:
        """
        Cuenta el total de usuarios.
        
        Args:
            active_only: Si True, solo cuenta usuarios activos
        
        Returns:
            Número total de usuarios
        """
        query = User.query
        
        if active_only:
            query = query.filter_by(Active=True)
        
        return query.count()
    
    @staticmethod
    def get_statistics() -> dict:
        """
        Obtiene estadísticas de usuarios.
        
        Returns:
            Diccionario con estadísticas
        """
        from datetime import timedelta
        
        total_users = User.query.count()
        active_users = User.query.filter_by(Active=True).count()
        
        # Usuarios registrados en los últimos 30 días
        thirty_days_ago = date.today() - timedelta(days=30)
        recent_users = User.query.filter(User.CreateDate >= thirty_days_ago).count()
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': total_users - active_users,
            'recent_registrations_30d': recent_users
        }