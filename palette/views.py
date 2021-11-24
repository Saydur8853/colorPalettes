from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response

from palette.models import ColorPalette
from palette.serializers import ColorPaletteSerializer, ColorSerializer


class ColorAPIView(generics.GenericAPIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    serializer_class = ColorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {
            "data": serializer.data,
            "message": "Request processed successfully",
            "success": True
        }
        return Response(data=response_data, status=status.HTTP_200_OK)


class ColorPaletteAPIView(ListAPIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    serializer_class = ColorPaletteSerializer
    queryset = ColorPalette.objects.all()

    def get_queryset(self):
        queryset = super(ColorPaletteAPIView, self).get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return queryset.filter(is_private=False)
        return queryset

    def get(self, request, *args, **kwargs):
        palette_id = self.kwargs.get('palette_id', None)
        if palette_id:
            try:
                color_palette = ColorPalette.objects.get(id=palette_id)
                serializer = self.serializer_class(color_palette, many=False)
                response_data = serializer.data
            except ColorPalette.DoesNotExist:
                response = {
                    "message": "No color palette found for given id.",
                    "success": False
                }
                return Response(data=response, status=status.HTTP_404_NOT_FOUND)
        else:
            response_data = super(ColorPaletteAPIView, self).get(request, *args, **kwargs).data
        return Response(data=response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            response = {
                "message": "User do not have permission to perform this action.",
                "success": False
            }
            return Response(data=response, status=status.HTTP_401_UNAUTHORIZED)

        request_data = request.data
        request_data['user'] = user.pk
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "data": serializer.data,
                "message": "Request processed successfully",
                "success": True
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        response_data = {
            "message": serializer.errors,
            "success": False
        }
        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        palette_id = self.kwargs.get('palette_id', None)
        if not palette_id:
            response = {
                "message": "Invalid request",
                "success": False
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        try:
            palette = ColorPalette.objects.get(id=palette_id)
        except ColorPalette.DoesNotExist:
            response = {
                "message": "Rent doesn't exist",
                "success": False
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated or request.user != palette.user:
            response = {
                "message": "User do not have permission to perform this action.",
                "success": False
            }
            return Response(data=response, status=status.HTTP_401_UNAUTHORIZED)

        request_data = request.data
        serializer = self.serializer_class(palette, data=request_data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "data": serializer.data,
                "message": "Request processed successfully",
                "success": True
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        response_data = {
            "message": serializer.errors,
            "success": False
        }
        return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
