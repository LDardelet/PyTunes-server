python3 -m venv env
source env/bin/activate

ydl_location="third_party/youtube-dl"
if [ ! $# -eq 0 ]
then
    if [ "$1" -eq "update" ]
    then
        echo "Updating local youtube-dl"
        wget https://yt-dl.org/downloads/latest/youtube-dl -O $ydl_location
        chmod a+xr $ydl_location
    fi
fi 

if [ ! -e $ydl_location ]
then
    echo "Downloading local youtube-dl"
    wget https://yt-dl.org/downloads/latest/youtube-dl -O $ydl_location
    chmod a+xr $ydl_location
fi

python manage.py runserver
