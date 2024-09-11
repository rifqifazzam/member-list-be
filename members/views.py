from django.shortcuts import render
from .models import Member
from rest_framework import viewsets
from .serializers import MemberSerializer

# Create your views here.
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
