FROM ubuntu:20.04

# update and install packages
RUN apt-get update \
  && apt-get update \
  && apt-get install python3 python3-pip git openssh-client apt-utils -y

# copy install the requirements
WORKDIR /root/
ADD ./idep-sanford-autodelegation.py /root/
ADD ./requirements.txt /root/
RUN pip3 install -r requirements.txt

# run the script
CMD python3 idep-sanford-autodelegation.py
