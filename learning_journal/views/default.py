from pyramid.response import Response
import os

HERE = os.path.abspath(__file__)
STATIC = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'static')
TEMPLATE = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'template')


def list_view(request):
    with open(os.path.join(TEMPLATE, "index.html")) as file:
        return Response(file.read())


def detail_view(request):
    with open(os.path.join(TEMPLATE, "detail.html")) as file:
        return Response(file.read())

def create_view(request):
    with open(os.path.join(TEMPLATE, "new_entry.html")) as file:
        return Response(file.read())

def update_view(request):
    with open(os.path.join(TEMPLATE, "edit_entry.html")) as file:
        return Response(file.read())