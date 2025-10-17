from rest_framework import serializers
from zoo_app.models import Enclosures
from zoo_app.enums.enums import Climate
from django.db import transaction
import re

class UpdateEnclosuresSerializer(serializers.ModelSerializer):
    """
    Serializer để cập nhật chuồng trại hiện có
    """
    climate = serializers.ChoiceField(
        choices=[(climate.value, climate.value) for climate in Climate],
        help_text="Climate type of the enclosure",
        required=False
    )
    
    class Meta:
        """
        Meta class cho UpdateEnclosuresSerializer
        """
        model = Enclosures
        fields = [
            'nameEnclosure', 
            'areaSize',
            'climate',
            'capacity'
        ]
    
    def validate_nameEnclosure(self, value):
        """
        Xác thực tên chuồng trại
        """
        if value is None:
            return value
            
        # Kiểm tra tên chuồng trại không trống
        if not value or not value.strip():
            raise serializers.ValidationError("Enclosure name cannot be empty")
        
        # Kiểm tra tên chuồng trại phải ít nhất 2 ký tự
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Enclosure name must be at least 2 characters long")
        
        # Kiểm tra tên chuồng trại không vượt quá 100 ký tự
        if len(value.strip()) > 100:
            raise serializers.ValidationError("Enclosure name cannot exceed 100 characters")
        
        # Kiểm tra tên chuồng trại chỉ chứa chữ cái, số, khoảng trắng và dấu gạch ngang
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', value.strip()):
            raise serializers.ValidationError("Enclosure name can only contain letters, numbers, spaces, and hyphens")
        
        # Kiểm tra tên chuồng trại không bắt đầu hoặc kết thúc bằng khoảng trắng
        if value.strip() != value:
            raise serializers.ValidationError("Enclosure name cannot start or end with spaces")
        
        # Kiểm tra tên chuồng trại không trùng lặp (trừ khi đang cập nhật chính nó)
        if hasattr(self, 'instance') and self.instance:
            if self.instance.nameEnclosure != value.strip():
                if Enclosures.objects.filter(nameEnclosure=value.strip()).exists():
                    raise serializers.ValidationError("Enclosure name already exists")
        else:
            if Enclosures.objects.filter(nameEnclosure=value.strip()).exists():
                raise serializers.ValidationError("Enclosure name already exists")
        
        return value.strip()
    
    def validate_areaSize(self, value):
        """
        Xác thực định dạng kích thước khu vực
        """
        if value is None:
            return value
            
        # Kiểm tra kích thước khu vực không trống
        if not value or not value.strip():
            raise serializers.ValidationError("Area size cannot be empty")
        
        # Kiểm tra kích thước khu vực phải ít nhất 2 ký tự
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Area size must be at least 2 characters long")
        
        # Kiểm tra kích thước khu vực không vượt quá 200 ký tự
        if len(value.strip()) > 200:
            raise serializers.ValidationError("Area size cannot exceed 200 characters")
        
        # Kiểm tra kích thước khu vực chỉ chứa chữ cái, số, khoảng trắng, dấu gạch ngang và dấu phẩy
        if not re.match(r'^[a-zA-Z0-9\s\-,.]+$', value.strip()):
            raise serializers.ValidationError("Area size can only contain letters, numbers, spaces, hyphens, commas, and periods")
        
        # Kiểm tra kích thước khu vực không bắt đầu hoặc kết thúc bằng khoảng trắng
        if value.strip() != value:
            raise serializers.ValidationError("Area size cannot start or end with spaces")
        
        return value.strip()
    
    def validate_climate(self, value):
        """
        Xác thực loại khí hậu
        """
        if value is None:
            return value
        
        # Kiểm tra giá trị có trong enum
        valid_climates = [climate.value for climate in Climate]
        if value not in valid_climates:
            raise serializers.ValidationError(
                f"Climate must be one of: {', '.join(valid_climates)}"
            )
        
        return value
    
    def validate_capacity(self, value):
        """
        Xác thực giá trị sức chứa
        """
        if value is None:
            return value
            
        # Kiểm tra sức chứa là số
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError("Capacity must be a number")
        
        # Kiểm tra sức chứa không âm
        if value <= 0:
            raise serializers.ValidationError("Capacity must be greater than 0")
        
        # Kiểm tra sức chứa không vượt quá 1000
        if value > 1000:
            raise serializers.ValidationError("Capacity cannot exceed 1000")
        
        # Chuyển thành số nguyên (tự động convert decimal)
        # Round down để đảm bảo không vượt quá capacity thực tế
        value = int(value)
        
        # Kiểm tra xem việc giảm sức chứa có gây ra tình trạng quá tải không
        if hasattr(self, 'instance') and self.instance:
            try:
                # Kiểm tra occupancy nếu có method
                if hasattr(self.instance, 'getCurrentOccupancy'):
                    current_occupancy = self.instance.getCurrentOccupancy()
                    if value < current_occupancy:
                        raise serializers.ValidationError(
                            f"Cannot reduce capacity below current occupancy ({current_occupancy})"
                        )
                # Nếu không có method, đếm số động vật trong chuồng
                elif hasattr(self.instance, 'idEnclosure'):
                    from zoo_app.models import Animals
                    current_count = Animals.objects.filter(
                        enclosureId=self.instance.idEnclosure
                    ).count()
                    if value < current_count:
                        raise serializers.ValidationError(
                            f"Cannot reduce capacity below current animal count ({current_count})"
                        )
            except serializers.ValidationError:
                raise
            except Exception as e:
                # Log error but don't fail validation
                pass
        
        return value
    
    def validate(self, attrs):
        """
        Xác thực liên kết giữa các trường
        """
        # Lấy giá trị hiện tại từ instance nếu có
        current_climate = getattr(self.instance, 'climate', None) if self.instance else None
        current_area_size = getattr(self.instance, 'areaSize', '') if self.instance else ''
        current_capacity = getattr(self.instance, 'capacity', 0) if self.instance else 0
        
        # Sử dụng giá trị mới nếu có, nếu không thì dùng giá trị hiện tại
        climate = attrs.get('climate', current_climate)
        area_size = attrs.get('areaSize', current_area_size)
        capacity = attrs.get('capacity', current_capacity)
        
        # Xác thực khí hậu phù hợp với yêu cầu kích thước khu vực
        if climate and area_size:
            area_size_lower = area_size.lower()
            
            if climate == Climate.AQUATIC.value:
                water_keywords = ['water', 'pool', 'pond', 'lake', 'river', 'aquatic']
                if not any(keyword in area_size_lower for keyword in water_keywords):
                    raise serializers.ValidationError(
                        "Aquatic enclosures should have water features mentioned in area size"
                    )
            
            elif climate == Climate.DESERT.value:
                desert_keywords = ['sand', 'desert', 'dry', 'arid', 'cactus']
                if not any(keyword in area_size_lower for keyword in desert_keywords):
                    raise serializers.ValidationError(
                        "Desert enclosures should have desert features mentioned in area size"
                    )
            
            elif climate == Climate.TROPICAL.value:
                tropical_keywords = ['tropical', 'rainforest', 'jungle', 'humid', 'trees']
                if not any(keyword in area_size_lower for keyword in tropical_keywords):
                    raise serializers.ValidationError(
                        "Tropical enclosures should have tropical features mentioned in area size"
                    )
        
        # Kiểm tra tính nhất quán giữa sức chứa và kích thước khu vực
        if capacity and area_size:
            # Logic kiểm tra sức chứa phù hợp với kích thước
            if capacity > 100 and 'small' in area_size.lower():
                raise serializers.ValidationError(
                    "Large capacity not suitable for small area"
                )
            elif capacity < 10 and 'large' in area_size.lower():
                raise serializers.ValidationError(
                    "Small capacity not suitable for large area"
                )
        
        return attrs
    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Cập nhật instance chuồng trại hiện có với transaction safety
        """
        # Kiểm tra instance có tồn tại không
        if not instance:
            raise serializers.ValidationError("Enclosure instance not found")
        
        # Cập nhật instance chuồng trại hiện có
        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
            else:
                raise serializers.ValidationError(f"Invalid field: {attr}")
        
        # Lưu instance
        instance.save()
        
        # Log thay đổi (có thể thêm vào đây)
        # logger.info(f"Enclosure {instance.idEnclosure} updated: {validated_data}")
        
        return instance
