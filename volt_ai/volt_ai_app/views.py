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
    
    
@api_view(['POST'])
def register(request):
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    username = request.data.get("username")
    raw_password = request.data.get("password")

    
    
    if not first_name or not last_name or not username or not raw_password:
        return Response({"message": "All the fields are required!"}, status = status.HTTP_400_BAD_REQUEST) 
    try:
        if User.objects.filter(username=username).exists():
             return Response({"message": f"Username already exists!"}, status = status.HTTP_409_CONFLICT)
        
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(raw_password)
        user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status = status.HTTP_200_OK)
        
    
    except Exception as e:
        return Response({"message": f"Something went wrong: {e}"}, status = status.HTTP_400_CONFLICT)
    


    


    
