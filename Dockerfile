FROM python:2.7.9

VOLUME [ "/input" ]
WORKDIR /input

COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -f requirements.txt \
		&& mkdir /install_dir 

COPY ./ /install_dir
RUN cd /install_dir \
    && python setup.py install \
		&& cd / \
    && rm -rf /install_dir

EXPOSE  9000 
COPY ./opentaxii-config.yml opentaxii-config.yml
ENV OPENTAXII_CONFIG=opentaxii-config.yml 
CMD [ "opentaxii-run-dev" ]
