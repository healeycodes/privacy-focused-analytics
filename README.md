## Privacy Focused Analytics From Scratch

> My blog post: [Privacy Focused Analytics From Scratch](https://healeycodes.com/privacy-focused-analytics-from-scratch/)

<br>

I wanted to learn about web analytics so I budgeted myself a few hours and built a small analytics system.

It uses a Flask application and a HTML snippet to collect **anonymous user data**.

<br>

### Features

- Uses a tracking pixel (optionally works without JavaScript)
- Collects information about:
  - What pages users visit
  - Where users are referred from
  - What browsers and screen sizes are used
- Lets you view time slices of this data

<br>

### Snippet

Include this on any page you want to gather analytics from.

Change `website` to wherever you host the Flask application.

```html
<script>
  const website = 'https://example.org'
  const url = new URL(website + "/pixel.gif")

  // '/'
  url.searchParams.append("path", location.pathname)

  // 'Analytics Test Page'
  url.searchParams.append("title", document.title)

  // 'https://www.google.com'
  url.searchParams.append("referrer", document.referrer)

  // '320,568'
  url.searchParams.append(
    "resolution",
    window.screen.width + "," + window.screen.height
  )

  const img = document.createElement("img")
  img.src = url
  // When the element exists in the DOM, the request is made
  document.body.appendChild(img)
</script>
<noscript>
  <!-- Without JavaScript, less information is available to be sent
  e.g. just the path and title, set via static template logic -->
  <img src="https://example.org/pixel.gif?path=%2F&title=Analytics%20Test%20Page" />
</noscript>
```
<br>

### Setup

Download a free [GeoLite2 country database](https://dev.maxmind.com/geoip/geoip2/geolite2/) to `./GeoLite2-Country.mmdb`

`pip install -r requirements.txt`

<br>

### Run

`env FLASK_APP=analytics.py flask run`

The tracking pixel is hosted from `/pixel.gif`.

Analytics can be viewed at `/analytics` and a `start` and `end` (UNIX seconds) can be passed as search parameters to view a time slice. `end` is optional so `/analytics?start=1596363446` works fine.

<br>

### Possible improvements

Hopefully none? This was a self-contained experiment to learn (and teach) something.

- Anonymously track sessions perhaps like [GoatCounter does](https://github.com/zgoat/goatcounter/blob/master/docs/sessions.markdown)
- Granular tracking (i.e. click events)

<br>

License: MIT.
