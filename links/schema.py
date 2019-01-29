import graphene
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id

from .models import Link, Vote
from users.schema import UserType


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (graphene.relay.Node,)
        description = "Model que representa votos."


class LinkNode(DjangoObjectType):
    class Meta:
        model = Link
        interfaces = (graphene.relay.Node,)
        description = "Model que representa links."


class LinkConnection(graphene.relay.Connection):
    class Meta:
        node = LinkNode


class Query(graphene.ObjectType):
    link = graphene.relay.Node.Field(LinkNode, description='Função link.')
    links = graphene.relay.ConnectionField(LinkConnection, description='Função links.')
    # links = graphene.List(LinkType, description="Função links")
    # votes = graphene.List(VoteType, description="Função votes")

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

class CreateLink(graphene.relay.ClientIDMutation):
    link = graphene.Field(LinkNode)
    # id = graphene.Int()
    # url = graphene.String()
    # description = graphene.String()
    # posted_by = graphene.Field(UserType)

    class Input:
        url = graphene.String(description='URL a ser incluída')
        description = graphene.String(description='Descrição da URL')

    def mutate_and_get_payload(self, info, **input):
        user = info.context.user or None
        link = Link(
            url=input.get('url'),
            description=input.get('description'),
            posted_by=input.get('user'))
        link.save()

        return CreateLink(link=link)


class CreateVote(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkNode)

    class Input:
        link_id = graphene.ID(description="ID do link a ser votado.")

    def mutate_and_get_payload(self, info, **input):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to vote!')

        link = Link.objects.filter(id=from_global_id(input.get('link_id'))[1]).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field(description='Adiciona um novo link.')
    create_vote = CreateVote.Field(description='Vota num link.')
