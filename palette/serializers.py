from rest_framework import serializers

from palette.models import ColorPalette, Color


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'hex_code')


class ColorPaletteSerializer(serializers.ModelSerializer):
    dominant_colors = ColorSerializer(many=True, read_only=True, required=False)
    accent_colors = ColorSerializer(many=True, read_only=True, required=False)

    def create(self, validated_data):
        self.instance = super(ColorPaletteSerializer, self).create(validated_data=validated_data)

        if 'dominant_colors' in self.initial_data:
            dominant_color_ids = self.initial_data['dominant_colors']
            dominant_colors = Color.objects.filter(id__in=dominant_color_ids)
            self.instance.dominant_colors.add(*dominant_colors)
        if 'accent_colors' in self.initial_data:
            accent_color_ids = self.initial_data['accent_colors']
            accent_colors = Color.objects.filter(id__in=accent_color_ids)
            self.instance.accent_colors.add(*accent_colors)

        return self.instance

    def update(self, instance, validated_data):
        if 'dominant_colors' in validated_data:
            instance.dominant_colors.clear()
            dominant_color_ids = validated_data['dominant_colors']
            dominant_colors = Color.objects.filter(id__in=dominant_color_ids)
            instance.dominant_colors.add(*dominant_colors)
        if 'accent_colors' in validated_data:
            instance.accent_colors.clear()
            accent_color_ids = validated_data['accent_colors']
            accent_colors = Color.objects.filter(id__in=accent_color_ids)
            instance.accent_colors.add(*accent_colors)
        return instance

    class Meta:
        model = ColorPalette
        fields = ('id', 'user', 'is_private', 'name', 'dominant_colors', 'accent_colors')
