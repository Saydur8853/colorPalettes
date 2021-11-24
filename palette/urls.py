from django.urls import path, include

from palette.views import ColorPaletteAPIView, ColorAPIView

urlpatterns = [
    path('api/user/', include('user.urls')),
    path('api/color/', ColorAPIView.as_view(), name='color_palette_create_view'),
    path('api/pallete/', ColorPaletteAPIView.as_view(), name='color_palette_create_view'),
    path('api/pallete/<int:palette_id>', ColorPaletteAPIView.as_view(), name='color_palette_detail_update_delete_view'),
]