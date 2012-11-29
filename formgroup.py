from django.shortcuts import render_to_response
from django.template.context import RequestContext

class FormGroup:
    def __init__(self, form_classes, request, form_save_methods=None):
        self.forms = []
        self.form_save_methods = form_save_methods
        if request.method == "POST":
            map(lambda x: self.forms.append(x(request.POST)),form_classes)
        else:
            map(lambda x: self.forms.append(x()),form_classes)
    def is_valid(self):
        return reduce(lambda x,y: x and y.is_valid(),self.forms,True)
    def save(self):
        if not self.form_save_methods:
            map(lambda x: x.save(),self.forms)
        else:
            form_save_methods(self.forms)
    def __iter__(self):
        for form in self.forms:
            yield form

def formsSave(request,template,form_classes):
    forms = FormGroup(form_classes,request)
    if request.method == "POST":
        if forms.is_valid():
            forms.save()
    return render_to_response('landing.html', locals(), context_instance=RequestContext(request))


