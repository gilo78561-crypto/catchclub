from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Conversation, Message

Dresseur = get_user_model()


@login_required
def liste_conversations(request):
    conversations = request.user.conversations.all()
    return render(request, 'messagerie/liste.html', {'conversations': conversations})


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
    autre = conversation.participants.exclude(id=request.user.id).first()
    conversations = request.user.conversations.all()
    return render(request, 'messagerie/detail.html', {
        'conversation': conversation, 'autre': autre, 'conversations': conversations,
    })


@login_required
@require_POST
def envoyer_message(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
    contenu = request.POST.get('contenu', '').strip()
    if contenu:
        Message.objects.create(conversation=conversation, auteur=request.user, contenu=contenu)
    return redirect('messagerie:detail', pk=pk)


@login_required
def demarrer_conversation(request, username):
    autre = get_object_or_404(Dresseur, username=username)
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=autre).first()
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, autre)
    return redirect('messagerie:detail', pk=conversation.pk)
