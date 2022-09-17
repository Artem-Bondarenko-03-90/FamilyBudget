from decimal import Decimal

from rest_framework import generics, status
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Cat, Sum, Week, Family, Profile
from django.contrib.auth.models import User

from .permissions import IsAdminOrReadOnly
from .serializers import CatSerializer, WeekSerializer, SumSerializer, FamilySerializer, ProfileSerializer, \
    UserSerializer


class APICatViewSet(ModelViewSet):
    queryset = Cat.objects.all().order_by('name')
    serializer_class = CatSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

class APIWeekViewSet(ReadOnlyModelViewSet):
    queryset = Week.objects.all().order_by('start_date')
    serializer_class = WeekSerializer
    permission_classes = (IsAdminOrReadOnly,)

class APIFamilyViewSet(ModelViewSet):
    queryset = Family.objects.all().order_by('name')
    serializer_class = FamilySerializer
    permission_classes = (IsAdminUser,)

@api_view(['GET', 'POST'])
def api_sum(request):
    if request.method == 'GET':
        sums = Sum.objects.all()
        serializer = SumSerializer(sums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        request.data['user'] = request.user.id
        serializer = SumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'GET', 'PUT', 'PATCH'])
def api_sum_detail(request, id):
    sum = Sum.objects.get(id=id)
    if request.method == 'GET':
        serializer = SumSerializer(sum)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = SumSerializer(instance=sum, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        sum.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#получение суммы по конкретной категории и неделе
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_sum_by_category_and_week(request, cat_id, week_id):
    family = Family.objects.filter(profile__user__id=request.user.id).first()
    if family != None:
        users = User.objects.filter(profile__family=family)
        sum = Sum.objects.filter(cat=cat_id, week=week_id, user__in=users).first()
        serializer = SumSerializer(sum)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'Error': 'Current user doesn\'t have family'}, status=status.HTTP_400_BAD_REQUEST)

#добавление суммы по конкретной категории и неделе
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_add_sum_by_category_and_week(request):
    family = Family.objects.filter(profile__user__id=request.user.id).first()
    if family != None:
        users = User.objects.filter(profile__family=family)
        #проверим имеется ли подходящая запись
        sum = Sum.objects.filter(cat=request.data['cat'], week=request.data['week'], user__in=users).first()
        if sum != None:
            val = sum.value
            val += Decimal(request.data['value'])
            request.data['value'] = val
            request.data['user'] = request.user.id
            serializer = SumSerializer(sum, request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            request.data['user'] = request.user.id
            serializer = SumSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'Error': 'Current user doesn\'t have family'}, status=status.HTTP_400_BAD_REQUEST)

#удаление суммы по конкретной категории и неделе
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_delete_sum_by_category_and_week(request):
    # проверим имеется ли подходящая запись
    sum = Sum.objects.filter(cat=request.data['cat_id'], week=request.data['week_id']).first()
    if sum != None:
        val = sum.value
        #проверяем, что убавляемая сумма не превышает имеющееся значение записи
        val = sum.value
        if val > request.data['value']:
            val -= Decimal(request.data['value'])
            request.data['value'] = val
            serializer = SumSerializer(sum, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            sum.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"Error": "Sum is not exist"}, status=status.HTTP_404_NOT_FOUND)

#выгрузка статистики по определённой категории
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_statistic_by_category(request, cat_id):
    sums = Sum.objects.filter(cat=cat_id).order_by('week__start_date').reverse()[:12]
    #serializer = SumSerializer(sums, many=True)
    res = []
    for sum in sums:
        d = {}
        d['id'] = sum.id
        d['value'] = sum.value
        d['week'] = sum.week.id
        d['start_week_date'] = sum.week.start_date
        d['end_week_date'] = sum.week.end_date
        d['cat'] = sum.cat.id
        d['cat_type'] = sum.cat.type
        res.append(d)
    return Response({'sums': res}, status=status.HTTP_200_OK)

#выгрузка статистики по всем категориям
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_statistic(request):
    sums = Sum.objects.all().order_by('week__start_date').reverse()[:12]
    #serializer = SumSerializer(sums, many=True)
    res = []
    for sum in sums:
        d = {}
        d['id'] = sum.id
        d['value'] = sum.value
        d['week'] = sum.week.id
        d['start_week_date'] = sum.week.start_date
        d['end_week_date'] = sum.week.end_date
        d['cat'] = sum.cat.id
        d['cat_type'] = sum.cat.type
        res.append(d)
    return Response({'sums': res}, status=status.HTTP_200_OK)

#подсчёт суммы за конкретную неделю
def total_sum_by_week(week_id):
    sums = Sum.objects.filter(week=week_id)
    total = 0.0
    for s in sums:
        if s.cat.type:
            total += float(s.value)
        else:
            total -= float(s.value)
    return total

#выгрузка статистики общих сумм по неделям
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_statistic_total(request):
    weeks = Week.objects.all().order_by('start_date').reverse()[:12]
    #serializer = SumSerializer(sums, many=True)
    res = []
    for w in weeks:
        d = {}
        d['id'] = w.id
        d['value'] = total_sum_by_week(w.id)
        d['week'] = w.id
        d['start_week_date'] = w.start_date
        d['end_week_date'] = w.end_date
        res.append(d)
    return Response({'total_sums': res}, status=status.HTTP_200_OK)

#подсчет суммы расходов/доходов за указанный перомежуток времени
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_total_by_period(request):
    total=0.0
    weeks = Week.objects.filter(start_date__gte=request.data['start_date'], end_date__lte=request.data['end_date']).order_by('start_date').reverse()
    if request.data['categories'] == []:
        sums = Sum.objects.filter(week__in=weeks)
        for s in sums:
            if s.cat.type:
                total += float(s.value)
            else:
                total -= float(s.value)
    else:
        sums = Sum.objects.filter(week__in=weeks, cat__in=request.data['categories'])
        for s in sums:
            if s.cat.type:
                total += float(s.value)
            else:
                total -= float(s.value)
    return Response({'total_sum': total}, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@permission_classes((IsAdminUser,))
def api_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'GET', 'PUT', 'PATCH'])
@permission_classes((IsAdminUser,))
def api_user_detail(request, id):
    user = User.objects.get(id=id)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)