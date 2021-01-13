from waitress import serve

from Api import main

serve(main.app, host='0.0.0.0', port=8080)
