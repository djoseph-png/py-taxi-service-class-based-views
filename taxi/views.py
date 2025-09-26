from __future__ import annotations

from django.views.generic import TemplateView, ListView, DetailView

from .models import Manufacturer, Car, Driver


class IndexView(TemplateView):
    template_name = "taxi/index.html"


class ManufacturerListView(ListView):
    model = Manufacturer
    paginate_by = 5
    queryset = Manufacturer.objects.order_by("name")


class CarListView(ListView):
    model = Car
    paginate_by = 5
    # Otimiza o acesso ao fabricante para evitar N+1
    queryset = Car.objects.select_related("manufacturer").order_by("id")


class CarDetailView(DetailView):
    model = Car
    # Também otimiza os relacionados exibidos no detalhe
    queryset = Car.objects.select_related(
        "manufacturer"
    ).prefetch_related("drivers")


class DriverListView(ListView):
    model = Driver
    paginate_by = 5
    queryset = Driver.objects.order_by("id")


class DriverDetailView(DetailView):
    model = Driver
    # Otimiza os carros do motorista e seus fabricantes para evitar N+1
    queryset = Driver.objects.prefetch_related(
        # "cars" é o related_name no ManyToMany de Car para Driver
        "cars__manufacturer"
    )
