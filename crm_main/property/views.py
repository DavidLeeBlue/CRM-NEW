from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Property, PropertyImage, PropertyComment, PropertyCommentImage
from .forms import PropertyForm, PropertyImageForm, PropertyCommentForm, PropertyCommentImageForm
from django.views.generic.edit import FormMixin

class PropertyListView(ListView):
    model = Property

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PropertyListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Property.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Property List'
        return context

class PropertyDetailView(FormMixin, DetailView):
    model = Property
    form_class = PropertyCommentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PropertyDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['image_form'] = PropertyCommentImageForm()
        context['comments'] = self.object.comments.all()
        context['page_title'] = 'Property Detail'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        image_form = PropertyCommentImageForm(request.POST, request.FILES)
        if form.is_valid() and image_form.is_valid():
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, image_form):
        comment = form.save(commit=False)
        comment.created_by = self.request.user
        comment.property = self.get_object()
        comment.save()
        for image in self.request.FILES.getlist('images'):
            PropertyCommentImage.objects.create(comment=comment, image=image)
        return redirect('properties:detail', pk=comment.property.pk)

class PropertyCreateView(CreateView):
    model = Property
    form_class = PropertyForm
    success_url = reverse_lazy('properties:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PropertyCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        files = self.request.FILES.getlist('image')
        for file in files:
            PropertyImage.objects.create(property=self.object, image=file)
        messages.success(self.request, 'Property created successfully!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = PropertyImageForm()
        context['page_title'] = 'Create Property'
        return context

class PropertyUpdateView(UpdateView):
    model = Property
    form_class = PropertyForm
    success_url = reverse_lazy('properties:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PropertyUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        files = self.request.FILES.getlist('image')
        for file in files:
            PropertyImage.objects.create(property=self.object, image=file)
        messages.success(self.request, 'Property updated successfully!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = PropertyImageForm()
        context['page_title'] = 'Update Property'
        return context

class PropertyDeleteView(DeleteView):
    model = Property
    success_url = reverse_lazy('properties:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PropertyDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Property deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Delete Property'
        return context

class AddPropertyCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        form = PropertyCommentForm(request.POST)
        image_form = PropertyCommentImageForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            comment = form.save(commit=False)
            comment.created_by = request.user
            comment.property_id = pk
            comment.save()
            for image in request.FILES.getlist('images'):
                PropertyCommentImage.objects.create(comment=comment, image=image)

        return redirect('properties:detail', pk=pk)