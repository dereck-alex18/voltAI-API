from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from volt_ai_app.serializers.serializers import UserSerializer

@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    raw_password = request.data.get("password")

    if not username or not raw_password:
        return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    
    except User.DoesNotExist:
        return Response({"message": "The credentials are invalid or the user does not exist"}, status = status.HTTP_400_BAD_REQUEST) 
    

    except Exception as e:
        return Response({"message": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serializer = UserSerializer(user)
    if user.check_password(raw_password):
        return Response(serializer.data, status = status.HTTP_200_OK)
    else:
        return Response({"message": "The credentials are invalid or the user does not exist"}, status = status.HTTP_400_BAD_REQUEST)
  
    

    
