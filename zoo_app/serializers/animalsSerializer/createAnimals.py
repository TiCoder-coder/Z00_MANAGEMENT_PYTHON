from rest_framework import serializers
from zoo_app.models.animalsModels import Animal
from zoo_app.models.enclosuresModel import Enclosure
from zoo_app.enums.enums import Gender, HealthStatus
from django.db import transaction
import re
class CreateAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 
                  'name', 
                  'age', 
                  'species', 
                  'gender', 
                  'weight', 
                  'healthStatus', 
                  'enclosureId', 
        read_only_fields = ['createAt', 'updateAt']
        
    def _validate_text_field(self, value, field_name):
        #Kiểm tra xem giá trị có phải là str hay không
        if not isinstance(value, str):
            raise serializers.ValidationError(f"{field_name} must be a string")
        #Kiểm tra xem giá trị có phải bị trống hay không
        if not value or not value.strip(): 
            raise serializers.ValidationError(f"{field_name} cannot be empty")
        #Kiểm tra xem giá trị có số lượng kí tự nằm trong khoảng từ 3-100 không
        if not 3 <= len(value) <= 100:
            raise serializers.ValidationError(f"{field_name} length must be between 3 and 100")
        #Kiểm tra xem giá trị có chỉ chứa chữ cái, số, dấu gạch ngang và dấu gạch dưới không
        if not re.match(r'^[a-zA-Z0-9_\-\s]+$', value):
            raise serializers.ValidationError(f"{field_name} can only contain letters, numbers, spaces, underscores, or hyphens")
        return value.strip()

    def validate_id(self, value):
        """
        Xác thực id động vật
        """
        return self._validate_text_field(value, "Animal ID")

    def validate_name(self, value):
        """
        Xác thực tên động vật
        """
        return self._validate_text_field(value, "Animal name")

    def validate_species(self, value):
        """
        Xác thực loài động vật
        """
        return self._validate_text_field(value, "Species")
    def validate_age(self, value):
        """
        Xác thực tuổi động vật
        """
        if value is None:
            raise serializers.ValidationError("Age cannot be null")
        #Kiểm tra xem tuổi có phải là chữ số không
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError("Animal age must be number")
        #Kiểm tra xem tuổi có phải lớn hơn hoặc bằng 0 hay không
        if not value>=0:
            raise serializers.ValidationError("Animal age cannot negative")
        #Kiểm tra xem tuổi có vượt quá 100 tuổi hay không
        if value>100:
            raise serializers.ValidationError("Animal age cannot exceed 100 years")
        if isinstance(value, float) and len(str(value).split('.')[-1]) > 2:
            raise serializers.ValidationError("Animal age cannot have more than 2 decimal places")
        return value
    def validate_gender(self, value):
        """
        Xác thực giới tính động vật
        """
        if value is None:
            return value
        #Kiểm tra xem giới tính có phải bị trống hay không
        if not value or not value.strip(): 
            raise serializers.ValidationError(f"Gender cannot be empty")
        #Kiểm tra xem giới tính có trong enums hay không
        gender_values=[g.value for g in Gender]
        if value not in gender_values:
            raise serializers.ValidationError(f"Invalid gender. Must be one of: {', '.join(gender_values)}")
        return value.strip()
    def validate_weight(self, value):
        if value is None:
            return value
        #Kiểm tra xem cân nặng có phải là số hay không
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError("Weight must be number")
        #Kiểm tra xem cân nặng có trên 0 hay không
        if value<0:
            raise serializers.ValidationError("Weight cannot negative")
        # Kiểm tra cân nặng động vật không vượt quá 10 tấn
        if value > 10000: 
            raise serializers.ValidationError("Weight cannot exceed 10000 kg")
        # Kiểm tra cân nặng động vật không phải là số thập phân quá phức tạp
        if isinstance(value, float) and len(str(value).split('.')[-1]) > 3:
            raise serializers.ValidationError("Weight cannot have more than 3 decimal places")
        return value
    def validate_healthStatus(self, value):
        if value is None:
            return value
        #Kiểm tra xem tình trạng sức khoẻ có phải bị trống hay không
        if not value or not value.strip(): 
            raise serializers.ValidationError(f"Health status cannot be empty")
        #Kiểm tra xem tình trang sức khoẻ có trong enums hay không
        healthStatus_value=[h.value for h in HealthStatus]
        if value not in healthStatus_value:
            raise serializers.ValidationError(f"Invalid health status. Must be one of: {', '.join(healthStatus_value)}")

        return value.strip()
    def validate_enclosureId(self, value):
        if value is None:
            return value
        value=self._validate_text_field(value, "Enclosure ID")
        try:
            enclosure=Enclosure.objects.get(idEnclosure=value)
            #Kiểm tra xem id chuồng có đang hoạt động không
            if hasattr(enclosure, 'isActive') and enclosure.isActive is False:
                raise serializers.ValidationError("Enclosure is not active")
            #Kiểm tra xem chuồng trại đã đầy hay chưa
            if hasattr(enclosure, 'isFull') and enclosure.isFull is True:
                raise serializers.ValidationError("Enclosure is full")
            # Kiểm tra khí hậu phù hợp với loài động vật
            if hasattr(self.instance, 'species') and hasattr(enclosure, 'climate'):
                # Logic kiểm tra khí hậu phù hợp có thể được thêm vào đây
                pass
        except Enclosure.DoesNotExist:
            raise serializers.ValidationError("Enclosure with this ID does not exist")
        except Exception as e:
            raise serializers.ValidationError(f"Error validating enclosure: {str(e)}")
        return value.strip()
    def validate(self, attrs):
        """
        Xác thực liên kết giữa các trường
        """
        # Lấy giá trị hiện tại từ instance nếu có
        age = getattr(self.instance, 'age', 0) if self.instance else 0
        weight = getattr(self.instance, 'weight', 0) if self.instance else 0
        species = getattr(self.instance, 'species', '') if self.instance else ''
        
        # Xác thực tỷ lệ tuổi vs cân nặng để đảm bảo hợp lý
        if age is not None and weight is not None:
            # Kiểm tra cả hai đều là số hợp lệ
            if age == 0 and weight > 50:  # Động vật non nhỏ không nên quá nặng
                raise serializers.ValidationError("Newborn animals typically weigh less than 50kg")
            
            # Kiểm tra tỷ lệ tuổi và cân nặng hợp lý
            if age > 0 and weight > 0:
                # Tỷ lệ cân nặng/tuổi không nên quá cao (ví dụ: 1000kg/tuổi)
                if weight / age > 1000:
                    raise serializers.ValidationError("Weight to age ratio seems unrealistic")
            
            # Kiểm tra động vật trưởng thành phải có cân nặng đủ
            if age > 5 and weight < 1:
                raise serializers.ValidationError("Adult animals should weigh at least 1kg")
        
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
    def create(self, validated_data):
        """
        Tạo mới bản ghi Animal với kiểm tra chuồng và cập nhật trạng thái liên quan
        """
        if not validated_data:
            raise serializers.ValidationError("Data cannot be null")

        enclosure_id = validated_data.get('enclosureId')

        with transaction.atomic():
            # Tạo mới bản ghi Animal
            animal = Animal.objects.create(**validated_data)

            # Nếu có enclosure, cập nhật số lượng động vật
            if enclosure_id:
                from zoo_app.models import Enclosure
                try:
                    enclosure = Enclosure.objects.get(idEnclosure=enclosure_id)
                    if hasattr(enclosure, 'updateOccupancy'):
                        enclosure.updateOccupancy()
                except Enclosure.DoesNotExist:
                    raise serializers.ValidationError("Enclosure does not exist")

            # Ghi log (nếu có logger)
            # logger.info(f"Animal {animal.id} created in enclosure {enclosure_id}")

        return animal
