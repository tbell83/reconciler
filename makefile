VIRTUALENV_DIR = ${HOME}/.virtualenv

all: ${VIRTUALENV_DIR}/chef_prune
	. ${VIRTUALENV_DIR}/chef_prune/bin/activate && pip install --upgrade .

${VIRTUALENV_DIR}/chef_prune:
	mkdir -p ${VIRTUALENV_DIR}
	cd ${VIRTUALENV_DIR} && virtualenv -p /usr/bin/python2.7 chef_prune

clean:
	rm -rf build dist *.egg-info
	find . -name \*pyc -type f | xargs rm -f

rebuild: clean
	pip install --editable .
