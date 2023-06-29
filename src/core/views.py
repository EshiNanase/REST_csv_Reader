from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from collections import defaultdict
from drf_spectacular.utils import extend_schema
from .serializers import DealSerializer, CustomerSerializer
from http import HTTPStatus
from .models import Customer, Stone, StoneItem


@extend_schema(request=DealSerializer)
@api_view(['POST'])
def upload_deal(request):
    serializer = DealSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data['file'].read().decode('utf-8').splitlines()[1:]
        for line in data:
            username, stone_name, spent_money, quantity, date = line.split(',')

            customer, created = Customer.objects.get_or_create(
                username=username,
            )
            customer.spent_money += int(spent_money)
            customer.save()

            stone, created = Stone.objects.get_or_create(name=stone_name)

            stone_item, created = StoneItem.objects.get_or_create(
                customer=customer,
                stone=stone,
            )
            stone_item.quantity += int(quantity)
            stone_item.save()

        return Response(status=HTTPStatus.OK)

    except Exception as e:
        return Response(
            status=HTTPStatus.BAD_REQUEST,
            data={'error': str(e)}
        )


@cache_page(30)
@api_view(['GET'])
def get_top_five_customers(request):
    customers = Customer.objects.prefetch_related('stones', 'stones__stone').all().order_by('-spent_money')[:5]
    serializer = CustomerSerializer(data=customers, many=True)
    serializer.is_valid()

    common_stones = defaultdict(int)
    for customer in serializer.data:
        stones = list(customer.items())[2][1]
        for stone in stones:
            common_stones[list(stone.values())[0]] += 1

    for customer in serializer.data:
        customer['stones'] = [list(stone.values())[0] for stone in customer['stones'] if common_stones[list(stone.values())[0]] >= 2]

    return Response(
        data={'response': serializer.data}
    )
