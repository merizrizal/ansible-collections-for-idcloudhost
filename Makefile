install:
	@cd merizrizal/idcloudhost; \
	ansible-galaxy collection build -f --output-path $$ROOT_DIR

	@version=`(yq '.version' merizrizal/idcloudhost/galaxy.yml)`; \
	ansible-galaxy collection install -f merizrizal-idcloudhost-$$version.tar.gz; \
	rm merizrizal-idcloudhost-$$version.tar.gz

ansible-sanity-test-lint: install
	@dir=`(ansible-doc -F merizrizal.idcloudhost | head -n 1 | awk '//{print $$2}' | sed 's/merizrizal/ /g' | awk '//{print $$1}')`; \
	cd $$dir/merizrizal/idcloudhost; \
	python=`(which python3)`; \
	ansible-test sanity --python-interpreter $$python --lint;
