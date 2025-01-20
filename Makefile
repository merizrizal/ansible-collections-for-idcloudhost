install:
	@cd merizrizal/idcloudhost; \
	ansible-galaxy collection build -f --output-path $$ROOT_DIR

	@version=`(yq '.version' merizrizal/idcloudhost/galaxy.yml)`; \
	ansible-galaxy collection install -f merizrizal-idcloudhost-$$version.tar.gz; \
	rm merizrizal-idcloudhost-$$version.tar.gz
