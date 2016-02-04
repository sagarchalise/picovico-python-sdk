import mock
import pytest
from six.moves.urllib import parse
from picovico.components import *
from picovico import urls as pv_urls
from picovico import base as pv_base
from picovico import exceptions as pv_exceptions

class TestComponentMixin:
    def test_component_property(self, success_response):
        pv_component = PicovicoComponentMixin()
        with pytest.raises(AttributeError):
            pv_component.music_component
        with pytest.raises(AttributeError):
            pv_component.other_component
        pv_component._ready_component_property()
        assert pv_component.photo_component
        with mock.patch('picovico.base.requests.request') as mr:
            mr.return_value = success_response
            pv_component.get_library_musics()
            mr.assert_called_with(method='get', url=parse.urljoin(pv_urls.PICOVICO_BASE, pv_urls.PICOVICO_MUSICS))
            pv_component.get_library_styles()
            mr.assert_called_with(method='get', url=parse.urljoin(pv_urls.PICOVICO_BASE, pv_urls.PICOVICO_STYLES))
        
        
class TestComponent:
    def test_component_methods(self):
        components = {k: None for k in ('music', 'photo', 'style', 'video')}
        classes = (PicovicoMusic, PicovicoPhoto, PicovicoStyle, PicovicoVideo)
        component_class = dict(zip(('music', 'photo', 'style', 'video'), classes))
        for name in components:
            components[name] = component_class[name](pv_base.PicovicoRequest())
        music_component = components.get('music')
        style_component = components.get('style')
        video_component = components.get('video')
        photo_component = components.get('photo')
        with pytest.raises(AttributeError):
            music_component.get_styles()
        with pytest.raises(AttributeError):
            style_component.get_videos()
        with pytest.raises(AttributeError):
            photo_component.get_music()
        with pytest.raises(AttributeError):
            video_component.get_photos()
    
    def test_photo_component(self):
        pv_comp = PicovicoPhoto(pv_base.PicovicoRequest())
        with pytest.raises(pv_exceptions.PicovicoAPINotAllowed):
            gm = pv_comp.get_photos()
            
    def test_style_component(self):
        pv_comp = PicovicoStyle(pv_base.PicovicoRequest())
        with pytest.raises(NotImplementedError):
            pv_comp.upload_style_file(1)
        with pytest.raises(NotImplementedError):
            pv_comp.delete_style(1)