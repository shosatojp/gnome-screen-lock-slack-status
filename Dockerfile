FROM alpine:3.16

RUN apk update \
    && apk add --no-cache python3 dbus py3-dbus py3-requests py3-gobject3

COPY entry.sh status.py /

ENTRYPOINT [ "/entry.sh" ]
