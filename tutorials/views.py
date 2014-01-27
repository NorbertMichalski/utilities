from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext

@staff_member_required
def tutorials_view(request):

  return render_to_response('tutorials.html',
  context_instance=RequestContext(request))
