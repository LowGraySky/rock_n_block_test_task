from django.http import HttpResponse


def CreateToken(reqeust):
    return HttpResponse('token createed')


def ListTokens(request):
    return HttpResponse('list of all tokens')


def TokenTotalSupply(request):
    return HttpResponse('total supply of token')