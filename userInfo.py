import dataclasses


@dataclasses.dataclass
class UserInfo:
    role_type: str = None
    user_availability: str = None
    user_experience: str = None
    role_tags: dict = None
    notice_period: int = None
    location: str = None
