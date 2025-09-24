from rest_framework import serializers
from .models import Product, CartItem, Order, OrderItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class CartAddSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        user = self.context['request'].user
        if user.is_anonymous:
            raise serializers.ValidationError("User must be authenticated to add items to cart.")
        product = data['product']
        if product.stock < data['quantity']:
            raise serializers.ValidationError(f"Only {product.stock} items left in stock.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        quantity = validated_data['quantity']

        cart_item, created = CartItem.objects.get_or_create(
            user=user, 
            product=product, 
            defaults={'quantity' : quantity})
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                raise serializers.ValidationError("Cannot add more items than available stock.")
                cart_item.save()
        else:
            cart_item.quantity = quantity

        # Check stock before saving
        if cart_item.quantity > product.stock:
            raise serializers.ValidationError("Cannot add more items than available stock.")

        cart_item.save()
        return cart_item
