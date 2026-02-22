from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from health.serializers import HealthSerializer
class HealthView(APIView):
    permission_classes = []
    queryset = None
    serializer_class = HealthSerializer
    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)