FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install ffmpeg build-essential -y

WORKDIR /youtube-bz

COPY . .

RUN python3 -m pip install -e .

ENTRYPOINT ["youtube-bz"]
CMD ["--help"]
