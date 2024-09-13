import secrets
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Member
from .serializers import MemberSerializer
from .models import CustomToken
from .authentication import CustomTokenAuthentication


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def validate_token(request):
    return Response({'message': 'Token is valid'}, status=status.HTTP_200_OK)

# Custom Login view
@csrf_exempt
@api_view(['POST'])
def custom_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate the user
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Check if the user already has a token
        try:
            token = CustomToken.objects.get(user=user)
            # Check if the token has expired
            if token.has_expired():
                token.delete()  # Delete the expired token
                token = None
        except CustomToken.DoesNotExist:
            token = None

        # Create a new token if no valid token exists
        if token is None:
            token = CustomToken.objects.create(user=user, key=secrets.token_hex(20))

        # Calculate the expiration time (UTC)
        expiration_time = timezone.now() + timedelta(minutes=1)

        # Convert the expiration time to the server's local timezone (Asia/Jakarta)
        expiration_time_local = timezone.localtime(expiration_time)

        return Response({
            'token': token.key,
            'expires_at': expiration_time_local.strftime('%Y-%m-%d %H:%M:%S')  # Convert to Asia/Jakarta time
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Custom Logout view
@api_view(['POST'])
def custom_logout(request):
    token_key = request.data.get('token')

    try:
        token = CustomToken.objects.get(key=token_key)
        token.delete()  # Delete the token on logout
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except CustomToken.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

# Create Member (POST)
@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])  # Use custom token authentication
@permission_classes([IsAuthenticated])  # Require user to be authenticated
def create_member(request):
    if request.method == 'POST':
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Read all members (GET)
@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])  # Use custom token authentication
@permission_classes([IsAuthenticated])  # Require user to be authenticated     # Require user to be authenticated
def list_members(request):
    if request.method == 'GET':
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

# Read a single member (GET)
@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])  # Use custom token authentication
@permission_classes([IsAuthenticated])  # Require user to be authenticated      # Require user to be authenticated
def get_member(request, pk):
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MemberSerializer(member)
    return Response(serializer.data)

# Update a member (PUT)
@api_view(['PUT'])
@authentication_classes([CustomTokenAuthentication])  # Use custom token authentication
@permission_classes([IsAuthenticated])  # Require user to be authenticated         # Require user to be authenticated
def update_member(request, pk):
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MemberSerializer(member, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a member (DELETE)
@api_view(['DELETE'])
@authentication_classes([CustomTokenAuthentication])  # Use custom token authentication
@permission_classes([IsAuthenticated])  # Require user to be authenticated     # Require user to be authenticated
def delete_member(request, pk):
    try:
        member = Member.objects.get(pk=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    member.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)