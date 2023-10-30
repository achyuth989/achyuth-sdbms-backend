FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ /roboxa-sdbms-backend

WORKDIR /roboxa-sdbms-backend
RUN ["chmod", "+x", "/roboxa-sdbms-backend/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--reload","--host","0.0.0.0"]

ENTRYPOINT ["/roboxa-sdbms-backend/entrypoint.sh"]