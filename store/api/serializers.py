from rest_framework import serializers
from store.models.product import Product, Color, Size, Category
from store.models.order import Order, Cart

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    picture = serializers.ImageField()
    available_colors = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(), many=True)
    size = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all(), many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'available_colors', 'rating', 'size', 'picture']

    def create(self, validated_data):
        colors_data = validated_data.pop('available_colors')
        size_data = validated_data.pop('size')
        product = Product.objects.create(**validated_data)
        product.available_colors.set(colors_data)
        product.size.set(size_data)
        return product
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        colors = instance.available_colors.all()
        sizes = instance.size.all()
        category = instance.category
        representation['available_colors'] = [{'id': color.id, 'name': color.name} for color in colors]
        representation['size'] = [{'id': size.id, 'name': size.name} for size in sizes]
        representation['category'] = {'id': category.id, 'name': category.name}

        return representation
    

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        user = instance.user
        representation['user'] = {'id': user.id, 'name': user.name}

        return representation