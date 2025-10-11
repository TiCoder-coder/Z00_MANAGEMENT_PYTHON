from rest_framework import serializers
from zoo_app.models import Animals
from zoo_app.enums.enums import Gender, HealthStatus
from django.db import transaction
import re

class UpdateAnimalsSerializer(serializers.ModelSerializer):
    """
    Serializer để cập nhật động vật hiện có
    """
    gender = serializers.ChoiceField(
        choices=[(gender.value, gender.value) for gender in Gender],
        help_text="Gender of the animal",
        required=False
    )
    healthStatus = serializers.ChoiceField(
        choices=[(status.value, status.value) for status in HealthStatus],
        help_text="Health status of the animal",
        required=False
    )
    
    class Meta:
        """
        Meta class cho UpdateAnimalsSerializer
        """
        model = Animals
        fields = [
            'name',
            'age',
            'species',
            'gender',
            'weight',
            'healthStatus',
            'enclosureId'
        ]
    
    def validate_name(self, value):
        """
        Xác thực tên động vật
        """
        if value is None:
            return value
            
        # Kiểm tra tên động vật không trống
        if not value or not value.strip():
            raise serializers.ValidationError("Animal name cannot be empty")
        
        # Kiểm tra tên động vật phải ít nhất 2 ký tự
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Animal name must be at least 2 characters long")
        
        # Kiểm tra tên động vật không vượt quá 100 ký tự
        if len(value.strip()) > 100:
            raise serializers.ValidationError("Animal name cannot exceed 100 characters")
        
        # Kiểm tra tên động vật chỉ chứa chữ cái, số, khoảng trắng và dấu gạch ngang
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', value.strip()):
            raise serializers.ValidationError("Animal name can only contain letters, numbers, spaces, and hyphens")
        
        # Kiểm tra tên động vật không bắt đầu hoặc kết thúc bằng khoảng trắng
        if value.strip() != value:
            raise serializers.ValidationError("Animal name cannot start or end with spaces")
        
        return value.strip()
    
    def validate_age(self, value):
        """
        Xác thực tuổi động vật
        """
        if value is None:
            return value
            
        # Kiểm tra tuổi động vật là số
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError("Age must be a number")
        
        # Kiểm tra tuổi động vật không âm
        if value < 0:
            raise serializers.ValidationError("Age cannot be negative")
        
        # Kiểm tra tuổi động vật không vượt quá 100 tuổi
        if value > 100:
            raise serializers.ValidationError("Age cannot exceed 100 years")
        
        # Kiểm tra tuổi động vật không phải là số thập phân quá phức tạp
        if isinstance(value, float) and len(str(value).split('.')[-1]) > 2:
            raise serializers.ValidationError("Age cannot have more than 2 decimal places")
        
        return value
    
    def validate_gender(self, value):
        """
        Xác thực giới tính
        """
        if value is None:
            return value
        
        # Kiểm tra giá trị có trong enum
        valid_genders = [gender.value for gender in Gender]
        if value not in valid_genders:
            raise serializers.ValidationError(
                f"Gender must be one of: {', '.join(valid_genders)}"
            )
        
        return value
    
    def validate_healthStatus(self, value):
        """
        Xác thực tình trạng sức khỏe
        """
        if value is None:
            return value
        
        # Kiểm tra giá trị có trong enum
        valid_statuses = [status.value for status in HealthStatus]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Health status must be one of: {', '.join(valid_statuses)}"
            )
        
        return value
    
    def validate_species(self, value):
        """
        Xác thực tên loài
        """
        if value is None:
            return value
            
        # Kiểm tra tên loài không trống
        if not value or not value.strip():
            raise serializers.ValidationError("Species cannot be empty")
        
        # Kiểm tra tên loài phải ít nhất 2 ký tự
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Species must be at least 2 characters long")
        
        # Kiểm tra tên loài không vượt quá 50 ký tự
        if len(value.strip()) > 50:
            raise serializers.ValidationError("Species cannot exceed 50 characters")
        
        # Kiểm tra tên loài chỉ chứa chữ cái, số, khoảng trắng và dấu gạch ngang
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', value.strip()):
            raise serializers.ValidationError("Species can only contain letters, numbers, spaces, and hyphens")
        
        return value.strip()
    
    def validate_weight(self, value):
        """
        Xác thực cân nặng động vật
        """
        if value is None:
            return value
            
        # Kiểm tra cân nặng động vật là số
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError("Weight must be a number")
        
        # Kiểm tra cân nặng động vật không âm
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0")
        
        # Kiểm tra cân nặng động vật không vượt quá 10 tấn
        if value > 10000:  # 10 tons max
            raise serializers.ValidationError("Weight cannot exceed 10000 kg")
        
        # Kiểm tra cân nặng động vật không phải là số thập phân quá phức tạp
        if isinstance(value, float) and len(str(value).split('.')[-1]) > 3:
            raise serializers.ValidationError("Weight cannot have more than 3 decimal places")
        
        return value
    
    def validate_enclosureId(self, value):
        """
        Xác thực ID chuồng trại tồn tại và có sức chứa
        """
        if value is None:
            return value
            
        from zoo_app.models import Enclosures
        
        # Kiểm tra ID chuồng trại không trống
        if not value or not value.strip():
            raise serializers.ValidationError("Enclosure ID cannot be empty")
        
        # Kiểm tra ID chuồng trại có định dạng hợp lệ
        if not re.match(r'^[a-zA-Z0-9\-_]+$', value.strip()):
            raise serializers.ValidationError("Enclosure ID can only contain letters, numbers, hyphens, and underscores")
        
        try:
            enclosure = Enclosures.objects.get(idEnclosure=value)
            
            # Kiểm tra chuồng trại có đang hoạt động không
            if hasattr(enclosure, 'isActive') and enclosure.isActive is False:
                raise serializers.ValidationError("Enclosure is not active")
            
            # Kiểm tra xem có di chuyển sang chuồng khác không
            if hasattr(self, 'instance') and self.instance:
                if self.instance.enclosureId != value:
                    # Di chuyển sang chuồng khác, kiểm tra sức chứa
                    if hasattr(enclosure, 'isFull') and enclosure.isFull():
                        raise serializers.ValidationError(
                            f"Enclosure {enclosure.nameEnclosure} is at full capacity"
                        )
                    
                    # Kiểm tra khí hậu phù hợp với loài động vật
                    if hasattr(self.instance, 'species') and hasattr(enclosure, 'climate'):
                        # Logic kiểm tra khí hậu phù hợp có thể được thêm vào đây
                        pass
            
        except Enclosures.DoesNotExist:
            raise serializers.ValidationError("Enclosure with this ID does not exist")
        except Exception as e:
            raise serializers.ValidationError(f"Error validating enclosure: {str(e)}")
        
        return value.strip()
    
    def validate(self, attrs):
        """
        Xác thực liên kết giữa các trường
        """
        # Lấy giá trị hiện tại từ instance nếu có
        current_age = getattr(self.instance, 'age', 0) if self.instance else 0
        current_weight = getattr(self.instance, 'weight', 0) if self.instance else 0
        current_species = getattr(self.instance, 'species', '') if self.instance else ''
        
        # Sử dụng giá trị mới nếu có, nếu không thì dùng giá trị hiện tại
        age = attrs.get('age', current_age)
        weight = attrs.get('weight', current_weight)
        species = attrs.get('species', current_species)
        
        # Xác thực tỷ lệ tuổi vs cân nặng để đảm bảo hợp lý
        if age is not None and weight is not None:
            # Kiểm tra cả hai đều là số hợp lệ
            if age == 0 and weight > 50:  # Động vật non nhỏ không nên quá nặng
                raise serializers.ValidationError(
                    "Newborn animals typically weigh less than 50kg"
                )
            
            # Kiểm tra tỷ lệ tuổi và cân nặng hợp lý
            if age > 0 and weight > 0:
                # Tỷ lệ cân nặng/tuổi không nên quá cao (ví dụ: 1000kg/tuổi)
                if weight / age > 1000:
                    raise serializers.ValidationError(
                        "Weight to age ratio seems unrealistic"
                    )
            
            # Kiểm tra động vật trưởng thành phải có cân nặng đủ
            if age > 5 and weight < 1:
                raise serializers.ValidationError(
                    "Adult animals should weigh at least 1kg"
                )
        
        # Kiểm tra tính nhất quán của dữ liệu về tuổi thọ theo loài
        if species and age is not None:
            # Một số loài có tuổi thọ tối đa khác nhau
            species_lower = species.lower()
            
            # Dictionary định nghĩa tuổi thọ tối đa cho các loài
            max_ages = {
                'elephant': 70,
                'lion': 25,
                'tiger': 26,
                'bear': 40,
                'turtle': 150,
                'tortoise': 150,
                'parrot': 80,
                'eagle': 30,
                'monkey': 40,
                'gorilla': 50,
                'dog': 20,
                'cat': 20,
                'rabbit': 12,
                'hamster': 4
            }
            
            for animal_type, max_age in max_ages.items():
                if animal_type in species_lower and age > max_age:
                    raise serializers.ValidationError(
                        f"{animal_type.capitalize()}s typically don't live beyond {max_age} years"
                    )
        
        return attrs
    
    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Cập nhật instance động vật hiện có với transaction safety
        """
        # Kiểm tra instance có tồn tại không
        if not instance:
            raise serializers.ValidationError("Animal instance not found")
        
        # Lưu ID chuồng cũ nếu đang thay đổi chuồng
        old_enclosure_id = instance.enclosureId if hasattr(instance, 'enclosureId') else None
        new_enclosure_id = validated_data.get('enclosureId', old_enclosure_id)
        
        # Cập nhật instance động vật hiện có
        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
            else:
                raise serializers.ValidationError(f"Invalid field: {attr}")
        
        # Lưu instance
        instance.save()
        
        # Nếu thay đổi chuồng, cập nhật số lượng động vật trong chuồng cũ và mới
        if old_enclosure_id and new_enclosure_id and old_enclosure_id != new_enclosure_id:
            from zoo_app.models import Enclosures
            try:
                # Cập nhật chuồng cũ (giảm số lượng)
                old_enclosure = Enclosures.objects.get(idEnclosure=old_enclosure_id)
                if hasattr(old_enclosure, 'updateOccupancy'):
                    old_enclosure.updateOccupancy()
                
                # Cập nhật chuồng mới (tăng số lượng)
                new_enclosure = Enclosures.objects.get(idEnclosure=new_enclosure_id)
                if hasattr(new_enclosure, 'updateOccupancy'):
                    new_enclosure.updateOccupancy()
            except Enclosures.DoesNotExist:
                pass  # Enclosure validation already done in validate_enclosureId
        
        # Log thay đổi (có thể thêm vào đây)
        # logger.info(f"Animal {instance.id} updated: {validated_data}")
        
        return instance
