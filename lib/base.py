import requests, json, sys
from lib import urls, utils, constants
class PicovicoBase:

	def set_tokens(self, access_key, access_token):
		self.access_key = access_key
		self.access_token = access_token

	def picovico_auth_headers(self):
		return {
			"X-Access-Key":self.access_key,
			"X-Access-Token":self.access_token
		}

	def upload_image_file(self, file_path, source=None):
		if utils.is_local_file(file_path):
			return requests.put(urls.PICOVICO_API_ENDPOINT + urls.UPLOAD_PHOTO, file_path, headers=self.picovico_auth_headers())
		else:
			data = {
				'url': file_path,
				'source': source,
				'thumbnail_url': file_path
			}
			response = requests.post(urls.PICOVICO_API_ENDPOINT + urls.UPLOAD_PHOTO, data, headers=self.picovico_auth_headers())
			return json.loads(response.text)

	def upload_music_file(self, file_path, source=None):
		if utils.is_local_file(file_path):
			data = {
				'X-Music-Artist': "Unknown",
				"X-Music-Title": "Unknown - {}".format('r')
			}
			return requests.put(urls.PICOVICO_API_ENDPOINT + urls.UPLOAD_MUSIC, file_path, data, headers=self.picovico_auth_headers())
		else:
			data = {
				'url': file_path,
				'preview_url': file_path
			}
			response = requests.post(urls.PICOVICO_API_ENDPOINT + urls.UPLOAD_MUSIC, data, headers=self.picovico_auth_headers())
			return json.loads(response.text)


	def append_image_slide(self, vdd, image_id, caption=None):
		data = {
			'name': 'image',
			'text': caption,
			'asset_id': image_id
		}
		self.append_vdd_slide(vdd, data)

	def append_vdd_slide(self, vdd, slide):

		if vdd:
			if not vdd['assets']:
				vdd['assets'] = {}
				print("empty assets")

			last_slide = None
			current_slides_count = len(vdd['assets'])
			last_end_time = 0

			if vdd['assets']:
				last_slide = vdd['assets'][len(vdd['assets'] - 1)]

				if last_slide:
					last_end_time = last_slide["end_time"]
				else:
					last_end_time = last_slide.end_time

			slide['start_time'] = last_end_time
			slide['end_time'] = last_end_time + self.STANDARD_SLIDE_DURATION
			vdd['assets'] = slide