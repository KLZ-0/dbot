VARS_DAEMON := DBOT_SILENTLOG="True"
VARS_RUN := DBOT_SILENTLOG=""
PIDFILE := dbot.pid

.PHONY: all init run start stop

all: init run

init: venv
	source venv/bin/activate && pip install -r requirements.txt

venv:
	python3 -m venv venv

run:
	source venv/bin/activate && $(VARS_RUN) python3 dbot.py

start: $(PIDFILE)

stop: $(PIDFILE)
	kill $$(cat $<) ; rm $<

$(PIDFILE):
	source venv/bin/activate && { $(VARS_DAEMON) python3 dbot.py & echo $$! > $@; }
