from rest_framework import serializers

from backend.movie.models import Category, Movie

# class CategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=30)

#     def create(self, validated_data):
#         """
#         Create and return a new `Category` instance, given the validated data.
#         Cria e retorna uma nova instância `Category`, de acordo com os dados validados.
#         :param validated_data:
#         """
#         return Category.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Category` instance, given the validated data.
#         Atualiza e retorna uma instância `Category` existente, de acordo com os dados validados.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.save()
#         return instance


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title',)


# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=30)
#     sinopse = serializers.CharField(max_length=255)
#     rating = serializers.IntegerField()
#     like = serializers.BooleanField(default=False)
#     category = CategorySerializer()

#     def create(self, validated_data):
#         """
#         Create and return a new `Movie` instance, given the validated data.
#         Cria e retorna uma nova instância `Movie`, de acordo com os dados validados.
#         :param validated_data:
#         """
#         category_data = {}
#         if 'category' in validated_data:
#             category_data = validated_data.pop('category')

#         if category_data:
#             category = Category.objects.create(**category_data)
#             movie = Movie.objects.create(category=category, **validated_data)
#         else:
#             movie = Movie.objects.create(**validated_data)

#         return movie

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Movie` instance, given the validated data.
#         Atualiza e retorna uma instância `Movie` existente, de acordo com os dados validados.
#         """
#         if 'category' in validated_data:
#             category_data = validated_data.pop('category')
#             title = category_data.get('title')
#             category, _ = Category.objects.get_or_create(title=title)
#             # Atualiza a categoria
#             instance.category = category

#         # Atualiza a instância
#         instance.title = validated_data.get('title', instance.title)
#         instance.sinopse = validated_data.get('sinopse', instance.sinopse)
#         instance.rating = validated_data.get('rating', instance.rating)
#         instance.like = validated_data.get('like', instance.like)
#         instance.save()

#         return instance


def positive_only_validator(value):
    if value == 0:
        raise serializers.ValidationError('Zero não é um valor permitido.')


class MovieSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)
    censure = serializers.IntegerField(min_value=0, validators=[positive_only_validator])

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'sinopse',
            'rating',
            'censure',
            'like',
            'created',
            'category'
        )
        # depth = 1

    # def validate_title(self, value):
    #     if 'lorem' in value.lower():
    #         raise serializers.ValidationError('Lorem não pode.')
    #     return value

    def validate(self, data):
        if 'lorem' in data['title'].lower():
            raise serializers.ValidationError('Lorem não pode.')
        return data

    def create(self, validated_data):
        """
        Create and return a new `Movie` instance, given the validated data.
        Cria e retorna uma nova instância `Movie`, de acordo com os dados validados.
        :param validated_data:
        """
        category_data = {}
        if 'category' in validated_data:
            category_data = validated_data.pop('category')

        if category_data:
            category, _ = Category.objects.get_or_create(**category_data)
            movie = Movie.objects.create(category=category, **validated_data)
        else:
            movie = Movie.objects.create(**validated_data)

        return movie

    def update(self, instance, validated_data):
        """
        Update and return an existing `Movie` instance, given the validated data.
        Atualiza e retorna uma instância `Movie` existente, de acordo com os dados validados.
        """
        if 'category' in validated_data:
            category_data = validated_data.pop('category')
            title = category_data.get('title')
            category, _ = Category.objects.get_or_create(title=title)
            # Atualiza a categoria
            instance.category = category

        # Atualiza a instância
        instance.title = validated_data.get('title', instance.title)
        instance.sinopse = validated_data.get('sinopse', instance.sinopse)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.like = validated_data.get('like', instance.like)
        instance.save()

        return instance


class MovieReadOnlySerializer(serializers.ModelSerializer):
    # category = CategorySerializer(required=False)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'sinopse', 'rating', 'like', 'created')
        read_only_fields = fields