from typing import List, Optional, Tuple
from datetime import datetime, date
from sqlalchemy import func, or_, text, true

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.models.userRegister import UserRegister
from DATABASE.models.user import User
from DATABASE import db


class UserRegisterRepository:
    
    @staticmethod
    def create(email: str,  name: str, last_name: str, second_last_name: str, about_me: str = None) -> UserRegister:
        """Crea un nuevo registro de usuario en la base de datos.
        
        Args:
            email: Correo electrónico del usuario            
            name: Nombre del usuario
            last_name: Primer apellido del usuario
            second_last_name: Segundo apellido del usuario
            about_me: Información adicional sobre el usuario (opcional)
        
        Returns:
            UserRegister: El registro de usuario creado
        """
        # Validar email
        is_valid, error_msg = UserRegister.validate_email(email)
        if not is_valid:
            raise ValueError(error_msg)        

        print(f"Validación exitosa para email: {email}")        
        
        # Validar nombre y apellidos
        for field_value, field_name in [(name, "Nombre"), (last_name, "Apellido"), (second_last_name, "Segundo Apellido")]:
            is_valid, error_msg = UserRegister.validate_name(field_value, field_name)
            if not is_valid:
                raise ValueError(error_msg)                

        # Verificar si el email ya está registrado
        existing_user = User.query.filter(func.lower(User.Email) == email.lower()).first()
        if existing_user:
            raise ValueError(f"El email '{email}' ya está registrado con otro usuario.")                

        existing_register = UserRegister.query.filter(func.lower(UserRegister.Email) == email.lower()).first()
        if existing_register:
            raise ValueError(f"El email '{email}' ya está registrado en el proceso de registro.")

        # Crear nuevo registro de usuario
        new_user = UserRegister(
            Email=email,
            Name=name,
            LastName=last_name,
            SecondLastName=second_last_name,
            AboutMe=about_me,
            CreateDate=date.today(),
            Active=True  # Por defecto inactivo hasta que se apruebe
        )
        
        db.db.session.add(new_user)
        db.db.session.commit()
        
        return new_user, None
    
    @staticmethod
    def approve(user_register_id: int) -> Optional[UserRegister]:        
        """Aprueba un registro de usuario, activándolo y estableciendo la fecha de aprobación.
        
        Args:
            user_register_id: ID del registro de usuario a aprobar
        
        Returns:
            UserRegister: El registro de usuario aprobado, o None si no se encuentra
        """
        user_register = UserRegister.query.get(user_register_id)
        if not user_register:
            return None
        
        user_register.Active = True
        user_register.ApprovalDate = date.today()
        
        db.db.session.commit()
        
        return user_register
    
    @staticmethod
    def decline(user_register_id: int) -> Optional[UserRegister]:
        """Declina un registro de usuario, desactivándolo y estableciendo la fecha de declinación.
        
        Args:
            user_register_id: ID del registro de usuario a declinar
            """
        user_register = UserRegister.query.get(user_register_id)
        if not user_register:
            return None
        
        user_register.Active = False                
        db.db.session.commit()
        
        return user_register

    @staticmethod
    def get_all() -> List[UserRegister]:
        """Obtiene todos los registros de usuario, con opción de filtrar solo los activos.
        
        Args:
            active_only: Si es True, solo devuelve registros activos. Si es False, devuelve todos los registros.
        
        Returns:
            List[UserRegister]: Lista de registros de usuario
        """
        query = UserRegister.query        
        query = query.filter_by(Active=True)
        
        return query.all()
    
    @staticmethod
    def get_pending() -> int:
        """Obtiene el número de registros de usuario pendientes de aprobación.
        
        Returns:
            int: Número de registros de usuario pendientes
        """
        return UserRegister.query.filter_by(Active=True, ApprovalDate=None).count()
    