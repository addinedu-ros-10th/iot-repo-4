"""
의존성 주입 컨테이너

Clean Architecture의 의존성 역전 원칙을 구현하는 컨테이너입니다.
서비스와 리포지토리의 의존성을 중앙에서 관리합니다.
"""

from typing import Dict, Type, Any
from app.interfaces.repositories.user_repository import IUserRepository
from app.interfaces.repositories.device_repository import IDeviceRepository
from app.interfaces.services.user_service_interface import IUserService
from app.infrastructure.repositories.postgresql_user_repository import PostgreSQLUserRepository
from app.infrastructure.repositories.postgresql_device_repository import PostgreSQLDeviceRepository
from app.domain.services.user_service import UserService


class DependencyContainer:
    """의존성 주입 컨테이너"""
    
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._repositories: Dict[Type, Any] = {}
        self._initialize_dependencies()
    
    def _initialize_dependencies(self):
        """기본 의존성을 초기화합니다."""
        # 리포지토리 등록
        self.register_repository(IUserRepository, PostgreSQLUserRepository())
        self.register_repository(IDeviceRepository, PostgreSQLDeviceRepository())
        
        # 서비스 등록
        user_repository = self.get_repository(IUserRepository)
        self.register_service(IUserService, UserService(user_repository))
    
    def register_service(self, interface: Type, implementation: Any) -> None:
        """서비스를 등록합니다."""
        self._services[interface] = implementation
    
    def register_repository(self, interface: Type, implementation: Any) -> None:
        """리포지토리를 등록합니다."""
        self._repositories[interface] = implementation
    
    def get_service(self, interface: Type) -> Any:
        """서비스를 가져옵니다."""
        if interface not in self._services:
            raise KeyError(f"서비스가 등록되지 않았습니다: {interface}")
        return self._services[interface]
    
    def get_repository(self, interface: Type) -> Any:
        """리포지토리를 가져옵니다."""
        if interface not in self._repositories:
            raise KeyError(f"리포지토리가 등록되지 않았습니다: {interface}")
        return self._repositories[interface]
    
    def has_service(self, interface: Type) -> bool:
        """서비스 등록 여부를 확인합니다."""
        return interface in self._services
    
    def has_repository(self, interface: Type) -> bool:
        """리포지토리 등록 여부를 확인합니다."""
        return interface in self._repositories
    
    def clear(self) -> None:
        """모든 의존성을 제거합니다."""
        self._services.clear()
        self._repositories.clear()
    
    # 구체적인 메서드들
    def get_user_service(self) -> IUserService:
        """사용자 서비스를 가져옵니다."""
        return self.get_service(IUserService)
    
    def get_user_repository(self) -> IUserRepository:
        """사용자 리포지토리를 가져옵니다."""
        return self.get_repository(IUserRepository)
    
    def get_device_repository(self) -> IDeviceRepository:
        """디바이스 리포지토리를 가져옵니다."""
        return self.get_repository(IDeviceRepository)


# 전역 의존성 컨테이너 인스턴스
container = DependencyContainer()


def get_container() -> DependencyContainer:
    """전역 의존성 컨테이너를 반환합니다."""
    return container


def register_dependencies() -> None:
    """기본 의존성을 등록합니다."""
    # 컨테이너 초기화 시 자동으로 등록됨
    pass 