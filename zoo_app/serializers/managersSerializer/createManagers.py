from rest_framework import serializers
from zoo_app.models.managersModel import Manager
from django.contrib.auth.hashers import make_password
class CreateManagersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields=[
            'id',
            'name',
            'userName',
            'password',
            'role'
        ]
    id=serializers.CharField(min_length=3, max_length=100, required=True, help_text="Mã định danh của người quản lý")
    name=serializers.CharField(min_length=3, max_length=100, required=True, help_text="Tên người quản lý")
    userName=serializers.CharField(min_length=3, max_length=100, required=True, help_text="Tên đăng nhập của người quản lý")
    password=serializers.CharField(min_length=3, max_length=255, required=True, write_only=True, help_text="Mật khẩu")
    role=serializers.ChoiceField(choices=Manager.choices(), required=True, help_text="Vai trò của người quản lý")
    # Kiểm tra trùng userName
    def validate_userName(self, value):
        if Manager.objects.filter(userName__iexact=value).exists():
            raise serializers.ValidationError("This username already exists.")
        return value

    # Mã hóa mật khẩu trước khi lưu
    def Encrypt_passwords(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    # Kiểm tra vai trò
    def validate_role(self, value):
        if value not in [choice[0] for choice in Manager.RoleChoices.choices]:
            raise serializers.ValidationError("Invalid role.")
        return value
