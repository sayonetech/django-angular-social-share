# Enable Rich Social Sharing in Your AngularJS App(w/o Prerender.io) using Django

## Problem With AngularJS

If yours is a public app, then rich social sharing is something you can't miss in your app.Facebook, Twitter,Google+ etc can fetch more than just the page title and image. This is achieved by using special meta tags in the HTML head. For example, Facebook and some other sites can read the Open Graph protocol.Twitter uses a very similar system, but with a prefix of “twitter:” rather than “og:”.

Search engines crawlers (or bots) were originally designed to crawl HTML content of web pages. As the web evolved, so did the technologies powering websites and JavaScript became an unavoidable part of the web.If you wanted to share something say an article with your Facebook friends, you’d paste the link into the status update box and hope to see something like this: 

![alt tag](https://github.com/jcblex/angular-social-share/blob/master/screenshots/screenshot1.jpg?raw=true)

However, even though you've have included all the necessary Open Graph meta tags, when you paste your link,you will be disappointed to see something more like this:

![alt tag](https://github.com/jcblex/angular-social-share/blob/master/screenshots/screenshot2.jpg?raw=true)

## The Reason

The crawlers that scrape the HTML do not evaluate JavaScript. Therefore, when they crawl the app, this is what they will see:
```html
<head>
    <meta property="og:title" content="" />
    <meta property="og:description" content="" />
    <meta property="og:image" content="" />
</head>
```
## The Solution

The solution is basically to pass the  social media crawler a custom url with a slug which generates a custom page that contains the desired meta tags, all filled with the correct information when the social media crawler arrives.

## What we will need

### 1. An angularjs directive for sharing urls and content on social networks such as (facebook, google+, twitter, pinterest and so on).

Here ***[angular-socialshare](https://github.com/720kb/angular-socialshare)*** is used.

*video_detail.html*
```html
   <div class="col-lg-6 col-md-6 col-sm-12 col-xs-12 social_share_widget">
                Share with
                <a data-toggle="tooltip"
                   ng-click="metaDescription=video.title"
                   title="Share on Facebook"
                   socialshare
                   socialshare-provider="facebook"
                   socialshare-url="{{location.protocol()}}://{{location.host()}}/api/videos/share-redirect-url/{{video.slug}}">
                    <i class="fa fa-facebook-official"></i>
                </a>
	  <a data-toggle="tooltip"
                   title="Share on Google"
                   ng-click="metaDescription=video.title"
                   socialshare
                   socialshare-provider="google"
                   socialshare-url="{{location.protocol()}}://{{location.host()}}/api/videos/share-redirect-url/{{video.slug}}">
                  <i class="fa fa-google-plus"></i>
                </a>
   </div>
```

Attribute 'socialshare-url' is used to define the url that is passed to the social media crawler for the purpose of grabbing the details while sharing.

Notice how a slug *{{video.slug}}* is passed on with the url.

### 2. Define the url pattern in urls.py

*urls.py*
```python 
urlpatterns = [
   ...,
   ...,
   url(r'^share-redirect-url/(?P<slug>[-\w]+)/$', RichSocialShare.as_view(), name='rich_share_redirect'),
   ...,   
]
```
### 3 Define the view to generate the custom page that will contain the desired meta tags 

*views.py*
```python 
class RichSocialShare(TemplateView):
    template_name = "social_share/rich_share.html"

    def get(self, request, *args, **kwargs):
        if kwargs['slug']:
            slug = kwargs['slug']
            video_obj = Video.objects.filter(slug=slug)[0]
            return render(request, self.template_name, {'video': video_obj})
        return render(request, self.template_name, {})
```
### 4. The template can be something as

*rich_share.html*
```html
<!DOCTYPE html>
<html>
<head lang="en">
    <!--for facebook-->
    <meta property="og:title" content="{{video.title}}"/>
    <meta property="og:description" content="{{video.content}}"/>
    <meta property="og:image" content="{{video.thumbnail_link}}"/>
    <!--for twitter-->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{video.title}}"/>
    <meta name="twitter:description" content="{{video.content }}"/>
    <meta name="twitter:image" content="{{video.thumbnail_link}}"/>  
    <title></title>

</head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>
<script type="text/javascript">
//    To redirect to the original content page upon clicking the link
   $( document ).ready(function() {
      window.location.href = window.location.origin + "/#/video/{{ video.slug }}" 
});
</script>
<body>
</body>
</html>
```
