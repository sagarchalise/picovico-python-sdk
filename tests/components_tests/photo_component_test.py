from six.moves.urllib import parse
from picovico.components import PicovicoPhoto
from picovico.baserequest import PicovicoRequest
from picovico import urls as pv_urls

class TestPhotoComponent:
    def test_upload_url(self, mocker, headers, response, method_calls):
        post_request = method_calls.POST.copy()
        auth_header = headers.AUTH.copy()
        req = PicovicoRequest(auth_header)
        ph_comp = PicovicoPhoto(req)
        assert ph_comp.component == 'photo'
        mr = mocker.patch('picovico.baserequest.requests.request')
        mr.return_value = response.SUCCESS.OK
        args = ("something", "something_thumb")
        ph_comp.upload_url(*args)
        post_request.update(url=parse.urljoin(pv_urls.PICOVICO_BASE, pv_urls.MY_PHOTOS))
        post_request.update(data=dict(zip(('url', 'thumbnail_url'), args)))
        post_request.update(headers=auth_header)
        mr.assert_called_with(**post_request)

