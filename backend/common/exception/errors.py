from typing import Any

from backend.common.response.response_code import CustomResponseCode, StandardResponseCode


class BaseExceptionError(Exception):
    """自定义异常基类"""

    def __init__(
        self,
        msg: str = 'Server Error',
        code: int = StandardResponseCode.HTTP_500,
        status_code: int = StandardResponseCode.HTTP_500,
        data: Any = None,
    ):
        self.msg = msg
        self.code = code
        self.status_code = status_code
        self.data = data


class PhoneAlreadyRegisteredError(BaseExceptionError):
    """手机号已注册异常"""

    def __init__(
        self,
        msg: str = 'Phone Already Registered',
        code: int = CustomResponseCode.USER_EXISTS,
        status_code: int = StandardResponseCode.HTTP_400,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class AuthorizationError(BaseExceptionError):
    """认证授权异常"""

    def __init__(
        self,
        msg: str = 'Authorization Failed',
        code: int = CustomResponseCode.TOKEN_INVALID,
        status_code: int = StandardResponseCode.HTTP_401,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class TokenError(BaseExceptionError):
    """Token 异常"""

    def __init__(
        self,
        msg: str = 'Token Invalid',
        code: int = CustomResponseCode.TOKEN_INVALID,
        status_code: int = StandardResponseCode.HTTP_401,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class TokenExpired(BaseExceptionError):
    """Token 过期"""

    def __init__(
        self,
        msg: str = 'Token Expired',
        code: int = CustomResponseCode.TOKEN_EXPIRED,
        status_code: int = StandardResponseCode.HTTP_401,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class NotFoundError(BaseExceptionError):
    """资源未找到"""

    def __init__(
        self,
        msg: str = 'Not Found',
        code: int = StandardResponseCode.HTTP_404,
        status_code: int = StandardResponseCode.HTTP_404,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class UserNotFoundError(BaseExceptionError):
    """用户未找到"""

    def __init__(
        self,
        msg: str = 'User Not Found',
        code: int = CustomResponseCode.USER_NOT_FOUND,
        status_code: int = StandardResponseCode.HTTP_404,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class ValidationError(BaseExceptionError):
    """参数校验失败"""

    def __init__(
        self,
        msg: str = 'Validation Error',
        code: int = StandardResponseCode.HTTP_422,
        status_code: int = StandardResponseCode.HTTP_422,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class RateLimitError(BaseExceptionError):
    """请求频率限制"""

    def __init__(
        self,
        msg: str = 'Too Many Requests',
        code: int = StandardResponseCode.HTTP_429,
        status_code: int = StandardResponseCode.HTTP_429,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class PasswordError(BaseExceptionError):
    """密码错误"""

    def __init__(
        self,
        msg: str = 'Password Error',
        code: int = CustomResponseCode.PASSWORD_ERROR,
        status_code: int = StandardResponseCode.HTTP_400,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class AccountDisabledError(BaseExceptionError):
    """账号已禁用"""

    def __init__(
        self,
        msg: str = 'Account Disabled',
        code: int = CustomResponseCode.ACCOUNT_DISABLED,
        status_code: int = StandardResponseCode.HTTP_403,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class PasswordNotSetError(BaseExceptionError):
    """密码未设置"""

    def __init__(
        self,
        msg: str = 'Password Not Set',
        code: int = CustomResponseCode.PASSWORD_NOT_SET,
        status_code: int = StandardResponseCode.HTTP_400,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class SMSCodeError(BaseExceptionError):
    """短信验证码错误"""

    def __init__(
        self,
        msg: str = 'SMS Code Error',
        code: int = CustomResponseCode.SMS_CODE_ERROR,
        status_code: int = StandardResponseCode.HTTP_400,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class SMSCodeExpired(BaseExceptionError):
    """短信验证码过期"""

    def __init__(
        self,
        msg: str = 'SMS Code Expired',
        code: int = CustomResponseCode.SMS_CODE_EXPIRED,
        status_code: int = StandardResponseCode.HTTP_400,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class SMSCodeNotSent(BaseExceptionError):
    """短信验证码未发送"""

    def __init__(
        self,
        msg: str = 'SMS Code Not Sent',
        code: int = CustomResponseCode.SMS_CODE_NOT_SENT,
        status_code: int = StandardResponseCode.HTTP_400,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class SMSCodeSendFailed(BaseExceptionError):
    """短信验证码发送失败"""

    def __init__(
        self,
        msg: str = 'SMS Code Send Failed',
        code: int = CustomResponseCode.SMS_CODE_SEND_FAILED,
        status_code: int = StandardResponseCode.HTTP_500,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)


class SMSCodeSendTooFrequently(BaseExceptionError):
    """短信验证码发送过于频繁"""

    def __init__(
        self,
        msg: str = 'SMS Code Send Too Frequently',
        code: int = CustomResponseCode.SMS_CODE_SEND_TOO_FREQUENTLY,
        status_code: int = StandardResponseCode.HTTP_429,
        data: Any = None,
    ):
        super().__init__(msg=msg, code=code, status_code=status_code, data=data)
