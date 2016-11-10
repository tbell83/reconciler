VIRTUALENV_DIR = ${HOME}/.virtualenv
PROJECT_NAME = dfchef

all: ${VIRTUALENV_DIR}/${PROJECT_NAME}
	. ${VIRTUALENV_DIR}/${PROJECT_NAME}/bin/activate && pip install --upgrade .

${VIRTUALENV_DIR}/${PROJECT_NAME}:
	mkdir -p ${VIRTUALENV_DIR}
	cd ${VIRTUALENV_DIR} && virtualenv -p /usr/bin/python2.7 ${PROJECT_NAME}

clean:
	rm -rf build dist *.egg-info
	find . -name \*pyc -type f | xargs rm -f

rebuild: clean
	pip install --editable .
