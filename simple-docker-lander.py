from bottle import route, run, template
import os
import yaml


DEFAULT_CONFIG = {
    'site-name': 'simple-docker-lander',
    'link-mode': 'default',
    'links': [
        {'name': 'Service 1', 'href': 'https://www.google.com/'},
        {'name': 'Service 2', 'href': 'https://www.reddit.com/'},
    ]
}


if __name__ == '__main__':
    config_env_var = yaml.safe_load(os.environ.get('CONFIG', '')) or {}

    # Merge the default config with the env config
    config = DEFAULT_CONFIG.copy()
    config.update(config_env_var)

    groups = [
        {'name': 'default', 'links': []}
    ]
    groups_index_map = {'default': 0}
    for link in config['links']:
        if 'group' in link:
            if link['group'] in groups_index_map:
                groups[groups_index_map[link['group']]]['links'].append(link)
            else:
                groups_index_map[link['group']] = len(groups)
                groups.append({
                    'name': link['group'],
                    'links': [link]
                })
        else:
            groups[0]['links'].append(link)

    @route('/')
    def index():
        return template('''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">

        <title>{{ config['site-name'] }}</title>

    <link rel="canonical" href="https://getbootstrap.com/docs/4.5/examples/cover/">

    <!-- Bootstrap core CSS -->
<link href="/docs/4.5/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">

<meta name="theme-color" content="#563d7c">


    <style>
a,
a:focus,
a:hover {
  color: #fff;
}

/* Custom default button */
.btn-secondary,
.btn-secondary:hover,
.btn-secondary:focus {
  color: #333;
  text-shadow: none; /* Prevent inheritance from `body` */
  background-color: #fff;
  border: .05rem solid #fff;
}


html,
body {
  height: 100%;
  background-color: #333;
}

body {
  display: -ms-flexbox;
  display: flex;
  color: #fff;
  text-shadow: 0 .05rem .1rem rgba(0, 0, 0, .5);
  box-shadow: inset 0 0 5rem rgba(0, 0, 0, 0);
}

.cover-container {
  max-width: 42em;
}


/*
 * Header
 */
.masthead {
  margin-bottom: 2rem;
}

.masthead-brand {
  margin-bottom: 0;
}

.nav-masthead .nav-link {
  padding: .25rem 0;
  font-weight: 700;
  color: rgba(255, 255, 255, .5);
  background-color: transparent;
  border-bottom: .25rem solid transparent;
}

.nav-masthead .nav-link:hover,
.nav-masthead .nav-link:focus {
  border-bottom-color: rgba(255, 255, 255, .25);
}

.nav-masthead .nav-link + .nav-link {
  margin-left: 1rem;
}

.nav-masthead .active {
  color: #fff;
  border-bottom-color: #fff;
}

@media (min-width: 48em) {
  .masthead-brand {
    float: left;
  }
  .nav-masthead {
    float: right;
  }
}


/*
 * Cover
 */
.cover {
  padding: 0 1.5rem;
}
.cover .btn-lg {
  padding: .75rem 1.25rem;
  font-weight: 700;
}


/*
 * Footer
 */
.mastfoot {
  color: rgba(255, 255, 255, .5);
}


      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
    </style>
  </head>


<body class="text-center">
    <div class="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">

  <header class="masthead mb-auto">
      <div class="inner">
            <h3 class="masthead-brand">{{ config['site-name'] }}</h3>
      <nav class="nav nav-masthead justify-content-center">
        <a class="nav-link active" href="#">Home</a>
        % if len(groups[0]['links']) > 0:
            % for link in groups[0]['links']:
                <a class="nav-link" href="{{ link['href'] }}">{{ link['name'] }}</a>
            % end
        % end
      </nav>
    </div>
  </header>


  <main role="main" class="inner cover">
        % if len(groups[0]['links']) > 0:
        <ul class="navbar-nav mr-auto">

                % for link in groups[0]['links']:
                    <h1 class="cover-heading">{{ link['name'] }}</h1>
                    <p class="lead">{{ link['text'] }}</p>
                    <p class="lead">
                    <a href="{{ link['href'] }}" class="btn btn-lg btn-secondary">{{ link['name'] }}</a>
                    </p>
                    <hr/>
                % end
            </ul>
            <br />
        % end


  </main>

  <footer class="mastfoot mt-auto">
    <div class="inner">
        <p>{{ config['footer'] }}</p>
    </div>
  </footer>
</div>


</body>
</html>''', config=config, groups=groups)

    run(
        server='paste',
        host='0.0.0.0',
        port='80'
    )
