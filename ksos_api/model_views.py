from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from ksos_api.utils import Utils


class MultipleAPIView(APIView):
    serializer = serializers.Serializer
    model = None
    permission_classes = ()

    def get(self, request):
        data = self.model.objects.all()
        return Response(self.serializer(data, many=True).data)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Utils.error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SingleAPIView(APIView):
    serializer = serializers.Serializer
    serializer_for_user = None
    model = None
    permission_classes = ()

    def get(self, request, related_id):
        try:
            data = self.model.objects.get(id=related_id)
            serializer = self.serializer(data)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return Utils.error_response(e.args, status.HTTP_404_NOT_FOUND)

    def patch(self, request, related_id):
        try:
            model = self.model.objects.get(id=related_id)
            if self.serializer_for_user is not None and not request.user.is_staff:
                serializer = self.serializer_for_user(model, data=request.data, partial=True)
            else:
                serializer = self.serializer(model, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Utils.error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Utils.error_response(e.args, status.HTTP_404_NOT_FOUND)

    def delete(self, request, related_id):
        try:
            model = self.model.objects.get(id=related_id)
            model.delete()
            return Response({'id': related_id}, status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Utils.error_response(e.args, status.HTTP_404_NOT_FOUND)


class MultipleRelatedAPIView(APIView):
    serializer = serializers.Serializer
    related_name = None
    model = None
    permission_classes = ()
    order = None

    def get(self, request, related_id):
        kwargs = {self.related_name: related_id}
        data = self.model.objects.filter(**kwargs)
        if self.order is not None:
            data = data.order_by(self.order)
        return Response(self.serializer(data, many=True).data)

    def post(self, request, related_id):
        data = request.data
        data[self.related_name] = related_id
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Utils.error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SingleRelatedAPIView(APIView):
    serializer = serializers.Serializer
    related_name = None
    model = None
    permission_classes = ()

    def get(self, request, related_id, model_id):
        try:
            kwargs = {self.related_name: related_id, 'id': model_id}
            model = self.model.objects.get(**kwargs)
            return Response(self.serializer(model).data)
        except ObjectDoesNotExist as e:
            return Utils.error_response(e.args, status.HTTP_404_NOT_FOUND)

    def patch(self, request, related_id, model_id):
        try:
            kwargs = {self.related_name: related_id, 'id': model_id}
            model = self.model.objects.get(**kwargs)
            serializer = self.serializer(model, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Utils.error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist as e:
            return Utils.error_response(e.args, status.HTTP_404_NOT_FOUND)

    def delete(self, request, related_id, model_id):
        try:
            kwargs = {self.related_name: related_id, 'id': model_id}
            model = self.model.objects.get(**kwargs)
            model.delete()
            return Response({'id': model_id}, status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Utils.error_response(e.args, status.HTTP_404_NOT_FOUND)
