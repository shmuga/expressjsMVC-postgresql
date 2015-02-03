


################################################################################
# VARIABLES
################################################################################


# PROJECT PATHS ################################################################

PROJECT_PATH        ?= $(shell pwd)
CONFIG_PATH         ?= $(PROJECT_PATH)/etc/build
TEMPLATES_PATH      ?= $(CONFIG_PATH)/templates
SOURCES_LISTS_PATH  ?= $(CONFIG_PATH)/sources-lists
INCLUDES_PATH       ?= $(PROJECT_PATH)/include
JS_BUILD_PATH       ?= $(PROJECT_PATH)/bin
JS_EXTERNS_PATH     ?= $(PROJECT_PATH)/externs
JS_SOURCES_PATH     ?= $(PROJECT_PATH)/lib
MODULES_PATH        ?= $(PROJECT_PATH)/node_modules
TOOLS_PATH          ?= $(MODULES_PATH)/livetex-tools
ENV_EXTERNS_PATH    ?= $(TOOLS_PATH)/externs


# ENVIRONMENT ##################################################################

JS_ENVIRONMENT      ?= node


# AUX VARS #####################################################################

JS_LINT             ?= $(foreach FILE, \
                       $(shell find $(SOURCES_LISTS_PATH)/js -maxdepth 1 \
                       -iname '*.jsd' ), \
                       $(shell basename $(FILE) | cut -d '.' -f 1))


JS_EXTERNS          ?= $(foreach FILE, \
                       $(shell find $(JS_BUILD_PATH) -maxdepth 1 \
                       -iname '*.js'), \
                       $(shell basename $(FILE) | cut -d '.' -f 1))


JS_TEMPLATES        ?= $(foreach FILE, \
                       $(shell find $(TEMPLATES_PATH)/js -maxdepth 1 \
                       -iname '*.jst'), \
                       $(shell basename $(FILE) | cut -d '.' -f 1))


JS_TESTS            ?= $(foreach FILE, \
                       $(shell find $(JS_BUILD_PATH) -maxdepth 1 \
                       -iname 'test-*.js'), \
                       $(shell basename $(FILE) | cut -d '.' -f 1))


# PREREQUISITES PATHS ##########################################################

vpath %.jst         $(TEMPLATES_PATH)/js
vpath %.jsd         $(SOURCES_LISTS_PATH)/js
vpath %.js          $(JS_BUILD_PATH)


################################################################################
# TOOLS
################################################################################

JS_COMPILER ?= java -jar $(TOOLS_PATH)/tools/closure-compiler.jar \
                    --warning_level     VERBOSE \
                    --language_in       ECMASCRIPT5_STRICT


JS_LINTER ?= $(TOOLS_PATH)/tools/closure-linter/gjslint.py \
		                --strict \
		                --custom_jsdoc_tags "namespace, event"


JS_EXTERNS_EXTRACTOR ?= $(TOOLS_PATH)/tools/externs-extractor/externsExtractor.py


REVERSIONER ?= $(TOOLS_PATH)/tools/reversioner.py package.json


TEMPLATER ?= $(TOOLS_PATH)/tools/templater.py


################################################################################
# RULES
################################################################################

################################################################################
# AUX RULES ####################################################################


# HEADERS ######################################################################

%.jsh: %.js-env-headers %.js-custom-headers %.js-headers
	@cat $(shell cat $^ < /dev/null) > $@


%.js-headers:
	@echo $(foreach DIR, $(wildcard $(MODULES_PATH)/*), \
	$(wildcard $(DIR)/externs/*.js)) > $@


%.js-custom-headers:
	@echo $(foreach DIR, $(INCLUDES_PATH), \
	$(wildcard $(DIR)/*.js)) > $@


%.js-env-headers:
	@echo $(foreach DIR, $(ENV_EXTERNS_PATH)/$(JS_ENVIRONMENT), \
	$(wildcard $(DIR)/*.js)) > $@


# COMPILATIONS #################################################################

%.js-compile: %.jsd
	@cat $(foreach FILE, $(shell cat $<), $(JS_SOURCES_PATH)/$(FILE))


%.js-compile-compressed: %.jsd
	@$(JS_COMPILER) \
	--js                $(foreach FILE, $(shell cat $<), \
	                    $(JS_SOURCES_PATH)/$(FILE))


# COMPRESSED COMPILATIONS ######################################################


%.js-externs-compile-compressed: %.jsd %.jsh
	@$(JS_COMPILER) \
	--js                $(foreach FILE, $(shell cat $<), \
	                    $(JS_SOURCES_PATH)/$(FILE)) \
	--externs           $(shell echo "$^" | cut -d " " -f 2)


# ADVANCED COMPILATION #########################################################

%.js-compile-advanced: %.jsd %.jsh
	@$(JS_COMPILER) \
	--compilation_level ADVANCED_OPTIMIZATIONS \
	--jscomp_error      checkTypes \
	--js                $(foreach FILE, $(shell cat $<), \
	                    $(JS_SOURCES_PATH)/$(FILE)) \
	--externs           $(shell echo "$^" | cut -d " " -f 2)


#################################################################### AUX RULES #
################################################################################


################################################################################
# MAIN RULES ###################################################################

%.js-lint: %.jsd
	@$(JS_LINTER) \
	$(foreach FILE, $(shell cat $^), $(JS_SOURCES_PATH)/$(FILE)) 1> /dev/null


%.js-check: %.jst
	@$(TEMPLATER) -a True $< > /dev/null


%.js-assemble: %.jst
	@mkdir -p $(JS_BUILD_PATH)
	@$(TEMPLATER) $< > \
	$(shell echo $(JS_BUILD_PATH)/$(shell echo $(shell basename $<) | \
	cut -d '.' -f 1).js)


%.js-extract-externs: %.js
	@mkdir -p $(JS_EXTERNS_PATH)
	@$(JS_EXTERNS_EXTRACTOR) $< \
	> $(JS_EXTERNS_PATH)/$(shell basename $<)


%.js-test: %.js
	@node --eval "require('$^').test.run('$(names)')"


################################################################################

%.highest-version:
	@$(REVERSIONER) -H $(shell echo $@ | cut -d '.' -f 1)


%.latest-version:
	@$(REVERSIONER) -L $(shell echo $@ | cut -d '.' -f 1)


################################################################### MAIN RULES #
################################################################################


################################################################################
# GENERAL RULES ################################################################


all: js


js: | js-build js-externs
	@echo $@: DONE


js-clean:
	@rm -rf $(wildcard $(JS_BUILD_PATH)/*.js) $(JS_EXTERNS_PATH)
	@echo $@: DONE


js-lint:
	@$(foreach TARGET_NAME, $(JS_LINT), \
	$(MAKE) -s $(shell echo $(TARGET_NAME).js-lint);)
	@echo $@: DONE


js-check: js-lint
	@$(foreach TARGET_NAME, $(JS_TEMPLATES), \
	$(MAKE) -s $(shell echo $(TARGET_NAME).js-check);)
	@echo $@: DONE


js-build: js-clean
	@mkdir -p $(JS_BUILD_PATH)
	@$(foreach TARGET_NAME, $(JS_TEMPLATES), \
	$(MAKE) -s $(shell echo $(TARGET_NAME).js-assemble);)
	@echo $@: DONE


js-externs:
	@mkdir -p $(JS_EXTERNS_PATH)
	@$(foreach TARGET_NAME, $(JS_EXTERNS), \
	$(MAKE) -s $(shell echo $(TARGET_NAME).js-extract-externs);)
	@echo $@: DONE


js-tests:
	@$(foreach TARGET_NAME, $(JS_TESTS), \
	$(MAKE) -s $(shell echo $(TARGET_NAME).js-test);)
	@echo $@: DONE


################################################################################

versions:
	@$(REVERSIONER)
	@echo $@: DONE


set-latest-versions:
	@$(foreach MODULE, $(shell $(REVERSIONER) -S True), \
	$(MAKE) -s $(MODULE).latest-version;)
	@echo $@: DONE


set-highest-versions:
	@$(foreach MODULE, $(shell $(REVERSIONER) -S True), \
	$(MAKE) -s $(MODULE).highest-version;)
	@echo $@: DONE


set-version:
	@$(REVERSIONER) -I True
	@echo $@: DONE


commit:
	@$(REVERSIONER) -C True
	@echo $@: DONE


npm-publish:
	@npm login --loglevel=silent
	@npm ls 1> /dev/null
	@npm publish --loglevel=silent
	@echo $@: DONE


publish: | js-check js set-version npm-publish commit
	@echo $@: DONE


################################################################ GENERAL RULES #
################################################################################
