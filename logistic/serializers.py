from rest_framework import serializers
from logistic.models import Product, StockProduct, Stock

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']

class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    # настройте сериализатор для склада
    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for i in positions:
            new_product = StockProduct.objects.create(product=i['product'], stock=stock, quantity=i['quantity'],
                                                           price=i['price'], positions=positions)
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for i in positions:
            StockProduct.objects.update_or_create(defaults={'quantity': i['quantity'], 'price': i['price']},
                                                  product=i['product'], stock=stock)
        return stock

    class Meta:
        model = Stock
        fields = ['address', 'products']
