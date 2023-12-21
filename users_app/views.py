from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import views, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users_app.models import CustomUser
from users_app.serializers import RegisterUserSerializer, LoginUserSerializer, PhoneNumberSerializer, \
    UserProfileSerializer, VerifyCodeSerializer


class RegisterUserView(views.APIView):
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Вы успешно зарегистрированы.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(views.APIView):
    serializer_class = LoginUserSerializer

    @extend_schema(
        description='Этот эндпоинт служит для получение токена, ну вы знаете, получаете access and refresh токены'
    )

    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            return Response({'user_id': user.id, 'access': access, 'refresh': str(refresh)},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class SetPhoneNumberAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='Этот эндпоинт служит для установки номера начиная , номер должен начинаться с 0 и далее 9 цифр',
        responses={200: {'description': 'Номер сохранен в базе теперь, теперь к коду'}},
        request=PhoneNumberSerializer
    )

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = PhoneNumberSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        verify_code = "1234"
        user.verify_code = verify_code
        user.save()
        return Response(
            {'message': 'Код отправлен на ваш номер.'},
            status=status.HTTP_200_OK
        )


class PhoneNumberActivateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='Этот эндпоинт служит для подтверждение кода',
        responses={200: {'description': 'Номер успешно зарегистрирован'}},
        request=VerifyCodeSerializer
    )

    def post(self, request):
        user = request.user
        verify_code = request.data.get('verify_code')
        if verify_code == user.verify_code:
            user.is_verified = True
            user.save()
            return Response(
                {'message': 'Номер телефона успешно зарегистрирован.'}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Введите правильный код.'}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    description='Этот эндпоинт служит для действий с данными пользователя'
)
class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):
        return self.request.user
