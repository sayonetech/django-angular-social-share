from django.conf import settings

class RichSocialShare(TemplateView):
    template_name = "path/rich_share.html"

    def get(self, request, *args, **kwargs):
        if kwargs['slug']:
            slug = kwargs['slug']
            video_obj = Video.objects.filter(slug=slug)[0]
            return render(request, self.template_name, {'video': video_obj})
        return render(request, self.template_name, {})
