import abc

from .. import exceptions as pv_exceptions
from .. import urls as pv_urls
from .. import constants as pv_constants
from .. import baserequest as pv_base
from .. import decorators as pv_decorator


class PicovicoBaseComponent(object):
    """ Picovico Base Component class. (Abstract)
    This class is the base for all other component classes and shouldn't be used alone.

    Attributes:
        component(str): Name of component currently initiated.
    """
    __metaclass__ = abc.ABCMeta
    _components = ('style', 'music', 'photo', 'video')

    @staticmethod
    def create_request_args(**kwargs):
        url_attr = kwargs.pop('url_attr', 'PICOVICO_STYLES')
        if 'method' not in kwargs:
            kwargs.update(method='get')
        req_url = getattr(pv_urls, url_attr)
        kwargs.update(path=req_url)
        return kwargs

    def _api_call(self, method='get', **request_args):
        assert method and method in pv_constants.ALLOWED_METHODS, 'Only {} allowed.'.format(','.join(pv_constants.ALLOWED_METHODS))
        assert ('path' in request_args and request_args['path'])
        assert (1 <= len(request_args) <= 3)
        return getattr(self._pv_request, method)(**request_args)

    def __init__(self, request_obj):
        """ Authenticated request object for component access. """
        assert isinstance(request_obj, pv_base.PicovicoRequest)
        self._pv_request = request_obj

    @abc.abstractproperty
    def component(self):
        raise NotImplementedError
    
    def __sanitize_single_url(self, url, url_args):
        return url.format(**url_args)

    @pv_decorator.pv_not_implemented(_components[1:])
    @pv_decorator.pv_auth_required
    def one(self, id):
        url_args =  {'{}_id'.format(self.component): id}
        req_args = self.create_request_args(**{
            'method': 'get',
            'url_attr': 'MY_SINGLE_{}'.format(self.component.upper()),
        })
        req_args.update(path=self.__sanitize_single_url(req_args.pop('path'), url_args))
        return self._api_call(**req_args)

    @pv_decorator.pv_auth_required
    def all(self):
        req_args = self.create_request_args(**{
            'method': 'get',
            'url_attr': 'MY_{}S'.format(self.component.upper())
        })
        return self._api_call(**req_args)

    @pv_decorator.pv_not_implemented(_components[1:3])
    @pv_decorator.pv_auth_required
    def upload_file(self, filename, data_headers=None):
        req_args = self.create_request_args(**{
            'method': 'put',
            'url_attr': 'MY_{}S'.format(self.component.upper()),
            'filename': filename
        })
        if data_headers:
            req_args.update(data_headers=data_headers)
        return self._api_call(**req_args)

    @pv_decorator.pv_not_implemented(_components[1:3])
    @pv_decorator.pv_auth_required
    def upload_url(self, url, **data):
        req_args = self.create_request_args(**{
            'method': 'post',
            'url_attr': 'MY_{}S'.format(self.component.upper()),
            'post_data': dict(url=url, **data),
        })
        return self._api_call(**req_args)

    @pv_decorator.pv_not_implemented(_components[1:])
    @pv_decorator.pv_auth_required
    def delete(self, id):
        url_args =  {'{}_id'.format(self.component): id}
        req_args = self.create_request_args(**{
            'method': 'delete',
            'url_attr': 'MY_SINGLE_{}'.format(self.component.upper()),
        })
        req_args.update(path=self.__sanitize_single_url(req_args.pop('path'), url_args))
        return self._api_call(**req_args)

    @pv_decorator.pv_not_implemented(_components[:2])
    @pv_decorator.pv_auth_required
    def get_library(self):
        req_args = self.create_request_args(**{
            'method': 'get',
            'url_attr': 'MY_{}S'.format(self.component.upper()),
        })
        return self._api_call(**req_args)

    @pv_decorator.pv_not_implemented(_components[:2])
    def get_free(self):
        free_req = pv_base.PicovicoRequest()
        return free_req.get(path=getattr(pv_urls, 'PICOVICO_{}S'.format(self.component.upper())))
