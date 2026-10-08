FROM python:3.12-slim AS build

WORKDIR /build
COPY .github/docker/requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY .github/docker/build.py .github/docker/test_build.py ./
COPY index.html ./index.html
COPY content/ ./content/
RUN python -m unittest test_build && python build.py

FROM nginx:stable-alpine AS runtime

# Keep only our generated website, not the Nginx welcome page.
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build /build/_site/ /usr/share/nginx/html/

EXPOSE 80
