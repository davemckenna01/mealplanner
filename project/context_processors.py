def mobile_context(request):
    host=request.META['HTTP_HOST']
    #mobile_host = "10.211.55.7:8000"
    mobile_host = "10.211.55.7:8001"
    print "got here"
    if host == mobile_host:
        return {
            "mobile":True,
            "base_template":"bases/base_mobile.html",
        }
    return {
        "mobile":False,
        "base_template":"bases/base_desktop.html",
    }