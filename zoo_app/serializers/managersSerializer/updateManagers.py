from rest_framework import serializers
from zoo_app.models import Managers
from zoo_app.enums.enums import Role
from django.db import transaction
import re
import string

class UpdateManagersSerializer(serializers.ModelSerializer):
    """
    Serializer để cập nhật nhân viên/quản lý hiện có
    """
    role = serializers.ChoiceField(
        choices=[(role.value, role.value) for role in Role],
        help_text="Role of the manager",
        required=False
    )
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=6,
        help_text="New password for the manager account (optional)"
    )
    
    class Meta:
        """
        Meta class cho UpdateManagersSerializer
        """
        model = Managers
        fields = [
            'name',
            'userName',
            'password',
            'role'
        ]
    
    def validate_name(self, value):
        """
        Xác thực tên nhân viên
        """
        if value is None:
            return value
            
        # Kiểm tra tên nhân viên không trống
        if not value or not value.strip():
            raise serializers.ValidationError("Manager name cannot be empty")
        
        # Kiểm tra tên nhân viên phải ít nhất 2 ký tự
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Manager name must be at least 2 characters long")
        
        # Kiểm tra tên nhân viên không vượt quá 100 ký tự
        if len(value.strip()) > 100:
            raise serializers.ValidationError("Manager name cannot exceed 100 characters")
        
        # Kiểm tra tên nhân viên chỉ chứa chữ cái, số, khoảng trắng và dấu gạch ngang
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', value.strip()):
            raise serializers.ValidationError("Manager name can only contain letters, numbers, spaces, and hyphens")
        
        # Kiểm tra tên nhân viên không bắt đầu hoặc kết thúc bằng khoảng trắng
        if value.strip() != value:
            raise serializers.ValidationError("Manager name cannot start or end with spaces")
        
        return value.strip()
    
    def validate_userName(self, value):
        """
        Xác thực tính duy nhất của tên đăng nhập
        """
        if value is None:
            return value
            
        # Kiểm tra tên đăng nhập không trống
        if not value or not value.strip():
            raise serializers.ValidationError("Username cannot be empty")
        
        # Kiểm tra tên đăng nhập phải ít nhất 3 ký tự
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long")
        
        # Kiểm tra tên đăng nhập không vượt quá 50 ký tự
        if len(value.strip()) > 50:
            raise serializers.ValidationError("Username cannot exceed 50 characters")
        
        # Kiểm tra tên đăng nhập chỉ chứa chữ cái, số và dấu gạch dưới
        if not re.match(r'^[a-zA-Z0-9_]+$', value.strip()):
            raise serializers.ValidationError("Username must contain only letters, numbers, and underscores")
        
        # Kiểm tra tên đăng nhập không bắt đầu bằng số
        if value.strip()[0].isdigit():
            raise serializers.ValidationError("Username cannot start with a number")
        
        # Kiểm tra xem tên đăng nhập có đang được thay đổi và tên đăng nhập mới có tồn tại không
        if hasattr(self, 'instance') and self.instance:
            if self.instance.userName != value.strip():
                if Managers.objects.filter(userName=value.strip()).exists():
                    raise serializers.ValidationError("Username already exists")
        else:
            if Managers.objects.filter(userName=value.strip()).exists():
                raise serializers.ValidationError("Username already exists")
        
        return value.strip()
    
    def validate_password(self, value):
        """
        Xác thực độ mạnh mật khẩu (chỉ khi được cung cấp)
        """
        if value:  # Chỉ kiểm tra nếu mật khẩu được cung cấp
            # Kiểm tra mật khẩu không trống
            if not value.strip():
                raise serializers.ValidationError("Password cannot be empty")
            
            # Kiểm tra mật khẩu phải ít nhất 8 ký tự
            if len(value) < 8:
                raise serializers.ValidationError("Password must be at least 8 characters long")
            
            # Kiểm tra mật khẩu không vượt quá 128 ký tự
            if len(value) > 128:
                raise serializers.ValidationError("Password cannot exceed 128 characters")
            
            # Kiểm tra mật khẩu có chứa ít nhất 1 chữ số
            if not any(c.isdigit() for c in value):
                raise serializers.ValidationError("Password must contain at least one digit")
            
            # Kiểm tra mật khẩu có chứa ít nhất 1 chữ cái
            if not any(c.isalpha() for c in value):
                raise serializers.ValidationError("Password must contain at least one letter")
            
            # Kiểm tra mật khẩu có chứa ít nhất 1 chữ cái viết hoa
            if not any(c.isupper() for c in value):
                raise serializers.ValidationError("Password must contain at least one uppercase letter")
            
            # Kiểm tra mật khẩu có chứa ít nhất 1 chữ cái viết thường
            if not any(c.islower() for c in value):
                raise serializers.ValidationError("Password must contain at least one lowercase letter")
            
            # Kiểm tra mật khẩu có chứa ít nhất 1 ký tự đặc biệt
            if not any(c in string.punctuation for c in value):
                raise serializers.ValidationError("Password must contain at least one special character")
            
            # Kiểm tra mật khẩu không chứa khoảng trắng
            if ' ' in value:
                raise serializers.ValidationError("Password cannot contain spaces")
            
            # Kiểm tra mật khẩu không chứa các ký tự không hợp lệ
            if not re.match(r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]+$', value):
                raise serializers.ValidationError("Password contains invalid characters")
        
        return value
    
    def validate(self, attrs):
        """
        Xác thực liên kết giữa các field
        """
        # Lấy giá trị hiện tại từ instance nếu có
        current_name = getattr(self.instance, 'name', '') if self.instance else ''
        current_username = getattr(self.instance, 'userName', '') if self.instance else ''
        current_role = getattr(self.instance, 'role', None) if self.instance else None
        
        # Sử dụng giá trị mới nếu có, nếu không thì dùng giá trị hiện tại
        name = attrs.get('name', current_name)
        username = attrs.get('userName', current_username)
        role = attrs.get('role', current_role)
        
        # Kiểm tra tính nhất quán giữa tên và username (chỉ khi CẢ HAI đều được update)
        # Chỉ validate nếu CẢ name VÀ username đều có trong attrs (đang được update cùng lúc)
        if 'name' in attrs and 'userName' in attrs and name and username:
            name_parts = name.lower().split()
            username_lower = username.lower()
            
            # Kiểm tra username không chứa tên đầy đủ (bảo mật)
            if len(name_parts) > 1:
                for part in name_parts:
                    if len(part) > 2 and part in username_lower:
                        raise serializers.ValidationError(
                            "Username should not contain full name for security reasons"
                        )
        
        # Kiểm tra password không chứa username hoặc name (security)
        # Chỉ validate khi password được cung cấp
        password = attrs.get('password')
        if password:
            # Kiểm tra với username
            if username and username.lower() in password.lower():
                raise serializers.ValidationError(
                    "Password should not contain username"
                )
            
            # Kiểm tra với name
            if name:
                name_parts = name.lower().split()
                for part in name_parts:
                    if len(part) > 2 and part in password.lower():
                        raise serializers.ValidationError(
                            "Password should not contain parts of your name"
                        )
        
        return attrs
    
    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Cập nhật instance nhân viên hiện có với transaction safety
        """
        # Kiểm tra instance có tồn tại không
        if not instance:
            raise serializers.ValidationError("Manager instance not found")
        
        # Xử lý mật khẩu riêng biệt
        password = validated_data.pop('password', None)
        
        # Cập nhật instance nhân viên hiện có
        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
            else:
                raise serializers.ValidationError(f"Invalid field: {attr}")
        
        # Cập nhật mật khẩu nếu được cung cấp
        if password:
            if hasattr(instance, 'set_password'):
                instance.set_password(password)
            elif hasattr(instance, 'setPassword'):
                instance.setPassword(password)
            else:
                # Fallback - store hashed password if possible
                from django.contrib.auth.hashers import make_password
                instance.password = make_password(password)
        
        # Lưu instance
        instance.save()
        
        # Log thay đổi (có thể thêm vào đây)
        # logger.info(f"Manager {instance.id} updated: {validated_data}")
        
        return instance
