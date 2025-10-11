from rest_framework import serializers
from zoo_app.models import Foods
from zoo_app.enums.enums import TypeFood
from django.db import transaction
import re

class UpdateFoodsSerializer(serializers.ModelSerializer):
    """
    Serializer để cập nhật thức ăn hiện có
    """
    typeFood = serializers.ChoiceField(
        choices=[(food_type.value, food_type.value) for food_type in TypeFood],
        help_text="Type of food",
        required=False
    )
    
    class Meta:
        """
        Meta class cho UpdateFoodsSerializer
        """
        model = Foods
        fields = [
            'nameFood',
            'typeFood',
            'caloriesPerUnit'
        ]
    
    def validate_nameFood(self, value):
        """
        Xác thực tên thức ăn
        """
        if value is None:
            return value
            
        # Kiểm tra tên thức ăn không trống
        if not value or not value.strip():
            raise serializers.ValidationError("Food name cannot be empty")
        
        # Kiểm tra tên thức ăn phải ít nhất 2 ký tự
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Food name must be at least 2 characters long")
        
        # Kiểm tra tên thức ăn không vượt quá 100 ký tự
        if len(value.strip()) > 100:
            raise serializers.ValidationError("Food name cannot exceed 100 characters")
        
        # Kiểm tra tên thức ăn chỉ chứa chữ cái, số, khoảng trắng và dấu gạch ngang
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', value.strip()):
            raise serializers.ValidationError("Food name can only contain letters, numbers, spaces, and hyphens")
        
        # Kiểm tra tên thức ăn không bắt đầu hoặc kết thúc bằng khoảng trắng
        if value.strip() != value:
            raise serializers.ValidationError("Food name cannot start or end with spaces")
        
        # Kiểm tra tên thức ăn không trùng lặp (trừ khi đang cập nhật chính nó)
        if hasattr(self, 'instance') and self.instance:
            if self.instance.nameFood != value.strip():
                if Foods.objects.filter(nameFood=value.strip()).exists():
                    raise serializers.ValidationError("Food name already exists")
        else:
            if Foods.objects.filter(nameFood=value.strip()).exists():
                raise serializers.ValidationError("Food name already exists")
        
        return value.strip()
    
    def validate_caloriesPerUnit(self, value):
        """
        Xác thực calo trên mỗi đơn vị
        """
        if value is None:
            return value
            
        # Kiểm tra calo trên mỗi đơn vị là số
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError("Calories per unit must be a number")
        
        # Kiểm tra calo trên mỗi đơn vị không âm
        if value <= 0:
            raise serializers.ValidationError("Calories per unit must be greater than 0")
        
        # Kiểm tra calo trên mỗi đơn vị không vượt quá 1000
        if value > 1000:
            raise serializers.ValidationError("Calories per unit cannot exceed 1000")
        
        # Kiểm tra calo trên mỗi đơn vị không phải là số thập phân quá phức tạp
        if isinstance(value, float) and len(str(value).split('.')[-1]) > 2:
            raise serializers.ValidationError("Calories per unit cannot have more than 2 decimal places")
        
        return value
    
    def validate(self, attrs):
        """
        Xác thực liên kết giữa các trường
        """
        # Lấy giá trị hiện tại từ instance nếu có
        current_type = getattr(self.instance, 'typeFood', None) if self.instance else None
        current_name = getattr(self.instance, 'nameFood', '') if self.instance else ''
        current_calories = getattr(self.instance, 'caloriesPerUnit', 0) if self.instance else 0
        
        # Sử dụng giá trị mới nếu có, nếu không thì dùng giá trị hiện tại
        food_type = attrs.get('typeFood', current_type)
        food_name = attrs.get('nameFood', current_name)
        calories = attrs.get('caloriesPerUnit', current_calories)
        
        # Kiểm tra tính nhất quán giữa loại thức ăn và tên (nếu cả hai đều có)
        if food_type and food_name:
            food_name_lower = food_name.lower()
            
            # Kiểm tra loại thức ăn phù hợp với tên (warning-level check)
            # These are suggestions, not strict requirements
            if food_type == TypeFood.MEAT.value:
                meat_keywords = ['meat', 'beef', 'chicken', 'pork', 'lamb', 'turkey', 'duck', 'venison', 'rabbit']
                # Soft check - just ensure it's not obviously wrong
                plant_keywords = ['vegetable', 'fruit', 'grain', 'plant', 'grass', 'leaf']
                if any(plant in food_name_lower for plant in plant_keywords):
                    raise serializers.ValidationError(
                        "Meat type food should not have plant-related names"
                    )
            
            elif food_type == TypeFood.PLANT.value:
                plant_keywords = ['plant', 'vegetable', 'fruit', 'leaf', 'grass', 'carrot', 'lettuce', 
                                 'spinach', 'broccoli', 'cabbage', 'apple', 'banana', 'berry', 'hay']
                meat_keywords = ['meat', 'beef', 'chicken', 'pork', 'fish']
                if any(meat in food_name_lower for meat in meat_keywords):
                    raise serializers.ValidationError(
                        "Plant type food should not have meat-related names"
                    )
            
            elif food_type == TypeFood.FISH.value:
                fish_keywords = ['fish', 'salmon', 'tuna', 'trout', 'mackerel', 'sardine', 'seafood']
                # Soft validation
                pass
            
            elif food_type == TypeFood.INSECT.value:
                insect_keywords = ['insect', 'cricket', 'mealworm', 'grasshopper', 'beetle', 'larvae', 'worm']
                # Soft validation
                pass
        
        # Kiểm tra tính hợp lý giữa loại thức ăn và calories
        if food_type and calories:
            # Meat typically has higher calories
            if food_type == TypeFood.MEAT.value and calories < 50:
                raise serializers.ValidationError(
                    "Meat typically has at least 50 calories per unit"
                )
            # Insects typically have moderate calories
            elif food_type == TypeFood.INSECT.value and calories > 500:
                raise serializers.ValidationError(
                    "Insect food typically has less than 500 calories per unit"
                )
        
        return attrs
    
    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Cập nhật instance thức ăn hiện có với transaction safety
        """
        # Kiểm tra instance có tồn tại không
        if not instance:
            raise serializers.ValidationError("Food instance not found")
        
        # Cập nhật instance thức ăn hiện có
        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
            else:
                raise serializers.ValidationError(f"Invalid field: {attr}")
        
        # Lưu instance
        instance.save()
        
        # Log thay đổi (có thể thêm vào đây)
        # logger.info(f"Food {instance.idFood} updated: {validated_data}")
        
        return instance
