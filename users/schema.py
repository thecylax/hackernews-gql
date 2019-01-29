from django.contrib.auth import get_user_model

# Create your models here.
import graphene
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        description = "Modelo de usuários"


class Query(graphene.ObjectType):
    viewer = graphene.Field(UserType, description='Função viewer.')
    users = graphene.List(UserType, description='Função users.')

    def resolve_viewer(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        
        return user

    def resolve_users(self, info):
        return get_user_model().objects.all()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True, description='Nome do usuário')
        password = graphene.String(required=True, description='Senha do usuário')
        email = graphene.String(required=True, description='Email do usuário')
 
 
    def mutate(self, info, username, password, email):
        user = get_user_model()(username=username, email=email)
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()