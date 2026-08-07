from flask_login import current_user
from app.models.setting import SystemSetting

def verify_sensitive_password(password: str) -> bool:
    """Verifies current logged in user's password for sensitive actions."""
    if not current_user or not current_user.is_authenticated:
        return False
    
    # Honor REQUIRE_PWD_CONFIRM_DELETE system setting
    require_confirm = SystemSetting.get_bool('REQUIRE_PWD_CONFIRM_DELETE', True)
    if not require_confirm:
        return True

    if not password:
        return False
    return current_user.check_password(password)
