from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User,Document
from .serializers import UserSerializer, DocumentSerializer


# Create your views here.

class UserRegistrationView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()


        response_data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "image": user.imageURL,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

#
# class UserLoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CreateDocumentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class GetUser(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#
#         all_users = User.objects.all()
#         serializer = UserSerializer(all_users, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class logoutview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class getdoc(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get (self,request):
        documents = Document.objects.filter(user=request.user)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


class DocEdit(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        doc_id = request.data.get('id')
        content = request.data.get('content')
        title = request.data.get('title')
        try:
            doc = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=404)

        doc.content = content
        doc.title = title
        doc.save()

        return Response({"message": "Document edited successfully"})

class GetDocByIdAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, document_id):  # Accept document_id parameter
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocSearch(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        filter_string = request.query_params.get('query')  # Use query_params instead of data for GET requests

        if filter_string is not None:
            # Filter the queryset based on the filter string
            queryset = Document.objects.filter(title__icontains=filter_string)

            # Serialize the queryset
            serializer = DocumentSerializer(queryset, many=True)

            # Return the serialized data
            return Response(serializer.data)
        else:
            # Handle the case where no query parameter is provided
            return Response({"error": "No query parameter provided"}, status=status.HTTP_400_BAD_REQUEST)


class DocDelete(APIView):
    def delete(self, request, document_id):
        try:
            document = Document.objects.get(pk=document_id)
        except Document.DoesNotExist:
            return Response({"message": "Document does not exist"}, status=status.HTTP_404_NOT_FOUND)

        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'imageURL': user.imageURL,
            # Add more fields as needed
        }
        return Response(data)

class ViewEditMode(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def post(self, request):
        id = request.data.get('id')
        doc = Document.objects.get(id=id)
        serializer = DocumentSerializer(doc, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['viewedit'] = True
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
