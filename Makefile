SHELL := /bin/bash

.PHONY=all,quality,test

clean: # Clean working directory
	-rm -rf node_modules/
	-rm -rf bower_components/
	-rm -rf dist/
	-find . -name *.pyc -delete
	-rm *acceptance*.png *acceptance*.log

# Localisation tasks
WORKING_DIR := chatgpt
JS_TARGET := $(WORKING_DIR)/static/js/translations
EXTRACT_DIR := $(WORKING_DIR)/translations/en/LC_MESSAGES
EXTRACTED_DJANGO := $(EXTRACT_DIR)/django-partial.po
EXTRACTED_DJANGOJS := $(EXTRACT_DIR)/djangojs-partial.po
EXTRACTED_TEXT := $(EXTRACT_DIR)/text.po
I18N_CONFIG_PATH = ./translations/config.yaml

extract_translations: ## extract strings to be translated, outputting .po files
	cd $(WORKING_DIR) && i18n_tool extract -c $(I18N_CONFIG_PATH)
	# mv $(EXTRACTED_DJANGO) $(EXTRACTED_TEXT)
	tail -n +20 $(EXTRACTED_DJANGOJS) >> $(EXTRACTED_TEXT)
	# rm $(EXTRACTED_DJANGOJS)
	sed -i'' -e 's/nplurals=INTEGER/nplurals=2/' $(EXTRACTED_TEXT)
	sed -i'' -e 's/plural=EXPRESSION/plural=\(n != 1\)/' $(EXTRACTED_TEXT)

compile_translations: ## compile translation files, outputting .mo files for each supported language
	cd $(WORKING_DIR) && i18n_tool generate -c $(I18N_CONFIG_PATH)
	# python manage.py compilejsi18n --output $(JS_TARGET)

dummy_translations: ## generate dummy translation (.po) files
	cd $(WORKING_DIR) && i18n_tool dummy -c $(I18N_CONFIG_PATH)
