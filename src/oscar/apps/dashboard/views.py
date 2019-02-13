import json
from datetime import timedelta
from decimal import Decimal as D
from decimal import ROUND_UP

from django.db.models import Avg, Count, Sum, QuerySet
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.timezone import now
from django.views.generic import TemplateView

# from oscar.apps.promotions.models import AbstractPromotion
from oscar.apps.dashboard.widgets import RelatedFieldWidgetWrapper
from oscar.core.compat import get_user_model
from oscar.core.loading import get_class, get_model

# RelatedFieldWidgetWrapper = get_class('dashboard.widgets', 'RelatedFieldWidgetWrapper')
# ConditionalOffer = get_model('offer', 'ConditionalOffer')
# Voucher = get_model('voucher', 'Voucher')
# Basket = get_model('basket', 'Basket')
# StockAlert = get_model('partner', 'StockAlert')
Product = get_model('catalogue', 'Product')
# Order = get_model('order', 'Order')
# Line = get_model('order', 'Line')
User = get_user_model()


class IndexView(TemplateView):
    """
    An overview view which displays several reports about the shop.

    Supports the permission-based dashboard. It is recommended to add a
    index_nonstaff.html template because Oscar's default template will
    display potentially sensitive store information.
    """

    def get_template_names(self):
        if self.request.user.is_staff:
            return ['dashboard/index.html', ]
        else:
            return ['dashboard/index_nonstaff.html', 'dashboard/index.html']

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        ctx.update(self.get_stats())
        return ctx

    def get_stats(self):
        stats = {'total_products': Product.objects.all().count(), }
        return stats


class PopUpWindowCreateUpdateMixin(object):

    def get_context_data(self, **kwargs):
        ctx = super(PopUpWindowCreateUpdateMixin, self).get_context_data(**kwargs)

        if RelatedFieldWidgetWrapper.TO_FIELD_VAR in self.request.GET or RelatedFieldWidgetWrapper.TO_FIELD_VAR in self.request.POST:
            to_field = self.request.GET.get(RelatedFieldWidgetWrapper.TO_FIELD_VAR,
                                            self.request.POST.get(RelatedFieldWidgetWrapper.TO_FIELD_VAR))
            ctx['to_field'] = to_field
            ctx['to_field_var'] = RelatedFieldWidgetWrapper.TO_FIELD_VAR

        if RelatedFieldWidgetWrapper.IS_POPUP_VAR in self.request.GET or RelatedFieldWidgetWrapper.IS_POPUP_VAR in self.request.POST:
            is_popup = self.request.GET.get(RelatedFieldWidgetWrapper.IS_POPUP_VAR,
                                            self.request.POST.get(RelatedFieldWidgetWrapper.IS_POPUP_VAR))
            ctx['is_popup'] = is_popup
            ctx['is_popup_var'] = RelatedFieldWidgetWrapper.IS_POPUP_VAR

        return ctx

    def forms_valid(self, form, formset):
        # So that base view classes can do pop-up window specific things, like
        # not displaying notification messages using the messages framework
        self.is_popup = False
        if RelatedFieldWidgetWrapper.IS_POPUP_VAR in self.request.POST:
            self.is_popup = True

        return super(PopUpWindowCreateUpdateMixin, self).forms_valid(form, formset)


class PopUpWindowCreateMixin(PopUpWindowCreateUpdateMixin):

    # form_valid and form_invalid are called, depending on the validation
    # result of just the form, and return a redirect to the success URL or
    # redisplay the form, respectively. In both cases we need to check our
    # formsets as well, so both methods should do the same.
    # If both the form and formset are valid, then they should call
    # forms_valid, which should be defined in the base view class, to in
    # addition save the formset, and return a redirect to the success URL.
    def forms_valid(self, form, formset):
        response = super(PopUpWindowCreateMixin, self).forms_valid(form, formset)

        if RelatedFieldWidgetWrapper.IS_POPUP_VAR in self.request.POST:
            obj = form.instance
            to_field = self.request.POST.get(RelatedFieldWidgetWrapper.TO_FIELD_VAR)
            if to_field:
                attr = str(to_field)
            else:
                attr = obj._meta.pk.attname
            value = obj.serializable_value(attr)
            popup_response_data = json.dumps({
                'value': six.text_type(value),
                'obj': six.text_type(obj),
            })
            return TemplateResponse(self.request, 'dashboard/widgets/popup_response.html', {
                'popup_response_data': popup_response_data,
            })

        else:
            return response


class PopUpWindowUpdateMixin(PopUpWindowCreateUpdateMixin):

    # form_valid and form_invalid are called, depending on the validation
    # result of just the form, and return a redirect to the success URL or
    # redisplay the form, respectively. In both cases we need to check our
    # formsets as well, so both methods should do the same.
    # If both the form and formset are valid, then they should call
    # forms_valid, which should be defined in the base view class, to in
    # addition save the formset, and return a redirect to the success URL.
    def forms_valid(self, form, formset):
        response = super(PopUpWindowUpdateMixin, self).forms_valid(form, formset)

        if RelatedFieldWidgetWrapper.IS_POPUP_VAR in self.request.POST:
            obj = form.instance
            opts = obj._meta
            to_field = self.request.POST.get(RelatedFieldWidgetWrapper.TO_FIELD_VAR)
            if to_field:
                attr = str(to_field)
            else:
                attr = opts.pk.attname
            # Retrieve the `object_id` from the resolved pattern arguments.
            value = self.request.resolver_match.kwargs['pk']
            new_value = obj.serializable_value(attr)
            popup_response_data = json.dumps({
                'action': 'change',
                'value': six.text_type(value),
                'obj': six.text_type(obj),
                'new_value': six.text_type(new_value),
            })
            return TemplateResponse(self.request, 'dashboard/widgets/popup_response.html', {
                'popup_response_data': popup_response_data,
            })

        else:
            return response


class PopUpWindowDeleteMixin(object):

    def get_context_data(self, **kwargs):
        ctx = super(PopUpWindowDeleteMixin, self).get_context_data(**kwargs)

        if RelatedFieldWidgetWrapper.IS_POPUP_VAR in self.request.GET:
            ctx['is_popup'] = self.request.GET.get(RelatedFieldWidgetWrapper.IS_POPUP_VAR)
            ctx['is_popup_var'] = RelatedFieldWidgetWrapper.IS_POPUP_VAR

        return ctx

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL, or closes the popup, it it is one.
        """
        # So that base view classes can do pop-up window specific things, like
        # not displaying notification messages using the messages framework
        self.is_popup = False
        if RelatedFieldWidgetWrapper.IS_POPUP_VAR in self.request.POST:
            self.is_popup = True

        obj = self.get_object()

        response = super(PopUpWindowDeleteMixin, self).delete(request, *args, **kwargs)

        if RelatedFieldWidgetWrapper.IS_POPUP_VAR in request.POST:
            obj_id = obj.pk
            popup_response_data = json.dumps({
                'action': 'delete',
                'value': six.text_type(obj_id),
            })
            return TemplateResponse(request, 'dashboard/widgets/popup_response.html', {
                'popup_response_data': popup_response_data,
            })

        else:
            return response
