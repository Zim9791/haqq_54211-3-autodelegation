FROM ubuntu:20.04

# update and install packages
RUN apt-get update \
  && apt-get update \
  && apt-get install python3 python3-pip git openssh-client apt-utils curl jq -y

# copy the iond files
WORKDIR /root/
RUN git clone https://github.com/IDEP-network/incentivized-testnet.git
RUN cp incentivized-testnet/binary/iond /usr/local/bin/
RUN chmod a+x /usr/local/bin/iond

# copy install the requirements
ADD ./idep-sanford-autodelegation.py /root/
ADD ./requirements.txt /root/
RUN pip3 install -r requirements.txt

# run the script
CMD /usr/local/bin/iond start --unsafe-skip-upgrades 800000
